import os
import re
import sys
from cgi import escape

ROOT = "/srv/home/users/warp10/wiildos"

# --------------------------------------------------------------------------- #
# Comments handling
# --------------------------------------------------------------------------- #

def comments_file():
    """Return the location of the comments."""
    return "%s/comments.txt" % ROOT

def get_comments():
    """Extract the comments from file, and return a dictionary
        containing comments corresponding to packages"""
    comments = {}

    with open(comments_file(), "r") as file_comments:
        # fcntl.flock(file_comments, fcntl.LOCK_SH)
        for line in file_comments:
            package, comment = line.rstrip("\n").split(": ", 1)
            comments[package] = comment

    return comments

def add_comment(package, comment):
    """Add a comment to the comments file"""
    with open(comments_file(), "a") as file_comments:
        # fcntl.flock(file_comments, fcntl.LOCK_EX)
        the_comment = comment.replace("\n", " ")
        the_comment = escape(the_comment[:100], quote=True)
        file_comments.write("%s: %s\n" % (package, the_comment))
    os.system("wiildos.py")

def remove_old_comments(status_file, merges):
    """Remove old comments from the comments file using
       component's existing status file and merges"""
    if not os.path.exists(status_file):
        return

    packages = [ m[2] for m in merges ]
    toremove = []

    with open(status_file, "r") as file_status:
        for line in file_status:
            package = line.split(" ")[0]
            if package not in packages:
                toremove.append(package)

    with open(comments_file(), "a+") as file_comments:
        # fcntl.flock(file_comments, fcntl.LOCK_EX)

        new_lines = []
        for line in file_comments:
            if line.split(": ", 1)[0] not in toremove:
                new_lines.append(line)

        file_comments.truncate(0)

        for line in new_lines:
            file_comments.write(line)

def gen_buglink_from_comment(comment):
    """Return an HTML formatted Debian/Ubuntu bug link from comment"""
    debian = re.search(".*bug #([0-9]{1,}).*", comment, re.I)
    ubuntu = re.search(".*bug LP#([0-9]{1,}).*", comment, re.I)

    html = ""
    if debian:
        html += "<img src=\".img/debian.png\" alt=\"Debian\" />"
        html += "<a href=\"http://bugs.debian.org/%s\">#%s</a>" \
            % (debian.group(1), debian.group(1))
    elif ubuntu:
        html += "<img src=\".img/ubuntu.png\" alt=\"Ubuntu\" />"
        html += "<a href=\"https://launchpad.net/bugs/%s\">#%s</a>" \
            % (ubuntu.group(1), ubuntu.group(1))
    else:
        html += "&nbsp;"

    return html
