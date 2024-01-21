import sphinx
from pygments.token import *
from pygments.style import Style

# Pygments Token/CSS Mappings: https://gist.github.com/TDKorn/f3a7fc98503eccb602ae7af428c0b981

# ====  GitHub PrettyLights - color variable -> hexcode mapping ====
# ~~~~  See ./_static/starry_night.css  ~~~~

pl = {
    "syntax-comment": "#8b949e",
    "syntax-constant": "#79c0ff",
    "syntax-entity": "#d2a8ff",
    "syntax-storage-modifier-import": "#c9d1d9",
    "syntax-entity-tag": "#7ee787",
    "syntax-keyword": "#ff7b72",
    "syntax-string": "#a5d6ff",
    "syntax-variable": "#ffa657",
    "syntax-brackethighlighter-unmatched": "#f85149",
    "syntax-invalid-illegal-text": "#f0f6fc",
    "syntax-invalid-illegal-bg": "#8e1519",
    "syntax-carriage-return-text": "#f0f6fc",
    "syntax-carriage-return-bg": "#b62324",
    "syntax-string-regexp": "#7ee787",
    "syntax-markup-list": "#f2cc60",
    "syntax-markup-heading": "#1f6feb",
    "syntax-markup-italic": "#c9d1d9",
    "syntax-markup-bold": "#e6edf3",
    "syntax-markup-deleted-text": "#ffdcd7",
    "syntax-markup-deleted-bg": "#67060c",
    "syntax-markup-inserted-text": "#aff5b4",
    "syntax-markup-inserted-bg": "#033a16",
    "syntax-markup-changed-text": "#ffdfb6",
    "syntax-markup-changed-bg": "#5a1e02",
    "syntax-markup-ignored-text": "#c9d1d9",
    "syntax-markup-ignored-bg": "#1158c7",
    "syntax-meta-diff-range": "#d2a8ff",
    "syntax-brackethighlighter-angle": "#8b949e",
    "syntax-sublimelinter-gutter-mark": "#484f58",
    "syntax-constant-other-reference-link": "#a5d6ff",
}


class TDKStyle(Style):
    """An attempt at creating a Pygments style similar to GitHub's pretty lights dark theme"""

    background_color = "#0d1117"
    default_style = ''

    styles = {
        Whitespace: "#f0f6fc",

        Comment: pl["syntax-comment"],
        Comment.Hashbang: pl["syntax-comment"],
        Comment.Multiline: pl["syntax-comment"],
        Comment.Preproc: pl["syntax-comment"],
        Comment.Single: pl["syntax-comment"],
        Comment.Special: pl["syntax-comment"],

        Generic: "#f0f6fc",
        Generic.Deleted: "#8b080b",
        Generic.Emph: "#f8f8f2 underline",
        Generic.Error: "#f8f8f2",
        Generic.Heading: "#f8f8f2 bold",
        Generic.Inserted: "#f8f8f2 bold",
        Generic.Output: "#adaeb6",
        Generic.Prompt: "#f8f8f2",
        Generic.Strong: "#f8f8f2",
        Generic.Subheading: "#f8f8f2 bold",
        Generic.Traceback: "#f8f8f2",
        Error: "#f8f8f2",

        Keyword: pl["syntax-keyword"],
        Keyword.Constant: pl["syntax-constant"],  # Ex. None
        Keyword.Declaration: pl["syntax-keyword"],
        Keyword.Namespace: pl["syntax-keyword"],
        Keyword.Pseudo: pl["syntax-entity"],
        Keyword.Reserved: pl["syntax-constant"],
        Keyword.Type: pl["syntax-constant"],

        Literal: "#f8f8f2",
        Literal.Date: "#f8f8f2",
        Literal.String.Affix: "#f8f8f2",
        Literal.String.Doc: "#f8f8f2",
        Literal.String.Double: "#f8f8f2",
        Literal.String.Interpol: "#f8f8f2",
        Literal.String.Single: "#f8f8f2",

        Name: pl["syntax-markup-bold"],
        Name.Variable: pl["syntax-markup-bold"],
        Name.Attribute: pl["syntax-markup-bold"],
        Name.Builtin.Pseudo: pl["syntax-markup-bold"],  # Ex. self
        Name.Builtin: pl["syntax-entity"],  # Ex. print()
        Name.Class: pl["syntax-variable"],
        Name.Constant: pl["syntax-constant"],
        Name.Decorator: pl["syntax-entity"],
        Name.Entity: pl["syntax-entity"],
        Name.Exception: pl["syntax-variable"],
        Name.Function: pl["syntax-entity"],
        Name.Function.Magic: pl["syntax-entity"],
        # Name.Label: "#8be9fd italic",
        Name.Namespace: pl["syntax-markup-bold"],
        Name.Other: pl["syntax-markup-bold"],
        # Name.Other: pl["syntax-variable"],
        # Name.Tag: "#ff79c6",
        Name.Variable.Class: pl["syntax-variable"],
        Name.Variable.Global: pl["syntax-variable"],
        Name.Variable.Instance: pl["syntax-markup-bold"],
        Name.Variable.Magic: pl["syntax-markup-bold"],

        Number: pl["syntax-constant"],
        Number.Bin: pl["syntax-constant"],
        Number.Float: pl["syntax-constant"],
        Number.Hex: pl["syntax-constant"],
        Number.Integer: pl["syntax-constant"],
        Number.Integer.Long: pl["syntax-constant"],
        Number.Oct: pl["syntax-constant"],
        Operator: pl["syntax-constant"],
        Operator.Word: pl["syntax-constant"],

        # Other: "#f8f8f2",
        Other.Constant: pl["syntax-constant"],
        Punctuation: "#f8f8f2",
        Punctuation.Definition.Comment: pl["syntax-comment"],
        String: pl["syntax-string"],
        String.Backtick: pl["syntax-string"],
        String.Char: pl["syntax-string"],
        String.Comment: pl["syntax-comment"],
        String.Doc: pl["syntax-string"],
        String.Double: pl["syntax-string"],
        String.Escape: pl["syntax-string"],
        String.Heredoc: pl["syntax-string"],
        String.Interpol: pl["syntax-string"],
        String.Other: pl["syntax-string"],
        String.Regex: pl["syntax-string"],
        String.Single: pl["syntax-string"],
        String.Symbol: pl["syntax-string"],
        Text: pl["syntax-markup-bold"],
    }


def setup(app):
    app.config.pygments_style = 'sphinx_github_style.TDKStyle'
    app.add_css_file('github_style.css')
    return {'version': sphinx.__display_version__, 'parallel_read_safe': True}
