# Voron 2.4 350mm Klipper Configuration Backup

This directory contains the Klipper and MainsailOS configuration files for the Voron 2.4 (350mm) build.

### Machine Specifications
* **Mainboard:** BigTreeTech Octopus V1.1 (connected via USB)
* **CAN Adapter:** BigTreeTech U2C V2.1 (connected via USB)
* **Toolhead Board:** BigTreeTech EBB SB2209 RP2040 (connected via CAN bus at 1 Mbps)
* **Extruder:** Galileo 2 (G2E) with LDO-36STH20-1004AHG(9T) pancake motor (`gear_ratio: 9:1`, `rotation_distance: 47.088`)
* **Probe:** Voron Tap V2 (`activate_gcode` nozzle cooling macro)
* **Hotend Thermistor:** `ATC Semitec 104NT-4-R025H42G`
* **Part Cooling Fan:** 5015 fan on `EBBCan:gpio13`
* **Hotend Fan:** 3010/4010 fan on `EBBCan:gpio14`
* **Accelerometer:** Onboard ADXL345 on EBB RP2040 SPI bus
* **Toolhead LEDs:** Stealthburner Neopixels on `EBBCan:gpio16`

### File Descriptions
* **`printer.cfg`**: Active printer configuration including kinematics, QGL, bed mesh, macros, and `[include ebb-sb2209.cfg]`.
* **`ebb-sb2209.cfg`**: Dedicated toolhead configuration for the EBB SB2209 RP2040 over CAN bus.
* **`printer-backup-before-canbus.cfg`**: Original working configuration prior to the CAN bus upgrade.
* **`setup_canbus_ebb.sh`**: Helper script to compile Katapult/Klipper, flash the EBB board, and auto-detect the CAN UUID.
* **`moonraker.conf`**: Moonraker API server and update manager settings.
* **`crowsnest.conf`**: Crowsnest camera streamer settings.
* **`sonar.conf`**: Sonar network keepalive settings.
