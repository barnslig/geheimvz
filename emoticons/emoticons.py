from django.templatetags.static import static

emoticons = [
    "arrow",
    "biggrin",
    "confused",
    "cool",
    "cry",
    "eek",
    "evil",
    "exclaim",
    "geek",
    "idea",
    "lol",
    "mad",
    "mrgreen",
    "neutral",
    "question",
    "razz",
    "redface",
    "rolleyes",
    "sad",
    "smile",
    "surprised",
    "twisted",
    "ugeek",
    "wink",
]

emoticons = [(f":{s}:", static(f"emoticons/icon_{s}.gif")) for s in emoticons]
