#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')

for pkg in wiildos_pkgs_list:
    query = "SELECT ubuntu_sources.version, sources.version, upstream.upstream_version FROM ubuntu_sources INNER JOIN sources ON ubuntu_sources.source=sources.source INNER JOIN upstream ON ubuntu_sources.source=upstream.source WHERE ubuntu_sources.source='" + pkg + "' AND ubuntu_sources.release='trusty' AND sources.release='sid';"
    cursor.execute(query)

    print "pkg, ubuntu, debian, upstream"
    for row in cursor.fetchall():
        ubuntu_version, debian_version, upstream_version = row
        print pkg, ubuntu_version, debian_version, upstream_version

#SELECT architecture FROM packages WHERE source='scribus' AND version='1.4.2.dfsg+r18267-1' AND architecture IN ('amd64', 'i386') AND release='sid';
# Query direttamente su packages?
