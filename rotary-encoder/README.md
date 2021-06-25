# Description
This tool allows using a KY-040 rotary encoder with `Mixxx` on a Raspberry Pi. The project is composed on the following:

* `knob_midi_startup.py`: Python script handling the hardware interrupts and translating them to MIDI commands, acting as a MIDI virtual device
* `ky040.service`: a systemd service file for starting the Python script at boot
* `ky040.midi.xml`: a mixxx MIDI controller file 

# Requirements

* A Raspberry Pi 3B or 4B
* A SmartPi Touch 2 case
* A breakout board for the KY040 rotary encoder
* Debian running on the Raspberry Pi

# Hardware instructions

First, follow the hardware instructions in `Hardware instructions.odt`.

# Installation

Copy the following files to their respective destinations:

* `knob_midi_startup.py` -> `/home/pi/`
	* This assumes that the user is `pi`
* `ky040.service` -> `/lib/systemd/system/`
	* If the user is not `pi` or if the Python script is located somewhere else than `/home/pi/`, then this systemd script must be edited
* `ky040.midi.xml` -> `~/.mixxx/controllers`

Enable and start the systemd service:
```bash
sudo systemctl enable ky040.service
sudo systemctl start ky040.service
```

Check the status of the systemd service:
```bash
sudo systemctl status ky040.service
```

It should return something like this:

```
● ky040.service - KY040 rotary encoder driver
   Loaded: loaded (/lib/systemd/system/ky040.service; enabled; vendor preset: enabled)
   Active: active (running) since Fri 2021-06-25 15:35:27 CEST; 3s ago
 Main PID: 1202 (python3)
    Tasks: 2 (limit: 4915)
   CGroup: /system.slice/ky040.service
           └─1202 /usr/bin/python3 /home/pi/knob_midi_startup.py > /home/pi/sample.log 2>&1

Jun 25 15:35:27 raspberrypi systemd[1]: Started KY040 rotary encoder driver.
```

Start mixxx and enable the KY040 MIDI controller

# Usage

The current MIDI mapping is the following:
* rotating clockwise: zoom in waveforms
* rotating counterclockwise: zoom out waveforms
* pressing button: hide/maximize library

The mapping can be changed using mixxx's MIDI learning wizard.
