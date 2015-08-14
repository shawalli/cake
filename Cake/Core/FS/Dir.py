
import os

import Glob
import Node

class Dir(Node.Node):
    def __init__(self, path, parent_node):
        print 'Dir.__init__ invoked'
        if parent_node is None:
            raise TypeError('Parent node must be provided for new Dir')

        parent_dirs, dirname = os.path.split(path)
        if parent_dirs != '':
            parent_node = parent_node.Dir(parent_dirs)

        Node.Node.__init__(self, path, parent_node)
        self.fs_type = 'dir'
        self.type = 'dir'
        self.name = dirname
        self.abspath = None
        self.get_abspath()

        self.parent_node.children.append(self)

    def __str__(self):
        return self.get_abspath()

    def __repr__(self):
        s = ['Dir node @ %s:' % hex(id(self))]
        s.append('  name:%s' % self.name)
        s.append('  abspath:%s' % self.abspath)
        s.append('  parent_node:%s @ %s' % (self.parent_node.name, hex(id(self.parent_node))))
        s.append('  children:')
        for c in self.children:
            s.append('  * ' + '\n  '.join(line for line in repr(c).splitlines()))

        return '\n'.join(s)

    def glob(self):
        return Glob.glob(self.get_abspath())

    def get_abspath(self):
        if self.abspath is None:
            self.abspath = \
                os.path.join(self.parent_node.abspath, self.name)
        return self.abspath

    def relpath(self, to):
        return os.path.normpath(os.path.relpath(to, self.get_abspath()))

    def is_dir(self):
        return True

    def File(self, filename):
        print 'Dir.File invoked'
        parent_node = self

        parent_dirs, filename = os.path.split(filename)
        if parent_dirs != '':
            parent_node = self.Dir(parent_dirs)

        child_node = parent_node.get_child(filename)
        if child_node is not None:
            return child_node
        else:
            import File
            return File.File(filename, parent_node=parent_node)

    def Dir(self, dirname):
        print 'Dir.Dir invoked'
        child_node = None

        parent_dirs, dirname = os.path.split(dirname)
        if parent_dirs != '':
            # dirname ~= 'grandparents/of/dirname'
            # parent_dirs ~= 'grandparents/of'
            child_dir, grandchildren = os.path.split(parent_dirs)
            # child_dir ~= 'grandparents'
            # grandchildren ~= 'of'
            if child_dir == '':
                # no grandchildren, so swap variables
                child_dir = grandchildren
                grandchildren = ''
            child_node = self.get_child(child_dir)
            if child_node is None:
                # child_dir (~= 'grandparents') doesn't exist as node yet
                child_node = Dir(child_dir, parent_node=self)
                self.children.append(child_node)
            # dirname ~= 'of/dirname'
            dirname = os.path.join(grandchildren, dirname)
        else:
            # dirname ~= 'dirname'
            child_node = self.get_child(dirname)
            if child_node is not None:
                # node already exists for dirname
                return child_node

        if child_node is not None:
            return child_node.Dir(dirname)
        else:
            return Dir(dirname, parent_node=self)
