# -*- coding: utf8 -*-
from BeautifulSoup import BeautifulSoup as Soup
from urllib2 import urlopen
import re

from drawtree import draw_tree

def get_tag(dom):
    if hasattr(dom, 'name'):
        return dom.name
    else:
        return 'text'

def iter_children(dom):
    return [d for d in dom]

def is_leaf(dom):
    return not hasattr(dom, 'name') or len(dom) == 0

def dom_clean(dom):
    [e.extract() for e in dom.findAll(text=lambda i: re.compile(r'^\s*$').match(i))]
    return dom

html = """
<html>
    <head>
        <script></script>
        <style></style>
        <title></title>
    </head>
    <body>
        <div>
            <div></div>
            <div>
                <ul>
                    <li></li>
                    <li></li>
                    <li></li>
                </ul>
            </div>
            <div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <div></div>
                <ul></ul>
            </div>
        </div>
        <div></div>
    </body>
</html>
"""

if __name__ == '__main__':
    soup = dom_clean(Soup(html))
    draw_tree(soup.body, 'htmltree.jpg', get_tag, iter_children, is_leaf)