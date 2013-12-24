#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_src_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')
UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'

for src_pkg in wiildos_src_pkgs_list:
    query = "SELECT DISTINCT ubuntu_sources.version, sources.version, upstream.upstream_version, upstream.status FROM ubuntu_sources LEFT OUTER JOIN sources ON ubuntu_sources.source=sources.source LEFT OUTER JOIN upstream ON sources.source=upstream.source WHERE ubuntu_sources.source='" + src_pkg + "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + "' AND sources.release='" + DEBIAN_RELEASE + "';"
    cursor.execute(query)

    print "=" * 80
    print "SOURCE PACKAGE: ", src_pkg
    for row in cursor.fetchall():  #fetchall() returns a list of tuples of strings, one tuple per match
        src_ubuntu_version, src_debian_version, src_upstream_version, src_upstream_status = row
        print "src_pkg, src_ubuntu_version, debian_version, upstream_version, upstream_status"
        print src_pkg, src_ubuntu_version, src_debian_version, src_upstream_version, src_upstream_status
