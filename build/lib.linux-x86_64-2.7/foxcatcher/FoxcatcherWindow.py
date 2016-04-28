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

from locale import gettext as _
from songkick import Songkick
from gi.repository import Gtk, Pango, GdkPixbuf # pylint: disable=E0611
import logging
import json, requests, urllib
import file_setting


logger = logging.getLogger('foxcatcher')

from foxcatcher_lib import Window
from foxcatcher.AboutFoxcatcherDialog import AboutFoxcatcherDialog
from foxcatcher.PreferencesFoxcatcherDialog import PreferencesFoxcatcherDialog

# See foxcatcher_lib.Window.py for more details about how this class works
class FoxcatcherWindow(Window):
    __gtype_name__ = "FoxcatcherWindow"

    def finish_initializing(self, builder): # pylint: disable=E1002
        """Set up the main window"""
        super(FoxcatcherWindow, self).finish_initializing(builder)

        self.AboutDialog = AboutFoxcatcherDialog
        self.PreferencesDialog = PreferencesFoxcatcherDialog
        
        # Code for other initialization actions should be added here.
        
        self.refresh_button = self.builder.get_object("refresh_button")
        self.scrolledwindow = self.builder.get_object("scrolledwindow")
        self.textview = self.builder.get_object("textview")
        self.check_concerts(FoxcatcherWindow)


    def delete_artist_list(self, widget):
        delete_artist_window = Gtk.Window()
        delete_artist_window.set_position( Gtk.WindowPosition.MOUSE)
        delete_artist_window.set_size_request(400, 400)
        delete_artist_window.set_title("Delete Artist")
        vbox = Gtk.VBox(False,0)
        delete_artist_window.add(vbox)
        vbox.show()

        scroll_wind = Gtk.ScrolledWindow()
        vbox.pack_start(scroll_wind, True, True, 0)
        scroll_wind.show()
        
        store = Gtk.ListStore(int,str)
        self.treeView = Gtk.TreeView(store)
        scroll_wind.add(self.treeView)

        artist_list = file_setting.parse_file_list("name_setting.txt")
        
        for item in artist_list:
            store.append(item)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("#", rendererText, text=0)
        column.set_sort_column_id(0)
        self.treeView.append_column(column)
        
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Artist Name", rendererText, text=1)
        column.set_sort_column_id(1)    
        self.treeView.append_column(column)
        self.treeView.show()
        
        delete_button = Gtk.Button( 'Delete Artist')
        delete_button.set_size_request(20,20)
        delete_button.show()
        delete_button.connect('clicked', self.delete_button_clicked, store)
        vbox.pack_start(delete_button, False, False, 0 )
        
        clear_button = Gtk.Button( 'Clear ALL')
        clear_button.set_size_request(20,20)
        clear_button.show()
        clear_button.connect('clicked', self.clear_button_clicked, store)
        vbox.pack_start(clear_button, False, False, 0 )

        
        
        delete_artist_window.show()


    def delete_button_clicked(self, widget, store):
        
        selection = self.treeView.get_selection()
   
        model, paths = selection.get_selected_rows()
        
        for path in paths:
            iter = model.get_iter(path)
            val = store.get_value(iter,1)
            file_setting.delete_data(val, "name_setting.txt")
            model.remove(iter)
            

    def clear_button_clicked(self, widget, store):
        file_setting.clear_file()
        store.clear()

    def manage_location(self, widget):
        location_window = Gtk.Window()
        location_window.set_position( Gtk.WindowPosition.MOUSE)
        location_window.set_size_request(400, 400)
        location_window.set_title("Manage Location")
        vbox = Gtk.VBox(False,0)
        location_window.add(vbox)
        vbox.show()

        scroll_wind = Gtk.ScrolledWindow()
        vbox.pack_start(scroll_wind, True, True, 0)
        scroll_wind.show()
        
        store = Gtk.ListStore(int,str)
        self.treeView = Gtk.TreeView(store)
        scroll_wind.add(self.treeView)
        
        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("#", rendererText, text=0)
        column.set_sort_column_id(0)
        self.treeView.append_column(column)

        rendererText = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("City Name", rendererText, text=1)
        column.set_sort_column_id(1)
        self.treeView.append_column(column)
        self.treeView.show()
        
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, False, 0)
        self.entry.show()

        
        search_button = Gtk.Button( 'Search Locations')
        search_button.set_size_request(20,20)
        search_button.show()
        search_button.connect('clicked', self.search_button_clicked, store)
        vbox.pack_start(search_button, False, False, 0 )

        addloc_button = Gtk.Button( 'Add Location')
        addloc_button.set_size_request(20,20)
        addloc_button.show()
        addloc_button.connect('clicked', self.add_location_button_clicked, store)
        vbox.pack_start(addloc_button, False, False, 0 )
        
        view_button = Gtk.Button( 'View Location')
        view_button.set_size_request(20,20)
        view_button.show()
        view_button.connect('clicked', self.view_location_button_clicked, store)
        vbox.pack_start(view_button, False, False, 0 )

        location_window.show()

    def search_button_clicked(self, widget, store):
        store.clear()
        city = self.entry.get_text().upper()
        
        city_list = file_setting.parse_file("cities.txt")
        
        possible_list = file_setting.show_matches(city, city_list)
        
        search_list = file_setting.data_list_tuple(possible_list)
        
        for item in search_list:
            store.append(item)
    def add_location_button_clicked(self, widget, store):
         
        selection = self.treeView.get_selection()

        model, paths = selection.get_selected_rows()

        for path in paths:
            iter = model.get_iter(path)
            val = store.get_value(iter,1)
            file_setting.write_data(val, "city_setting.txt")
            self.entry.set_text("")
            model.remove(iter)

        
    def view_location_button_clicked(self, widget, store):
        store.clear()
        location = file_setting.parse_file_list("city_setting.txt")
        for item in location:
            store.append(item)

    def add_artist(self, widget):
        add_artist_window = Gtk.Window()
        add_artist_window.set_position( Gtk.WindowPosition.MOUSE)
        add_artist_window.set_size_request(400, 100)
        add_artist_window.set_title("Add Artist")
        vbox = Gtk.VBox(False,0)
        add_artist_window.add(vbox)
        vbox.show()
        
        self.entry = Gtk.Entry()
        vbox.pack_start(self.entry, False, False, 0)
        self.entry.show()
        
        button = Gtk.Button( 'ADD')
        button.set_size_request(20,20)
        button.show()
        button.connect('clicked', self.add_button_clicked)
        #button.connect('Entered', self.add_button_clicked)
        vbox.pack_start(button, False, False, 0)
        
        
        self.success = Gtk.Label()
        #self.success.set_markup('<a href="http://www.w3schools.com/html/">Visit our HTML tutorial</a>')
        self.success.set_markup('<span color="green">SUCCESS ADDING ARTIST!</span>')
        vbox.pack_start(self.success, False, False, 0)
        
        self.failed_add = Gtk.Label()
        self.failed_add.set_markup('<span color="red">Failed Adding Artist-Check Spelling!</span>')
        vbox.pack_start(self.failed_add, False, False, 0)
        

        add_artist_window.show()
        

    def add_button_clicked(self, widget):
        dev_key  = "yBb9DilAbXqZ0MCH"
        artist_name = self.entry.get_text().upper()
        first_part_url = "http://api.songkick.com/api/3.0/search/artists.json?query="
        third_part_url = "&apikey=" + dev_key
        url = first_part_url + artist_name + third_part_url

        result = json.load(urllib.urlopen(url))
        temp = int(result['resultsPage']['totalEntries'])
        if temp > 0:
            
            infile = open("name_setting.txt", "ab")
            infile.write(artist_name.upper() + "\n")
            infile.close()
            self.entry.set_text("")
            self.failed_add.hide()
            self.success.show()
        else:
            self.success.hide()
            self.failed_add.show()

    def check_concerts(self, widget):
  
        self.textview.get_buffer().set_text("")
        #pixbuf = GdkPixbuf.Pixbuf.new_from_file('SK_badge.png')
        bad_names = []
        dev_key  = "yBb9DilAbXqZ0MCH"
        try:
            songkick = Songkick(api_key = dev_key)
        except:
             self.textview.get_buffer().set_text("ERROR: Unable to access SongKick!\n")
             return None

        infile = open("name_setting.txt", "r")
        temp = infile.read().split("\n")
        temp = filter(None, temp)
        artist_names = list(set(temp))
        
        #self.url_lib = Gtk.Label()
        #self.url_lib.set_markup('<a href="http://www.w3schools.com/html/">Visit our HTML tutorial</a>')
        self.ebox = Gtk.Button("PLEASE")
        self.ebox.show()
        #anchor = Gtk.TextChildAnchor()
        #buffer1 = self.textview.get_buffer()
        #iter1 = buffer1.get_end_iter()
        #anchor = buffer1.create_child_anchor(iter1)
        #self.textview.add_child_at_anchor(self.url_lib, anchor)
        #self.textview.show_all()
        #self.textview.get_buffer().insert_with_tags(self.textview.get_buffer().get_end_iter(),  self.url_lib)
#       anchor = self.textview.create_child_anchor(self.textview.get_buffer().get_end_iter())
        if not artist_names:
           self.textview.get_buffer().set_text("Your List of Artists is Empty!\n")
           return
        file_setting.write_new_file(artist_names, "name_setting.txt")
        new_city = file_setting.parse_file("city_setting.txt")
        try:
            search = new_city[0]
        except:
            search = ""
            pass
        if search == "":
            error_mess = "you currently do not have a location set!"
            self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + error_mess)
            return None
        #search = search.lower()
        search = search.title()
        user_city = search
        
        for name in artist_names:
            events = songkick.events.query(artist_name = name )
            try:
                for event in events:
                    city = event.location.city.encode('ascii', 'ignore').split(",")
    
                    if city[0] == user_city:
                        url1 = "<a href="
                        url2 = event.uri.encode('ascii','ignore')
                        url3 = ">Check Tickets</a>"
                        final_url = url1 + "\"" + url2 + "\"" + url3
                        index = final_url.find('utm_medium')
                        tickets_url = final_url[:index] + "amp;" + final_url[index:]
                        event_name = event.display_name.encode('ascii','ignore')
                        event_loc = event.location.city.encode('ascii','ignore')
                        event_venue = event.venue.display_name.encode('ascii','ignore')
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),"\n" + "--------------------------------------------------------------------------------------------------")
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + "*")
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + name)
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + "*")
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + event_name)
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n" + event_loc)
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  ", " + event_venue)
                        #self.textview.get_buffer().insert_pixbuf(self.textview.get_buffer().get_end_iter(), pixbuf)
                        self.textview.get_buffer().insert(self.textview.get_buffer().get_end_iter(),  "\n") 
                        test_url = '<a href="http://www.w3schools.com/html/">Check Tickets</a>'
                        #print test_url
                        #print tickets_url
                        #print final_url
                        self.url_lib = Gtk.Label()
                        self.url_lib.set_markup(tickets_url)
                        buffer1 = self.textview.get_buffer()
                        iter1 = buffer1.get_end_iter()
                        anchor = buffer1.create_child_anchor(iter1)
                        self.textview.add_child_at_anchor(self.url_lib, anchor)
                        self.textview.show_all()
            except:
                bad_names.append(name)
            continue
        if bad_names:
            for name in bad_names:
                
                file_setting.delete_data(name , "name_setting.txt")


