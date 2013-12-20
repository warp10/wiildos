#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')

for pkg in wiildos_pkgs_list:

    query = "SELECT ubuntu_sources.source, ubuntu_sources.version, sources.version FROM ubuntu_sources INNER JOIN sources ON ubuntu_sources.source=sources.source WHERE ubuntu_sources.source='" + pkg + "' AND ubuntu_sources.release='trusty' AND sources.release='sid';"
    cursor.execute(query)
    print "pkg, ubuntu_version, debian_version"
    for i in  cursor.fetchall():
        print i



