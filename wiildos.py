#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_src_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')
UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'

up_to_date = []
newer_version_available = []
other=[]

f = open('report.html', 'w+')


def print_header():
    pass

def print_row():
    pass

def print_footer():
    pass

for src_pkg in wiildos_src_pkgs_list:
    query = "SELECT DISTINCT ubuntu_sources.source, ubuntu_sources.version, sources.version, upstream.upstream_version, upstream.status FROM ubuntu_sources LEFT OUTER JOIN sources ON ubuntu_sources.source=sources.source LEFT OUTER JOIN upstream ON sources.source=upstream.source WHERE ubuntu_sources.source='" + src_pkg + "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + "' AND sources.release='" + DEBIAN_RELEASE + "';"
    cursor.execute(query)

    for row in cursor.fetchall():  #fetchall() returns a list of tuples of strings, one tuple per match
        if row[-1] == 'up to date':
            up_to_date.append(row)
        elif row[-1] == 'Newer version available':
            newer_version_available.append(row)
        else:
            other.append(row)

print_header()

for row in other:
    print_row()
for row in newer_version_available:
    print_row()
for row in other:
    print_row()

print_footer()
