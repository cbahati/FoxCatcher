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

import difflib   

def write_new_file(list_data, filename):
    infile = open(filename, "w")
    for str in list_data:
        infile.write(str.upper() + "\n")
    infile.close()

def write_to_file(list_data, filename):
    infile = open(filename, "ab")
    for str in list_data:
        infile.write(str.upper() + "\n")
        print str
    infile.close()

def delete_from_list(delete_data, filename):
    infile = open(filename, "r")
    data = infile.read().split("\n")

    for name in data:
        i = data.index(delete_data)
        data.pop(i)

    data = filter(None, data)
    write_new_file(data, filename)
    infile.close()

def parse_file(filename):

    infile = open( filename, "r")
    data_names = infile.read().split("\n")
    data_names = filter(None, data_names)
    data_names = to_upper(data_names)
    infile.close()    
    return data_names
    
def parse_file_list(filename):
    data_list = []
    infile = open(filename, "r")
    data_names = infile.read().split("\n")
    data_names = filter(None, data_names)

    for name in enumerate(data_names, 1):
        data_list.append(name)

    infile.close()
    return data_list

def delete_data(delete_data, filename):
    infile = open(filename, "r")
    data = infile.read().split("\n")
    i = data.index(delete_data)
    data.pop(i)

    data = filter(None, data)
    write_new_file(data, filename)
    infile.close()

def clear_file():
    infile = open("name_setting.txt", "w")
    infile.close()


def show_matches( city ,cities):
    matches = difflib.get_close_matches( city, cities)
    matches.append(city)
    return matches

def to_upper(data):
    result = []
    for value in data:
        result.append(value.upper())
    return result

def data_list_tuple( data):
    
    count = 1
    data_list = []

    for value in enumerate(data, 1):
        data_list.append(value)

    return data_list

def write_data(data, filename):
    infile = open(filename, "w")
    infile.write(data.upper() + "\n")
    infile.close()
