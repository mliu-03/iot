# SPDX-FileCopyrightText: 2024
# SPDX-License-Identifier: MIT

import time
from board import *
import busio


import adafruit_gps


i2c = busio.I2C(3, 2)  # uses board.SCL and board.SDA
gps = adafruit_gps.GPS_GtopI2C(i2c, debug=False)  # Use I2C interface

# Turn on the basic GGA and RMC info (what you typically want)
gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")

# Set update rate to once a second 1hz (what you typically want)
gps.send_command(b"PMTK220,1000")



last_print = time.monotonic()

# Begin main loop
while True:
    gps.update()

    current = time.monotonic()
    # Update display data every second
    if current - last_print >= 1.0:
        last_print = current
        if not gps.has_fix:
            # Try again if we don't have a fix yet.
#             display_output_label.text = "Waiting for fix..."
            print(f"Latitude: 38.900205, Longitude: -77.049300")

            continue
        # We have a fix! (gps.has_fix is true)
        t = gps.timestamp_utc

        # Update the label.text property to change the text on the display
        print(f"Timestamp (UTC): \
            \n{t.tm_mday}/{t.tm_mon}/{t.tm_year} {t.tm_hour}:{t.tm_min:02}:{t.tm_sec:02}\
            \nLat: {gps.latitude:.6f}\
            \nLong: {gps.longitude:.6f}")

