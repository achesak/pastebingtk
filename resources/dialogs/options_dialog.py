# -*- coding: utf-8 -*-


# This file defines the Add New dialog.


# Import GTK for the dialog.
from gi.repository import Gtk


class OptionsDialog(Gtk.Dialog):
    """Shows the "Options" dialog."""
    def __init__(self, parent, config):
        """Create the dialog."""
        
        # This window should be modal.
        Gtk.Dialog.__init__(self, "Options", parent, Gtk.DialogFlags.MODAL)
        # Don't allow the user to resize the window.
        self.set_resizable(False)
        
        # Create the notebook.
        notebook = Gtk.Notebook()
        # Set tab position to top.
        notebook.set_tab_pos(Gtk.PositionType.TOP)
        
        # Add the buttons.
        self.add_button("Cancel", Gtk.ResponseType.CANCEL)
        self.add_button("OK", Gtk.ResponseType.OK)
        
        # Create the first grid.
        opt_box = self.get_content_area()
        opt_grid1 = Gtk.Grid()
        opt_grid1_lbl = Gtk.Label("General")
        
        # Create the prompt for login checkbox.
        self.log_chk = Gtk.CheckButton("Prompt for login")
        self.log_chk.set_active(config["prompt_login"])
        opt_grid1.attach(self.log_chk, 0, 0, 2, 1)
        
        # Create the remember last username checkbox.
        self.user_chk = Gtk.CheckButton("Remember last username")
        self.user_chk.set_active(config["remember_username"])
        opt_grid1.attach_next_to(self.user_chk, self.log_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the restore window size checkbox.
        self.win_chk = Gtk.CheckButton("Restore window size")
        self.win_chk.set_active(config["restore_window"])
        opt_grid1.attach_next_to(self.win_chk, self.user_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the confirm on exit checkbox.
        self.exit_chk = Gtk.CheckButton("Confirm on exit")
        self.exit_chk.set_active(config["confirm_exit"])
        opt_grid1.attach_next_to(self.exit_chk, self.win_chk, Gtk.PositionType.BOTTOM, 2, 1)
        
        # Create the second grid.
        opt_grid2 = Gtk.Grid()
        opt_grid2_lbl = Gtk.Label("Defaults")
        
        # Create the default name label and entry.
        name_lbl = Gtk.Label("Default name: ")
        name_lbl.set_alignment(0, 0.5)
        opt_grid2.attach(name_lbl, 0, 0, 1, 1)
        self.name_ent = Gtk.Entry()
        self.name_ent.set_text(config["default_name"])
        opt_grid2.attach_next_to(self.name_ent, name_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default format label and combobox.
        form_lbl = Gtk.Label("Default format: ")
        form_lbl.set_alignment(0, 0.5)
        opt_grid2.attach_next_to(form_lbl, name_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.form_com = Gtk.ComboBoxText()
        for i in ["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"]:
            self.form_com.append_text(i)
        self.form_com.set_active(["None", "4CS", "6502 ACME Cross Assembler", "6502 Kick Assembler", "6502 TASM/64TASS", "ABAP", "ActionScript", "ActionScript 3", "Ada", "ALGOL 68", "Apache Log", "AppleScript", "APT Sources", "ARM", "ASM (NASM)", "ASP", "Asymptote", "autoconf", "Autohotkey", "AutoIt", "Avisynth", "Awk", "BASCOM AVR", "Bash", "Basic4GL", "BibTeX", "Blitz Basic", "BNF", "BOO", "BrainFuck", "C", "C for Macs", "C Intermediate Language", "C#", "C++", "C++ (with QT extensions)", "C: Loadrunner", "CAD DCL", "CAD Lisp", "CFDG", "ChaiScript", "Clojure", "Clone C", "Clone C++", "CMake", "COBOL", "CoffeeScript", "ColdFusion", "CSS", "Cuesheet", "D", "DCL", "DCPU-16", "DCS", "Delphi", "Delphi Prism (Oxygene)", "Diff", "DIV", "DOS", "DOT", "E", "ECMAScript", "Eiffel", "Email", "EPC", "Erlang", "F#", "Falcon", "FO Language", "Formula One", "Fortran", "FreeBasic", "FreeSWITCH", "GAMBAS", "Game Maker", "GDB", "Genero", "Genie", "GetText", "Go", "Groovy", "GwBasic", "Haskell", "Haxe", "HicEst", "HQ9 Plus", "HTML", "HTML 5", "Icon", "IDL", "INI file", "Inno Script", "INTERCAL", "IO", "J", "Java", "Java 5", "JavaScript", "jQuery", "KiXtart", "Latex", "LDIF", "Liberty BASIC", "Linden Scripting", "Lisp", "LLVM", "Loco Basic", "Logtalk", "LOL Code", "Lotus Formulas", "Lotus Script", "LScript", "Lua", "M68000 Assembler", "MagikSF", "Make", "MapBasic", "MatLab", "mIRC", "MIX Assembler", "Modula 2", "Modula 3", "Motorola 68000 HiSoft Dev", "MPASM", "MXML", "MySQL", "Nagios", "newLISP", "NullSoft Installer", "Oberon 2", "Objeck Programming Langua", "Objective C", "OCalm Brief", "OCaml", "Octave", "OpenBSD PACKET FILTER", "OpenGL Shading", "Openoffice BASIC", "Oracle 11", "Oracle 8", "Oz", "ParaSail", "PARI/GP", "Pascal", "PAWN", "PCRE", "Per", "Perl", "Perl 6", "PHP", "PHP Brief", "Pic 16", "Pike", "Pixel Bender", "PL/SQL", "PostgreSQL", "POV-Ray", "Power Shell", "PowerBuilder", "ProFTPd", "Progress", "Prolog", "Properties", "ProvideX", "PureBasic", "PyCon", "Python", "Python for S60", "q/kdb+", "QBasic", "R", "Rails", "REBOL", "REG", "Rexx", "Robots", "RPM Spec", "Ruby", "Ruby Gnuplot", "SAS", "Scala", "Scheme", "Scilab", "SdlBasic", "Smalltalk", "Smarty", "SPARK", "SPARQL", "SQL", "StoneScript", "SystemVerilog", "T-SQL", "TCL", "Tera Term", "thinBasic", "TypoScript", "Unicon", "UnrealScript", "UPC", "Urbi", "Vala", "VB.NET", "Vedit", "VeriLog", "VHDL", "VIM", "Visual Pro Log", "VisualBasic", "VisualFoxPro", "WhiteSpace", "WHOIS", "Winbatch", "XBasic", "XML", "Xorg Config", "XPP", "YAML", "Z80 Assembler", "ZXBasic"].index(config["default_format"]))
        opt_grid2.attach_next_to(self.form_com, form_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default expiration label and combobox.
        expi_lbl = Gtk.Label("Default expiration: ")
        expi_lbl.set_alignment(0, 0.5)
        opt_grid2.attach_next_to(expi_lbl, form_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expi_com = Gtk.ComboBoxText()
        for i in ["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"]:
            self.expi_com.append_text(i)
        self.expi_com.set_active(["Never", "10 Minutes", "1 Hour", "1 Day", "1 Week", "2 Weeks", "1 Month"].index(config["default_expiration"]))
        opt_grid2.attach_next_to(self.expi_com, expi_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Create the default exposure label and combobox.
        expo_lbl = Gtk.Label("Default exposure: ")
        expo_lbl.set_alignment(0, 0.5)
        opt_grid2.attach_next_to(expo_lbl, expi_lbl, Gtk.PositionType.BOTTOM, 1, 1)
        self.expo_com = Gtk.ComboBoxText()
        for i in ["Public", "Unlisted", "Private"]:
            self.expo_com.append_text(i)
        self.expo_com.set_active(["Public", "Unlisted", "Private"].index(config["default_exposure"]))
        opt_grid2.attach_next_to(self.expo_com, expo_lbl, Gtk.PositionType.RIGHT, 1, 1)
        
        # Add the notebook.
        opt_box.add(notebook)
        
        # Add the tabs to the notebook.
        notebook.append_page(opt_grid1, opt_grid1_lbl)
        notebook.append_page(opt_grid2, opt_grid2_lbl)
        
        # Show the dialog. The response gets handled by the function
        # in the main class.
        self.show_all()
