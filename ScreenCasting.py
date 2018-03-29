#Libraries
import cv2,wave,pyaudio,keyboard,subprocess
import numpy as np
from PIL import ImageGrab

#Four Character Code
fourcc = cv2.VideoWriter_fourcc(*'XVID')
output = cv2.VideoWriter('output.avi',fourcc, 20.0, (1600,900))

#initializing PyAudio values
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = (1100*2)
RECORD_SECONDS = 1
voice = pyaudio.PyAudio()
FILENAME="voice.wav"

#Record voice and video
try:
    voice_record = voice.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)

    print ("Recording Starts................\n")
    print ("Enter q to Exit")
    packets = []
     
    while (True):
        #read the signals
        voiceData = voice_record.read(CHUNK)
        #make a packet of signal
        packets.append(voiceData)
        #grab the screenshot
        img = ImageGrab.grab()
        #conversion to numpy array
        img_np = np.array(img,np.uint8)
        #conversion to rgb 
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame,(1600,900))
        output.write(frame)
    
        #break while loop 
        if keyboard.is_pressed('q'):
            break
        else:
            continue
    voice_record.stop_stream()
    voice_record.close()
    voice.terminate()
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(voice.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(packets))
    waveFile.close()
    output.release()
    #command to merge video and audio
    subprocess.call(["ffmpeg","-i", "output.avi", "-i", "voice.wav", "-shortest", "mergevideo.avi","-y"],shell=True)
    #command to slow down video and audio
    subprocess.call('ffmpeg -i mergevideo.avi -filter_complex "[0:v]setpts=1.5*PTS[v];[0:a]atempo=0.7[a]" -map "[v]" -map "[a]" final.avi -y',shell=True)
    cv2.destroyAllWindows()
    
    print("done")
#Raise exception if there is no handfree plugin
except OSError:
    print ("Plug Handsfree")
