# -*- coding: utf8 -*-
"""
This is a small tool to visualize a dom tree 
structure.

It depends on PIL, BeautifulSoup
"""
from BeautifulSoup import BeautifulSoup as Soup
from urllib2 import urlopen
from PIL import Image, ImageDraw
import re

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

def draw_tree(dom, filepath):
    scalex = 40
    scaley = 30
    width = get_width(dom) * scalex
    depth = get_depth(dom) * scaley
    
    print width, depth
    
    img = Image.new('RGB', (width, depth), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    text = dom.name
    draw.text(((width - len(text)*5)/2, 0), text, (255, 0, 0))
    draw_node(draw, dom, 1, (width/2, 10), scalex, scaley)
    img.save(filepath)
    
def draw_node(draw, dom, level, parent, scalex=20, scaley=20, left=0):
    if not hasattr(dom, 'name'):
        draw.line((parent[0], parent[1], left + scalex / 2, level * scaley), (255, 0, 0))
        draw.text((left + scalex / 2 - 8, level * scaley), 'text', (255, 0, 0))
        return
    names = []
    for d in dom:
        if hasattr(d, 'name'):
            names.append(d.name)
        else:
            names.append('text')
    if not len(names): return
#    print 'names:', names
    
    widths = [get_width(d) * scalex for d in dom]
#    print 'width:', widths
    width_range = [widths[i] + sum(widths[:i]) for i in range(len(widths))]
#    print 'range:', width_range
    xs = [0]
    xs[0] = (width_range[0] - len(names[0]) * 4) / 2
    xs.extend([ width_range[i-1] + (width_range[i] - width_range[i-1] - len(names[i]) * 4) / 2 for i in range(1, len(names))])
#    print 'xs', xs
    points = [(width_range[0] / 2 + left, level * scaley)]
    points.extend([ (width_range[i-1] + (width_range[i] - width_range[i-1]) / 2 + left, level * scaley) for i in range(1, len(names))])
#    print points
    # draw line with parent and children
    for p in points:
        draw.line((parent[0], parent[1], p[0], p[1]), fill=(255, 0, 0))
    for i in range(len(xs)):
        draw.text((xs[i] + left, level * scaley), names[i], (255, 0, 0))
    for i in range(len(dom)):
        if hasattr(dom.contents[i], 'name'):
            if i == 0:
                draw_node(draw, dom.contents[i], level + 1, (points[i][0], points[i][1]+10), scalex, scaley, left)
            else:
                draw_node(draw, dom.contents[i], level + 1, (points[i][0], points[i][1]+10), scalex, scaley, left + width_range[i-1])
                
if __name__ == '__main__':
    url = "http://music.douban.com/"
    soup = dom_clean(Soup(urlopen(url)))
    #soup = dom_clean(Soup(html))
    draw_tree(soup.body, 'e:/a.jpg')