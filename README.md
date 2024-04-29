# Novel-Sound-Signal-Detection
# Cognitive Remediation Tool for Auditory Hallucinations

- This script is to be used with an initialized Raspberry Pi (running Raspberry Pi OS 64-bit full) connected to an IQaudIO Codec Zero HAT.
- This python script interacts with the Raspberry Pi, attached hardware, and Google Gemini to record ambient sound and compare the last 15 seconds of recording versus the prior minute and 45 seconds and determine if a sound signal is present.
- Google's Gemini API is queried to decide if a sound signal is detected in the final 15 seconds of the recording.
- If a novel sound signal is detected a green LED on the Codec Zero lights up, if not a red LED lights up.
- This can be used by an indivual expericing transient auditory hallucinations to differentiate a hallucination from an actual ambient sound.

##  Raspberry Pi Initialization:
Follow the steps at: https://www.raspberrypi.com/documentation/computers/getting-started.html

I used a RPi Zero 2 W but any model with a standard 40-pin GPIO header will work with the HAT.

## Codec Zero Attachment and Configuration:
Follow the steps for the Codec Zero at: https://www.raspberrypi.com/documentation/accessories/audio.html


