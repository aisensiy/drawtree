# -*- coding: utf8 -*-

from drawtree import draw_tree, draw_node

def get_tag(node):
    if type(node) != list: return str(node)
    return 'list'

def iter_children(node):
    return node

def is_leaf(node):
    return not node or type(node) != list

def get_width(node):
    if is_leaf(node): return 1
    return sum(get_width(n) for n in iter_children(node))

def get_depth(node):
    if is_leaf(node): return 1
    return max(get_depth(n) for n in iter_children(node)) + 1

tree = [[1, 2, 3, 4], [5, 7]]

if __name__ == '__main__':
    draw_tree(tree, 'e:/a.jpg', get_width, get_depth, get_tag, iter_children, is_leaf)