
#again making some changes
#!/bin/env python
import sys
import os
import subprocess
import threading


#-a <integer>
#Amplitude, 0 to 200, default is 100
#-g <integer>
#Word gap. Pause between words, units of 10mS at the default speed
#-p <integer>
#Pitch adjustment, 0 to 99, default is 50
#-s <integer>
#Speed in words per minute, 80 to 370, default is 170
#-v <voice name>
#Use voice file of this name from espeak-data/voices

class espeak:
	
	def __init__(self):
		self.cmd = {}
		self.cmd['-a'] = 100
		self.cmd['-g'] = 10
		self.cmd['-p'] = 50
		self.cmd['-s'] = 170
		self.cmd['-v'] = "default"
		self.thread_running=1
		t=threading.Thread(target=self.SpeakingThread,args=())
		lock1=threading.Lock()
		lock1.acquire()
		t.start()
		#cmd['-v'] = ''
		#call(['cmd', 'arg1', 'arg2'])
		
	
	def set_amplitude(self,amp):
		self.cmd['-a'] = int(amp)
	def set_word_gap(self,gap):
		self.cmd['-g'] = int(gap)
	def set_pitch(self,pitch):
		self.cmd['-p'] = int(pitch)
	def set_speed(self,speed):
		self.cmd['-s'] = int(speed)
	def set_voice(self,voice):
		self.cmd['-v'] = str(voice)
		
	def get_amplitude(self):
		return self.cmd['-a']
	def get_word_gap(self):
		return self.cmd['-g']
	def get_pitch(self):
		return self.cmd['-p']
	def get_speed(self):
		return self.cmd['-s']
	def get_voice(self):
		return self.cmd['-v']
		

	def speech(self,word):
		#cmd = "espeak"
		args = ['espeak']
		i = 0
		#cmd3 = "espeak "
		for k in self.cmd.keys():
			#cmd3 = cmd3 + str(k) + ' ' + str(self.cmd[k]) + ' '
			args.append(str(k) + ' ' + str(self.cmd[k]))
		#cmd3 = cmd3 + "'" + word + "'"
		args.append(word)
		#args[i] = word
		#print cmd3
		#os.execlp(cmd3)
		subprocess.call(args)
		
	def SpeakingThread(self):
		while self.thread_running:
			if not q.empty():
				text=q.get(1)
				self.speech(text)
		
if __name__ == "__main__":
	
	k = espeak()
	k.speak("hello my name is chirag jain.")
	print("Hello my name is chirag Jain")
	k.speak("what is your name?")