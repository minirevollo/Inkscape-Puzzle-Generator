#! /usr/bin/env python
# -*- coding: utf-8 -*-
'''
@author: mini@revollo.de
member of the erfindergarden

Inkscape Erweiterung - Puzzle Generator
13.01.2019

Danke an neon22    https://github.com/Neon22/inkscape_extension_template
Nach seiner Anleitung konnte ich dieses Programm erstellen.

'''

import inkex       # Required
import simplestyle # will be needed here for styles support
from random import randint 

__version__ = '0.2'

inkex.localize()

def points_to_svgd(p, close = False):
    """ convert list of points (x,y) pairs
        into a closed SVG path list
    """
    f = p[0]
    p = p[1:]
    svgd = 'M %.2f,%.2f C' % f
    for x in p:
        svgd += ' %.4f,%.4f' % x
    if close:
        svgd += 'z'
    return svgd



### Your main function subclasses the inkex.Effect class

class Puzzle(inkex.Effect): 
    ###Erstellt das Puzzle.
    
    def __init__(self):
        " define how the options are mapped from the inx file "
        inkex.Effect.__init__(self) # initialize the super class
        
            
        # Define your list of parameters defined in the .inx file
        self.OptionParser.add_option("", "--spalten",
                                     action="store", type="int",
                                     dest="spalten", default = 16,
                                     help="Spalten des Puzzles")
        
        self.OptionParser.add_option("", "--zeilen",
                                     action="store", type="int",
                                     dest="zeilen", default = 12,
                                     help="Zeilen des Puzzles")
        
        self.OptionParser.add_option("", "--groesse",
                                     action="store", type="int", 
                                     dest="groesse", default = 2,
                                     help="Groesse der Nasen")
        
        # here so we can have tabs - but we do not use it directly - else error
        self.OptionParser.add_option("", "--active-tab",
                                     action="store", type="string",
                                     dest="active_tab", default='title', # use a legitmate default
                                     help="Active tab.")
        
        self.raster_x = 80
        self.raster_y = 80
        
        self.pfade = [] 
        self.pfad_punkte = []
        
        
    def punkte_erstellen(self, x, y):
        ###Schreibt die aktuellen Koordinaten in die Punkteliste
        
        self.pfad_punkte.append((x, y))
        
    def pfad_erstellen(self):        
        # Die gesammelten x und y Koordinaten der Punkte werden in Pfade (d) umgewandelt.  
        
        self.pfade.append(points_to_svgd(self.pfad_punkte ))
        del  self.pfad_punkte[:]
    
    def pfade_schreiben(self):
        ###Schreibt alle Pfade nacheinander in die Szene
         
        path_stroke = '#101010'  # Farbe für die Box
        path_fill   = 'none'     # keine Füllung, nur eine Linie
        path_stroke_width  = '0.4' # can also be in form '0.6mm'
        
        for nummer in range(len(self.pfade)):
            # define style using basic dictionary
            pfad_attribute = {'id': "pfad%d"%nummer, 'stroke': path_stroke,
                              'fill': path_fill, 'stroke-width': path_stroke_width,
                              'd': self.pfade[nummer]}
            # add path to scene                
            pfad = inkex.etree.SubElement(self.topgroup, inkex.addNS('path','svg'), pfad_attribute )
    
    def rand_erstellen(self):
        ###Schreibt die Umrandung in die Szene
         
        path_stroke = '#0000ff'  # Farbe für den Rand
        path_fill   = 'none'     # keine Füllung, nur eine Linie
        path_stroke_width  = '0.6' # can also be in form '0.6mm'
        
        # define style using basic dictionary
        rand_attribute = {'id': "rand", 'stroke': path_stroke, 'fill': path_fill,
                          'stroke-width': path_stroke_width , 'x': '0', 'y': '0',
                          'height': str(self.hoehe), 'width': str(self.breite),
                          'rx': '5', 'ry': '5'}
        # add path to scene                
        rand = inkex.etree.SubElement(self.topgroup, inkex.addNS('rect','svg'), rand_attribute )
    
    
    def spalten_erstellen(self):
        ###Erstellt für die Spalten einen Teilpfad nach dem anderen und fügt ihn der Punkteliste hinzu.###
        
        ###Position x wird auf 0 gesetzt.               
        for reihe in range(1, self.spalten):
            ausrichtung = [-2, 2]
            p1x = reihe * self.raster_x
            p1y = 0
            self.punkte_erstellen(p1x, p1y)
            for zeile in range(self.zeilen):
                dir = ausrichtung[randint(0, 1)]
                p2x = p1x + randint(-2, 2) 
                p2y = p1y + randint(28, 32)
                p3x = p1x
                p3y = p1y + randint(48, 52)                
                p4x = p1x
                p4y = p1y + self.raster_y   
                              
                c1x = p1x + randint(-2, 2)
                c1y = p1y + 10
                
                c2x = p1x - randint(4, 8) * dir
                c2y = p1y + randint(26, 34)
                                
                c3x = p2x + (randint(10, 15) + self.nase) * dir
                c3y = 2 * p1y + 40 - c2y - self.nase
                
                c4x = p2x + (randint(10, 15) + self.nase) * dir
                c4y = p1y + randint(60, 68) + self.nase
                                
                c5x = p3x - randint(2, 8) * dir
                c5y = 2 * p1y + 110 - c4y                
                
                c6x = p1x + randint(-2, 2)
                c6y = p1y + self.raster_y - 10             
                                
                self.punkte_erstellen(c1x, c1y)
                self.punkte_erstellen(c2x, c2y)
                self.punkte_erstellen(p2x, p2y)
                self.punkte_erstellen(c3x, c3y) 
                self.punkte_erstellen(c4x, c4y)
                self.punkte_erstellen(p3x, p3y)
                self.punkte_erstellen(c5x, c5y)
                self.punkte_erstellen(c6x, c6y)
                self.punkte_erstellen(p4x, p4y)
                p1x = p4x
                p1y = p4y
            self.pfad_erstellen()
                
    def zeilen_erstellen(self):
        ###Erstellt für die Zeilen einen Teilpfad nach dem anderen und fügt ihn der Punkteliste hinzu.###
        
        ###Position x wird auf 0 gesetzt. 
        for zeile in range(1, self.zeilen):
            ausrichtung = [-1, 1]
            p1x = 0
            p1y = zeile * self.raster_y
            
            self.punkte_erstellen(p1x, p1y)
            for splate in range(self.spalten):
                dir = ausrichtung[randint(0, 1)]
                p2x = p1x + randint(28, 33) 
                p2y = p1y + randint(-2, 2)
                p3x = p1x + randint(47, 52)
                p3y = p1y + randint(-2, 2)
                p4x = p1x + self.raster_x
                p4y = p1y
                
                c1x = p1x + 10
                c1y = p1y + randint(-2, 2)
                
                c2x = p1x + randint(25, 29)
                c2y = p1y + randint(6, 10) * dir
                
                c3x = p1x +  randint(13, 15) - self.nase
                c3y = p2y - (randint(20, 26) + self.nase) * dir 
                
                c4x = p1x + randint(56, 63) + self.nase
                c4y = p2y - (randint(20, 26) + self.nase) * dir
               
                c5x = p1x + randint(45, 50)
                c5y = p3y + randint(6, 10) * dir
                
                c6x = p1x + self.raster_x - 10
                c6y = p1y + randint(-2, 2)
                                
                self.punkte_erstellen(c1x, c1y)
                self.punkte_erstellen(c2x, c2y)
                self.punkte_erstellen(p2x, p2y)
                self.punkte_erstellen(c3x, c3y) 
                self.punkte_erstellen(c4x, c4y)
                self.punkte_erstellen(p3x, p3y)
                self.punkte_erstellen(c5x, c5y)
                self.punkte_erstellen(c6x, c6y)
                self.punkte_erstellen(p4x, p4y)
                p1x = p4x
                p1y = p4y
            self.pfad_erstellen()
       
    
    
### -------------------------------------------------------------------
### This is your main function and is called when the extension is run.
    
    def effect(self):
        ###Hauptprogramm
        
        
        # holt die Parameter aus Inkscape
        self.spalten = self.options.spalten
        self.zeilen = self.options.zeilen
        self.nase = self.options.groesse
        
        
        # berechnet die Groesse des Puzzles
        self.breite = self.raster_x * self.spalten
        self.hoehe = self.raster_y * self.zeilen    
       
        
        # what page are we on
        page_id = self.options.active_tab # sometimes wrong the very first time

        #Eigenschaften der SVG auslesen und die Größe dem Puzzle anpassen
        svg = self.document.getroot()
        viewbox_size = '0 0 ' + str(self.breite) + ' ' + str(self.hoehe)
        svg.set('viewBox', viewbox_size)
        svg.set('height', str(self.hoehe))
        svg.set('width', str(self.breite))
        
        # Embed the path in a group to make animation easier:
        # Be sure to examine the internal structure by looking in the xml editor inside inkscape
        
        # Make a nice useful name
        g_attribs = { inkex.addNS('label','inkscape'): 'puzzle-gruppe', 'id': "puzzle",}
        # add the group to the document's current layer
        self.topgroup = inkex.etree.SubElement(self.current_layer, 'g', g_attribs )
        # Create SVG Path under this top level group
        self.spalten_erstellen()
        self.zeilen_erstellen()
        self.pfade_schreiben()
        self.rand_erstellen()
        # Make a nice useful name
        text_g_attribs = { inkex.addNS('label','inkscape'): 'puzzle-gruppe', 'id': "Branding",}
        # add the group to the document's current layer
        textgroup = inkex.etree.SubElement(self.current_layer, 'g', text_g_attribs )

        line_style = {'font-size': '25px', 'font-style':'normal', 'font-weight': 'normal',
                     'fill': '#ff0000', 'font-family': 'Consolas',
                     'text-anchor': 'middle', 'text-align': 'center'}
        branding_line_attribs = {inkex.addNS('label','inkscape'): 'branding-text',
                       'id': 'front text',
                       'style': simplestyle.formatStyle(line_style),
                       'x': str(self.breite / 2),
                       'y': str(self.hoehe / 2)
                       }
        
        branding_line = inkex.etree.SubElement(textgroup, inkex.addNS('text','svg'), branding_line_attribs)
        branding_line.text = 'puzzle-generator by mini revollo member of the erfindergarden'

        
        
        
if __name__ == '__main__':
    puzzle = Puzzle()
    puzzle.affect()

# Notes

