#########################################################

from utils.misc import dir_listing_as_list, read_string_from_file, write_string_to_file, firstbetween
from os import stat

#########################################################

HTML_DIRS = [
    ".",
    "templates"
]

VERSIONED_FILES = [
    "static/css/staticpage.css",
    "static/css/dom.css",
    "static/css/system.css",
    "static/css/app.css",
    "static/css/board.css",

    "static/js/app.js",

    "static/clientjs/app.js",
    "static/clientjs/basicboard.js",
    "static/clientjs/board.js",
    "static/clientjs/client.js",
    "static/clientjs/connection.js",
    "static/clientjs/dom.js",
    "static/clientjs/forumgame.js",
    "static/clientjs/org.transcrypt.__runtime__.js",
    "static/clientjs/schema.js",
    "static/clientjs/system.js",
    "static/clientjs/utils.js",
    "static/clientjs/widgets.js",

    "static/js/dom.js",
    "static/js/lichess.js"
]

VERSION_DELIMS = [
    {
        "find": '<link rel="stylesheet"',
        "left": 'href="',
        "right": '"'
    },
    {
        "find": '<script src="',        
        "left": 'src="',
        "right": '"'
    }
]

#########################################################

print("versioning assets")

allhtmls = []

for htmldir in HTML_DIRS:
    files = dir_listing_as_list(htmldir)
    for file in files:
        if file["ext"] == "html":
            allhtmls.append([htmldir, file])

for file in allhtmls:
    path = file[0] + "/" + file[1]["name"]
    content = read_string_from_file(path, "")
    newlines = []
    changed = False
    for line in content.splitlines():
        newline = line        
        for delim in VERSION_DELIMS:
            if delim["find"] in line:                
                fullname = firstbetween(line, delim["left"], delim["right"])
                propername = firstbetween(fullname, '', '?')
                print("examining", propername)
                if propername in VERSIONED_FILES:
                    print("*", propername, "is versioned")
                    mtime = "{:.0f}".format(stat(propername).st_mtime)
                    newfullname = propername + "?ver=" + mtime                    
                    newline = line.replace(fullname, newfullname)                
                    if not ( newline == line ):
                        print("-->", newfullname, path)
                        changed = True
        newlines.append(newline)
    if changed:
        newcontent = "\n".join(newlines)
        print("------\nupdating {}\n------".format(path))
        write_string_to_file(path, newcontent)