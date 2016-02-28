# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # Create the dialog.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        self.set_resizable(False)
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the notebook.
        notebook = Gtk.Notebook()
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Create the General tab
        opt_box = self.get_content_area()
        gen_grid = Gtk.Grid()
        gen_grid.set_column_spacing(10)
        gen_grid.set_row_spacing(5)
        gen_grid_lbl = Gtk.Label("General")
        
        # Create the prompt for login checkbox.
        self.log_chk = Gtk.CheckButton("Prompt for login")
        self.log_chk.set_active(config["prompt_login"])
        gen_grid.attach(self.log_chk, 0, 0, 2, 1)
        
        # Create the remember last username checkbox.
        self.user_chk = Gtk.CheckButton("Remember last username")
        self.user_chk.set_active(config["remember_username"])
        gen_grid.attach_next_to(self.user_chk, self.log_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_active(config["restore_window"])
        gen_grid.attach_next_to(self.win_chk, self.user_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the confirm on exit checkbox.
        self.exit_chk = Gtk.CheckButton("Confirm on exit")
        self.exit_chk.set_active(config["confirm_exit"])
        gen_grid.attach_next_to(self.exit_chk, self.win_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the check for spam filter checkbox.
        self.spam_chk = Gtk.CheckButton("Check for spam filter")
        self.spam_chk.set_active(config["check_spam"])
        gen_grid.attach_next_to(self.spam_chk, self.exit_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the pastes to retrieve label and spinbutton.
        lnum_lbl = Gtk.Label("Pastes to retrieve: ")
        lnum_lbl.set_alignment(0, 0.5)
        gen_grid.attach_next_to(lnum_lbl, self.spam_chk, Gtk.PositionType.BOTTOM, 1, 1)
        lnum_adj = Gtk.Adjustment(lower = 1, upper = 1000, step_increment = 1)
        self.lnum_sbtn = Gtk.SpinButton(digits = 0, adjustment = lnum_adj)
        self.lnum_sbtn.set_numeric(False)
        self.lnum_sbtn.set_value(config["pastes_retrieve"])
        gen_grid.attach_next_to(self.lnum_sbtn, lnum_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Defaults tab.
        def_grid = Gtk.Grid()
        def_grid.set_column_spacing(10)
        def_grid.set_row_spacing(5)
        def_grid_lbl = Gtk.Label("Defaults")
        
        # Create the default name label and entry.
        name_lbl = Gtk.Label("Default name: ")
        name_lbl.set_alignment(0, 0.5)
        def_grid.attach(name_lbl, 0, 0, 1, 1)
        self.name_ent = Gtk.Entry()
        self.name_ent.set_text(config["default_name"])
        def_grid.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default format label and combobox.
        form_lbl = Gtk.Label("Default format: ")
        form_lbl.set_alignment(0, 0.5)
        def_grid.attach_next_to(form_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.form_com = Gtk.ComboBoxText()
        for i in ["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"]:
            self.form_com.append_text(i)
        self.form_com.set_active(["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"].index(config["default_format"]))
        def_grid.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default expiration label and combobox.
        expi_lbl = Gtk.Label("Default expiration: ")
        expi_lbl.set_alignment(0, 0.5)
        def_grid.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in ["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.expi_com.append_text(i)
        self.expi_com.set_active(["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"].index(config["default_expiration"]))
        def_grid.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default exposure label and combobox.
        expo_lbl = Gtk.Label("Default exposure: ")
        expo_lbl.set_alignment(0, 0.5)
        def_grid.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in ["Public", "Unlisted", "Private"]:
            self.expo_com.append_text(i)
        self.expo_com.set_active(["Public", "Unlisted", "Private"].index(config["default_exposure"]))
        def_grid.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the Editing tab.
        edit_grid = Gtk.Grid()
        edit_grid.set_column_spacing(10)
        edit_grid.set_row_spacing(5)
        edit_grid_lbl = Gtk.Label("Editing")
        
        # Create the show line numbers checkbox.
        self.lin_chk = Gtk.CheckButton("Show line numbers")
        self.lin_chk.set_active(config["line_numbers"])
        edit_grid.attach(self.lin_chk, 0, 0, 2, 1)
        
        # Create the Technical tab.
        tech_grid = Gtk.Grid()
        tech_grid.set_column_spacing(10)
        tech_grid.set_row_spacing(5)
        tech_grid_lbl = Gtk.Label("Technical")
        
        # Create the developer key label and entry.
        devk_lbl = Gtk.Label("Developer key: ")
        devk_lbl.set_alignment(0, 0.5)
        tech_grid.attach(devk_lbl, 0, 0, 1, 1)
        self.devk_ent = Gtk.Entry()
        self.devk_ent.set_text(config["dev_key"])
        tech_grid.attach_next_to(self.devk_ent, devk_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the developer key description label.
        devk_desc_lbl = Gtk.Label("Please add your own developer key to\nprevent limits to the number of pastes that\ncan be created.\nThank you.")
        tech_grid.attach_next_to(devk_desc_lbl, devk_lbl, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Add the notebook.
        opt_box.add(notebook)
        notebook.append_page(gen_grid, gen_grid_lbl)
        notebook.append_page(def_grid, def_grid_lbl)
        notebook.append_page(edit_grid, edit_grid_lbl)
        notebook.append_page(tech_grid, tech_grid_lbl)
        
        # Show the dialog.
        self.show_all()
