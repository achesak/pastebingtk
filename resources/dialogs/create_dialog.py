# -*- coding: utf-8 -*-


# This file defines the Create Paste dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class CreatePasteDialog(Gtk.Dialog):
    """Shows the new paste dialog."""
    
    def __init__(self, parent):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Create Paste", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the grid.
        new_box = self.get_content_area()
        new_grid = Gtk.Grid()
        # Add the grid to the dialog's content area.
        new_box.add(new_grid)
        
        # Create the name label and entry.
        name_lbl = Gtk.Label("Name: ")
        name_lbl.set_alignment(0, 0.5)
        new_grid.add(name_lbl)
        self.name_ent = Gtk.Entry()
        new_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the format label and combobox.
        form_lbl = Gtk.Label("Format: ")
        form_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(form_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.form_com = Gtk.ComboBoxText()
        for i in ["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"]:
            self.form_com.append_text(i)
        self.form_com.set_active(0)
        new_grid.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the expiration label and combobox.
        expi_lbl = Gtk.Label("Expiration: ")
        expi_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in ["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.expi_com.append_text(i)
        self.expi_com.set_active(0)
        new_grid.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the exposure label and combobox.
        expo_lbl = Gtk.Label("Exposure: ")
        expo_lbl.set_alignment(0, 0.5)
        new_grid.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in ["Public", "Unlisted", "Private"]:
            self.expo_com.append_text(i)
        self.expo_com.set_active(0)
        new_grid.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
