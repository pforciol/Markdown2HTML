#!/usr/bin/python3
"""Markdown to HTML module.

This module contains a basic script with no utility for now.

"""
import sys
import os
import re

if __name__ == "__main__":

    args = sys.argv[1:]
    args_len = len(args)

    if args_len < 2:
        sys.exit("Usage: ./markdown2html.py README.md README.html")

    if not os.path.isfile(args[0]):
        sys.exit("Missing {:s}".format(args[0]))

    with open(args[0], "r") as f:
        content = f.readlines()

    html = []
    for line in content:
        # HEADINGS CONVERSION
        if line.startswith("#"):
            level = len(line.split(" ", 1)[0])
            if level > 6:
                html.append(line)
                continue
            html.append("<h{0}>{1}</h{0}>\n"
                        .format(level, line.split(" ", 1)[1].strip()))

        else:
            html.append(line)

    html_len = len(html)

    # UNORDERED LISTS
    status = 0
    for i in range(html_len):
        if html[i].startswith("-"):
            if status == 0:
                html[i] = ("<ul>\n<li>{}</li>\n"
                           .format(html[i].split(" ", 1)[1].strip()))
            else:
                html[i] = ("<li>{}</li>\n"
                           .format(html[i].split(" ", 1)[1].strip()))

            status = 1

            if i + 1 >= html_len or not html[i + 1].startswith("-"):
                html[i] += "</ul>\n"
                status = 0

    # ORDERED LISTS
    status = 0
    for i in range(html_len):
        if html[i].startswith("*"):
            if status == 0:
                html[i] = ("<ol>\n<li>{}</li>\n"
                           .format(html[i].split(" ", 1)[1].strip()))
            else:
                html[i] = ("<li>{}</li>\n"
                           .format(html[i].split(" ", 1)[1].strip()))

            status = 1

            if i + 1 >= html_len or not html[i + 1].startswith("*"):
                html[i] += "</ol>\n"
                status = 0

    with open(args[1], "w") as f:
        f.writelines(html)
