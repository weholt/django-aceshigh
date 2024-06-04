from django.db import models
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager

User = get_user_model()

FONT_SIZE_CHOICES = [(i, str(i)) for i in range(8, 33, 2)]

THEME_CHOICES = [
    ("ambiance", "Ambiance"),
    ("chaos", "Chaos"),
    ("chrome", "Chrome"),
    ("clouds", "Clouds"),
    ("clouds_midnight", "Clouds Midnight"),
    ("cobalt", "Cobalt"),
    ("crimson_editor", "Crimson Editor"),
    ("dawn", "Dawn"),
    ("dracula", "Dracula"),
    ("dreamweaver", "Dreamweaver"),
    ("eclipse", "Eclipse"),
    ("github", "GitHub"),
    ("gob", "Gob"),
    ("gruvbox", "Gruvbox"),
    ("idle_fingers", "Idle Fingers"),
    ("iplastic", "Iplastic"),
    ("katzenmilch", "Katzenmilch"),
    ("kr_theme", "KR Theme"),
    ("kuroir", "Kuroir"),
    ("merbivore", "Merbivore"),
    ("merbivore_soft", "Merbivore Soft"),
    ("mono_industrial", "Mono Industrial"),
    ("monokai", "Monokai"),
    ("pastel_on_dark", "Pastel on dark"),
    ("solarized_dark", "Solarized Dark"),
    ("solarized_light", "Solarized Light"),
    ("sqlserver", "SQL Server"),
    ("terminal", "Terminal"),
    ("textmate", "TextMate"),
    ("tomorrow", "Tomorrow"),
    ("tomorrow_night", "Tomorrow Night"),
    ("tomorrow_night_blue", "Tomorrow Night Blue"),
    ("tomorrow_night_bright", "Tomorrow Night Bright"),
    ("tomorrow_night_eighties", "Tomorrow Night Eighties"),
    ("twilight", "Twilight"),
    ("vibrant_ink", "Vibrant Ink"),
    ("xcode", "XCode"),
]

MODE_CHOICES = [
    ("python", "Python"),
    ("css", "CSS"),
    ("javascript", "JavaScript"),
    ("html", "HTML"),
    ("markdown", "Markdown"),
    ("abap", "ABAP"),
    ("abc", "ABC"),
    ("actionscript", "ActionScript"),
    ("ada", "ADA"),
    ("apache_conf", "Apache Conf"),
    ("applescript", "AppleScript"),
    ("asciidoc", "AsciiDoc"),
    ("assembly_x86", "Assembly x86"),
    ("autohotkey", "AutoHotkey"),
    ("batchfile", "BatchFile"),
    ("c9search", "C9Search"),
    ("c_cpp", "C/C++"),
    ("cirru", "Cirru"),
    ("clojure", "Clojure"),
    ("cobol", "Cobol"),
    ("coffee", "CoffeeScript"),
    ("coldfusion", "ColdFusion"),
    ("csharp", "C#"),
    ("css", "CSS"),
    ("curly", "Curly"),
    ("d", "D"),
    ("dart", "Dart"),
    ("diff", "Diff"),
    ("dockerfile", "Dockerfile"),
    ("dot", "Dot"),
    ("drools", "Drools"),
    ("edifact", "Edifact"),
    ("eiffel", "Eiffel"),
    ("ejs", "EJS"),
    ("elixir", "Elixir"),
    ("elm", "Elm"),
    ("erlang", "Erlang"),
    ("forth", "Forth"),
    ("fortran", "Fortran"),
    ("ftl", "FreeMarker"),
    ("gcode", "Gcode"),
    ("gherkin", "Gherkin"),
    ("gitignore", "Gitignore"),
    ("glsl", "Glsl"),
    ("golang", "Go"),
    ("groovy", "Groovy"),
    ("haml", "HAML"),
    ("handlebars", "Handlebars"),
    ("haskell", "Haskell"),
    ("haxe", "Haxe"),
    ("html", "HTML"),
    ("html_elixir", "HTML (Elixir)"),
    ("html_ruby", "HTML (Ruby)"),
    ("ini", "INI"),
    ("io", "Io"),
    ("jack", "Jack"),
    ("jade", "Jade"),
    ("java", "Java"),
    ("javascript", "JavaScript"),
    ("json", "JSON"),
    ("jsoniq", "JSONiq"),
    ("jsp", "JSP"),
    ("jsx", "JSX"),
    ("julia", "Julia"),
    ("kotlin", "Kotlin"),
    ("latex", "LaTeX"),
    ("less", "LESS"),
    ("liquid", "Liquid"),
    ("lisp", "Lisp"),
    ("livescript", "LiveScript"),
    ("logiql", "LogiQL"),
    ("lsl", "LSL"),
    ("lua", "Lua"),
    ("luapage", "LuaPage"),
    ("lucene", "Lucene"),
    ("makefile", "Makefile"),
    ("markdown", "Markdown"),
    ("mask", "Mask"),
    ("matlab", "MATLAB"),
    ("maze", "Maze"),
    ("mel", "MEL"),
    ("mips", "MIPS"),
    ("mushcode", "MUSHCode"),
    ("mysql", "MySQL"),
    ("nix", "Nix"),
    ("nsis", "NSIS"),
    ("objectivec", "Objective-C"),
    ("ocaml", "OCaml"),
    ("pascal", "Pascal"),
    ("perl", "Perl"),
    ("pgsql", "pgSQL"),
    ("php", "PHP"),
    ("plain_text", "Plain Text"),
    ("powershell", "Powershell"),
    ("praat", "Praat"),
    ("prolog", "Prolog"),
    ("properties", "Properties"),
    ("protobuf", "Protobuf"),
    ("python", "Python"),
    ("r", "R"),
    ("razor", "Razor"),
    ("rdoc", "RDoc"),
    ("rhtml", "RHTML"),
    ("rst", "reStructuredText"),
    ("ruby", "Ruby"),
    ("rust", "Rust"),
    ("sass", "Sass"),
    ("scad", "SCAD"),
    ("scala", "Scala"),
    ("scheme", "Scheme"),
    ("scss", "SCSS"),
    ("sh", "SH"),
    ("sjs", "SJS"),
    ("smarty", "Smarty"),
    ("snippets", "Snippets"),
    ("soy_template", "Soy Template"),
    ("space", "Space"),
    ("sql", "SQL"),
    ("sqlserver", "SQL Server"),
    ("stylus", "Stylus"),
    ("svg", "SVG"),
    ("swift", "Swift"),
    ("tcl", "TCL"),
    ("tex", "TeX"),
    ("text", "Text"),
    ("textile", "Textile"),
    ("toml", "TOML"),
    ("tsx", "TSX"),
    ("twig", "Twig"),
    ("typescript", "TypeScript"),
    ("vala", "Vala"),
    ("vbscript", "VBScript"),
    ("velocity", "Velocity"),
    ("verilog", "Verilog"),
    ("vhdl", "VHDL"),
    ("wollok", "Wollok"),
    ("xml", "XML"),
    ("xquery", "XQuery"),
    ("yaml", "YAML"),
]


class EditorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    default_theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="github")
    default_mode = models.CharField(max_length=50, choices=MODE_CHOICES, default="html")
    default_editor_css = models.TextField(
        default="""#editor { 
        width: 100%; 
        height: 500px;
    }
    """
    )
    enable_snippets = models.BooleanField(default=False)


class EditorModeProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="mode_profiles")
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="github")
    editor_css = models.TextField(null=True, blank=True,
        default="""#editor { 
        width: 100%; 
        height: 500px;
    }
    """
    )


class EditorSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    mode = models.CharField(
        max_length=50, choices=MODE_CHOICES, default="html"
    )
    tags = TaggableManager(blank=True)
    snippet = models.TextField()
    public = models.BooleanField(default=False)
