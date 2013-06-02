#!/usr/bin/python
import sys
from lxml import etree
import json


def members(file):
    root = etree.parse(file)
    members = root.xpath("//member")
    return [dict(member.attrib.items()) for member in members]


def main(file):
    print json.dumps(members(file))

if __name__ == "__main__":
    main(sys.argv[1])
