# -*- coding: utf8 -*-
"""
This is a small tool to visualize a tree 
structure.

You should write the following functions for the draw_tree
function to use:

get_tag          : return the node name to print
iter_children    : get the children
is_leaf          : check if the node is a leaf

It depends on PIL
"""

__author__ = 'aisensiy<aisensiy@gmail.com>'

from PIL import Image, ImageDraw

def draw_tree(dom, filepath, get_tag, iter_children, is_leaf):
    def get_width(node):
        if is_leaf(node): return 1
        return sum(get_width(n) for n in iter_children(node))

    def get_depth(node):
        if is_leaf(node): return 1
        return max(get_depth(n) for n in iter_children(node)) + 1

    scalex = 60
    scaley = 30
    width = get_width(dom) * scalex
    depth = get_depth(dom) * scaley
    
    print width, depth
    
    img = Image.new('RGB', (width, depth), (255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    text = get_tag(dom)
    draw.text(((width - len(text)*5)/2, 0), text, (255, 0, 0))
    draw_node(draw, dom, 1, (width/2, 10), iter_children, is_leaf, get_tag, get_width, scalex, scaley)
    img.save(filepath)
    
def draw_node(draw, dom, level, parent, iter_children, is_leaf, get_tag, get_width, scalex=20, scaley=20, left=0):
    if is_leaf(dom): return
    names = []
    
    children = iter_children(dom)
    for d in children:
        names.append(get_tag(d))
    
    widths = [get_width(d) * scalex for d in children]
    width_range = [widths[i] + sum(widths[:i]) for i in range(len(widths))]
    xs = [0]
    xs[0] = (width_range[0] - len(names[0]) * 4) / 2
    xs.extend([ width_range[i-1] + (width_range[i] - width_range[i-1] - len(names[i]) * 4) / 2 for i in range(1, len(names))])
    points = [(width_range[0] / 2 + left, level * scaley)]
    points.extend([ (width_range[i-1] + (width_range[i] - width_range[i-1]) / 2 + left, level * scaley) for i in range(1, len(names))])
    
    # draw line with parent and children
    for p in points:
        draw.line((parent[0], parent[1], p[0], p[1]), fill=(255, 0, 0))
    for i in range(len(xs)):
        draw.text((xs[i] + left, level * scaley), names[i], (255, 0, 0))
    for i in range(len(children)):
        draw_node(draw, 
                  children[i], level + 1, 
                  (points[i][0], points[i][1]+10), 
                  iter_children, is_leaf, get_tag, get_width,
                  scalex, scaley, left + (i == 0 and [0] or [width_range[i - 1]])[0])

