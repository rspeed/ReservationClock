from copy import copy
from io import open as open_file
from json import load as read_json, dump as write_json

from typing import Any, TypedDict


__all__ = 'Settings', 'settings'



class SettingsFileSchema(TypedDict):
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



class Settings:
	"""Settings for the Reservation Clock app."""

	"""Path to the file that stores settings."""
	FILE_PATH: str = 'settings.json'

	DEFAULTS: SettingsFileSchema = {
		'wlans': [],
		'google_api_credentials': {},
		'google_api_scopes': [],
		'google_calendar_id': '',
		'display_gpio_pins': [],
		'display_pixel_count': 5 * 7
	}

	KEYS: tuple = tuple(DEFAULTS.keys())

	_settings: SettingsFileSchema


	def __init__ (self) -> None:
		"""Read the settings from storage."""

		self._settings = self.DEFAULTS
		self._dirty = False

		self.load()


	def load (self):
		try:
			with open_file(self.FILE_PATH, 'r') as f:
				self._settings = read_json(f)

		except (OSError, ValueError):
			# Stick with the defaults
			pass


	def flush (self) -> None:
		"""Write the settings to storage."""

		with open_file(self.FILE_PATH, 'w') as f:
			write_json(self._settings, f)


	def __getattr__ (self, key: str) -> Any:
		try:
			return self._settings[key]  # type: ignore
		except KeyError:
			pass

		try:
			return copy(self.DEFAULTS[key])  # type: ignore
		except KeyError:
			raise AttributeError(key)


	def __setattr__ (self, key: str, value: Any) -> None:
		if key not in self.KEYS:
			return super().__setattr__(key, value)

		self._settings[key] = value  # type: ignore



settings = Settings()
