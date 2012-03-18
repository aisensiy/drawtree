# -*- coding: utf8 -*-
from BeautifulSoup import BeautifulSoup as Soup
from urllib2 import urlopen
import re

from drawtree import draw_tree, draw_node

def get_tag(dom):
    if hasattr(dom, 'name'):
        return dom.name
    else:
        return 'text'

def iter_children(dom):
    return [d for d in dom]

def is_leaf(dom):
    return not hasattr(dom, 'name') or len(dom) == 0

def get_width(dom):
    if hasattr(dom, 'name') and dom.width: return dom.width
    if not hasattr(dom, 'name'): return 1
    if dom.contents and len(dom) > 0:
        width = 0
        for d in dom:
            if hasattr(d, 'name'):
                width += get_width(d)
            else:
                width += 1
        if hasattr(d, 'name'):
            dom.width = width
    else:
        return 1
    return width

def get_depth(dom):
    if hasattr(dom, 'name') and dom.depth: return dom.depth
    if not hasattr(dom, 'name'): return 1
    if dom.contents and len(dom) > 0:
        max  = 0
        for d in dom:
            if hasattr(d, 'name'):
                de = get_depth(d)
            else:
                de = 1
            if de > max:
                max = de
        if hasattr(d, 'name'):
            dom.depth = max + 1
        return max + 1
    else:
        return 1

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
    url = "http://music.douban.com/"
    #soup = dom_clean(Soup(urlopen(url)))
    soup = dom_clean(Soup(html))
    draw_tree(soup.body, 'e:/a.jpg', get_width, get_depth, get_tag, iter_children, is_leaf)