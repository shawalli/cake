
import os

import Core.Types

class Node(object):
    def __init__(self, name, parent_node):
        self.name = name
        self.up_to_date = False
        self.parent_node = parent_node
        self.fs_type = 'node'
        self.children = Core.Types.List()

    def get_child(self, name):
        for c in self.children:
            if name == c.name:
                return c
        return None

    def exists(self):
        return False

    def prepare(self):
        pass

    def is_file(self):
        return False

    def is_dir(self):
        return False

    def is_trivial(self):
        return False

    def is_cake(self):
        return False

