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

* [x] **Motion System & Kinematics:** 100% printed and assembled (CNC A/B drives, CNC XY-joints, GE5C Z-joints, SBFI front idlers, BZI top idlers, CNC Tap V2).
* [x] **Electronics & CAN Bench Test:** 100% verified (Pi 4, U2C v2.1, EBB SB2209 RP2040 flashed with Katapult + Klipper, UUID discovered, 60 $\Omega$ bus termination verified).
* [ ] **Next Step 1:** Mount EBB SB2209 to Galileo 2 toolhead with PG7 cable mount and cable door.
* [ ] **Next Step 2:** Route 4-wire umbilical cable through frame to electronics bay.
  * Connect Red (+24V) & Black (GND) to 24V WAGO distribution blocks.
  * Connect Yellow (CAN_H) & Green (CAN_L) horizontally to U2C 4-pin header.
  * ⚠️ **Ensure `USB_5V` jumper on EBB SB2209 is REMOVED before applying 24V!**
* [ ] **Next Step 3:** Connect Octopus board via USB to Raspberry Pi 4 and power on printer.
* [ ] **Next Step 4:** Print electronics bay mounts (`Mods_Electronics_U2C_Pi`), skirts, and panels.
