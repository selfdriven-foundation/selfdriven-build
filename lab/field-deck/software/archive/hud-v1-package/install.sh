#!/usr/bin/env bash
# Field Deck HUD installer — run ON THE PI, from this folder:  sudo bash install.sh
set -euo pipefail
[ "$(id -u)" -eq 0 ] || { echo "run with sudo"; exit 1; }
REAL_USER="${SUDO_USER:-pi}"
REAL_HOME="$(getent passwd "$REAL_USER" | cut -d: -f6)"
DEST=/opt/fielddeck

echo "== packages =="
apt-get update -qq
apt-get install -y -qq python3-pip python3-smbus i2c-tools python3-gi \
    gir1.2-gtk-3.0 rtl-sdr fonts-dejavu-core wireless-tools
pip3 install --break-system-packages -q luma.oled smbus2 gpiozero

echo "== enable I2C =="
raspi-config nonint do_i2c 0

echo "== RTL-SDR: keep the DVB kernel driver off the dongle =="
cat > /etc/modprobe.d/blacklist-rtlsdr-dvb.conf <<'EOF'
blacklist dvb_usb_rtl28xxu
blacklist rtl2832
blacklist rtl2830
EOF

echo "== install package =="
mkdir -p "$DEST"
cp -r fielddeck "$DEST/"
cat > /usr/local/bin/fielddeck-bat <<EOF
#!/usr/bin/env bash
exec python3 -c "import sys; sys.path.insert(0,'$DEST'); from fielddeck.battery import main; main()" "\$@"
EOF
chmod +x /usr/local/bin/fielddeck-bat

echo "== HUD systemd service =="
cat > /etc/systemd/system/fielddeck-hud.service <<EOF
[Unit]
Description=Field Deck HUD (OLED + encoder)
After=multi-user.target

[Service]
Type=simple
User=$REAL_USER
Environment=PYTHONPATH=$DEST
ExecStart=/usr/bin/python3 -m fielddeck.hud
Restart=on-failure
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF
systemctl daemon-reload
systemctl enable fielddeck-hud.service

echo "== battery widget autostart (desktop session) =="
sudo -u "$REAL_USER" mkdir -p "$REAL_HOME/.config/autostart"
cat > "$REAL_HOME/.config/autostart/fielddeck-battery.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Field Deck battery
Exec=python3 -c "import sys; sys.path.insert(0,'$DEST'); from fielddeck.battery_widget import main; main()"
X-GNOME-Autostart-enabled=true
EOF
chown "$REAL_USER":"$REAL_USER" "$REAL_HOME/.config/autostart/fielddeck-battery.desktop"

echo
echo "DONE. Reboot once (I2C + driver blacklist), then:"
echo "  fielddeck-bat                         # battery in the terminal"
echo "  sudo systemctl start fielddeck-hud    # or it starts itself on boot"
echo "  python3 -c 'import sys; sys.path.insert(0,\"$DEST\")' # (module lives in $DEST)"
echo "Bench mode with live event logging:"
echo "  sudo systemctl stop fielddeck-hud && PYTHONPATH=$DEST python3 -m fielddeck.hud --bench"
