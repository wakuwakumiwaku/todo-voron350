# Voron 2.4 350mm Klipper Configuration Backup

This directory contains the Klipper and MainsailOS configuration files and hardware documentation for the **Voron 2.4 (350mm)** build.

---

## 1. Stepper Motor Specifications & Driver Configuration

| Axis / Function | Stepper Motor Model | Form Factor & Temp Rating | Step Angle | Full Steps / Rev | Rated Current | Klipper `run_current` | Microsteps | Rotation Distance | Gear Ratio | Board Port & TMC2209 UART |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **X (B - Left)** | `LDO-42STH48-2004MAH(VRN)` | NEMA 17 (High Temp) | **0.9°** | 400 | 2.0 A | **0.80 A** | 32 | 40 mm | 1:1 | Octopus `MOTOR_0` (UART: `PC4`) |
| **Y (A - Right)** | `LDO-42STH48-2004MAH(VRN)` | NEMA 17 (High Temp) | **0.9°** | 400 | 2.0 A | **0.80 A** | 32 | 40 mm | 1:1 | Octopus `MOTOR_1` (UART: `PD11`) |
| **Z0 (Front Left)** | `LDO-42STH48-2004AC` | NEMA 17 (High Temp) | **1.8°** | 200 | 2.0 A | **1.20 A** | 32 | 40 mm | 80:16 | Octopus `MOTOR_2` (UART: `PC6`) |
| **Z1 (Rear Left)** | `LDO-42STH48-2004AC` | NEMA 17 (High Temp) | **1.8°** | 200 | 2.0 A | **1.20 A** | 32 | 40 mm | 80:16 | Octopus `MOTOR_3` (UART: `PC7`) |
| **Z2 (Rear Right)** | `LDO-42STH48-2004AC` | NEMA 17 (High Temp) | **1.8°** | 200 | 2.0 A | **1.20 A** | 32 | 40 mm | 80:16 | Octopus `MOTOR_4` (UART: `PF2`) |
| **Z3 (Front Right)**| `LDO-42STH48-2004AC` | NEMA 17 (High Temp) | **1.8°** | 200 | 2.0 A | **1.20 A** | 32 | 40 mm | 80:16 | Octopus `MOTOR_5` (UART: `PD3`) |
| **Extruder (E0)** | `LDO-36STH20-1004AHG(9T)`| NEMA 14 Pancake (Class H 180°C)| **1.8°** | 200 | 1.0 A | **0.65 A** | 16 | 47.088 mm | 9:1 | EBB SB2209 (UART: `EBBCan:gpio20`) |

### Stepper Driver Notes
* **Driver Type:** Trinamic TMC2209 on all axes.
* **Sense Resistors:** `sense_resistor: 0.110` across all drivers.
* **Interpolation:** `interpolate: false` on all drivers.
* **Stealthchop:** `stealthchop_threshold: 0` (SpreadCycle enabled globally for positional accuracy and high-speed torque).

---

## 2. Motion System & Kinematics

* **Kinematics:** CoreXY
* **Build Volume:** 350 mm × 350 mm × 310 mm
* **Max Velocity:** 400 mm/s
* **Max Acceleration:** 8,000 mm/s²
* **Max Z Velocity:** 10 mm/s
* **Max Z Acceleration:** 60 mm/s²
* **Square Corner Velocity:** 5.0 mm/s
* **Homing Speeds:**
  * X Homing: 50 mm/s (`endstop_pin: PG11`)
  * Y Homing: 25 mm/s (`endstop_pin: PG6`)
  * Z Homing: 8 mm/s initial, 3 mm/s second (`probe:z_virtual_endstop` via Voron Tap)

---

## 3. Toolhead & Extruder (CAN Bus Upgrade)

* **Toolhead MCU:** BigTreeTech EBB SB2209 RP2040 (CAN bus at 1,000,000 baud)
* **USB-CAN Bridge:** BigTreeTech U2C V2.1 (STM32G0B1)
* **Extruder:** Galileo 2 (G2E) Planetary Gearbox
  * `gear_ratio: 9:1`
  * `rotation_distance: 47.088`
  * `pressure_advance: 0.03` (smooth time `0.030`)
* **Hotend Heater:** HE0 on `EBBCan:gpio7` (Max Power: 0.95, Max Temp: 300°C)
* **Hotend Thermistor:** `ATC Semitec 104NT-4-R025H42G` on `EBBCan:gpio27`
* **Hotend Fan:** 3010/4010 24V Fan on `EBBCan:gpio14` (Thermostatic trigger: 50°C)
* **Part Cooling Fan:** 5015 24V Fan on `EBBCan:gpio13` (`kick_start_time: 0.5`)
* **Probe:** Voron Tap V2 (CNC Aluminum Carriage)
  * Probe Pin: `^EBBCan:gpio6` (5V logic)
  * Offsets: `x_offset: 0`, `y_offset: 0`, `z_offset: 0`
  * `activate_gcode`: Nozzle temperature wait macro (ensures nozzle is cooled to ≤150°C before probing bed surface to avoid melting PEI)
* **Accelerometer:** Onboard ADXL345 on EBB RP2040 SPI (`gpio0`, `gpio1`, `gpio2`, `gpio3`), `axes_map: z,-y,x`
* **Lighting:** Stealthburner 3-LED Neopixel chain on `EBBCan:gpio16` (GRBW)

---

## 4. Bed, Chamber & Enclosure

* **Heated Bed:** Keenovo Silicone Heater with SSR control on `PA1`
  * Thermistor: `Generic 3950` on `PF3`
  * Bed PID: `Kp=47.377, Ki=1.497, Kd=374.872` (Max Power: 0.70 / 120°C max)
* **Chamber Temperature Sensor:** Custom NTC Thermistor on `PF7` (`beta: 3244`)
* **Chamber Airflow & Filtration:**
  * Chamber Heater Fan: `PD12`
  * Chamber Exhaust Fan: `PD15` (`max_power: 0.6`)
  * PCB Cooling Fan: `PD14`
* **Leveling System:** Quad Gantry Leveling (QGL)
  * Points: `(50,25)`, `(50,275)`, `(300,275)`, `(300,25)`
  * Gantry Corners: `(-60,-10)`, `(410,420)`
  * Retry tolerance: `0.0275 mm`

---

## 5. File Inventory

* **`printer.cfg`**: Active main printer configuration (includes kinematics, QGL, bed mesh, macros, and `[include ebb-sb2209.cfg]`).
* **`ebb-sb2209.cfg`**: Dedicated toolhead configuration for the EBB SB2209 RP2040 board over CAN bus.
* **`printer-backup-before-canbus.cfg`**: Original working configuration prior to the CAN bus upgrade.
* **`setup_canbus_ebb.sh`**: Turnkey interactive script to compile/flash Katapult & Klipper onto the EBB board and auto-detect the CAN UUID.
* **`moonraker.conf`**: Moonraker API server and update manager settings.
* **`crowsnest.conf`**: Crowsnest camera streamer settings.
* **`sonar.conf`**: Sonar network keepalive settings.
