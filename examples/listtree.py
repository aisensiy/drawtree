# -*- coding: utf8 -*-

from drawtree import draw_tree, draw_node

def get_tag(node):
    if type(node) != list: return str(node)
    return 'list'

def iter_children(node):
    return node

def is_leaf(node):
    return not node or type(node) != list

if __name__ == '__main__':
	tree = [[1, 2, 3, 4], [5, 7]]
    draw_tree(tree, 'listtree.jpg', get_tag, iter_children, is_leaf)