from datetime import datetime, timezone, timedelta
from requests import request, Response
from logging import getLogger

from google.oauth2.service_account import Credentials
from google.auth.transport.requests import Request

from .util.timer import Timer
from .clock import Clock
from .settings import settings


__all__ = 'Reservations'

log = getLogger(__name__)



def iso_format_for_google (value: datetime) -> str:
	"""Google's calendar API seems to only accept UTC with the Zulu shorthand."""

	# Convert to UTC, format as ISO 8601, but then replace the timezone offset with Zulu
	return value.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')



class Reservations:
	"""Pulls reservation data from a Google calendar."""

	"""Run the callback every 300,000 milliseconds (5 minutes)."""
	_TICK_LENGTH: int = 300_000

	__slots__ = '_timer', '_credentials', 'clock'

	"""Manages the periodic execution of the ``tick`` method."""
	_timer: Timer

	"""Google API service account credentials."""
	_credentials: Credentials

	"""Clock object."""
	clock: Clock


	def __init__ (self):
		self.clock = Clock()

		# Credentials for the service account
		self._credentials = Credentials.from_service_account_info(settings.google_api_credentials, scopes = settings.google_api_scopes)

		# Start the timer
		self._timer = Timer(period = self._TICK_LENGTH, mode = Timer.PERIODIC, callback = self.update)


	def __del__ (self):
		self._timer.deinit()


	def update (self, _: Timer | None):
		"""Runs periodically to check for reservations."""

		now: datetime = datetime.now(tz = timezone.utc)

		# Find all events in a 24-hour window
		events = self.get_events(now - timedelta(hours = 12), now + timedelta(hours = 12))

		for start, end in events:
			# Match events that are occurring now
			if start <= now <= end:
				log.debug(f"An active reservation started at {start.time().isoformat()} and will end at {end.time().isoformat()}")
				self.clock.set_countdown(end)

				return  # When there are overlapping reservations, only honor the first


	def get_events (self, start: datetime, end: datetime) -> list[datetime, datetime]:
		"""Fetch reservation events which overlap with a specified period."""

		if not self._credentials.valid:
			# Update the token
			self._credentials.refresh(Request())

		query: dict[str, str] = {
			'timeMin': iso_format_for_google(start),
			'timeMax': iso_format_for_google(end),
			'singleEvents': True,
			'orderBy': 'startTime'
		}
		querystring: str = '&'.join([f'{k}={v}' for k, v in query.items()])

		calendar_url: str = f'https://www.googleapis.com/calendar/v3/calendars/{settings.google_calendar_id}/events?{querystring}'

		request_headers = {}
		self._credentials.apply(request_headers)

		response: Response = request('get', calendar_url, headers = request_headers)
		response_data = response.json()

		for event in response_data['items']:
			start: datetime = datetime.fromisoformat(event['start']['dateTime'])
			end: datetime = datetime.fromisoformat(event['end']['dateTime'])

			yield start, end
