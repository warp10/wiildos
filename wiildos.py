#!/usr/bin/python

import psycopg2

conn = psycopg2.connect("service=udd")
cursor = conn.cursor()

wiildos_src_pkgs_list = ('python-whiteboard', 'curtain', 'spotlighter', 'ardesia', 'epoptes', 'cellwriter', 'gnome-orca', 'gpicview', 'xournal', 'dia', 'inkscape', 'librecad', 'pinta', 'scribus', 'geany', 'scratch', 'kicad', 'osmo', 'pdfmod', 'freeplane', 'fbreader', 'ocrfeeder', 'tuxpaint', 'collatinus', 'geogebra', 'tuxmath', 'wxmaxima', 'lybniz', 'celestia', 'chemtool', 'gperiodic', 'stellarium', 'gnome-chemistry-utils', 'gcompris', 'jclic', 'numptyphysics', 'pingus', 'musescore', 'marble', 'florence')

UBUNTU_RELEASE = 'trusty'
DEBIAN_RELEASE = 'sid'

for src_pkg in wiildos_src_pkgs_list:
    query = "SELECT ubuntu_sources.version, sources.version, upstream.upstream_version, ubuntu_sources.bin, upstream.status FROM ubuntu_sources LEFT OUTER JOIN sources ON ubuntu_sources.source=sources.source LEFT OUTER JOIN upstream ON sources.source=upstream.source WHERE ubuntu_sources.source='" + src_pkg + "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + "' AND sources.release='" + DEBIAN_RELEASE + "';"
    cursor.execute(query)

    print "src_pkg, ubuntu_version, debian_version, upstream_version, ubuntu_pkg_list, upstream_status"
    for row in cursor.fetchall():  #fetchall() returns a list of tuples of strings, one tuple per match
        ubuntu_version, debian_version, upstream_version, ubuntu_pkg_list, upstream_status = row
        ubuntu_pkg_list = tuple(ubuntu_pkg_list.split(", ")) #ubuntu_pkg_list  is a comma-separated string of pkg names"

        print "=" * 80
        print "SOURCE PACKAGE: ", src_pkg
        print "src_pkg, ubuntu_version, debian_version, upstream_version, upstream_status"
        print src_pkg, ubuntu_version, debian_version, upstream_version, upstream_status

        for pkg in ubuntu_pkg_list:
            query = "SELECT ubuntu_packages.architecture FROM ubuntu_packages WHERE ubuntu_packages.source='" + pkg + "' AND ubuntu_packages.version='" + ubuntu_version + "' AND ubuntu_packages.release='" + UBUNTU_RELEASE + "';"
            cursor.execute(query)
            for row in cursor.fetchall():
                ubuntu_pkg_architecture = row
            print "pkg", "ubuntu_architecture"
            print pkg, ubuntu_pkg_architecture

