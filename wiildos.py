#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')

UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'

for src_pkg in wiildos_pkgs_list:
    query = "SELECT ubuntu_sources.version, sources.version, upstream.upstream_version, ubuntu_sources.bin, upstream.status FROM ubuntu_sources LEFT OUTER JOIN sources ON ubuntu_sources.source=sources.source LEFT OUTER JOIN upstream ON sources.source=upstream.source WHERE ubuntu_sources.source='" + src_pkg + "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + "' AND sources.release='" + DEBIAN_RELEASE + "';"
    cursor.execute(query)

    print "pkg_name, ubuntu_version, debian_version, upstream_version, ubuntu_bin, upstream_status"
    for row in cursor.fetchall():
        ubuntu_version, debian_version, upstream_version, ubuntu_bin, upstream_status = row
        print src_pkg, ubuntu_version, debian_version, upstream_version, ubuntu_bin, upstream_status

