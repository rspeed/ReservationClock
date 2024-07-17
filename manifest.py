# Manifest file for building a Micropython board firmware with frozen dependencies

include('$(BOARD_DIR)/manifest.py')

metadata(description = "A clock that pulls info from a reservation system.", version = "0.0.1", author = "Rob Speed", license = "MIT")

add_library('google-auth', 'lib/micropython-google-auth')

# Dependencies
require('copy')
require('datetime')
require('logging')
require('collections-defaultdict')
require('google-auth', library='google-auth')

# Packaged libraries
module('typing.py', base_path = 'lib/micropython-stubs/mip')

# Don"t freeze the application package during development
#package("reservation_clock")
