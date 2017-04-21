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
import random
import sqlite3
# Provides the API to control the dictionary.

global __debug
__debug = True

# ********* Do not remove this comment ***********
		# This is mapping of level with length and frequency
		#619 (252)		3 (1, 30000000000, 302000000) (1)
		#1984(868)		4 (1, 26400000000, 1650000000), (2, 1620000000, 261000000), (3, 260000000, 110000000)(1,2,3)
		#3156(1740)		5 (2, 21700000000, 371000000), (3, 368000000, 105000000)(4, 104000000, 38700000)(2,3,4)
		#5618(2700)		6 (3,19800000000, 176000000), (4,175000000,51500000), (5,51400000,20300000)(3,4,5)
		#6681(2500)		7 (4,19100000000,203000000),(5,201000000,59300000),(6,59100000,25900000)(4,5,6)
		#6878(3000)		8 (5,15000000000,89600000)(6,89400000,28700000)(7,28700000,11600000)(5,6,7)
		#6274(3000)		9 (6,21700000000,57000000),(7,56900000,16000000),(8,16000000,6600000)(6,7,8)
		#5017(2400)		10(7,5330000000,44100000),(8,44100000,13100000)(9,13100000,5150000)(7,8,9)
		#3571(1500)		11(8,15300000000,42800000),(9,42800000,12100000)(10,12000000,5020000)(8,9,10)
		#2341(1050)		12(9,3240000000,27500000), (10,27400000,8270000), (11,8230000,3400000) (9,10,11)
		#1521(630)		13(10,6540000000,12000000),(11,12000000,2990000)(10,11)
		#774(270)		14(11,1540000000,3030000)(11)
		#413(245)		15(12,391000000,685000)(12)
		#187(90)		16(13,75300000,740000)(13)
		#100(70)		17(14,76700000,1740)(14)
		#20				18(15,19200000,2970)(15)
		#11				19(15,5600000,1990)(15)
		#6				20(15,87700000,812000)(15)
		#1				21(15,330000,330000)(15)
		#1				23(15,638000,638000)(15)




class Dict:

	
		
	def __init__(self, sqliteDB = None):
				
		self.level_map = {'1':{'3':{'s':30000000000, 'e':302000000}, '4':{'s':26400000000, 'e':1650000000 }},
				 '2':{'4':{'s':1620000000,  'e':261000000}, '5':{'s':21700000000, 'e':371000000 }},
				 '3':{'4':{'s':260000000,  'e':110000000}, '5':{'s':368000000, 'e':105000000 }, '6':{'s':19800000000, 'e':176000000}},
				 '4':{'5':{'s':104000000,'e':38700000}, '6':{'s':175000000,'e':51500000}, '7':{'s':19100000000,'e':203000000}},
				 '5':{'6':{'s':51400000,'e':20300000}, '7':{'s':201000000, 'e':59300000}, '8':{'s':15000000000,'e':89600000}},
				 '6':{'7':{'s':59100000,'e':25900000}, '8':{'s':89400000,'e':28700000}, '9':{'s':21700000000,'e':57000000}},
				 '7':{'8':{'s':28700000,'e':11600000}, '9':{'s':56900000,'e':16000000}, '10':{'s':5330000000,'e':44100000}},
				 '8':{'9':{'s':16000000,'e':6600000}, '10':{'s':44100000,'e':13100000}, '11':{'s':15300000000,'e':42800000}},
				 '9':{'10':{'s':13100000,'e':5150000}, '11':{'s':42800000,'e':12100000}, '12':{'s':3240000000,'e':27500000}},
				 '10':{'11':{'s':12000000,'e':5020000}, '12':{'s':27400000,'e':8270000}, '13':{'s':6540000000,'e':12000000}},
				 '11':{'12':{'s':8230000,'e':3400000}, '13':{'s':12000000,'e':2990000}, '14':{'s':1540000000,'e':3030000}},
				 '12':{'15':{'s':391000000,'e':685000}},
				 '13':{'16':{'s':75300000,'e':740000}},
				 '14':{'17':{'s':76700000,'e':1740}},
				 '15':{'18':{'s':19200000,'e':2970}, '19':{'s':5600000,'e':1990}, '20':{'s':87700000,'e':81200}, '21':{'s':330000, 'e':330000}, '23':{'s':638000,'e':638000}}
				 } # ********* Do not remove this ***********
		
		if sqliteDB == None:
			return False
		global DBname
		DBname = sqliteDB
		self.conn = sqlite3.connect(sqliteDB, isolation_level=None)
		# Turn on autocommit mode
		# Set isolation_level to "IMMEDIATE"
		self.conn.isolation_level = "IMMEDIATE"
		self.cur = self.conn.cursor()
		self.num_words = -1
		self.wordid_list = []
		self.level = 0

	def get_random_wordid(self, level, numwords=0):
		if self.wordid_list == [] or self.level != level:
			lev = str(level)
			if self.level_map.has_key(lev):
				self.level = level
				self.wordid_list = []
				it = self.level_map[lev].iterkeys()
				for k in it:
					l = k #self.level_map[level]
					#print l
					uf = self.level_map[lev][k]['s'] # upper frequency
					#print uf
					lf = self.level_map[lev][k]['e'] # lower frequency
					#print lf
					self.cur.execute("SELECT wordid from las_word where length = ? and exclude = 0 and freq >= ? and freq <= ?", (l, lf, uf ))
					self.wordid_list.extend( self.cur.fetchall())
		#count = self.wordid_list.count
		#print len(self.wordid_list)
		if numwords <= 0:
			random.shuffle(self.wordid_list)
			return self.wordid_list
		else:
			randids = random.sample(self.wordid_list , numwords)
		return randids
	
	def exit_game(self):
		self.conn.close()
	
	def get_DB_name(self):
		return 

	
	
class Word:

	def __init__(self, identifier=None, value= None):
		
		self.conn = sqlite3.connect(DBname, isolation_level=None)
		# Turn on autocommit mode
		# Set isolation_level to "IMMEDIATE"
		self.conn.isolation_level = "IMMEDIATE"
		self.cur = self.conn.cursor()
		if identifier == "las_word_id":
			self.las_word_id = value
			self.cur.execute("SELECT * from las_word where laswid = ?", (value,))
		elif identifier == "wordid":
			self.wordid = value
			self.cur.execute("SELECT * from las_word where wordid = ?", (value,))
		elif identifier == "word":
			self.word = value
			self.cur.execute("SELECT * from las_word where lemma = ?", (value,))
		elif identifier == None or value == None:
			self.las_word_id = None
			self.wordid = None
			self.word = None
			self.length = None
			self.freq = None
			self.synsetid_list = []
			return None
		else:
			return "Invalid Usage"

		(laswid, wordid, lemma, length, freq, exclude) = self.cur.fetchone()
		self.las_word_id = laswid
		self.wordid = wordid
		self.word = lemma
		self.length = length
		self.freq = freq
		self.synsetid_list = []

	def get_word(self):
		return self.word

	def get_wordid(self):
		return self.wordid
	
	def get_category(self, categoryid):
		self.category_list = []
		self.cur.execute("SELECT * from las_categorydef where categoryid = ?", (categoryid,))
		(categoryid, name, pos) = self.cur.fetchone()
		return name


	def get_synsetid(self):
		self.cur.execute("SELECT * from las_sense where wordid = ?", (self.wordid,))
		for (wordid, synsetid, rank) in self.cur:
			self.synsetid_list.append(synsetid)
		return self.synsetid_list

	
	def get_freq(self):
		return self.freq
	def get_def(self):
		self.def_list = []
		if self.synsetid_list == []:
			self.get_synsetid()
		for synsetid in self.synsetid_list:
			self.cur.execute("SELECT * from las_synset where synsetid = ?", (synsetid,) )
			for (synsetid, pos, categoryid,	definition) in self.cur:
				cat_name = self.get_category(categoryid)
				self.def_list.append((pos, definition, cat_name))
		return self.def_list

	def get_usage(self):
		self.usage_list = []
		if self.synsetid_list == []:
			self.get_synsetid()
		for synsetid in self.synsetid_list:
			self.cur.execute("SELECT * from las_sample where synsetid = ?", (synsetid,))
			for (synsetid, sampleid, sample) in self.cur:
				self.usage_list.append((sample))
		return self.usage_list

	def update_score(self, wordid, action = "correct"):
		if action == "correct":
			try:
				self.cur.execute("SELECT * from las_score where wordid = ?", (wordid,))
				(wordid, num_played, num_correct) = self.cur.fecthone()
				num_played = num_played + 1
				num_correct = num_correct + 1
				self.cur.execute("UPDATE las_score SET num_played = ? , num_correct = ? where wordid = ?", (num_played, num_correct, wordid,))
			except :
				self.cur.execute("INSERT into las_score (wordid, num_played, num_correct) VALUES (?,?,?) ", (wordid,1,1, ))
		elif action == "incorrect":
			try:
				self.cur.execute("SELECT * from las_score where wordid = ?", (wordid,))
				(wordid, num_played, num_correct) = self.cur.fecthone()
				num_played = num_played + 1
				self.cur.execute("UPDATE las_score SET num_played = ? where wordid = ?", (num_played, wordid,))
			except :
				self.cur.execute("INSERT into las_score (wordid, num_played) VALUES (?,?) ", (wordid,1, ))
		self.conn.commit()

	
	
	
	def get_phoneme(self):
		self.cur.execute("SELECT * from las_phoneme where wordid = ?", (self.wordid,))
		t = self.cur.fetchone()
		if t != None:
			(wordid, phoneme, num_syllabe, is_correct) = t
			return (phoneme, is_correct)
		else:return None
	
	def update_phoneme(self, phoneme, is_correct = True):
		#try:
			#if is_correct == True:
				#self.cur.execute("UPDATE las_phoneme SET phoneme = ?, is_correct = ? where wordid = ?", (phoneme, 1, self.wordid,))
			#else:
				#self.cur.execute("UPDATE las_phoneme SET phoneme = ?, is_correct = ? where wordid = ?", (phoneme, 0, self.wordid,))
		#except:
		try:
			if is_correct == True:
				self.cur.execute("INSERT into las_phoneme (wordid, phoneme, is_correct ) VALUES (?,?,?) ", (self.wordid, phoneme, 1, ))
			else:
				self.cur.execute("INSERT into las_phoneme (wordid, phoneme, is_correct ) VALUES (?,?,?) ", (self.wordid, phoneme, 0, ))
		except sqlite3.OperationalError:
			if is_correct == True:
				self.cur.execute("UPDATE las_phoneme SET phoneme = " + phoneme + ", is_correct = 1 where wordid = ?", (self.wordid,))
			else:
				self.cur.execute("UPDATE las_phoneme SET phoneme = " + phoneme +", is_correct = 0 where wordid = ?", (self.wordid,))
			
		self.conn.commit()
	def exit_game(self):
		self.conn.close()
if __name__ == "__main__":
	k = Dict()
	num_words = k.get_num_words()
	print num_words

	id = k.get_random_wordid(length = 5, numwords = 3) #will return word of length 5
	for (wordid,) in id:
		print wordid
		l = Word("wordid", wordid )

		print l.get_word()
		print l.get_def()
		print l.get_usage()
