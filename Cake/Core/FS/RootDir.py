
import os

import Node
import Dir

class RootDir(Dir.Dir):
    def __init__(self, path):
        parent_dirs, dirname = os.path.split(path)
        
        Node.Node.__init__(self, dirname, None)
        self.fs_type = 'root'
        self.type = 'dir'
        self.name = dirname
        self.abspath = os.path.abspath(path)

    def get_abspath(self):
        return self.abspath

    def __repr__(self):
        s = ['RootDir node @ %s:' % hex(id(self))]
        s.append('  name:%s' % self.name)
        s.append('  abspath:%s' % self.abspath)
        s.append('  parent_node: None')
        s.append('  children:')
        for c in self.children:
            s.append('  * ' + '\n  '.join(line for line in repr(c).splitlines()))

        return '\n'.join(s)
