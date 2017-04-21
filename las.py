# ListenSpell.activity :  A simple Game to teach children new words in an exiciting and funny manner
# 
# Copyright (C) 2008 chirag Jain, Assim Deodia,
# 
# Chiragjain1989@gmail.com
#assim.deodia@gmail.com
#manu@laptop.org
#
#This file is a part of ListenSpellActivity
#     ListenSpell.activity is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
# 
#     ListenSpell.activity is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
# 
#     You should have received a copy of the GNU General Public License
#     along with ListenSpell.activity.  If not, see <http://www.gnu.org/licenses/>.
#!/bin/env python

import sys
import os
import dbus
import random
import gtk
import commands
from dict import Dict
from dict import Word
from time import sleep

# My class for key detection
#class _Getch:
	#"""Gets a single character from standard input.  Does not echo to the screen."""
	#def __init__(self):
		#try:
			#self.impl = _GetchWindows()
		#except ImportError:
			#self.impl = _GetchUnix()

	#def __call__(self): return self.impl()

#class _GetchUnix:
	#def __init__(self):
		#import tty, sys

	#def __call__(self):
		#import sys, tty, termios
		#fd = sys.stdin.fileno()
		#old_settings = termios.tcgetattr(fd)
		#try:
			#tty.setraw(sys.stdin.fileno())
			#ch = sys.stdin.read(1)
		#finally:
			#termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
		#return ch

#class _GetchWindows:
	#def __init__(self):
		#import msvcrt

	#def __call__(self):
		#import msvcrt
		#return msvcrt.getch()
		
		
		
		
class Listenspell():

	def __init__(self):
		self.skill_level = 0
		self.points = 0
		self.words_played = 0
		self.words_correct = 0
		self.path1 = "."
		self.path2 = "."
		#self.espeak_init = False
		#self.espeak_obj = espeak()
		#self.initial=1
		#self.__espeak_default_config = {'pitch':0, 'rate':0, 'language':'en', 'volume':100, 'voice':'MALE1',
							   #'spelling':False, 'punctuation':espeak.PunctuationMode.SOME }
		#self.__espeak_default_config = {'pitch':0, 'rate':0, 'language':'en', 'volume':100}
		#self.__espeak_default_config = {'pitch':50, 'rate':170, 'language':'default','word_gap':10,'volume':100 }
		#self.__espeak_config = self.__espeak_default_config
		#self.espeak_obj=espeak()
		#pipeline = 'espeak name=src ! autoaudiosink'
		#self.pipe = gst.parse_launch(pipeline)
 
		#self.src = self.pipe.get_by_name('src')
 
		#bus = self.pipe.get_bus()
		#bus.add_signal_watch()
		#bus.connect('message', self.gstmessage_cb)
		
	
	#*****************************************SOUND BASE**********************************************************************
	
	
		
	
			
		
		
	#def __start_espeak(self):  
		#try:
			#self.client = espeak.SSIPClient('spd-test')
			#self.client.set_output_module('espeak')
			#self.client.set_language('en')
			#self.client.set_punctuation(espeak.PunctuationMode.SOME)
			#self.speech_state = None
		#except dbus.exceptions.DBusException:
			#print "Speech Dispatcher is not turned on."
			#return False
		#self.espeak_init = True
		
		
	

#*****************************************************SOUND BASE END*****************************************************	
	
	#def set_path(self, path1, path2):
		#if path1 != "":
			#self.path1 = path1 + "/"
		#else:
			#self.path1= path1	
		#if path2 !="":
			#self.path2=path2+"/"
		#else:
			#self.path2=path2
			
	def set_path1(self,path1):
		self.path1=path1+"/"
		
	def set_path2(self,path2):
		self.path2=path2+"/"
	
	



	def load_db(self, SQLiteDB):
		if self.path1 == ".":
			return False
		#print self.path + SQLiteDB
		self.dict_obj = Dict(self.path1 + SQLiteDB)	#Always intitiate first Dict object then Word object
		self.word_obj = Word()
		




	def play_sound(self,event):

		os.popen("aplay --quiet " + self.path2 + event + ".wav")

	def set_skill_level(self,level):
		self.skill_level = level
		#self.reset_counters()

	def reset_counters(self):
		self.points = 0
		self.words_played = 0
		self.words_correct = 0
	
	def get_skill_level(self):
		return self.skill_level

	def get_words_played(self):
		return self.words_played

	def get_words_correct(self):
		return self.words_correct

	def get_points(self):
		return self.points

	def ans_correct(self, wordid):
		#self.play_sound("correct")
		#sleep(1)
		self.points = self.points + self.skill_level
		self.words_correct = self.words_correct + 1
		self.word_obj.update_score(wordid)

	def ans_incorrect(self, wordid):
		#self.play_sound("incorrect")
		#sleep(1)
		self.word_obj.update_score(wordid, "incorrect")

	#def clear_screen(self,numlines=100):
		#"""Clear the console.
        #numlines is an optional argument used only as a fall-back.
        #"""
		#import os
		#if os.name == "posix":
			# Unix/Linux/MacOS/BSD/etc
			#os.system('clear')
		#elif os.name in ("nt", "dos", "ce"):
			# DOS/Windows
			#os.system('CLS')
		#else:
			# Fallback for other operating systems.
			#print '\n' * numlines 

	def load_wordid(self, num_words = 0):
		temp_list = []
		self.wordid_list = []
		temp_list = self.dict_obj.get_random_wordid(self.skill_level, num_words)
		for(wordid, ) in temp_list:
			self.wordid_list.append(wordid)
		return self.wordid_list

	def get_word_info(self,wordid, attribute):
		if self.word_obj.get_wordid() != wordid:
			self.word_obj.__init__(identifier = "wordid", value= wordid)
			self.words_played = self.words_played + 1

		if attribute == "def":
			return self.word_obj.get_def()
		elif attribute == "usage":
			return self.word_obj.get_usage()
		elif attribute == "word":
			return self.word_obj.get_word()  
		elif attribute == "phnm":
			phnm = self.word_obj.get_phoneme()
			if phnm == None:
				phnm = self.__get_phoneme(self.word_obj.get_word())
				return phnm
			else:
				(phoneme, is_correct) = phnm
				return phoneme
		else: return False
		
	def __get_phoneme(self, word = None):
		if word == None:
			return False
		phnm = commands.getoutput("/usr/bin/espeak -q -x " + word)
		self.word_obj.update_phoneme(phnm)
		return phnm
		
	#def get_key(self):
		#for longestinput in range(15):
			#inkey = _Getch()
			#for i in xrange(sys.maxint):
				#k=inkey()
				#if k<>'':break
				#elif k == '\r': break
			#return k

	def exit_game(self):
		self.word_obj.exit_game()
		self.dict_obj.exit_game()
		#self.client.close()
		sys.exit()
