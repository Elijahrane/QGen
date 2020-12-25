import gi
import sys
import os
import re
from shutil import copyfile
import Qformats

gi.require_version("Gtk","3.0")
from gi.repository import Gtk
class MainWindow(Gtk.Window):
        def __init__(self):
            self.box = Gtk.Box(orientation=1,spacing=6)
            self.grid = Gtk.Grid()
            self.availFormats = Qformats.Qformats
            self.formatSelect = Gtk.ComboBoxText()
            self.buttonComp = Gtk.Button(label="Compile")
            self.questionDict = {}  #This will be used to get the question : replace term pairs from formatSelect's text
            self.filenameDict = {}  #This method kind of sucks but there isnt a good way to extract stuff other than the label from ComboBoxText
            for z in self.availFormats:
                self.formatSelect.append_text(z.friendlyName)
                self.questionDict[z.friendlyName] = z.replaceTerms
                self.filenameDict[z.friendlyName] = z.filename
            Gtk.Window.__init__(self, title="Reading Quiz Generator")
            self.add(self.box)

            self.box.pack_start(self.formatSelect, False, False, 0)
            self.formatSelect.set_active(0) #select the first item by default
            self.formatSelect.connect("changed", self.refreshGrid)
            self.box.pack_start(self.grid, True, False, 0)
            self.box.pack_start(self.buttonComp, False, False, 0)
            self.buttonComp.connect("clicked", self.compilePDF)
        def populateGrid(self, selectedFormat):
            i = 0
            valueBank = self.questionDict[selectedFormat]
            prompts = valueBank.values()
            for value in prompts:
                print(value)
                entry = Gtk.Entry()
                label = Gtk.Label(label=value)
                self.grid.attach(label, 0, i, 1, 1)
                self.grid.attach(entry, 1, i, 1, 1)
                i = i + 1
            self.show_all()

        def refreshGrid(self, widget):
            self.box.remove(self.grid)
            self.box.remove(self.buttonComp)
            self.grid = Gtk.Grid.new()
            self.box.pack_start(self.grid, True, False, 0)
            self.box.pack_start(self.buttonComp, False, False, 0)
            text = self.formatSelect.get_active_text()
            self.populateGrid(text)

        def compilePDF(self, widget):
            filename = self.filenameDict[win.formatSelect.get_active_text()]
            copyfile(filename, filename[:-3])
            filename = filename[:-3]

            with open(filename, 'r+') as f:                    
                text = f.read()
                i = 0
                terms = self.questionDict[win.formatSelect.get_active_text()]
                keys = terms.keys()
                for key in keys:
                    print(key)
                    replacementCell = self.grid.get_child_at(1,i)
                    replacement = replacementCell.get_text()
                    text = re.sub(key, replacement, text)
                    i = i + 1
                f.seek(0)
                f.write(text)
                f.truncate()
                f.close()
            os.system('latexmk ./' + filename + ' -pdf -quiet')
            os.system('rm '+ filename[:-4] + '.aux '+ filename[:-4] + '.fls '+ filename[:-4] + '.tex '+ filename[:-4] + '.fdb_latexmk '+ filename[:-4] + '.log')
            os.system('xdg-open '+ filename[:-4] + '.pdf')

win = MainWindow()
win.populateGrid(win.formatSelect.get_active_text())
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
