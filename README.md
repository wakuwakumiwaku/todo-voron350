# Voron 2.4 R2 (350 mm) – Printed Parts Checklist & Build Tracker

Automated parts tracker and progress checklist for the **Voron 2.4 R2 350 mm** build based on the print history from Fluidd / Klipper (`192.168.1.80`).

---

## Machine Specifications & Mods

* **Build Volume:** 350 × 350 × 350 mm
* **Base Kit:** LDO Motors Voron 2.4 R2 Kit
* **Toolhead:** Voron Stealthburner
* **Hotend:** Phaetus Revo Voron
* **Extruder:** Galileo 2 Extruder (G2E) – Planetary 9:1
* **Toolhead PCB:** BigTreeTech EBB SB2209 RP2040 CAN Bus (PG7 Cable Gland Umbilical)
* **Probe / X-Carriage:** ChaoticLab CNC Voron TAP V2 (All-Metal CNC Aluminum)
* **Front Idlers:** Shang Bo Front Idlers Mod (SBFI V2.4)
* **Z-Joints:** GE5C Spherical Bearing Mod (igus EGLM-05)
* **XY-Endstop:** Hartk D2F Microswitch PCB Pod
* **Controller:** BigTreeTech Octopus / Octopus Pro
* **SBC:** Raspberry Pi

---

## Recommended Slicer Settings (Voron Standard)

* **Material:** ASA / ABS (e.g. IEMAI ASA)
* **Nozzle Temperature:** 265 – 270 °C (First Layer: 267 °C)
* **Bed Temperature:** 110 °C (Preheated / Chamber Heat-Soaked)
* **Layer Height:** 0.20 mm (First Layer: 0.20 mm)
* **Extrusion Width:** 0.40 mm forced (First Layer: 0.45 mm)
* **Wall Count:** 4 perimeters (Loops)
* **Top / Bottom Solid Layers:** 5 layers
* **Infill:** 40% Gyroid (or Grid / Cubic)
* **Supports:** **NONE** (All Voron parts are self-supporting with built-in 0.2 mm sacrificial bridges)
* **Part Cooling Fan:** 10 – 30% max, 0% for the first 5 layers, 40% on overhangs

---

## Progress Overview

```
[====================>               ] ~55% Complete (All Toolhead & Core Motion Done)
```

| Subsystem | Status | Progress | Notes |
| :--- | :---: | :---: | :--- |
| **Toolhead (SB + G2E + Revo + CAN)** | **100%** | 15 / 15 parts | Fully printed & assembled |
| **Probe (CNC Tap V2)** | **100%** | Hardware | ChaoticLab CNC aluminum carriage |
| **Front Idlers (SBFI Mod)** | **100%** | 8 / 8 parts | Fully printed |
| **Z-Joints (GE5C Mod)** | **100%** | 8 / 8 parts | Fully printed |
| **XY Endstop** | **100%** | 1 / 1 part | Hartk D2F pod printed |
| **Z-Drives (Lower 4 Corners)** | **83%** | 10 / 12 parts | Only `z_drive_main_b_x2.stl` missing! |
| **Z-Idlers (Upper 4 Corners)** | **0%** | 0 / 8 parts | Pending |
| **A/B-Drive Units (Rear Motors)** | **20%** | 2 / 7 parts | Frame mounts pending |
| **XY-Joints (MGN12)** | **0%** | 0 / 5 parts | Pending |
| **Electronics Bay** | **0%** | 0 / ~14 parts | Pending |
| **Skirts (350 mm)** | **0%** | 0 / ~16 parts | Pending |
| **Panels & Doors (4 mm)** | **0%** | 0 / ~35 parts | Pending |

---

## 1. Completed Parts (`[x]`)

### Stealthburner & Galileo 2 Extruder (G2E)
- [x] `[a]_stealthburner_main_body.stl`
- [x] `stealthburner_printhead_revo_voron_front.stl`
- [x] `stealthburner_printhead_revo_voron_rear_cw2.stl`
- [x] `front_body_ECAS_coupler.stl` (Galileo 2 front)
- [x] `front_body.stl` (Galileo 2 front alternative)
- [x] `rear_body.stl` (Galileo 2 rear)
- [x] `[a]_front_half_g2.stl`
- [x] `[a]_rear_half_g2.stl`
- [x] `[a]_front_bearing_holder.stl`
- [x] `idler_bearing_cover.stl`
- [x] `cable_cover.stl`
- [x] `g2_ptfe_cutting_tool.stl`
- [x] `1_G2E_CAN_Cable_Mount_PG7.stl`
- [x] `2_G2E_Cable_Door_for_CAN.stl`
- [x] `3_Optional_12mm_Standoff.stl`
- [x] `4_BTT_EBB_PCB_Cover.stl`

### Front Idlers (Shang Bo Front Idlers – SBFI V2.4)
- [x] `SBFI-V2.4_Housing_x2.stl` (Housing left & right)
- [x] `Idler_Body_1.stl` (2× printed)
- [x] `Carrier_1.stl` (2× printed – bearing carrier)
- [x] `[a]_SBFI-V2.4_Front_Magnetic_Cover_x2.stl`
- [x] `[a]_SBFI-V2.4_Belt_Clamp_x4.stl`
- [x] `[a]_SBFI-V2.4_Belt_Clamp_AB_Drives_x2.stl`

### Z-Joints (GE5C Spherical Bearing Mod)
- [x] `z_joint_ge5c_igus_eglm-05_x4.stl` (4× Z-joints for igus bearings)
- [x] `[a]_z_belt_clamp_lower_x4.stl` (4× lower belt clamps)

### XY-Endstop
- [x] `[a]_endstop_pod_D2F_switch.stl` (Hartk microswitch pod)

### Z-Drives (Bottom 4 Corners)
- [x] `[a]_z_drive_baseplate_a_x2.stl` (2× baseplate side A)
- [x] `[a]_z_drive_baseplate_b_x2.stl` (2× baseplate side B)
- [x] `[a]_belt_tensioner_a_x2.stl` (2× tensioner arm side A)
- [x] `[a]_belt_tensioner_b_x2.stl` (2× tensioner arm side B)
- [x] `z_motor_mount_a_x2.stl` (2× motor mount side A)
- [x] `z_motor_mount_b_x2.stl` (2× motor mount side B)
- [x] `z_drive_retainer_a_x2.stl` (2× retainer side A)
- [x] `z_drive_retainer_b_x2.stl` (2× retainer side B)
- [x] `z_drive_main_a_x2.stl` (2× main body side A)

---

## 2. Missing Parts Todo List (`[ ]`)

### Priority 1: Motion System & Frame Mechanics

#### Z-Drives (Finish Lower Assembly)
- [ ] `z_drive_main_b_x2.stl` – **Qty: 2** *(Primary Color) – The final piece needed to complete all 4 Z-Drives!*

#### Z-Idlers (Top Frame Corners)
- [ ] `z_tensioner_bracket_a_x2.stl` – **Qty: 2** *(Primary Color)*
- [ ] `z_tensioner_bracket_b_x2.stl` – **Qty: 2** *(Primary Color)*
- [ ] `[a]_z_tensioner_9mm_x4.stl` – **Qty: 4** *(Accent Color)*

#### A/B-Drive Units (Rear Upper Motor Mounts)
- [ ] `a_drive_frame_upper.stl` – **Qty: 1** *(Primary Color)*
- [ ] `a_drive_frame_lower.stl` – **Qty: 1** *(Primary Color)*
- [ ] `b_drive_frame_upper.stl` – **Qty: 1** *(Primary Color)*
- [ ] `b_drive_frame_lower.stl` – **Qty: 1** *(Primary Color)*
- [ ] `[a]_cable_cover.stl` – **Qty: 1** *(Accent Color)*

#### XY-Joints (MGN12)
- [ ] `xy_joint_left_upper_MGN12.stl` – **Qty: 1** *(Primary Color)*
- [ ] `xy_joint_left_lower_MGN12.stl` – **Qty: 1** *(Primary Color)*
- [ ] `xy_joint_right_upper_MGN12.stl` – **Qty: 1** *(Primary Color)*
- [ ] `xy_joint_right_lower_MGN12.stl` – **Qty: 1** *(Primary Color)*
- [ ] `[a]_xy_joint_cable_bridge_2hole.stl` – **Qty: 1** *(Accent Color – LDO 2-hole drag chain version)*

#### Z Drag Chain Guides
*(Note: X/Y drag chains omitted due to CAN bus umbilical)*
- [ ] `z_chain_bottom_anchor.stl` – **Qty: 1**
- [ ] `z_chain_guide.stl` – **Qty: 1**
- [ ] `[a]_z_chain_retainer_bracket_x2.stl` – **Qty: 2**

---

### Priority 2: Electronics Bay (DIN Rails & Underbed)

#### Controller & SBC Mounts
- [ ] `Octopus_bracket_set.stl` – **Qty: 1 set** *(BigTreeTech Octopus / Octopus Pro)*
- [ ] `raspberrypi_bracket.stl` (or LDO `beefy_raspberry_bracket.stl`) – **Qty: 1**
- [ ] `pcb_din_clip_x3.stl` – **Qty: 6 to 8 clips** *(DIN rail clips for all electronics)*

#### Power Supply Brackets (LDO Kit PSUs)
- [ ] `lrs_200_psu_bracket_x2.stl` – **Qty: 2** *(MeanWell LRS-200-24 24V PSU)*
- [ ] `rs25_psu_bracket.stl` – **Qty: 1** *(MeanWell RS-25-5 5V PSU)*
- [ ] `PSU_stabilizer_50mm.stl` – **Qty: 1**

#### Terminal Mounts
- [ ] `wago_221-415_mount_3by5.stl` – **Qty: 1** *(WAGO 221-415 distribution blocks)*
- [ ] `bed_wago_mount.stl` – **Qty: 1** *(LDO bed heater terminal block mount)*

---

### Priority 3: Skirts & Inlets (Size 350 mm)

#### 350 mm Outer Skirts
- [ ] `front_skirt_a_350.stl` – **Qty: 1**
- [ ] `front_skirt_b_350.stl` – **Qty: 1**
- [ ] `side_skirt_a_350_x2.stl` – **Qty: 2**
- [ ] `side_skirt_b_350_x2.stl` – **Qty: 2**
- [ ] `rear_center_skirt_350.stl` – **Qty: 1**

#### Skirt Inserts & Fan Grills
- [ ] `[a]_belt_guard_a_x2.stl` – **Qty: 2** *(Accent Color)*
- [ ] `[a]_belt_guard_b_x2.stl` – **Qty: 2** *(Accent Color)*
- [ ] `[a]_fan_grill_a_x2.stl` – **Qty: 2** *(Accent Color)*
- [ ] `[a]_fan_grill_b_x2.stl` – **Qty: 2** *(Accent Color)*
- [ ] `[a]_fan_grill_retainer_x2.stl` – **Qty: 2** *(Accent Color)*
- [ ] `side_fan_support_x2.STL` – **Qty: 2**

#### Power Inlet & Interface
- [ ] `power_inlet_IECGS_1.2mm.stl` (or 1.0mm) – **Qty: 1** *(Matches LDO switched fused inlet)*
- [ ] `keystone_panel.stl` – **Qty: 1**
- [ ] `[a]_keystone_blank_insert.stl` – **Qty: 1 to 2**
- [ ] Display Mount – **Qty: 1** *(e.g. BTT Pi TFT4.3 mount from LDO repo)*

---

### Priority 4: Panels (4 mm LDO), Doors & Filtration

#### Panel Mounting (LDO 4 mm Panels)
- [ ] `deck_support_4mm_x8.stl` – **Qty: 8** *(Supports 4 mm deck plate)*
- [ ] `corner_panel_clip_4mm_x8.stl` – **Qty: 8**
- [ ] `midspan_panel_clip_4mm_x7.stl` – **Qty: 7**
- [ ] `bottom_panel_clip_x4.stl` – **Qty: 4**
- [ ] `bottom_panel_hinge_x2.stl` – **Qty: 2**
- [ ] `z_belt_cover_a_x2.stl` – **Qty: 2** (or LDO LED wire pass-through version)
- [ ] `z_belt_cover_b_x2.stl` – **Qty: 2**

#### Front Doors
- [ ] `door_hinge_x6.stl` – **Qty: 6** (or LDO custom numbered hinges)
- [ ] `handle_a_x2.stl` & `handle_b_x2.stl` – **Qty: 1 set**
- [ ] `latch_x2.stl` – **Qty: 2**

#### Air Filtration (Nevermore V5 Duo)
- [ ] Nevermore Micro V5 Duo Housing & Plenum *(Included in LDO Kit)*
- [ ] `exhaust_cover.stl` + `exhaust_filter_grill.stl` *(Seals stock rear exhaust cutout when running Nevermore)*

---

### Priority 5: Assembly Jigs & Utility

- [ ] `pulley_jig.stl` – **CRITICAL TOOL:** Used to space GT2 pulleys on stepper motor shafts with exact clearance before installing motors into drive housings.
- [ ] `spool_holder.stl` – **Qty: 1**
- [ ] `bowden_retainer.stl` – **Qty: 1**
- [ ] `MGN12_rail_guide_x2.stl` – **Qty: 2** *(Useful for centering rails on 2020 extrusions)*

---

*Last updated: 01.10.2026 via Fluidd print audit.*
