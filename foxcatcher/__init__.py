# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
### BEGIN LICENSE
# Copyright (C) 2015 Christian Bahati cbahati@luc.edu
# This program is free software: you can redistribute it and/or modify it 
# under the terms of the GNU General Public License version 3, as published 
# by the Free Software Foundation.
# 
# This program is distributed in the hope that it will be useful, but 
# WITHOUT ANY WARRANTY; without even the implied warranties of 
# MERCHANTABILITY, SATISFACTORY QUALITY, or FITNESS FOR A PARTICULAR 
# PURPOSE.  See the GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along 
# with this program.  If not, see <http://www.gnu.org/licenses/>.
### END LICENSE

import optparse
from time import sleep

from locale import gettext as _

from gi.repository import Gtk,GdkPixbuf # pylint: disable=E0611

from foxcatcher import FoxcatcherWindow

from foxcatcher_lib import set_up_logging, get_version


class splashScreen():
    def __init__(self):
        #DONT connect 'destroy' event here!                                                                                    
        self.loading_window = Gtk.Window()
        self.loading_window.set_position( Gtk.WindowPosition.CENTER)
        #self.loading_window.set_default_size(400,400)
        self.loading_window.set_decorated(False)

        self.logo = Gtk.Image()
        self.logo.set_from_file("foxcatcher6.jpg")
        self.loading_window.add(self.logo)
        self.logo.show()
        self.loading_window.show_all()
        while Gtk.events_pending():
            Gtk.main_iteration()

def parse_options():
    """Support for command line options"""
    parser = optparse.OptionParser(version="%%prog %s" % get_version())
    parser.add_option(
        "-v", "--verbose", action="count", dest="verbose",
        help=_("Show debug messages (-vv debugs foxcatcher_lib also)"))
    (options, args) = parser.parse_args()

    set_up_logging(options)

def main():
    'constructor for your class instances'

    parse_options()
    splScr = splashScreen()
    #If you don't do this, the splash screen will show, but wont render it's contents
    while Gtk.events_pending():
        Gtk.main_iteration()
    #Here you can do all that nasty things that take some time.
#    sleep(3)
    # Run the application.    
    window = FoxcatcherWindow.FoxcatcherWindow()
    splScr.loading_window.destroy()
    window.show()
    Gtk.main()
