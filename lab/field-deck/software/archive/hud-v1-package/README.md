# 6 - HUD Software (fielddeck-hud v1.0)

OLED stats HUD + EC11 encoder + X1201 battery readout + RTL-SDR setup for the
selfdriven.you Field Deck. Pin map is the locked one in
`2 - Docs/FieldDeck-HUD-Wiring.png` (OLED pins 1/3/5/9 @0x3C; encoder GPIO17/27/22).

- `install.sh` — one-shot installer ON THE PI (`sudo bash install.sh`, then reboot)
- `DRYRUN.md` — table-top bench test, start here BEFORE the case exists
- `fielddeck/battery.py` — X1201 fuel gauge (I2C 0x36) + `fielddeck-bat` CLI
- `fielddeck/hud.py` — OLED service, 4 pages, encoder paging, systemd unit
- `fielddeck/battery_widget.py` — always-on-top battery pill for the touch display

Getting it onto the Pi: copy this whole folder over (`scp -r "6 - HUD Software"
<user>@<pi-ip>:~/` — SSH by IP, .local is unreliable on this LAN).
