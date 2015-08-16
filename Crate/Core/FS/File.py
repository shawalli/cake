
import os

import Node

class File(Node.Node):
    def __init__(self, path, parent_node):
        print 'File.__init__ invoked'
        Node.Node.__init__(self, path, parent_node)

        parent_dirs, filename = os.path.split(path)
        if parent_dirs != '':
            parent_node = parent_node.Dir(parent_dirs)

        self.parent_node = parent_node
        self.fs_type = 'file'
        self.type = 'trivial'
        _, self.name = os.path.split(path)
        self.name, self.suffix = os.path.splitext(self.name)
        self.abspath = None
        self.get_abspath()

        # .hidden_file
        if self.name == '':
            self.name = self.suffix
            self.suffix = ''

        if self.name == '.crate':
            self.type = 'crate'

        self.parent_node.children.append(self)

    def __str__(self):
        return self.get_abspath

    def __repr__(self):
        s = ['File node @ %s:' % hex(id(self))]
        s.append('  name:%s' % self.name)
        s.append('  suffix:%s' % self.suffix)
        s.append('  abspath:%s' % self.abspath)
        s.append('  parent_node:%s @ %s' % (self.parent_node.name, hex(id(self.parent_node))))
        s.append('  type:%s' % self.type)
        
        return '\n'.join(s)

    def get_abspath(self):
        if self.abspath is None:
            self.abspath = \
                os.path.join(self.parent_node.abspath, self.name)
        return self.abspath

    def relpath(self, to):
        return os.path.normpath(os.path.relpath(to, self.get_abspath()))

    def is_file(self):
        return True

    def is_source(self):
        return self.type == 'source'

    def is_target(self):
        return self.type == 'target'

    def is_crate(self):
        return self.type == 'crate'

    def is_trivial(self):
        return self.type == 'trivial'

    def File(self, filename):
        print 'File.File invoked'
        dir_node = self.parent_node
        parent_dirs, filename = os.path.split(filename)
        if parent_dirs != '':
            dir_node = self.Dir(parent_dirs)

        return dir_node.File(filename)

    def Dir(self, dirname):
        print 'File.Dir invoked'
        return self.parent_node.Dir(dirname)
