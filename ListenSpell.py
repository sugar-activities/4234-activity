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
#!/usr/bin/env python
import pygtk
pygtk.require('2.0')
from time import sleep
import gtk
import os
import string
from las import Listenspell
from sugar.activity import activity
from sugar.datastore import datastore
import logging
from gettext import gettext as _
import gobject
import threading
import subprocess
from progress import ProgressBar
#import simplejson
import shutil
from Queue import Queue
q=Queue(50)
gtk.gdk.threads_init()

class espeak:
	
	def __init__(self):
		self.cmd = {}
		self.cmd['-a'] = 100
		self.cmd['-g'] = 10
		self.cmd['-p'] = 50
		self.cmd['-s'] = 170
		self.cmd['-v'] = "default"
		self.thread_running=1
		self.t=threading.Thread(target=self.SpeakingThread,args=())
		self.lock1=threading.Lock()
		self.lock1.acquire()
		self.t.start()
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
			args.append(str(k)) 
			args.append(str(self.cmd[k]))
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



				
class ListenSpell(activity.Activity):
			
	def __init__(self, handle = None, is_stand_alone = False):
		self.espeak_obj=espeak()
		self.is_stand_alone = is_stand_alone
		self.play_mode="practice"
		#self.espeak_obj=espeak()
		self.config_file = 'ls-espeak-config'
		self.las = Listenspell()
		DBname = "dict.db"
		if not self.is_stand_alone:
			activity.Activity.__init__(self, handle)
			self._name = handle
			self._logger = logging.getLogger('ListenSpell')
			path1=os.path.join(activity.get_activity_root(), "data")
			path2=activity.get_bundle_path()
			self.las.set_path1(path1)
			self.las.set_path2(path2)
			self.set_path1(path1)
			self.set_path2(path2)
			if not os.path.isfile(self.las.path1+DBname):
				shutil.copy(self.las.path2+DBname,self.las.path1+DBname)
		else:
			path=__file__
			path=path.rpartition("/")
			self.las.set_path1(path[0])
			self.las.set_path2(path[0])
			self.set_path1(path[0])
			self.set_path2(path[0])
		self.__espeak_default_config = {'pitch':50, 'rate':170, 'language':'default','word_gap':10,'volume':100 }
		self.__espeak_config = self.__espeak_default_config

		self.load_espeak_config()
		self.use_phoneme = False
		
		self.high_score_file='high_score'
		self.highest_score={'0':'Anonymous','1':0}
		
		try:
			fp = open(self.las.path1 + self.high_score_file)
		except IOError:
			#File doesn't exist, create it 
			fp = open(self.las.path1 + self.high_score_file, 'w', 0)
			#simplejson.dump(self.highest_score, fp)
			fp.write(str(self.highest_score))
		else:
			self.highest_score=eval(fp.read())
			#self.highest_score = simplejson.load(fp)
		fp.close()
		
		self.las.load_db(DBname)
		self.load_activity_interface()
		self.las.play_sound("begin")
		self.say_text("Welcome to Listen and Spell!", wait = False)
		self.show_about_activity()
		self.las.set_skill_level(4)
		self.say_text("This is practice mode. Click start Game button to start the game.")
		self.display_console("This is practice mode. \nClick 'Start Game' button to start the game.")
		self.play_game("start")
		#gtk.main()
		
		
		
		
	def get_espeak_config(self, default =0):
		if default == 1:
			return self.__espeak_default_config
		else:
			return self.__espeak_config
	
	
	def load_espeak_config(self):
		try:
			fp = open(self.path1 + self.config_file)
		except IOError:
			#File doesn't exist, create it and write default config
			fp = open(self.path1 + self.config_file, 'w', 0)
			speech_config = self.get_espeak_config(1)
			fp.write(str(speech_config))
			#simplejson.dump(speech_config, fp)
		else:
			speech_config=eval(fp.read())
			#speech_config = simplejson.load(fp)
		for attr in speech_config:
			self.espeak_config(attr, speech_config[attr])
		fp.close()
		return speech_config

	def __set_espeak_config(self, attribute = None, value = None, mode = 'one', config_obj = None):
		if mode == 'one':
			if attribute == None or value == None:
				return False
			#print attribute + ":" + str(value)
			self.__espeak_config[attribute] = value
			fp = open(self.path1 + self.config_file, 'w', 0)
			fp.write(str(self.__espeak_config))
			#simplejson.dump(self.__espeak_config, fp)
			fp.close()
		elif mode == 'all':
			if config_obj == None:
				return False
			fp = open(self.path1 + self.config_file, 'w', 0)
			self.__espeak_config = config_obj
			fp.write(str(self.__espeak_config))
			#simplejson.dump(self.__espeak_config, fp)
			fp.close()
			
	def espeak_config(self, attribute = None, data = None):
		
		if attribute == None or data == None:
			return False
		
		#if self.espeakinit == False:
			#if self.__start_espeak() == False:
				#return False
		
		attribute_list = ['pitch', 'rate', 'volume', 'voice', 'output_module', 
						  'language', 'punctuation', 'spelling', 'synthesis_voice','word_gap']
		
		if attribute in attribute_list:
			try:
				self.__set_espeak_config(attribute, data)
				if attribute == "pitch":
					#self.src.props.pitch=int(data) # -100 to 100
					self.espeak_obj.set_pitch(int(data)) # 0 to 99
					#self.client.set_pitch(int(data)) #-100 to 100
				elif attribute == "rate":
					#self.src.props.rate=int(data) # -100 to 100
					self.espeak_obj.set_speed(int(data)) # 80 to 370
					#self.client.set_rate(int(data)) # -100 to 100
				elif attribute == "word_gap":
					#self.src.gap=int(data) #in units of 10ms
					self.espeak_obj.set_word_gap(int(data)) # in uinits of 10ms
					#self.client.set_volume(int(data)) #-100 to 100
				elif attribute == "language":
					#self.src.props.voice=str(data)
					self.espeak_obj.set_voice(str(data))
				elif attribute == "volume":
					#self.client.set_voice(str(data))#(FE)MALE(1,2,3), CHILD_(FE)MALE
					self.espeak_obj.set_amplitude(int(data))
				#elif attribute == "output_module":
					#self.client.set_output_module(str(data))
				#elif attribute == "language":
					#self.client.set_language(str(data))
				#elif attribute == "punctuation":
					#self.client.set_punctuation(data)
				#elif attribute == "spelling":
					#self.client.set_spelling(bool(data)) # True or False
				#elif attribute == "synthesis_voice":
					#self.client.set_synthesis_voice(str(data))#self.client.list_synthesis_voices()
			except AssertionError, e:
				print "Assertion Error: " + str(e) + ":" + str(attribute) + ":" + str(data)
				return False
		else: return False
			
 
	def say_text(self, text1, wait= True):
		q.put(text1,1)

		
	def set_path1(self,path1):
		self.path1=path1+"/"
		
	def set_path2(self,path2):
		self.path2=path2+"/"		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		

	def show_about_activity(self):
		self.display_console("\t\t  WELCOME TO LISTEN AND SPELL\n")
		self.display_console("Default difficulty Level is 4.")
		self.say_text("Default difficulty Level is 4.")
		self.display_console("Click 'Change difficulty level' button to change it.\n")
		self.say_text("Click Change difficulty level button to change it.")
	def load_activity_interface(self):
				
#**************If activity is stand alone*****************
		if self.is_stand_alone:
			self.main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
			self.main_window.connect("destroy", self.destroy)
			self.main_window.set_border_width(10)
			self.main_window.set_title("Listen and Spell")

#*************If activity is not stand alone***************		
		
		if not self.is_stand_alone:
			toolbox = activity.ActivityToolbox(self)			
			self.set_toolbox(toolbox)
			toolbox.show_all()
			# Set title for our Activity
			self.set_title('Listen and Spell')


#****************Containers******************************			
			
		self.Hcontainer   = gtk.HBox()
		self.Hcontainer.show()
		self.Hcontainer_bottom = gtk.HBox()
		self.Hcontainer_bottom.show()
		if self.is_stand_alone:
			self.main_window.add(self.Hcontainer)
		self.vcontainer_left = gtk.VBox()
		self.vcontainer_left.set_border_width(10)
		self.vcontainer_left.show()
		self.vcontainer_right = gtk.VBox()
		self.vcontainer_right.set_border_width(10)
		self.vcontainer_right.show()
		self.Hcontainer.pack_start(self.vcontainer_left,True, True,0)
		self.Hcontainer.pack_end(self.vcontainer_right,False, False,0)
		
		#####################Left Pane widgets##########################

		
		self.text_input = gtk.Entry()
		self.text_input.show()
		self.text_input.connect("focus-in-event", self.text_input_focus, None)
		self.text_input.connect("activate", self.text_input_activate, None)
		self.text_input.set_flags(gtk.CAN_FOCUS)
		self.console_text_view = gtk.TextView()
		
		###################BUTTONS####################

		self.text_submit_button = gtk.Button(label="Check")
		self.text_submit_button.show()
		self.text_submit_button.connect("clicked", self.submit_button_clicked, None)
		self.give_up_button = gtk.Button(label="Skip")
		self.give_up_button.show()
		self.give_up_button.connect("clicked",self.give_up_button_clicked, None)
		self.start_button=gtk.Button("Start Game")
		self.start_button.show()
		self.start_button.connect("clicked",self.start_game_button_clicked,None)
		self.Hcontainer_bottom.pack_start(self.text_submit_button,True,True,0)
		self.Hcontainer_bottom.pack_end(self.give_up_button,True,True,0)
		self.show_rules_button=gtk.Button("Rules")
		self.show_rules_button.show()
		self.show_rules_button.connect("clicked",self.show_rules_button_clicked,None)
		

#################Right pane wigets Buttons##############################

		self.v_buttonbox = gtk.VButtonBox()
		self.repeat_word_button = gtk.Button("Speak again")
		self.repeat_word_button.connect("clicked", self.repeat_word_button_clicked, None)

		self.get_def_button = gtk.Button("Get Definition")
		self.get_def_button.connect("clicked", self.get_def_button_clicked, None)

		self.get_usage_button = gtk.Button("Get Usage")
		self.get_usage_button.connect("clicked", self.get_usage_button_clicked, None)

		self.get_word_length_button = gtk.Button("Get Word Length")
		self.get_word_length_button.connect("clicked", self.get_word_length_button_clicked, None)

		self.change_skill_level_button = gtk.Button("Change difficulty Level")
		self.change_skill_level_button.connect("clicked", self.change_skill_level_button_clicked, None)
		
		self.change_espeak_config_button = gtk.Button("Speech Configuration")
		self.change_espeak_config_button.connect("clicked", self.speech_configuration_button_clicked, None)


##################Text buffer and text view###################
		
		
		self.console_text_buffer = gtk.TextBuffer()
		self.console_text_view.set_editable(False)
		self.console_text_view.set_buffer(self.console_text_buffer)
		self.console_text_view.set_cursor_visible(False)
		self.console_text_view.set_wrap_mode(gtk.WRAP_WORD)
		self.enditer = self.console_text_buffer.get_end_iter()
		self.console_text_sw = gtk.ScrolledWindow()
		self.mark=self.console_text_buffer.create_mark("end",self.console_text_buffer.get_end_iter(),False)
		self.console_text_sw.set_shadow_type(gtk.SHADOW_ETCHED_IN)
		self.console_text_sw.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
		self.console_text_sw.add(self.console_text_view)
		self.console_text_frame = gtk.Frame("Listen and Spell:")
		self.console_text_frame.add(self.console_text_sw)
		self.console_text_frame.show_all()

		self.vcontainer_left.pack_start(self.console_text_frame, True, True )
		self.vcontainer_left.pack_start(self.text_input, False, True )
		#self.vcontainer_left.pack_start(self.text_submit_button, False, False )
		self.vcontainer_left.pack_start(self.Hcontainer_bottom, False, False )
		################################################True################

				
		self.v_buttonbox.add(self.start_button)
		self.v_buttonbox.add(self.repeat_word_button)
		self.v_buttonbox.add(self.get_def_button)
		self.v_buttonbox.add(self.get_usage_button)
		self.v_buttonbox.add(self.get_word_length_button)
		self.v_buttonbox.add(self.change_skill_level_button)
		self.v_buttonbox.add(self.change_espeak_config_button)
		self.v_buttonbox.add(self.show_rules_button)
		self.v_buttonbox.show_all()

		self.button_frame = gtk.Frame("Menu")
		self.button_frame.add(self.v_buttonbox)
		self.button_frame.show()

		self.vcontainer_right.add(self.button_frame)

		self.stats_frame = gtk.Frame("Performance statistics")

		self.stats_table = gtk.Table(4,2,True)

		self.score_label = gtk.Label("Score: ")
		self.score_value_label = gtk.Label("0")
		
		self.skill_level_label = gtk.Label("Difficulty Level: ")
		self.skill_level_value_label = gtk.Label("0")

		self.words_played_label = gtk.Label("Words spelled: ")
		self.words_played_value_label = gtk.Label("0")

		self.words_correct_label = gtk.Label("Spelled correctly: ")
		self.words_correct_value_label = gtk.Label("0")
		
		self.high_score_label=gtk.Label("Best Score: ")
		self.high_score_label_value=gtk.Label(self.highest_score['0']+" : "+str(self.highest_score['1']))

		self.stats_table.attach(self.score_label, 0, 1, 0, 1)
		self.stats_table.attach(self.score_value_label, 1, 2, 0, 1)

		self.stats_table.attach(self.skill_level_label, 0, 1, 1, 2)
		self.stats_table.attach(self.skill_level_value_label, 1, 2, 1, 2)

		self.stats_table.attach(self.words_played_label, 0, 1, 2, 3)
		self.stats_table.attach(self.words_played_value_label, 1, 2, 2, 3)

		self.stats_table.attach(self.words_correct_label, 0, 1, 3, 4)
		self.stats_table.attach(self.words_correct_value_label, 1, 2, 3, 4)
		
		self.stats_table.attach(self.high_score_label,0,1,4,5)
		self.stats_table.attach(self.high_score_label_value,1,2,4,5)
		self.tag_table = self.console_text_buffer.get_tag_table()

		self.vcontainer_right.add(self.stats_frame)
		self.stats_frame.add(self.stats_table)

		self.stats_frame.show_all()
		if not self.is_stand_alone:
			self._logger.debug('activity loaded')

		################################################################
		if self.is_stand_alone:
			self.main_window.show()
		else:
			self.set_canvas(self.Hcontainer)
			self.show_all()
		##################Call Backs####################################

	
	
	
	def start_game_button_clicked(self,widget,data=None):
		self.las.play_sound("button")
		if self.play_mode=="practice":
			self.say_text("Welcome to Listen Spell Game")
			self.ask_about_ready()
		else:
			self.start_game()

	    	 
	
	
	
	
	
	def ask_about_ready(self):
		self.ask_rule_dialog = gtk.Dialog("Start the game", self, 0,("Yes", gtk.RESPONSE_OK, "No", gtk.RESPONSE_CANCEL))
		self.say_text("Are you ready to play the game?")
		hbox = gtk.HBox(False, 8)
		hbox.set_border_width(8)
		self.ask_rule_dialog.vbox.pack_start(hbox, False, False, 0)
		table = gtk.Table(1, 1)
		table.set_row_spacings(4)
		table.set_col_spacings(4)
		hbox.pack_start(table, True, True, 0)
		label = gtk.Label("Are you ready to play the game?")
		#label.set_use_underline(True)
		table.attach(label, 0, 1, 0, 1)
		
		self.ask_rule_dialog.show_all()
		response = self.ask_rule_dialog.run()
		self.las.play_sound("button")
		#skill_level_scale.grab_focus()

		if response == gtk.RESPONSE_OK:
			self.ask_rule_dialog.destroy()
			self.start_game()
		else:
			self.ask_rule_dialog.destroy()
	def start_game(self):
		#self.console_text_buffer.set_text("")
		if self.play_mode=="practice":
			self.display_console("\nThis is Game mode.\nYour time starts now")
			self.say_text("Your Time starts now")
			self.las.reset_counters()
			self.update_all()
			self.play_mode="game"
			self.counter=ProgressBar(self)
			self.play_game("start")
		else:
			self.say_text("\nThis is already Game mode. Do you want to start a new game?")
			self.new_game_dialog = gtk.Dialog("New game", self, 0,("Yes", gtk.RESPONSE_OK, "No", gtk.RESPONSE_CANCEL))
			#self.say_text("Are you ready to play the game?")
			hbox = gtk.HBox(False, 8)
			hbox.set_border_width(8)
			self.new_game_dialog.vbox.pack_start(hbox, False, False, 0)
			table = gtk.Table(1, 1)
			table.set_row_spacings(4)
			table.set_col_spacings(4)
			hbox.pack_start(table, True, True, 0)
			label = gtk.Label("Do you want to start a new game?")
			#label.set_use_underline(True)
			table.attach(label, 0, 1, 0, 1)
		
			self.new_game_dialog.show_all()
			response = self.new_game_dialog.run()
			self.las.play_sound("button")
		
		#skill_level_scale.grab_focus()

			if response == gtk.RESPONSE_OK:
				self.new_game_dialog.destroy()
				self.counter.destroy_progress()
				self.play_mode="practice"
				self.start_game()
			else:
				self.new_game_dialog.destroy()
				self.text_input.grab_focus()
	
	
	
	
	

	def end_game(self):
		#gobject.source_remove(self.timer)
		self.say_text("Your time is up!")
		self.display_console("Your time is up!")
		final_score=self.las.get_points()
		self.say_text("Your final Score is: "+str(final_score))
		self.display_console("Your final Score is: "+str(final_score))
		self.las.reset_counters()
		if final_score>(self.highest_score['1']):
			#self.update_best_score()
			self.say_text("Congratulations! You break the previous record.")
			self.display_console("Congratulations!! You break the previous record.")
			self.highest_score['1']=final_score
			self.update_best_score()
		else:
			self.say_text(". Sorry! The previous best score is "+str(self.highest_score['1']))
			self.say_text("Try again to break it.")
			self.display_console("Sorry! The previous best score is "+str(self.highest_score['1']))
			self.display_console("Try again to break it.")
		self.say_text("You are again in practice mode. Press Start game button to play again.")
		self.display_console("You are again in practice mode.\nPress Start game button to play again.")
		self.play_mode="practice"	
		self.play_game("start")
		
		
	def update_best_score(self):
		score_dialog = gtk.Dialog("Best Score", self,0,(gtk.STOCK_OK, gtk.RESPONSE_OK))
		hbox = gtk.HBox(False, 8)
		hbox.set_border_width(8)
		score_dialog.vbox.pack_start(hbox, False, False, 0)
		table = gtk.Table(1, 1)
		table.set_row_spacings(4)
		table.set_col_spacings(4)
		hbox.pack_start(table, True, True, 0)
		label = gtk.Label("Enter your name:")
	#label.set_use_underline(True)
		table.attach(label, 0, 1, 0, 1)
		name_text_entry = gtk.Entry()
		score_dialog.action_area.pack_start(name_text_entry, False, False, 0)
		score_dialog.show_all()
		name_text_entry.grab_focus()	
		self.say_text("Please enter your name.")
		response=score_dialog.run()
		
		if response==gtk.RESPONSE_OK:
			score_dialog.destroy()
			self.highest_score['0']=name_text_entry.get_text()
			self.high_score_label_value.set_text(self.highest_score['0'] + " : " + str(self.highest_score['1']))
			self.say_text("Congratulations! " + name_text_entry.get_text())
		fp = open(self.las.path1+ self.high_score_file, 'w', 0)
		fp.write(str(self.highest_score))
		#simplejson.dump(self.highest_score, fp)
		fp.close()
			
	
	def show_rules_button_clicked(self,widget,data=None):
		self.las.play_sound("button")
		text="Rules:\n"
		text=text+"1.  You will be given a total of 10 minutes.\t\t\n"
		text=text+"2.  You will hear different words of difficulty according to your difficulty level.\n"
		text=text+"3.  You will have to guess the word and spell it correctly.\n"
		text=text+"4.  After spelling the word press the check button.\n"
		text=text+"5.  If you spelled the word correctly then you will be awarded a score equal to your difficulty level.\n"
		text=text+"6.  If you spelled the word incorrectly then you will have to spell it again.\n"
		text=text+"7.  You can skip the word by clicking the skip button.\n"
		text=text+"8.  If you skipped any word then the activity will give you the correct spelling.\n"
		text=text+"9.  You can change your difficulty level anytime during the game.\n"
		text=text+"10. Your aim is to break the previous best score.\n"
		self.console_text_buffer.set_text("")
		self.display_console(text)
		self.say_text(text)
		

	
	
	
	
	def _update_configuration(self, widget, attribute ):
		if attribute == "language":
			self.espeak_config(attribute, widget.get_active_text())
		elif(attribute == "skill_level"):
			self.las.set_skill_level(int(widget.skill_level))
		else:
			self.espeak_config(attribute, widget.get_value())


	def _speech_test(self, widget, speech_text):
		self.las.play_sound("button")
		self.say_text(str(speech_text))
	
	def speech_configuration_button_clicked(self, widget, data = None):
		self.las.play_sound("button")
		self.config_dialog = gtk.Dialog("Speech Configure", self,0,(gtk.STOCK_OK, gtk.RESPONSE_OK, gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL))
		#self.say_text("Skill Level")
		#vbox = gtk.VBox(False, 8)
		#Vbox.set_border_width(8)
		
		config_table = gtk.Table(4,2)
		config_table.set_row_spacings(4)
		config_table.set_col_spacings(4)
		
		speech_frame= gtk.Frame("Speech Configuration")
		speech_frame.add(config_table)

		self.config_dialog.vbox.pack_start(speech_frame, False, False, 0)
		
		speech_config = self.get_espeak_config().copy()
		#print "getting config"
		
		#volume_adj = gtk.Adjustment(float(speech_config['volume']), -100, 101, 1, 1, 1)
		#rate_adj = gtk.Adjustment(float(speech_config['rate']), -100, 101, 1, 1, 1)
		#pitch_adj = gtk.Adjustment(float(speech_config['pitch']), -100, 101, 1, 1, 1)

		word_gap_adj = gtk.Adjustment(float(speech_config['word_gap']), 0, 101, 1, 1, 1)
		rate_adj = gtk.Adjustment(int(speech_config['rate']), 80, 371, 1, 1, 1)
		pitch_adj = gtk.Adjustment(int(speech_config['pitch']), 0, 100, 1, 1, 1)
		volume_adj = gtk.Adjustment(int(speech_config['volume']),0,201,1,1,1)

		
		word_gap_hscale = gtk.HScale(word_gap_adj)
		rate_hscale = gtk.HScale(rate_adj)
		pitch_hscale = gtk.HScale(pitch_adj)
		volume_hscale = gtk.HScale(volume_adj)
		
		word_gap_hscale.set_digits(0)
		rate_hscale.set_digits(0)
		pitch_hscale.set_digits(0)
		volume_hscale.set_digits(0)
		
		
		word_gap_hscale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
		rate_hscale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
		pitch_hscale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
		volume_hscale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
		language_box = gtk.combo_box_new_text()
		#voices=self.las.src.props.voices
		language_list=['afrikaans','bosnian','czech','welsh-test','german','greek','default','en-german-5','en-rhotic','en-scottish','english','lancashire','english_rp','english_wmids','en-westindies','esperanto','spanish','finnish','french','greek-ancient','hindi-test','croatian','hungarian','icelandic-test','italian','lojban','latin','macedonian-test','dutch-test','norwegian-test','polish-test','brazil','portugal','romanian','russian-test','slovak','serbian','swedish','swahihi-test','vietnam-test','Mandarin test','cantonese-test']
		#for voice in voices:
			#language_list.append(voice[0])
		#scale4 = gtk.HScale(adj4)
		for language in language_list:
			language_box.append_text(language)
		
		try:
			language_index = language_list.index(speech_config['language'])
		except ValueError:
			language_box.set_active(0)
		else:
			language_box.set_active(language_index)
		
		word_gap_label = gtk.Label("Word Gap")
		language_label=gtk.Label("Voice")
		rate_label = gtk.Label("Rate")
		pitch_label = gtk.Label("pitch")
		volume_label = gtk.Label("Volume")
		
		volume_adj.connect('value_changed',self._update_configuration, "volume")
		rate_adj.connect('value_changed',self._update_configuration, "rate")
		pitch_adj.connect('value_changed',self._update_configuration, "pitch")
		language_box.connect('changed', self._update_configuration, "language")
		
		
		config_table.attach(language_label, 0,1,0,1)
		config_table.attach(volume_label, 0,1,1,2)
		config_table.attach(rate_label, 0,1,2,3)
		config_table.attach(pitch_label, 0,1,3,4)
		config_table.attach(word_gap_label, 0,1,4,5)		
		
		config_table.attach(language_box,1,2,0,1)
		config_table.attach(volume_hscale, 1,2,1,2)
		config_table.attach(rate_hscale, 1,2,2,3)
		config_table.attach(pitch_hscale, 1,2,3,4)
		config_table.attach(word_gap_hscale, 1,2,4,5)
		
		
		speech_test_frame = gtk.Frame("Test Speech Setting")
		
		self.config_dialog.vbox.pack_start(speech_test_frame, False, False, 0)
		
		
		
		speech_test_table = gtk.Table(2,1)
		speech_test_table.set_row_spacings(4)
		speech_test_table.set_col_spacings(4)

		speech_test_frame.add(speech_test_table)
		
		speech_test_text_entry = gtk.Entry()
		speech_test_text_entry.set_text("The quick brown fox jumps over the lazy dog")
		
		speech_test_button = gtk.Button("Test")
		
		speech_test_button.connect("clicked", self._speech_test, speech_test_text_entry.get_text())

		speech_test_table.attach(speech_test_text_entry, 0,1,0,1)
		speech_test_table.attach(speech_test_button, 0,1,1,2)
		
		
		
		self.config_dialog.show_all()
		
		response = self.config_dialog.run()
		self.las.play_sound("button")
		
		if response == gtk.RESPONSE_OK:
			self.config_dialog.destroy()
		elif response == gtk.RESPONSE_CANCEL:
			#print "going back"
			for k in speech_config:
				#print k + " " + str(previous_espeak_config[k])
				self.espeak_config(k, speech_config[k])
			self.config_dialog.destroy()
		self.text_input.grab_focus()
		
	
	def submit_button_clicked(self, widget, data = None):
		if self.play_mode=="practice":
			self.las.play_sound("button")
		answer = self.text_input.get_text()
		answer=answer.lower()
		self.display_console("\nYou Spelled: ")
		self.display_console(answer, newline = False)
		if self.play_mode=="practice":
			self.say_text("You Spelled")
			self.shout(answer)
		#self.say_text(answer)
			#sleep(len(answer)-2)

		if answer == self.elem:
			
			self.las.ans_correct(self.wordid)
			
			self.display_console("Correct")
			if self.play_mode=="game":
				self.las.play_sound("correct")
				sleep(1)
			self.say_text("Correct")
			self.update_all()
			self.play_game(mode="next word")
		else:
			self.las.ans_incorrect(self.wordid)
						#self.display_console("Incorrect. The correct spelling is.. ")
			if self.play_mode=='game':
				self.las.play_sound("incorrect")
				sleep(1)
			self.display_console("Incorrect.\nPlease spell again  ___________________")
			self.say_text("Incorrect")

			#self.say_text("The correct spelling is")
			self.say_text("Please spell again ")
			#self.shout(self.elem)
			self.say_text(self.elem)
			self.update_all()
			self.text_input.set_text("") 
		#self.update_all()
		#self.play_game("next word")
		return False
#################################Give up Button#################################################

	def give_up_button_clicked(self,widget,data=None):
		self.las.play_sound("button")
		self.say_text("The correct spelling is ")
		self.shout(self.elem)
		self.display_console("The correct spelling is: "+self.elem)
		self.update_all()
		self.play_game("next word")
		if not self.is_stand_alone:
			self._logger.debug('submit button clicked : ' + self.elem + '')
		return False
##########################End of give up#########################################################		

	def text_input_focus(self, widget, event, data= None):
		#print "text_input_focus_in"
		return False

	def text_input_activate(self, widget, data=None):
		self.submit_button_clicked(widget, data)
		#print "text_input_activate"
		return False

	def repeat_word_button_clicked(self, widget, data = None):
		if self.elem != self.pronounelem and self.use_phoneme:
			self.say_text(self.pronounelem, is_phoneme = True)
		else:
			self.say_text(self.elem)
		if not self.is_stand_alone:
			self._logger.debug('repeat button clicked : ' + self.elem + '')
		self.text_input.grab_focus()
	def get_def_button_clicked(self, widget, data = None):
		self.las.play_sound("button")
		def_list = self.las.get_word_info(self.wordid, "def")
		self.display_console("Definition: ")
		self.say_text("Definition   ")
		for (pos, definition, name) in def_list:
			self.display_console(pos + "(" + name + ") : " + definition)
			self.say_text(definition)
		self.text_input.grab_focus()
	def get_usage_button_clicked(self, widget, data = None):
		if self.usage_used == -1:
			self.usage = self.las.get_word_info(self.wordid, "usage")
			print self.usage
			self.total_num_usage = len(self.usage)
		if self.total_num_usage == 0:
			self.display_console("No usage in the database")
		else:
			if self.total_num_usage == self.usage_used:
				self.usage_used = 0
			(sample) = self.usage[self.usage_used]
			self.say_text(sample)
			self.usage_used = self.usage_used + 1
		if not self.is_stand_alone:
			self._logger.debug('get usage button clicked : ' + self.elem + '')
		self.text_input.grab_focus()

	def get_word_length_button_clicked(self, widget, data = None):
		self.las.play_sound("button")
		self.display_console("Word Length: " + str(len(self.elem)))
		self.say_text("Word Length "+str(len(self.elem)))
		if not self.is_stand_alone:
			self._logger.debug('get word length button clicked : ' + self.elem + '')
		self.text_input.grab_focus()

	def change_skill_level_button_clicked(self, widget, data=None):
		self.las.play_sound("button")
		self.skill_level_dialog = gtk.Dialog("Enter difficulty Level", self, 0,(gtk.STOCK_OK, gtk.RESPONSE_OK,"Cancel",gtk.RESPONSE_CANCEL))
		self.say_text("Enter your difficulty Level")
		hbox = gtk.HBox(False, 8)
		hbox.set_border_width(8)
		self.skill_level_dialog.vbox.pack_start(hbox, False, False, 0)
		
		table = gtk.Table(1, 1)
		table.set_row_spacings(4)
		table.set_col_spacings(4)
		hbox.pack_start(table, True, True, 0)

		#label = gtk.Label("Enter your Skill Level")
		#label.set_use_underline(True)
		#table.attach(label, 0, 1, 0, 1)
		
		skill_level_adj = gtk.Adjustment(float(self.las.get_skill_level()), 1,16,1,1,1)
		skill_level_scale = gtk.HScale(skill_level_adj)
		skill_level_scale.set_digits(0)
		skill_level_scale.set_update_policy(gtk.UPDATE_DISCONTINUOUS)
		skill_level_scale.set_flags(gtk.CAN_FOCUS)
		#skill_level_adj.connect('value_changed',self._update_configuration, "skill_level")
		
			
		
			
		#local_skill_level = gtk.Entry()
		#local_skill_level.set_text(str(self.las.get_skill_level()))
		#skill_level_scale.connect("activate", self.skill_level_activate, None)
		table.attach(skill_level_scale, 1, 2, 0, 1)
		#label.set_mnemonic_widget(skill_level_scale)

		self.skill_level_dialog.show_all()
		skill_level_scale.grab_focus()
		response=self.skill_level_dialog.run()
		self.las.play_sound("button")
		
		 

		if response==gtk.RESPONSE_OK:
			skill_level = int (skill_level_adj.get_value())

			self.skill_level_dialog.destroy()
			self.las.set_skill_level(skill_level)
			self.display_console("\nDifficulty level changed\n")
			self.say_text("Difficulty level changed.")
			self.update_all()
			self.play_game("start")
			self.text_input.grab_focus()
		#elif response==gtk.RESPONSE_CANCEL:
		self.text_input.grab_focus()
		self.skill_level_dialog.destroy()
			
	def local_skill_level_focus(self, widget, event, data= None): # not in use
		#print "text_input_focus_in"
		return False

	def skill_level_activate(self, widget, data=None):
		self.skill_level_dialog.response(gtk.RESPONSE_OK)

	
	

	def shout(self,string):
		#self.display_console("")
		for char in string:
			self.say_text(char)
		self.say_text(string)
	
	
	################################################################

	#####################Update methods#############################
	def update_all(self):
		self.update_score()
		self.update_skill_level()
		self.update_words_played()
		self.update_words_correct()
		
	def update_score(self, score = None):
		if score ==None:
			score = self.las.get_points()
		self.score_value_label.set_text(str(score))

	def update_skill_level(self, skill_level = None):
		if skill_level ==None:
			skill_level = self.las.get_skill_level()
		self.skill_level_value_label.set_text(str(skill_level))

	def update_words_played(self, words_played = None):
		if words_played ==None:
			words_played = self.las.get_words_played()
		self.words_played_value_label.set_text(str(words_played))

	def update_words_correct(self, words_correct = None):
		if words_correct ==None:
			words_correct = self.las.get_words_correct()
		self.words_correct_value_label.set_text(str(words_correct))

	def play_word(self):
		self.usage_used = -1
		self.total_num_usage = -1
		self.text_input.grab_focus()
		self.text_input.set_text("") # Clear answer field
		
		# Initilazing variable for eacch word
		
		self.elem        = self.las.get_word_info(self.wordid, "word")   #get a word from the list
		self.pronounelem = self.las.get_word_info(self.wordid, "phnm")   #get a pronounciation from the list

		self.display_console("Spell   ___________________")       # say the explanation if the word is ambiguous.
		if self.use_phoneme and self.elem != self.pronounelem:    # determine whether to bother pronouncing a description
			self.say_text("Spell  ___________________" + self.pronounelem, is_phoneme = True)
		else:
			#print "Spell... "
			self.say_text("Spell  ___________________" + self.elem)
		self.text_input.grab_focus()
		
		
	def play_game(self, mode = "start"):
		if mode == "start":
			#self.this_level_size = 7
			#self.this_level_max_error = 3
			self.wordid_list = self.las.load_wordid()
			self.this_level_num_words = len(self.wordid_list)
			self.this_level_words_left = self.this_level_num_words
			self.word_index = 1
			self.wordid = self.wordid_list[self.word_index]
			self.play_word()
		elif mode == "next word":
			self.this_level_words_left -= 1
			if self.this_level_words_left == 0:
				self.display_console("You have crossed this level")
				self.say_text("congratulations!!! You have crossed this skill Level.")
				self.say_text("Please select a new level to play the game.")
				self.display_console("Please select new level to play the game")
				self.ask_skill_level()
				self.play_game("start")
			else:
				self.word_index += 1
				self.wordid = self.wordid_list[self.word_index]
				self.play_word()
			#thread.start_new_thread(self.play_word,())

	########################Display Methods#########################

	def display_console(self, data, newline = True ):
		if newline == True:
			data = "\n" + data
		#pos = self.console_text_buffer.get_start_iter()
		self.console_text_buffer.insert_at_cursor(data)
		self.console_text_view.scroll_to_mark(self.mark,0.05,True,0.0,1.0)
		start,end=self.console_text_buffer.get_bounds()
		self.size_tag = gtk.TextTag()
		self.size_tag.set_property("size-points", 10)
		self.tag_table.add(self.size_tag)
		self.console_text_buffer.apply_tag(self.size_tag,start,end)

	#def display_main_output(self, data, newline = True, clear_previous = True):
		#if clear_previous == True:
			#self.main_output_buffer.set_text(data)
		#elif newline == True:
			#text = "\n" + data
			#self.main_output_buffer.insert_at_cursor(data)
		#else:
			#self.main_output_buffer.insert_at_cursor(data)

	
	################################################################

	def close(self):
		self.game_exit()
	
	def game_exit(self):
		self._logger.debug('Quiting Game')
		self.espeak_obj.thread_running=0
		self.las.exit_game()
		gtk.main_quit()

	

	def main(self):
		# All PyGTK applications must have a gtk.main(). Control ends here
		# and waits for an event to occur (like a key press or mouse event).
		gtk.main()
		
		


# If the program is run directly or passed as an argument to the python
# interpreter then create a HelloWorld instance and show it
if __name__ == "__main__":
	gui = ListenSpell(is_stand_alone = True)
	#gui.__init__()
	#gui.play_game("start")
	#gui.main()
