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
import gtk, gobject
from time import sleep
# Update the value of the progress bar so that we get
# some movement
def progress_timeout(pbobj):
    pbobj.show_text("Time Left(secs): "+str(pbobj.timeleft))
    if pbobj.timeleft>=0:
	pbobj.timeleft=pbobj.timeleft-1
    new_val = pbobj.pbar.get_fraction() + 0
    if new_val>1:
        new_val=0
    if pbobj.timeleft==-1:
	pbobj.destroy_progress()
	pbobj.ls_obj.end_game()
	    
 # Set the new value
    pbobj.pbar.set_fraction(new_val)

 # As this is a timeout function, return TRUE so that it
 # continues to get called
    return True

class ProgressBar:
 # Callback that toggles the text display within the progress
 # bar trough
    def show_text(self, data=None):
    	self.pbar.set_text(data)


 # Callback that toggles the orientation of the progress bar
    def destroy_progress(self):
    	gobject.source_remove(self.timer)
    	self.timer = 0
  
		
    def __init__(self,obj):
    	
 # Create the ProgressBar
    	self.pbar = gtk.ProgressBar()
	self.pbar.show()
	self.ls_obj=obj
	self.ls_obj.stats_table.attach(self.pbar,0,2,5,6)
		
		#skill_level_scale.grab_focus()

	 # Add a timer callback to update the value of the progress bar
	self.timer = gobject.timeout_add (1000, progress_timeout, self)	
	self.timeleft=600


def main():
    gtk.main()
    return 0

if __name__ == "__main__":
    ProgressBar()
    main()
   
    
