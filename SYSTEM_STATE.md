# Voron 2.4 (350mm) – System State & Agent Handoff Guide

> [!IMPORTANT]
> **For AI Agents & Developers:** This file serves as the definitive live status, network configuration, and hardware registry for this Voron 2.4 R2 build. Read this first when continuing work on this project from any machine.

---

## 1. Network & Access Credentials

| Service | Target / Value | Notes |
| :--- | :--- | :--- |
| **Voron Raspberry Pi 4** | `192.168.1.120` (`Voron.local`) | Fixed DHCP / Wi-Fi SSID `ast` |
| **SSH User & Password** | `admin` / `1234flan` | Password authentication enabled |
| **Mainsail Web UI** | [http://192.168.1.120](http://192.168.1.120) | Mainsail v2.19.0 running |
| **Parts Printer (Snapmaker U1)** | `192.168.1.80` | Fluidd / Klipper (used to print Voron parts) |

---

## 2. Hardware Registry & CAN-Bus Topology

```text
[Raspberry Pi 4]
  │
  ├── USB 2.0 ──> [BTT U2C v2.1] (CandleLight gs_usb @ 1,000,000 baud, 120R Jumper ON)
  │                     │
  │                     └── CAN Bus (can0, 1 Mbit/s) ──> [BTT EBB SB2209 RP2040 V1.0.1]
  │                                                           ├── UUID: c56c83111439
  │                                                           ├── Bootloader: Katapult (0x10000000)
  │                                                           ├── Firmware: Klipper v0.13.0-800
  │                                                           ├── CAN Pins: GPIO 4 (RX) / 5 (TX)
  │                                                           └── 120R Jumper: ON
  │
  ├── USB 2.0 ──> [BTT Octopus V1.1 / Pro] (serial: /dev/serial/by-id/usb-Klipper_stm32f446xx_0B002D000D50535556323420-if00)
  └── USB 3.0 ──> [USB Webcam] (Crowsnest stream on port 8080)
```

### Verified CANbus UUID
* **Toolhead Board (EBBCan):** `c56c83111439`
* **Configuration File:** [`klipper_config/ebb-sb2209.cfg`](klipper_config/ebb-sb2209.cfg) (included by `printer.cfg`)
* **Bench Test Status:** **100% Verified** on 18.10.2026. Handshake complete, 147 MCU commands loaded, ADXL345 streaming verified (`1554, 3552, -8886`), onboard NTC verified (`31.0 °C`), 0 bus errors.

---

## 3. Directory Mapping & Config Synchronization

The files in `klipper_config/` in this repository map directly to `/home/admin/printer_data/config/` on the live Raspberry Pi 4:

| Repo File | Live Target on Voron Pi | Purpose |
| :--- | :--- | :--- |
| `klipper_config/printer.cfg` | `/home/admin/printer_data/config/printer.cfg` | Primary Klipper configuration |
| `klipper_config/ebb-sb2209.cfg` | `/home/admin/printer_data/config/ebb-sb2209.cfg` | Toolhead CAN-bus configuration (`c56c83111439`) |
| `klipper_config/moonraker.conf` | `/home/admin/printer_data/config/moonraker.conf` | Moonraker API server settings |
| `klipper_config/crowsnest.conf` | `/home/admin/printer_data/config/crowsnest.conf` | Webcam streaming configuration |
| `klipper_config/sonar.conf` | `/home/admin/printer_data/config/sonar.conf` | Sonar keepalive daemon |
| `klipper_config/printer-backup-before-canbus.cfg` | `/home/admin/printer_data/config/printer-backup-before-canbus.cfg` | Pre-CAN baseline backup |

### Deploying Changes to the Live Pi
To push updated configs from this repo to the live printer:
```bash
rsync -avz ./klipper_config/ admin@192.168.1.120:~/printer_data/config/
ssh admin@192.168.1.120 "sudo systemctl restart klipper"
```

---

## 4. SD Card & Disaster Recovery Procedure

If the Raspberry Pi 4 SD card is lost or corrupted, full recovery takes under 10 minutes:

1. **Flash OS:** Use Raspberry Pi Imager to flash official **MainsailOS (64-bit)** onto any micro-SD card.
2. **Configure Wi-Fi & Credentials:**
   * User: `admin`, Password: `1234flan`
   * Wi-Fi SSID: `ast`
3. **Configure CAN-Bus Interface:**
   Create `/etc/network/interfaces.d/can0` on the Pi:
   ```text
   allow-hotplug can0
   iface can0 can static
       bitrate 1000000
       up ip link set can0 txqueuelen 1024
   ```
4. **Restore Configs:**
   Clone this repo and sync `klipper_config/*` into `~/printer_data/config/`.
5. **Restart Klipper:** Everything connects automatically using UUID `c56c83111439`.

---

## 5. Current Project Status & Next Steps

*Last updated: 2026-11-16*

* [x] **Motion System & Kinematics:** 100% printed and assembled (CNC A/B drives, CNC XY-joints, GE5C Z-joints, SBFI front idlers, BZI top idlers, CNC Tap V2).
* [x] **Electronics & CAN Bench Test:** 100% verified (Pi 4, U2C v2.1, EBB SB2209 RP2040 flashed with Katapult + Klipper, UUID discovered, 60 $\Omega$ bus termination verified).
* [x] **Thermistor Cable Repair & Bay Disassembly (2026-11-16):**
  * Thermistor cable repaired (live Klipper check pending power-on).
  * Bottom electronics bay cables unplugged to reseat **Octopus v1.1**, **Raspberry Pi 4**, and **BTT U2C v2.1** on DIN rails.
  * Identified and removed/retired unnecessary previous-owner wiring: unused 4-color SFS-style `STOP`/`DIAG` cable and obsolete `ABL` inductive-probe lead (`^PG15`, replaced by Voron Tap V2 on `EBBCan:gpio6`).
  * Verified USB-A to USB-C data+power cable with BTT U2C (`lsusb`: `1d50:606f`, `can0` detected).
* [ ] **Next Step 1 – Splice & Test `XY STOP` (Eliminating LDO Breakout PCB):**
  * Measure 4-pin `XY STOP` cable (`~0 Ω` untouched, `OL` when pressed) to identify common `GND`, `X-Signal`, `Y-Signal`, and unused `Vin` (insulate `Vin`).
  * Splice `XY STOP` directly onto the Octopus-side 3-pin pigtails of `XES` (`DIAG3` / `PG11`) and `YES` (`DIAG0` / `PG6`): split `GND` to both middle pins, `X` / `Y` to the populated outer signal pins (`5V` pin stays empty).
* [ ] **Next Step 2 – Reseat Bottom Boards & Open Pre-Duct Wiring:**
  * Reseat **Octopus v1.1**, **Raspberry Pi 4**, and **BTT U2C v2.1** on DIN rails (keep cable ducts open during testing; use 90° USB cables/adapters or pre-plug USBs if clearance is tight).
  * Reconnect Octopus per active `klipper_config/printer.cfg`: Bed SSR on `BED_OUT` (`PA1`), `Z`/`Z1`/`Z2` on `MOTOR2_1`/`MOTOR3`/`MOTOR4`, `Z3` on `MOTOR7`, `X` on `DIAG3` (`PG11`), `Y` on `DIAG0` (`PG6`), `12V` jumpers on `FAN4` and `FAN6`/`FAN7` where needed.
  * Connect U2C USB-C to RPi 4 black USB 2.0 port, verify U2C `120R` jumper (`MCU-CAN-12R`) is ON, connect CAN horizontally (`Green = CAN_L` left, `Yellow = CAN_H` right), and connect EBB SB2209 24V via WAGO blocks.
  * ⚠️ **Ensure `USB_5V` jumper on EBB SB2209 is REMOVED before applying 24V!**
* [ ] **Next Step 3 – Open Bench Power-On & Klipper Verification (Before Closing Ducts):**
  * Multimeter short check across `24V+` / `24V-` before powering on.
  * Verify Pi USB/CAN recognition (`ls /dev/serial/by-id/*`, `ip -s link show can0`).
  * With Toolhead (`EBBCan` + hotend thermistor), bed thermistor (`TB`/`PF3`), chamber thermistor (`T3`/`PF7`), Z motors, and provisionally A/B motors + `XY STOP` connected (never plug/unplug steppers or CAN while powered): verify Mainsail (`http://192.168.1.120`), temperatures, `QUERY_ENDSTOPS`, `QUERY_PROBE`, fans, and `STEPPER_BUZZ` (no homing).
* [ ] **Next Step 4 – Gantry Assembly, Cable Ducts & Final Verification:**
  * Assemble/install gantry and Z drives/belts, route cables neatly into ducts only after open tests pass, and re-verify `QUERY_ENDSTOPS`, `QUERY_PROBE`, and thermistors once ducts are closed.
* [ ] **Next Step 5:** Print remaining electronics bay mounts, skirts, and panel hardware as needed.
