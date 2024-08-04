from copy import deepcopy
from io import open as open_file
from json import load as read_json, dump as write_json


__all__ = 'Settings', 'settings'



class Settings:
	"""Settings for the Reservation Clock app."""

	"""Path to the file that stores settings."""
	FILE_PATH: str = 'settings.json'

	DEFAULTS: dict = {
		'wlans': [],
		'google_api_credentials': {},
		'google_api_scopes': [],
		'google_calendar_id': '',
		'display_gpio_pins': [],
		'display_pixel_count': 5 * 7
	}

	"""SSIDs and passwords of wireless networks to attempt to access."""
	wlans: list[list[str, str]]

	"""Similar to ``credentials.json`` but with a decoded private key."""
	google_api_credentials: dict[str, str | dict]

	"""List of authorized API scopes."""
	google_api_scopes: list[str]

	"""Unique ID of the reservations calendar."""
	google_calendar_id: str

	"""GPIO pins used to control the display."""
	display_gpio_pins: list[int]

	"""The number of pixels in each digit of the display."""
	display_pixel_count: int


	def __init__ (self) -> None:
		"""Read the settings from storage."""

		saved_settings: dict = self._saved_settings()

		for key, default_value in self.DEFAULTS.items():
			# Set local attributes to a saved value or a default
			setattr(self, key, saved_settings.get(key, deepcopy(default_value)))


	def _saved_settings (self) -> dict:
		"""Loads the settings from storage."""
		try:
			with open_file(self.FILE_PATH, 'r') as f:
				return read_json(f)

		except (OSError, ValueError):
			# Stick with the defaults
			return {}


	def flush (self) -> None:
		"""Write the settings to storage."""

		with open_file(self.FILE_PATH, 'w') as f:
			write_json(f, {key: getattr(self, key) for key in self.DEFAULTS.keys()})



settings = Settings()
