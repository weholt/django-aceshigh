from aceshigh.common import (
    FONT_SIZE_CHOICES,
    KEYBINDIMG_CHOICES,
    MODE_CHOICES,
    THEME_CHOICES,
)
from aceshigh.fields import AceEditorField
from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class EditorProfile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    default_theme = models.CharField(
        max_length=50, choices=THEME_CHOICES, default="github"
    )
    default_mode = models.CharField(max_length=50, choices=MODE_CHOICES, default="html")
    default_editor_css = models.CharField(
        max_length=200, default="width: 100%;  height: 500px;", null=True, blank=True
    )
    keybinding = models.CharField(
        max_length=50, choices=KEYBINDIMG_CHOICES, default="ace/keyboard/vscode"
    )
    enable_snippets = models.BooleanField(default=False)
    enable_basic_autocompletion = models.BooleanField(default=False)
    enable_live_atocompletion = models.BooleanField(default=False)
    show_gutter = models.BooleanField(default=False)
    show_line_numbers = models.BooleanField(default=False)


class EditorModeProfile(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="mode_profiles"
    )
    mode = models.CharField(max_length=50, choices=MODE_CHOICES)
    font_size = models.IntegerField(choices=FONT_SIZE_CHOICES, default=14)
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default="github")
    keybinding = models.CharField(
        max_length=50, choices=KEYBINDIMG_CHOICES, default="ace/keyboard/vscode"
    )
    editor_css = models.CharField(
        max_length=200, default="width: 100%;  height: 500px;", null=True, blank=True
    )
    enable_basic_autocompletion = models.BooleanField(default=False)
    enable_snippets = models.BooleanField(default=False)
    enable_live_atocompletion = models.BooleanField(default=False)
    show_gutter = models.BooleanField(default=False)
    show_line_numbers = models.BooleanField(default=False)


class EditorSnippet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    mode = models.CharField(max_length=50, choices=MODE_CHOICES, default="html")
    tags = TaggableManager(blank=True)
    snippet = AceEditorField()
    public = models.BooleanField(default=False)

    def tags_list(self):
        return list(self.tags.names())


#   selectionStyle: 'line',// "line"|"text"
#   highlightActiveLine: true, // boolean
#   highlightSelectedWord: true, // boolean
#   readOnly: false, // boolean: true if read only
#   cursorStyle: 'ace', // "ace"|"slim"|"smooth"|"wide"
#   mergeUndoDeltas: true, // false|true|"always"
#   behavioursEnabled: true, // boolean: true if enable custom behaviours
#   wrapBehavioursEnabled: true, // boolean
#   autoScrollEditorIntoView: undefined, // boolean: this is needed if editor is inside scrollable page
#   keyboardHandler: null, // function: handle custom keyboard events

#   // renderer options
#   animatedScroll: false, // boolean: true if scroll should be animated
#   displayIndentGuides: false, // boolean: true if the indent should be shown. See 'showInvisibles'
#   showInvisibles: false, // boolean -> displayIndentGuides: true if show the invisible tabs/spaces in indents
#   showPrintMargin: true, // boolean: true if show the vertical print margin
#   printMarginColumn: 80, // number: number of columns for vertical print margin
#   printMargin: undefined, // boolean | number: showPrintMargin | printMarginColumn
#   showGutter: true, // boolean: true if show line gutter
#   fadeFoldWidgets: false, // boolean: true if the fold lines should be faded
#   showFoldWidgets: true, // boolean: true if the fold lines should be shown ?
#   showLineNumbers: true,
#   highlightGutterLine: false, // boolean: true if the gutter line should be highlighted
#   hScrollBarAlwaysVisible: false, // boolean: true if the horizontal scroll bar should be shown regardless
#   vScrollBarAlwaysVisible: false, // boolean: true if the vertical scroll bar should be shown regardless
#   fontSize: 12, // number | string: set the font size to this many pixels
#   fontFamily: undefined, // string: set the font-family css value
#   maxLines: undefined, // number: set the maximum lines possible. This will make the editor height changes
#   minLines: undefined, // number: set the minimum lines possible. This will make the editor height changes
#   maxPixelHeight: 0, // number -> maxLines: set the maximum height in pixel, when 'maxLines' is defined.
#   scrollPastEnd: 0, // number -> !maxLines: if positive, user can scroll pass the last line and go n * editorHeight more distance
#   fixedWidthGutter: false, // boolean: true if the gutter should be fixed width
#   theme: 'ace/theme/textmate', // theme string from ace/theme or custom?

#   // mouseHandler options
#   scrollSpeed: 2, // number: the scroll speed index
#   dragDelay: 0, // number: the drag delay before drag starts. it's 150ms for mac by default
#   dragEnabled: true, // boolean: enable dragging
#   focusTimout: 0, // number: the focus delay before focus starts.
#   tooltipFollowsMouse: true, // boolean: true if the gutter tooltip should follow mouse

#   // session options
#   firstLineNumber: 1, // number: the line number in first line
#   overwrite: false, // boolean
#   newLineMode: 'auto', // "auto" | "unix" | "windows"
#   useWorker: true, // boolean: true if use web worker for loading scripts
#   useSoftTabs: true, // boolean: true if we want to use spaces than tabs
#   tabSize: 4, // number
#   wrap: false, // boolean | string | number: true/'free' means wrap instead of horizontal scroll, false/'off' means horizontal scroll instead of wrap, and number means number of column before wrap. -1 means wrap at print margin
#   indentedSoftWrap: true, // boolean
#   foldStyle: 'markbegin',
