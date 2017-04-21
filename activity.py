#!/usr/bin/python
# -*- encoding: utf-8 -*-

# Copyright 2013 Patricia Espinola y Victor Cubas
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Piensa y Escribe: A case study for developing an activity."""

import gtk
import logging
import voice
from ConfigParser import SafeConfigParser

from gettext import gettext as _

from sugar.activity import activity
from sugar.graphics.toolbarbox import ToolbarBox
from sugar.activity.widgets import ActivityButton
from sugar.activity.widgets import ActivityToolbox
from sugar.activity.widgets import TitleEntry
from sugar.activity.widgets import StopButton
from sugar.activity.widgets import ShareButton


class PiensaEscribeActivity(activity.Activity):
    """PiensaEscribe class as specified in activity.info"""

    def __init__(self, handle):
        """Set up the PiensaEscribe activity."""
        activity.Activity.__init__(self, handle)

        # we do not have collaboration features
        # make the share option insensitive
        self.max_participants = 1

        # toolbar with the new toolbar redesign
        toolbar_box = ToolbarBox()

        activity_button = ActivityButton(self)
        toolbar_box.toolbar.insert(activity_button, 0)
        activity_button.show()

        title_entry = TitleEntry(self)
        toolbar_box.toolbar.insert(title_entry, -1)
        title_entry.show()

        share_button = ShareButton(self)
        toolbar_box.toolbar.insert(share_button, -1)
        share_button.show()
        
        separator = gtk.SeparatorToolItem()
        separator.props.draw = False
        separator.set_expand(True)
        toolbar_box.toolbar.insert(separator, -1)
        separator.show()

        stop_button = StopButton(self)
        toolbar_box.toolbar.insert(stop_button, -1)
        stop_button.show()

        self.set_toolbar_box(toolbar_box)
        toolbar_box.show()
        
        self.createGUI()
        # label with the text, make the string translatable

    def createGUI(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        try :
            self.indice = int(self.metadata['indice'])
            print self.indice
        except:
            self.indice = 1

        self.ITERACION = 10
        vbox = gtk.VBox()
        hbox = gtk.HBox()
        vbox.add(hbox)

        imagen1 = gtk.Image() 
        imagen2 = gtk.Image()
        button1 = gtk.Button()
        button2 = gtk.Button()
        button3 = gtk.Button()

        imagen1.set_from_file(parser.get('Pregunta' + str(self.indice), 'imagen1'))
        imagen2.set_from_file(parser.get('Pregunta' + str(self.indice), 'imagen2'))
        
        button1.set_label(parser.get('Pregunta' + str(self.indice), 'opcion1'))
        button2.set_label(parser.get('Pregunta' + str(self.indice), 'opcion2'))
        button3.set_label(parser.get('Pregunta' + str(self.indice), 'opcion3'))	
        	
        button1.connect('enter', self.__sobre_boton_cb)
        button2.connect('enter', self.__sobre_boton_cb)
        button3.connect('enter', self.__sobre_boton_cb)
        button1.connect('clicked', self.__correcto_cb, imagen1,
								imagen2, button1, button2, button3)
        button2.connect('clicked', self.__correcto_cb, imagen1,
								imagen2, button1, button2, button3)
        button3.connect('clicked', self.__correcto_cb, imagen1,
								imagen2, button1, button2, button3)

        hbox.add(imagen1)
        hbox.add(imagen2)
        vbox.add(button1)
        vbox.add(button2)
        vbox.add(button3)

        self.set_canvas(vbox)
        vbox.show_all()

    def resetear(self, imagen1, imagen2, button1, button2, button3):
        parser = SafeConfigParser()
        parser.read('config.ini')
        
        self.indice += 1
        imagen1.set_from_file(parser.get('Pregunta' + str(self.indice), 'imagen1'))
        imagen2.set_from_file(parser.get('Pregunta' + str(self.indice), 'imagen2'))
        
        button1.set_label(parser.get('Pregunta' + str(self.indice), 'opcion1'))
        button2.set_label(parser.get('Pregunta' + str(self.indice), 'opcion2'))
        button3.set_label(parser.get('Pregunta' + str(self.indice), 'opcion3'))	
        
    def __correcto_cb(self, button, imagen1, imagen2, button1, button2, button3):
        parser = SafeConfigParser()
        parser.read('config.ini')
        
        if button.get_label() == parser.get('Pregunta' + str(self.indice), 'Respuesta'):
		    voice.say('Opcion correcta')
		    
		    if self.ITERACION == self.indice:
		           self.indice = 0
		    self.resetear(imagen1, imagen2, button1, button2, button3)
        else:
		    voice.say('Opcion incorrecta - Intente de nuevo')

 
    def __sobre_boton_cb(self, button):
        voice.say(button.get_label())
        
    def write_file(self, file_name):
        self.metadata['indice'] = self.indice
