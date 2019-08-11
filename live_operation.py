#coding=utf-8
from picamera import PiCamera
from time import sleep
import speech_recognition as sr
import pyaudio
import re
import RPi.GPIO as GPIO
import datetime
import alsaaudio
import os
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
RELAIS=21
camera = PiCamera()
def loadASoundrcFile():
	asoundrs_file=open("/home/pi/.asoundrc","w")
	asoundrs_file.writelines("""pcm.!default {
			type asym
			capture.pcm "mic"
			playback.pcm "speaker"
	}
	pcm.mic {
			type plug
			slave {
			 pcm "hw:1,0"
			}
	}
	pcm.speaker {
			type plug
			slave {
			 pcm "hw:1,0"
			}
	
	}""")
	asoundrs_file.close()
	mic=alsaaudio.Mixer('Mic',cardindex=1)
	mic.setvolume(40)
	speaker=alsaaudio.Mixer('Speaker',cardindex=1)
	speaker.setvolume(65)
	agc=alsaaudio.Mixer('Auto Gain Control',cardindex=1)
	agc.setvolume(60)
	
	
	

def StartPreview():
	camera.resolution=(1100,768)
	camera.start_preview()
def StopPreview():
	camera.stop_preview()
def Record(time):
	StartPreview()
	camera.start_recording('/media/pi/DB2E-16B7/{}.h264'.format(time))
def Stop():
	StopPreview()
	camera.stop_recording()
def LightOn():
	GPIO.setup(RELAIS,GPIO.OUT)
	GPIO.output(RELAIS,GPIO.HIGH)
def LightOff():
	GPIO.setup(RELAIS,GPIO.OUT)
	GPIO.output(RELAIS,GPIO.LOW)
def AssisstantCamOn():
	mixer.init()
	mixer.music.load('/home/pi/video/lance.mp3')
	mixer.music.play()
def AssisstantCamOff():
	mixer.init()
	mixer.music.load('/home/pi/video/arrete.mp3')
	mixer.music.play()
def Recognition():
	while True:
		try:	
			
			r = sr.Recognizer()
			with sr.Microphone() as source:  
				print("Say something!")  
				audio = r.listen(source) 
			stt= r.recognize_google(audio,language="fr-FR")
			print(stt)
			allumer=re.search('allu*',stt)			
			eteindre=re.search('ndre*',stt)
			if allumer:
				print ("allumer")
				LightOn()
			if eteindre:
				print ("eteindre")
				LightOff()
			lancer_camera=re.search('lanc*',stt)			
			if lancer_camera:
				Record(datetime.datetime.now().strftime("(%y_%m_%d)_(%H_%M_%S)"))
				AssisstantCamOn()
			arreter_camera=re.search('arr*',stt)			
			if arreter_camera:
				Stop()
				AssisstantCamOff()
		except Exception:
			print("error")
			
		
loadASoundrcFile()		
Recognition()
	
