from logging import getLogger
from time import sleep


try:
	from network import WLAN, STA_IF, STAT_CONNECTING
except ImportError:
	WLAN = STA_IF = STAT_CONNECTING = None

from .settings import settings


__all__ = 'connect_wlan'

log = getLogger(__name__)



class WiFiConnected(BaseException):
	"""Raised to indicate that the board has successfully connected to a Wi-Fi network."""
	pass



def connect_wlan () -> None:
	"""Connects the board to a Wi-Fi networks."""

	# Short-circuit when there's no wireless LAN
	if WLAN is None:
		return

	wlan = WLAN(STA_IF)

	try:
		for ssid, password in settings.wlans:
			# Enable Wi-Fi and attempt to connect
			wlan.active(True)
			wlan.connect(ssid, password)

			log.info(f"Attempting to connect to SSID {ssid}")

			for _ in range(50):
				if wlan.isconnected():
					log.debug(f"Status: {wlan.status()}")
					raise WiFiConnected()

				if wlan.status() < 0:
					# Failure
					break

				sleep(0.1)

			# Reset the network interface
			wlan.disconnect()
			wlan.active(False)

		raise RuntimeError("Could not connect to a wireless network.")

	except WiFiConnected:
		# Success!
		log.info(f"Wi-Fi connected! ip = {wlan.ifconfig()[0]}")

	except RuntimeError as e:
		log.error(e)
		raise
