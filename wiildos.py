#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Wiildos Packages Health Status Report Generator
#
# Copyright © 2013-2014 Andrea Colangelo <warp10@debian.org>
#
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. The full text of the license is available at:
# http://www.wtfpl.net/txt/copying/


import psycopg2
import datetime
import HTML


WIILDOS_SRC_PKGS_LIST = ('python-whiteboard', 'curtain', 'spotlighter',
                         'ardesia', 'epoptes', 'cellwriter', 'gnome-orca',
                         'gpicview', 'xournal', 'dia', 'inkscape', 'librecad',
                         'pinta', 'scribus', 'geany', 'scratch', 'kicad',
                         'osmo', 'pdfmod', 'freeplane', 'fbreader',
                         'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra',
                         'tuxmath', 'wxmaxima', 'lybniz', 'celestia',
                         'chemtool', 'gperiodic', 'stellarium',
                         'gnome-chemistry-utils', 'gcompris', 'jclic',
                         'numptyphysics', 'pingus', 'musescore', 'marble',
                         'florence')
UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'
REPORT = "/home/groups/ubuntu-dev/htdocs/ubuntu-it/report.html"
TIMESTAMP = datetime.datetime.utcnow().strftime("%A, %d %B %Y, %H:%M UTC")


def make_debian_links(pkg, version):
    pts_base = "http://packages.qa.debian.org/"
    bts_base = "http://bugs.debian.org/cgi-bin/pkgreport.cgi?src="
    deb_buildd_base = "https://buildd.debian.org/status/logs.php?arch=&pkg="

    pts = HTML.link('PTS', pts_base + pkg)
    bts = HTML.link('BTS', bts_base + pkg)
    deb_buildd = HTML.link('Buildd', deb_buildd_base + pkg)

    return " ".join((pts, bts, deb_buildd))


def make_ubuntu_links(pkg, version):
    puc_base = "http://packages.ubuntu.com/search?searchon=sourcenames&keywords="
    lp_base = "https://launchpad.net/ubuntu/+source/"
    ubu_bugs_base = "https://launchpad.net/ubuntu/+source/%s/+bugs"
    ubu_buildd_base = "https://launchpad.net/ubuntu/+source/%s/%s"

    puc = HTML.link('packages.u.c.', puc_base + pkg)
    lp = HTML.link('LP', lp_base + pkg)
    ubu_bugs = HTML.link('Bugs', ubu_bugs_base % pkg)
    ubu_buildd = HTML.link('Buildd', ubu_buildd_base % (pkg, version))

    return " ".join((puc, lp, ubu_bugs, ubu_buildd))


def write_header():
    header = """<!DOCTYPE html>
<html>
<head>
        <meta http-equiv="Content-Type" content="text/html;charset=utf-8" >
        <title>Wiildos Packages Health Status Monitor</title>
</head>
<body>
        <h1> Wiildos Packages Health Status</h1>
        <p> Report generated: <b>%s</b></p>""" % TIMESTAMP
    write_to_file(header, 'w+')


def write_footer():
    footer = """</br>
<p> Wiildos Packages Health Status Report Generator is Copyright © 2013-2014 \
Andrea Colangelo <warp10@debian.org></br>
<a href="http://ubuntu-dev.alioth.debian.org/ubuntu-it/wiildos.py"> \
Source code</a> is available, patches are welcome.
</body>
</html>
"""
    write_to_file(footer, 'a')


def write_to_file(text, mode):
    with open(REPORT, mode) as f:
        f.write(text)


def write_table(title, data):
    output = "<h1>" + title + "</h1>"
    table = HTML.Table(header_row=['Source package', 'Ubuntu', 'Debian',
                                   'Upstream', 'Status', 'Debian Links',
                                   'Ubuntu Links'])
    for item in data:
        table.rows.append(make_row(item))
    output += str(table)
    output += ("<p>")
    write_to_file(output, 'a')


def make_row(item):
    for key, value in item.items():
        exec("%s = '%s'" % (key, value))
    deb_links = make_debian_links(source, deb_version)
    ubu_links = make_ubuntu_links(source, ubu_version)
    if homepage:
        source= """<a href="%s">%s</a>""" % (homepage, source)
    return source, ubu_version, deb_version, upstream_version, \
           upstream_status, deb_links, ubu_links


if __name__ == "__main__":
    conn = psycopg2.connect("service=udd")
    cursor = conn.cursor()

    up_to_date = []
    newer_version_available = []
    other = []

    for src_pkg in WIILDOS_SRC_PKGS_LIST:
        query = "SELECT DISTINCT sources.homepage, ubuntu_sources.source, \
                 ubuntu_sources.version, sources.version, \
                 upstream.upstream_version, upstream.status \
                 FROM ubuntu_sources LEFT OUTER JOIN sources \
                 ON ubuntu_sources.source=sources.source LEFT OUTER JOIN \
                 upstream ON sources.source=upstream.source \
                 WHERE ubuntu_sources.source='" + src_pkg + \
                 "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + \
                 "' AND sources.release='" + DEBIAN_RELEASE + "';"
        cursor.execute(query)

        keys = ["homepage", "source", "ubu_version", "deb_version",
                "upstream_version", "upstream_status"]
        for row in cursor.fetchall():  # returns a list of tuples of strings, one tuple per match
            item = dict(zip(keys, row))
            if item["upstream_status"] == 'up to date':
                up_to_date.append(item)
            elif item["upstream_status"] == 'Newer version available':
                newer_version_available.append(item)
            else:
                other.append(item)

    write_header()

    write_table("Packages with issues:", other)
    write_table("Newer upstream version available:", newer_version_available)
    write_table("Upstream up to date:", up_to_date)

    write_footer()
