import signal
from gpiozero import Button, LED
import subprocess
import time
from time import sleep
import os
import google.generativeai as genai

# set api key and initialize model
API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# Set the duration and sample rate
max_duration = 120  # seconds
fs = 44100  # Sample rate

#create audio files
recording_file = "/home/ac/recording"
file_extension = ".wav"
filename = recording_file + file_extension
trimmed_filename =   recording_file + "-trimmed" + file_extension
pre_trimmed_filename = recording_file + "-pre-trimmed" + file_extension
temp_filename = "/home/ac/temp" + file_extension
exists = os.path.exists(filename)
if not exists:
    with open(os.path.join(filename), 'w') as fp:
        pass
other_exists = os.path.exists(trimmed_filename)

if not other_exists:
    cmd = "arecord -f S16_LE -d 5 -c 1 -r 44100 {}".format(trimmed_filename)
    subprocess.call(cmd, shell=True)

temp_exists = os.path.exists(temp_filename)
if not temp_exists:
    with open(os.path.join(temp_filename), 'w') as fp:
        pass

temp2_exists = os.path.exists(pre_trimmed_filename)

if not temp2_exists:
    cmd = "ffmpeg -i {} -c copy {}".format(trimmed_filename, pre_trimmed_filename)
    subprocess.call(cmd, shell = True)


#functions


def process_terminate():
    # Terminate the recording process
    process.terminate()


def record_audio():
    green_led.on()
    red_led.on()
    sleep(3)
    green_led.off()
    red_led.off()
    command = [ "arecord", "-f", "S16_LE", "-c", "1", "-r", "44100", filename]
    global process
    process = subprocess.Popen(command)


def green_LED_on():
    green_led.on()
    sleep(2)
    green_led.off()


def red_LED_on():
    red_led.on()
    sleep(2)
    red_led.off()


def get_duration(file_path):
    cmd = 'ffprobe -i {} -show_entries format=duration -of csv="p=0"'.format(file_path)
    bytecode = subprocess.check_output(cmd, shell=True)
    string = bytecode.decode("utf-8")
    output = float(string)
    print(output)
    return float(output)  # Duration in seconds


def signal_handler():
    process_terminate()
    # add files together
    cmd= 'ffmpeg -y -i {} -i {} -filter_complex [0:a][1:a]concat=n=2:v=0:a=1 {}'.format(trimmed_filename, filename, pre_trimmed_filename)
    subprocess.call(cmd, shell=True)

    clip_last_two_minutes(pre_trimmed_filename, trimmed_filename)
    api_call()

def clip_last_two_minutes(file_path, output_path):
    duration = get_duration(file_path)
    if duration < 120:
        cmd = 'ffmpeg -y -i {} -t 120  {}'.format(file_path, output_path)
        subprocess.call(cmd, shell=True)
    else:
        start_time = duration - 120
        cmd = 'ffmpeg -y -i {} -ss {} -t 120 {}'.format(file_path, start_time, output_path)
        subprocess.call(cmd, shell=True)

def api_call():
    print("openning trimmed_filename")
    # Load and encode your audio data
    with open(trimmed_filename, "rb") as f:
         ambient = f.read()
    print("uploading trimmed_filename")
    sample_file = genai.upload_file(path= trimmed_filename,
                            display_name="Trimmed_Recording")
    print("uploaded {} as {}".format(sample_file.display_name, sample_file.uri))
    uri = sample_file.uri
    data = [
         "does the final 15 seconds of this sound file contain any sounds that significantly differ from the profile of the first minute and 45 seconds? if a novel sound signal exists in the final 15 seconds of audio data preface your answer with a 1. If no such sound signal is present preface your answer with a 0 (1 or 0 should be the absolutely first character in your response)", sample_file ]
    print("making api call")
    response = model.generate_content(data)
    print(response.text)
    if response.text[0] == "0":
        print("red on")
        red_LED_on()
    else:
        print("green on")
        green_LED_on()
    genai.delete_file(sample_file.name)
    record_audio()

# LEDs and button
green_led = LED(23)
red_led = LED(24)
button = Button(27)

#set signal handler and run program
button.when_pressed = signal_handler
record_audio()
signal.pause()
