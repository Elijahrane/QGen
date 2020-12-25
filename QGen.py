import gi
import sys
import os
import re
from shutil import copyfile
import Qformats

gi.require_version("Gtk","3.0")
from gi.repository import Gtk
class MainWindow(Gtk.Window):
        box = Gtk.Box(orientation=1,spacing=6)
        grid = Gtk.Grid()
        availFormats = Qformats.Qformats
        formatSelect = Gtk.ComboBoxText()
        buttonComp = Gtk.Button(label="Compile")
        for z in availFormats:
            formatSelect.append_text(z)
        def __init__(self):
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
            valueBank = Qformats.Qformats[selectedFormat]
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
            copyfile("readingquiz.tex.bk", "readingquiz.tex")
            filename ="readingquiz.tex"

            with open(filename, 'r+') as f:                    
                text = f.read()
                i = 0
                keys =  Qformats.frTermsOEQ.keys()
                for key in keys:
                    replacementCell = self.grid.get_child_at(1,i)
                    replacement = replacementCell.get_text()
                    text = re.sub(key, replacement, text)
                    i = i + 1
                f.seek(0)
                f.write(text)
                f.truncate()
                f.close()
            os.system('latexmk ./readingquiz.tex -pdf -quiet')
            os.system('rm readingquiz.aux readingquiz.fls readingquiz.tex readingquiz.fdb_latexmk readingquiz.log')
            os.system('xdg-open readingquiz.pdf')

win = MainWindow()
win.populateGrid(win.formatSelect.get_active_text())
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
