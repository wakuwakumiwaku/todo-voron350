#!/usr/bin/env bash
# EBB SB2209 RP2040 Flash & Setup Helper Script for Voron 2.4 LDO Rev C
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SCRIPT_DIR/printer_data/config"
EBB_CFG="$CONFIG_DIR/ebb-sb2209.cfg"

echo "=========================================================="
echo "    BTT EBB SB2209 RP2040 Setup & Flash Assistant         "
echo "=========================================================="
echo "1) Build Katapult (bootloader) for EBB RP2040"
echo "2) Flash Katapult via USB (Board in BOOTSEL mode)"
echo "3) Build Klipper firmware for EBB RP2040 (with Katapult 16KiB offset)"
echo "4) Flash Klipper over CAN using Katapult"
echo "5) Flash Klipper directly via USB (No bootloader)"
echo "6) Query CANbus UUID and automatically update ebb-sb2209.cfg"
echo "7) Check CANbus status and error counters"
echo "8) Optimize CAN network interface (set txqueuelen 1024)"
echo "q) Quit"
echo "----------------------------------------------------------"
read -rp "Select an option [1-8, q]: " choice


case "$choice" in
    1)
        echo "--> Building Katapult for RP2040 (CAN on GPIO 4/5, 1Mbps)..."
        cd "$SCRIPT_DIR/katapult"
        make clean || true
        cat << 'EOF' > .config
CONFIG_LOW_LEVEL_OPTIONS=y
CONFIG_MACH_RPXXXX=y
CONFIG_MACH_RP2040=y
CONFIG_RPXXXX_CANBUS=y
CONFIG_RPXXXX_CANBUS_GPIO_RX=4
CONFIG_RPXXXX_CANBUS_GPIO_TX=5
CONFIG_CANBUS_FREQUENCY=1000000
EOF
        make olddefconfig
        make -j4
        echo "Katapult build successful: $SCRIPT_DIR/katapult/out/katapult.uf2"
        ;;

    2)
        echo "--> Flashing Katapult via USB..."
        echo "Make sure the board is in BOOTSEL mode (hold BOOT while plugging into USB)."
        cd "$SCRIPT_DIR/katapult"
        make flash FLASH_DEVICE=2e8a:0003
        echo "Katapult flashed successfully!"
        ;;

    3)
        echo "--> Building Klipper for RP2040 (CAN GPIO 4/5, 1Mbps, 16KiB offset)..."
        cd "$SCRIPT_DIR/klipper"
        make clean || true
        cat << 'EOF' > .config
CONFIG_LOW_LEVEL_OPTIONS=y
CONFIG_MACH_RPXXXX=y
CONFIG_MACH_RP2040=y
CONFIG_RPXXXX_FLASH_START_4000=y
CONFIG_RPXXXX_CANBUS=y
CONFIG_RPXXXX_CANBUS_GPIO_RX=4
CONFIG_RPXXXX_CANBUS_GPIO_TX=5
CONFIG_CANBUS_FREQUENCY=1000000
EOF
        make olddefconfig
        make -j4
        echo "Klipper build successful: $SCRIPT_DIR/klipper/out/klipper.bin"
        ;;

    4)
        echo "--> Querying Katapult UUID on can0..."
        KAT_UUID=$(python3 "$SCRIPT_DIR/katapult/scripts/flashtool.py" -i can0 -q | grep -oE "0x[0-9a-fA-F]+|[0-9a-fA-F]{12}" | head -n1 || true)
        if [ -z "$KAT_UUID" ]; then
            read -rp "Could not auto-detect Katapult UUID. Enter Katapult UUID manually: " KAT_UUID
        else
            echo "Found Katapult UUID: $KAT_UUID"
        fi
        echo "--> Flashing Klipper over CAN bus..."
        python3 "$SCRIPT_DIR/katapult/scripts/flashtool.py" -i can0 -u "$KAT_UUID" -f "$SCRIPT_DIR/klipper/out/klipper.bin"
        echo "Klipper successfully flashed over CAN!"
        ;;

    5)
        echo "--> Building & Flashing Klipper directly via USB (No bootloader)..."
        cd "$SCRIPT_DIR/klipper"
        make clean || true
        cat << 'EOF' > .config
CONFIG_LOW_LEVEL_OPTIONS=y
CONFIG_MACH_RPXXXX=y
CONFIG_MACH_RP2040=y
CONFIG_RPXXXX_FLASH_START_0100=y
CONFIG_RPXXXX_CANBUS=y
CONFIG_RPXXXX_CANBUS_GPIO_RX=4
CONFIG_RPXXXX_CANBUS_GPIO_TX=5
CONFIG_CANBUS_FREQUENCY=1000000
EOF
        make olddefconfig
        make -j4
        echo "Flashing via USB..."
        make flash FLASH_DEVICE=2e8a:0003
        echo "Done!"
        ;;

    6)
        echo "--> Scanning can0 for Klipper UUID..."
        FOUND_UUID=$("$SCRIPT_DIR/klippy-env/bin/python" "$SCRIPT_DIR/klipper/scripts/canbus_query.py" can0 | grep -oE "[0-9a-fA-F]{12}" | head -n1 || true)
        if [ -n "$FOUND_UUID" ]; then
            echo "Discovered UUID: $FOUND_UUID"
            if [ -f "$EBB_CFG" ]; then
                sed -i "s/canbus_uuid:.*/canbus_uuid: $FOUND_UUID/" "$EBB_CFG"
                echo "Successfully updated $EBB_CFG with UUID: $FOUND_UUID"
                echo "Restarting Klipper service..."
                sudo systemctl restart klipper || true
            else
                echo "Warning: $EBB_CFG not found."
            fi
        else
            echo "No CAN devices detected on can0. Check wiring, termination jumpers, and power."
        fi
        ;;

    7)
        echo "--> Checking can0 interface status..."
        ip -details -statistics link show can0 || true
        ;;

    8)
        echo "--> Setting txqueuelen 1024 and configuring 25-can.network..."
        sudo tee /etc/systemd/network/25-can.network > /dev/null << 'EOF'
[Match]
Name=can*

[CAN]
BitRate=1M

[Link]
TransmitQueueLength=1024
RequiredForOnline=no
EOF
        sudo systemctl restart systemd-networkd || true
        echo "CAN network settings updated!"
        ;;

    q|Q)

        exit 0
        ;;

    *)
        echo "Invalid selection."
        ;;
esac
