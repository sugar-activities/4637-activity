#!/usr/bin/python
# -*- encoding: utf-8 -*-
import gtk
import voice
from ConfigParser import SafeConfigParser


class MyApp():
    def __init__(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        self.indice = 1
        self.ITERACION = 10

        window = gtk.Window()
        vbox = gtk.VBox()
        hbox = gtk.HBox()

        window.connect('destroy', self.destroy)
        window.add(vbox)
        window.set_title('Piensa y Escribe')
        window.set_size_request(700,600)
        window.set_position(gtk.WIN_POS_CENTER)
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
        window.show_all()

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
       

    def destroy(self, window, data=None):
        gtk.main_quit()
    
    def __sobre_boton_cb(self, button):
        voice.say(button.get_label())

if __name__ == "__main__":
    my_app = MyApp()
    gtk.main()
