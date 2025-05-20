# Hand-Gesture-Spotify-Controlled-music-player
Hand Gesture Spotify Controlled music player


Here's a `README.md` file for your Python script `music_system_control.py`, which appears to control a music system using voice commands:

---

````markdown
# Music System Control using Voice Commands

This project provides a Python-based voice-controlled interface to manage and control your system’s default music player. It allows users to perform actions like play, pause, stop, next track, and volume control using spoken commands.

## Features

- Voice command recognition using the microphone
- Control media playback:
  - Play
  - Pause
  - Stop
  - Next
  - Previous
- Adjust system volume:
  - Volume Up
  - Volume Down
- Supports continuous command processing in a loop

## Requirements

- Python 3.6+
- Works on Windows OS

### Python Libraries Used

- `speech_recognition`
- `pyttsx3`
- `pycaw` (for controlling system audio)
- `keyboard` (for simulating keypresses)
- `comtypes`

Install the required packages using:

```bash
pip install -r requirements.txt
````

### `requirements.txt` Example

```text
SpeechRecognition
pyttsx3
pycaw
keyboard
comtypes
```

## Usage

1. Clone the repository or download the `music_system_control.py` file.
2. Ensure your microphone is working.
3. Run the script:

```bash
python music_system_control.py
```

4. Speak clearly into the microphone. Supported commands include:

   * "Play music"
   * "Pause"
   * "Stop"
   * "Next song"
   * "Previous song"
   * "Volume up"
   * "Volume down"
   * "Exit" (to terminate the script)

## Notes

* This script uses the `keyboard` library to simulate media key presses. Ensure it is run with appropriate permissions.
* `pycaw` is used to interface with the Windows audio session to manage volume levels.
* Make sure the default music player responds to multimedia keys.

## License

This project is provided for educational and personal use. Modify and distribute freely with proper attribution.

