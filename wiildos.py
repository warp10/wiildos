#!/usr/bin/python

import psycopg2
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
REPORT = "report.html"

def write_to_file(text, mode):
    with open(REPORT, mode) as f:
        f.write(text)


def write_header():
    header =  """<html>
<head>
        <title>Wiildos Packages Health Status Monitor</title>
</head>
<body>
        <h1> Wiildos Packages Health Status</h1>"""
    write_to_file(header, 'w+')


def write_footer():
    footer="""
</body>
</html>
"""
    write_to_file(footer, 'a')


def write_table(title, data):
    output = "<h1>" + title + "</h1>"
    output += HTML.table(data,
                         header_row=['Source package', 'Ubuntu', 'Debian',
                                     'Upstream', 'Status'])
    output += ("<p>")

    write_to_file(output, 'a')

def links_creator(pkg, version):
    pts_base = "http://packages.qa.debian.org/"
    bts_base = "http://bugs.debian.org/cgi-bin/pkgreport.cgi?src="
    deb_buildd_base = "https://buildd.debian.org/status/logs.php?arch=&pkg="
    puc_base = "http://packages.ubuntu.com/search?searchon=sourcenames&keywords="
    lp_base = "https://launchpad.net/ubuntu/+source/"
    ubu_bugs_base = "https://launchpad.net/ubuntu/+source/%s/+bugs"
    ubu_buildd_base = "https://launchpad.net/ubuntu/+source/%s/%s"

    pts = HTML.link('Debian PTS', pts_base + pkg)
    bts = HTML.link('Debian BTS', bts_base + pkg)
    deb_buildd = HTML.link('Debian buildd', deb_buildd_base + pkg)
    puc = HTML.link('Ubuntu packages.u.c.', puc_base + pkg)
    lp = HTML.link('Ubuntu LP', lp_base + pkg)
    ubu_bugs = HTML.link('Ubuntu Bugs', ubu_bugs_base % pkg)
    ubu_buildd = HTML.link('Ubuntu buildd', ubu_buildd_base % (pkg, version))

    return pts, bts, deb_buildd, puc, lp, ubu_bugs, ubu_buildd


if __name__ == "__main__":
    conn = psycopg2.connect("service=udd")
    cursor = conn.cursor()

    up_to_date = []
    newer_version_available = []
    other=[]

    for src_pkg in WIILDOS_SRC_PKGS_LIST:
        query = "SELECT DISTINCT ubuntu_sources.source, \
                 ubuntu_sources.version, sources.version, \
                 upstream.upstream_version, upstream.status \
                 FROM ubuntu_sources LEFT OUTER JOIN sources \
                 ON ubuntu_sources.source=sources.source LEFT OUTER JOIN \
                 upstream ON sources.source=upstream.source \
                 WHERE ubuntu_sources.source='" + src_pkg + \
                 "' AND ubuntu_sources.release='" + UBUNTU_RELEASE + \
                 "' AND sources.release='" + DEBIAN_RELEASE + "';"
        cursor.execute(query)

        for row in cursor.fetchall():  #returns a list of tuples of strings, one tuple per match
            if row[-1] == 'up to date':
                up_to_date.append(row)
            elif row[-1] == 'Newer version available':
                newer_version_available.append(row)
            else:
                other.append(row)

    write_header()

    write_table("Packages with issues:", other)
    write_table("Newer upstream version available:", newer_version_available)
    write_table("Upstream up to date:", up_to_date)

    write_footer()
