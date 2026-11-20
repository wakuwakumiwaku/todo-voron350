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

*Last updated: 2026-11-20*

### Immediate Task (In Progress on Snapmaker U1 / Desktop)
* **Print `RSP-200-24` Terminal Cover + Compact 2× `WAGO 221-415` Mount:**
  * **Terminal Cover:** Safety cover over the MeanWell `RSP-200-24` AC/DC screw terminals.
  * **WAGO Mount:** Note that stock Voron `wago_221-415_mount_3by5.stl` is **`126.8 × 23.0 mm`** and spans across **two** parallel DIN rails (`23 mm` rail length). Since free DIN rail length near the PSU is limited (`< 3 cm`), print either a **compact stacked/vertical 2× WAGO 221-415 single-rail mount** (`~15–20 mm` along rail), a **2020-extrusion M3 mount**, or a **deck-plate mount** near the `24V` (`+V`/`-V`) end of the PSU (away from `AC/L`/`AC/N`).

### Completed & Verified
* [x] **Motion System & Kinematics:** 100% printed and assembled (CNC A/B drives, CNC XY-joints, GE5C Z-joints, SBFI front idlers, BZI top idlers, CNC Tap V2).
* [x] **Electronics & CAN Bench Test:** 100% verified (Pi 4, U2C v2.1, EBB SB2209 RP2040 flashed with Katapult + Klipper, UUID discovered, 60 $\Omega$ bus termination verified).
* [x] **24V PSU (`RSP-200-24`) Mounted on DIN Rail (2026-11-19):**
  * Printed and installed **DIN Rail End Stops** on the 35 mm DIN rail; **MeanWell RSP-200-24** is now secured on the rail.
  * Finalized **central 24V WAGO 221-415 (`32 A` IEC, `0.14–4 mm²`) distribution architecture**:
    * Short **`14 or 16 AWG`** main feeders (`~6–10 cm`, fork lugs at PSU `0.8–1.0 N·m`, bare `~11 mm` in WAGO) from **1× `+V`** and **1× `-V`** on `RSP-200-24` into **2× WAGO 221-415** (`+24V` bus and `GND` bus), positioned on the 24V side away from 230V AC terminals.
    * **4× separate `18 AWG` silicone pairs** (lightly hand-twisted ~1 turn per 4–5 cm, untwisted last ~4–5 cm; ferrules on Octopus ends, bare `~11 mm` in WAGO without ferrules) to **`MOTOR POWER +/-`**, **`POWER +/-`**, **`BED POWER +/-`**, and **`CANBUS +24V/GND`**.
* [x] **USB Webcam Bench Test (`icSpring`, 2026-11-19) & Sustained Datarate / RPi 4 Spec Verification (2026-11-20):**
  * Detected plug-and-play via Linux `uvcvideo` (`lsusb`: `32e6:9221 icSpring icspring camera`, serial `24091116320721`, `bcdUSB 2.00` High-Speed `480 Mbit/s`, isochronous video endpoint up to `3×1024 B`, `bMaxPower: 100mA` descriptor / ~0.5–1.3 W active).
  * `v4l2-ctl` capabilities: native **`MJPG`** at `1920×1080`, `1280×720`, and `640×480` (`15 / 30 fps`); `YUYV` at `640×480` (`30 fps`). Fixed focus (no autofocus hunting), `power_line_frequency=50Hz`, `white_balance_automatic=0` (`5600 K` default).
  * **2026-11-19 check:** Verified `1280×720` MJPG snapshot and **5 s `1920×1080 @ 30 fps` recording (`149` frames in `5.04 s`, `~28.2 Mbit/s`) + live `mpv` feed** — sharp wide-angle lens, zero drops.
  * **2026-11-20 live `v4l2-ctl --stream-mmap` & sustained stream test:**
    * `1920×1080 MJPG` (30 fps requested): **~19.8–25.8 fps**, **~141–145 KB/frame** (`~22.5 Mbit/s` / `~2.8 MB/s` at 19.86 fps), **0 dropped frames** (consecutive sequence numbers; `auto_exposure=3` Aperture Priority Mode lengthens exposure to ~50 ms in dim lighting). `640×480 YUYV` streamed cleanly at `~19.85–19.88 fps`.
    * Sustained **~5m46s `mpv` Wayland (`gpu-next`) `1920×1080` MJPG stream**: **0** kernel USB / `xhci_hcd` / `uvcvideo` errors, resets, or disconnects (`journalctl -k`).
  * **RPi 4 USB 3.0 & Multi-Device Budget Verified:**
    * **Blue USB-A (USB 3.0) port:** Backwards-compatible; `bcdUSB 2.00` camera negotiates **USB 2.0 High-Speed (480 Mbit/s)** on the blue port.
    * **Combined Bandwidth (Webcam + Octopus v1.1 + U2C v2.1):** `~35–40 Mbit/s` total (`~22–34 Mbit/s` 1080p MJPG webcam + `<1 Mbit/s` each for USB 2.0 Full-Speed Octopus & U2C) — well within RPi 4's `480 Mbit/s` USB 2.0 bus / `4 Gbit/s` PCIe xHCI link.
    * **Combined USB 5V Power:** `~150–200 mA` total (`100 mA` webcam + `~50–100 mA` U2C + `~0 mA` Octopus with `USB-PWR`/`VBUS` 5V jumper removed) out of RPi 4's `1200 mA` shared USB limit (requires solid `5.1V 3A` RPi 4 PSU).
* [x] **Thermistor Cable Repair & Bay Disassembly (2026-11-16):**
  * Thermistor cable repaired (live Klipper check pending power-on).
  * Bottom electronics bay cables unplugged to reseat **Octopus v1.1**, **Raspberry Pi 4**, and **BTT U2C v2.1** on DIN rails.
  * Printed `Octopus_bracket_set.stl` (verified from STL: `96.6 mm` bar, `90.5 mm` ear spacing, `7.0 mm` ear offset, `4 mm` bar + `3 mm` standoff = `7 mm`; mount **ears pointing INWARD** toward board center so DIN clips sit **OUTER** at `~164 mm` span for maximum stability; check lower bar clearance vs USB-C plug; align `pcb_din_clip` release tabs consistently toward the accessible side).
  * Identified and removed/retired unnecessary previous-owner wiring: unused 4-color SFS-style `STOP`/`DIAG` cable and obsolete `ABL` inductive-probe lead (`^PG15`, replaced by Voron Tap V2 on `EBBCan:gpio6`).
  * Verified USB-A to USB-C data+power cable with BTT U2C (`lsusb`: `1d50:606f`, `can0` detected).
  * Inspected 24V PSU & Octopus power harness:
    * PSU is **MeanWell RSP-200-24** (`200 W` / `~8.3 A` total across 3× `+V` and 3× `-V` M3.5 terminals; terminal torque **0.8–1.0 N·m**; bottom M4 holes `150×50 mm`, max **3 mm** screw depth).
    * LDO harness uses 3× `+` (`POWER +`, `MOTOR POWER +`, `BED POWER +`) and 1× `-` (`POWER -`), since Octopus `-` (`GND`) terminals share an internal ground plane; 2× `-V` PSU terminals are free (one can take CAN umbilical `GND` directly).
    * **If replacing the stiff LDO harness with `18 AWG` silicone (~7–10 A continuous in bay ducts):** MUST run **separate `-` (`GND`) wires** for both `POWER` and `MOTOR POWER` (do NOT share a single `18 AWG` return wire for motors + logic!), with ferrules on Octopus terminals and fork lugs on the PSU. `18 AWG` is also plenty for CAN umbilical `24V`/`GND` (`~2.5–3.5 A`).

### USB Cable Measurements & Ordering Specs (2026-11-16)
* **Measured Lengths (Net + Recommended Order Length incl. Slack):**
  1. **RPi 4 (USB 2.0) $\leftrightarrow$ BTT U2C v2.1 (USB-C):** `30 cm` (duct) + `5 cm` (RPi) + `8 cm` (U2C) = **`43 cm` net $\rightarrow$ order `50 cm` (0.5 m)**
  2. **RPi 4 (USB 2.0) $\leftrightarrow$ BTT Octopus v1.1 (USB-C):** `25–30 cm` (duct) + RPi/Octopus leads $\approx$ **`35–40 cm` net $\rightarrow$ order `50 cm` (0.5 m)**
  3. **5V PSU (RS-25-5) $\rightarrow$ RPi 4 (USB-C Power):** `5 + 7 + 14 + 14 + 2` = **`42 cm` net $\rightarrow$ order `50 cm` (0.5 m)** *(needs thick `18–20 AWG` power wires / 3A-rated USB-C cable or 2-wire 90° USB-C pigtail to prevent RPi undervoltage; strip/crimp PSU end with ferrules or fork lugs for RS-25-5 screw terminals)*
* **Ordering Guidelines:**
  * **Jacket:** **NOT braided** (no nylon sleeve – too stiff, snags on duct teeth); use soft **silicone, TPE, smooth PVC, or FPC ribbon** USB cables.
  * **Data Specs (for U2C & Octopus):** Must be **shielded USB 2.0 data-sync cables** (no charge-only cables; USB 3.0 is unnecessary and stiffer). Avoid stacked plug-in 90° adapters (prefer molded 90° cables).
  * **Right-Angle (90°) Connector Checks Before Ordering:**
    * **USB-C end:** Check whether the 90° exit needs to go **sideways (left/right parallel to PCB)** vs **up/down** (note: USB-C flips 180° for up/down, NOT for sideways-vs-up!). On RPi 4 power, watch clearance next to Micro-HDMI 0.
    * **USB-A end (RPi 4):** USB-A is **not reversible** and the two black USB 2.0 ports are stacked vertically right beside the blue USB 3.0 ports! Ensure two stacked 90° USB-A plugs exit in a non-blocking direction (e.g., both sideways away from the USB 3.0 ports, or straight USB-A at Pi + 90° USB-C at Octopus/U2C if Pi has clearance).
  * **USB Webcam Extension Cable (`icSpring` 1080p Camera $\rightarrow$ RPi 4 blue USB 3.0 port):**
    * Order a **shielded USB 2.0 extension cable (`USB-A male to USB-A female`, `0.5–1.0 m`**, keep total length ≤ ~1.5 m).
    * **Do NOT splice/solder** the tiny `28–30 AWG` twisted `D+`/`D-` pair or break the 5th shield wire (480 Mbit/s impedance & shielding are critical near stepper/230V wiring). Secure the USB-A coupling with heatshrink/electrical tape, mount the camera low/front (cooler during ABS prints), route via lower 2020 slot $\rightarrow$ rear Z-chain/deck cutout (avoid 230V duct), and route chamber LED wires (`HE2`/`PB10`) via rear `Z1`/`Z2` & `z_belt_cover` wire pass-through.

### CAN Umbilical Support & Shopping Notes (2026-11-16)
* **Purpose:** Keeps the floating CAN umbilical (`1_G2E_CAN_Cable_Mount_PG7.stl` at toolhead to rear frame) arched cleanly upward so it never sags into A/B belts or extrusions.
* **What to buy (choose ONE spine + sleeve):**
  1. **Internal Spine (pick one):**
     * **Option A (Preferred): Spring Steel / Piano Wire `0.8 mm`** (gold standard for 350 mm Voron; up to `1.0 mm` only for extra-heavy bundles; `≥1.2 mm` is too stiff). ⚠️ **Must round/file cut ends and seal with heatshrink/glue** so it cannot puncture wire insulation; clamp ends mechanically only.
     * **Option B (Safer/simpler): Nylon Trimmer Line (weed-whacker cord) `2.4–3.0 mm`** (safer around wires, easy to cut, though nylon can take a slight permanent bend in hot chambers over time).
  2. **Outer Sleeve:** **PET Expandable Braided Sleeve `8–10 mm`** (melt cut ends slightly with a lighter; route CAN cable + spine together inside the sleeve, and terminate/heatshrink the sleeve cleanly at the PG7 gland if all layers together are too tight inside the `3–6.5 mm` PG7 seal). *(Note: Do NOT use braided USB cables in the bottom bay ducts; braided PET sleeve is specifically for the upper moving CAN umbilical.)*

### Next Steps
* [x] **Next Step 1 – Print & Install 35 mm DIN Rail End Stops:**
  * Completed 2026-11-19: **MeanWell RSP-200-24** secured on the 35 mm DIN rail.
* [ ] **Next Step 2 – Print `RSP-200-24` Terminal Cover & Compact 2× `WAGO 221-415` Mount:**
  * Print terminal cover for `RSP-200-24` and a compact 2× `WAGO 221-415` holder (single-rail `~1.5–2 cm`, 2020 extrusion M3 mount, or deck-plate mount).
* [ ] **Next Step 3 – Splice & Test `XY STOP` (Eliminating LDO Breakout PCB):**
  * Measure 4-pin `XY STOP` cable (`~0 Ω` untouched, `OL` when pressed) to identify common `GND`, `X-Signal`, `Y-Signal`, and unused `Vin` (insulate `Vin`).
  * Splice `XY STOP` directly onto the Octopus-side 3-pin pigtails of `XES` (`DIAG3` / `PG11`) and `YES` (`DIAG0` / `PG6`): split `GND` to both middle pins, `X` / `Y` to the populated outer signal pins (`5V` pin stays empty).
* [ ] **Next Step 4 – Reseat Bottom Boards & Open Pre-Duct Wiring:**
  * Reseat **Octopus v1.1** (`M3` PCB / `M2x10` DIN clips), **Raspberry Pi 4** (`M2.5x6`/`M2.5x8` PCB — never force `M3` through Pi `M2.5` holes / `M2x10` DIN clips), and **BTT U2C v2.1** (`M3x6`/`M3x8` PCB / `M2x10` DIN clips) on DIN rails (keep cable ducts open during testing; use 90° USB cables/adapters or pre-plug USBs if clearance is tight).
  * **Finalized 3-Duct Routing Plan (EMC separation):**
    * **Left duct:** USB data cables (`RPi 4 ↔ U2C` and `RPi 4 ↔ Octopus`) + CAN data/umbilical (keep away from 230V AC / SSR).
    * **Center duct:** Octopus motor/sensor/fan cables + RPi 4 5V USB-C power (routed from right $\rightarrow$ bottom $\rightarrow$ center up to RPi 4 using a thick, low-drop 5V cable).
    * **Right duct (and area between right & center duct):** 230V AC mains/SSR wiring, `RSP-200-24`, and SSR.
  * Reconnect Octopus per active `klipper_config/printer.cfg`: Bed SSR on `BED_OUT` (`PA1`), `Z`/`Z1`/`Z2` on `MOTOR2_1`/`MOTOR3`/`MOTOR4`, `Z3` on `MOTOR7`, `X` on `DIAG3` (`PG11`), `Y` on `DIAG0` (`PG6`), `12V` jumpers on `FAN4` and `FAN6`/`FAN7` where needed.
  * Wire 24V power via **2× WAGO 221-415** (`14/16 AWG` short feeders from `RSP-200-24` `+V`/`-V` at `0.8–1.0 N·m`, then 4× lightly hand-twisted `18 AWG` silicone pairs to `MOTOR POWER`, `POWER`, `BED POWER`, and `CANBUS`).
  * Connect U2C USB-C to RPi 4 black USB 2.0 port, verify U2C `120R` jumper (`MCU-CAN-12R`) is ON, connect CAN horizontally (`Green = CAN_L` left, `Yellow = CAN_H` right) with strain relief at the bay entry and loose service loop (keep excess coiled loosely / away from 230V until gantry is fitted).
  * ⚠️ **Ensure `USB_5V` jumper on EBB SB2209 AND the `USB-PWR` (`VBUS`) 5V jumper next to the USB-C port on BTT Octopus v1.1 are REMOVED before applying 24V!**
* [ ] **Next Step 5 – Open Bench Power-On & Klipper Verification (Before Closing Ducts):**
  * Multimeter short check across `24V+` / `24V-` before powering on.
  * Verify Pi USB/CAN recognition (`ls /dev/serial/by-id/*`, `ip -s link show can0`).
  * With Toolhead (`EBBCan` + hotend thermistor), bed thermistor (`TB`/`PF3`), chamber thermistor (`T3`/`PF7`), Z motors, and provisionally A/B motors + `XY STOP` connected (never plug/unplug steppers or CAN while powered): verify Mainsail (`http://192.168.1.120`), temperatures, `QUERY_ENDSTOPS`, `QUERY_PROBE`, fans, and `STEPPER_BUZZ` (no homing).
  * **Webcam (`klipper_config/crowsnest.conf`):** Plug `icSpring` camera into RPi 4 blue USB 3.0 port (plug-and-play `uvcvideo` on port `8080`); bump `resolution` from `640x480` to `1280x720` (or `1920x1080` @ `15–20 fps`), optionally switch `/dev/video0` to `/dev/v4l/by-id/...`, and tune `white_balance_automatic=1` via `v4l2ctl` / rotation in Mainsail once mounted.
* [ ] **Next Step 6 – Gantry Assembly, Cable Ducts & Final Verification:**
  * Assemble/install gantry and Z drives/belts, verify full travel before trimming CAN umbilical slack, route cables neatly into ducts only after open tests pass, and re-verify `QUERY_ENDSTOPS`, `QUERY_PROBE`, and thermistors once ducts are closed.
* [ ] **Next Step 7:** Print remaining electronics bay mounts, skirts, and panel hardware as needed.
