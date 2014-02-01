#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# WiildOS Packages Health Status Report Generator
#
# Copyright © 2013-2014 Andrea Colangelo <warp10@debian.org>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. The full text of the license is available at:
# http://www.wtfpl.net/txt/copying/


import psycopg2
from datetime import datetime
from subprocess import call
from sys import exit
import HTML


UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'

REPORT = "/home/groups/ubuntu-dev/htdocs/wiildos/report.html"

TIMESTAMP = datetime.utcnow().strftime("%A, %d %B %Y, %H:%M UTC")

UBU_LT_DEB_COLOR = "FF4444"  # light red
UBU_GT_DEB_COLOR = "6571DE"  # light blue
UBU_EQ_DEB_COLOR = "FFFFFF"  # try guess
MIS_IN_DEB_COLOR = "F9F940"  # light yellow

TODO_PACKAGES = {
"sankore": "<a href=\"http://open-sankore.org\">http://open-sankore.org</a>, <a href=\"http://bugs.debian.org/673322\">#673322</a>, Contatto: Claudio Valerio &lt;<a href=\"mailto:claudio@open-sankore.org\">claudio@open-sankore.org</a>&gt;",
"eviacam": "<a href=\"http://eviacam.sourceforge.net/\">http://eviacam.sourceforge.net</a>",
"easystroke": "<a href=\"http://easystroke.sourceforge.net/\">http://easystroke.sourceforge.net</a>",
"pencil2d": "<a href=\"http://www.pencil2d.org\">http://www.pencil2d.org</a>",
"wiidynamic": "",
"omnitux": "<a href=\"http://omnitux.sourceforge.net/\">http://omnitux.sourceforge.net</a>",
"gspeech": "<a href=\"https://github.com/tuxmouraille/MesApps\">https://github.com/tuxmouraille/MesApps</a>",
"vue": "<a href=\"http://vue.tufts.edu/\">http://vue.tufts.edu</a>",
"educazionik": "",
"vox-launcher": "<a href=\"http://code.google.com/p/vox-launcher/\">http://code.google.com/p/vox-launcher</a>"}

OTHER_PACKAGES = {
"dasher": "bugged, many deps, http://ftp.gnome.org/pub/GNOME/sources/dasher/",
"wiican": "RM, https://launchpad.net/wiican",
"simple-scan": "not considered for inclusion, https://launchpad.net/simple-scan",
"homebank": "not considered for inclusion, http://homebank.free.fr/",
"gvb": "not considered for inclusion, http://www.pietrobattiston.it",
"gbrainy": "not considered for inclusion,  https://live.gnome.org/gbrainy",
"virtual magnifying glass": "obsoleted by gnome-orca, http://magnifier.sourceforge.net/",
"xfce4-screenshooter": "http://goodies.xfce.org/projects/applications/xfce4-screenshooter",
"drawswf": "http://drawswf.sourceforge.net/",
"pydinamic": "https://bitbucket.org/zambu/pywiimote",
"osp-tracker": "http://www.cabrillo.edu/~dbrown/tracker/",
"xuggler": "http://www.xuggle.com/xuggler",
"gtk-recordmydesktop": "http://recordmydesktop.sourceforge.net/about.php"}

WIILDOS_SRC_PKGS_LIST = (
'python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes',
'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape',
'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod',
'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra',
'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic',
'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics',
'pingus', 'musescore', 'marble', 'florence', 'xinput-calibrator')


def make_debian_links(pkg, version):
    """Return a string containing debian links for a package"""
    pts_base = "http://packages.qa.debian.org/"
    bts_base = "http://bugs.debian.org/cgi-bin/pkgreport.cgi?src="
    deb_buildd_base = "https://buildd.debian.org/status/logs.php?arch=&amp;pkg="

    pts = HTML.link('PTS', pts_base + pkg)
    bts = HTML.link('BTS', bts_base + pkg)
    deb_buildd = HTML.link('Buildd', deb_buildd_base + pkg)

    return " ".join((pts, bts, deb_buildd))


def make_ubuntu_links(pkg, version):
    """Return a string containing ubuntu links for a package"""
    puc_base = "http://packages.ubuntu.com/search?searchon=sourcenames&amp;keywords="
    lp_base = "https://launchpad.net/ubuntu/+source/"
    ubu_bugs_base = "https://launchpad.net/ubuntu/+source/%s/+bugs"
    ubu_buildd_base = "https://launchpad.net/ubuntu/+source/%s/%s"

    puc = HTML.link('packages.u.c.', puc_base + pkg)
    lp = HTML.link('LP', lp_base + pkg)
    ubu_bugs = HTML.link('Bugs', ubu_bugs_base % pkg)
    ubu_buildd = HTML.link('Buildd', ubu_buildd_base % (pkg, version))

    return " ".join((puc, lp, ubu_bugs, ubu_buildd))


def write_header():
    """Write the report header to file"""
    header = """<!DOCTYPE html>
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>WiildOS Packages Health Status Report</title>
</head>
<body>
        <center><h1>WiildOS Packages Health Status</h1></center>
        <p> Report generated on: <b>%s</b><br>
        Ubuntu target release is: <b>%s</b><br>
        Debian target release is: <b>%s</b></p>
        """ % (TIMESTAMP, UBUNTU_RELEASE, DEBIAN_RELEASE)
    write_to_file(header, 'w+')


def write_footer():
    """Write the footer header to file"""
    footer = """<br>
<p> WiildOS Packages Health Status Report Generator is Copyright © 2013-2014 \
Andrea Colangelo &lt;warp10@debian.org&gt; and is released under the terms of \
the <a href="http://www.wtfpl.net/">WTFPL</a><br>
<a href="https://github.com/warp10/wiildos"> \
Source code</a> is available, patches are welcome.
</body>
</html>
"""
    write_to_file(footer, 'a')


def write_legend():
    """Write a legend explaining the meaning of the tables"""
    t1 = HTML.Table(header_row=["Legend"])
    t1.rows.append(HTML.TableRow(("Ubuntu version lower than Debian version",),
                                bgcolor=UBU_LT_DEB_COLOR))
    t1.rows.append(HTML.TableRow(("Ubuntu version greater than Debian version",),
                                bgcolor=UBU_GT_DEB_COLOR))
    t1.rows.append(HTML.TableRow(("Ubuntu version matches Debian version", ),
                                bgcolor=UBU_EQ_DEB_COLOR))
    t1.rows.append(HTML.TableRow(("Ubuntu package missing in Debian", ),
                                bgcolor=MIS_IN_DEB_COLOR))

    t2 = HTML.Table(header_row=["Status message", "Meaning"])
    t2.rows.append(("error", "The watchfile couldn't be parsed. Either the watchfile is wrong or upstream changed something."))
    t2.rows.append(("&lt;no message&gt;", "The watchfile is missing and couldnt' be checked."))
    t2.rows.append(("Debian version newer than remote site", "The watchfile is obsolete or not working and should be updated."))
    t2.rows.append(HTML.TableRow(("Newer version available <br> Up to date", "Self-explanatory.")))

    write_to_file(str(t1) + "<br>", 'a')
    write_to_file(str(t2) + "<br>", 'a')


def write_to_file(text, mode):
    """Actually write text to file"""
    with open(REPORT, mode) as f:
        f.write(text)


def query_udd(conn, query):
    """Actually execute a query on udd"""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


def write_table(title, data):
    """Write a table's items to file"""
    output = "<h1>" + title + "</h1>"
    table = HTML.Table(header_row=['Source package', 'Ubuntu', 'Debian',
                                   'Upstream', 'Status', 'Debian Links',
                                   'Ubuntu Links'])
    for item in data:
        table.rows.append(make_row(item))
    output += str(table)
    output += ("<br>")
    write_to_file(output, 'a')


def make_row(item):
    """Return the content of a table's row"""
    for key, value in item.items():  # FIXME: ugly
        if value:
            exec("%s = '%s'" % (key, value))
        else:
            exec("%s = None" % key)
    deb_links = make_debian_links(source, deb_version)
    ubu_links = make_ubuntu_links(source, ubu_version)
    if homepage:
        source = """<a href="%s">%s</a>""" % (homepage, source)
    if not deb_version:
        bgcolor = MIS_IN_DEB_COLOR
        deb_version = "MISSING"
        upstream_status = "MISSING IN DEBIAN"
    else:
    # the following if's are not'ed since dpkg return 0 when successful
        if not call(["dpkg", "--compare-versions", ubu_version, "gt",
                     deb_version]):
            bgcolor = UBU_GT_DEB_COLOR
        elif not call(["dpkg", "--compare-versions", ubu_version, "lt",
                       deb_version]):
            bgcolor = UBU_LT_DEB_COLOR
        else:
            bgcolor = UBU_EQ_DEB_COLOR
    return HTML.TableRow((source, ubu_version, deb_version, upstream_version,
        upstream_status, deb_links, ubu_links), bgcolor)


def write_other_pkgs_table(title, data):
    output = "<h2>%s</h2>" % title
    table = HTML.Table(header_row=["Software", "WNPP", "Notes"])
    for item in data:
        table.rows.append(HTML.TableRow(item))
    output += str(table)
    output += ("<br>")
    write_to_file(output, 'a')


def query_other_pkgs(conn, pkg_list):
    output = []

    for pkg in sorted(pkg_list.keys()):
        # FIXME: false positives
        query = "SELECT id, title FROM wnpp WHERE title ~ '%s';" % pkg
        keys = ["bug_number", "bug_title"]

        result = query_udd(conn, query)
        if result:
            for row in result:
                item = dict(zip(keys, row))
                link_text = "#%s, %s" % (item["bug_number"], item["bug_title"])
                link_anchor = "http://bugs.debian.org/%s" % item["bug_number"]
                link = HTML.link(link_text, link_anchor)
                output.append((pkg, link, pkg_list[pkg]))
        else:
            output.append((pkg, "", pkg_list[pkg]))
    return output


if __name__ == "__main__":
    up_to_date = []
    newer_version_available = []
    other = []

    try:
        conn = psycopg2.connect("service=udd")
    except:
        print "UDD accept connections from alioth.debian.org and \
people.debian.org only. This script is thought to be run on alioth."
        exit()

    for src_pkg in sorted(WIILDOS_SRC_PKGS_LIST):
        query = """SELECT DISTINCT s.homepage, u_s.source, u_s.version,
                s.version, u.upstream_version, u.status FROM ubuntu_sources u_s
                LEFT OUTER JOIN sources s ON u_s.source=s.source LEFT OUTER
                JOIN upstream u ON s.source=u.source WHERE u_s.source='%s' AND
                u_s.release='%s' AND (s.release IS NULL OR s.release='%s')
                """ % (src_pkg, UBUNTU_RELEASE, DEBIAN_RELEASE)
        keys = ["homepage", "source", "ubu_version", "deb_version",
                "upstream_version", "upstream_status"]

        for row in query_udd(conn, query):  # can return multiple rows per pkg
            item = dict(zip(keys, row))
            if item["upstream_status"] == 'up to date':
                up_to_date.append(item)
            elif item["upstream_status"] == 'Newer version available':
                newer_version_available.append(item)
            else:
                other.append(item)

    todo_packages = query_other_pkgs(conn, TODO_PACKAGES)
    other_packages = query_other_pkgs(conn, OTHER_PACKAGES)

    write_header()
    write_legend()
    write_table("Packages that may (or may not) have issues:", other)
    write_table("Newer upstream version available:", newer_version_available)
    write_table("Upstream up to date:", up_to_date)
    write_other_pkgs_table("Software to be packaged and uploaded to archive:",
                           todo_packages)
    write_other_pkgs_table("Software not considered for inclusion in WiildOS:",
                           other_packages)
    write_footer()
