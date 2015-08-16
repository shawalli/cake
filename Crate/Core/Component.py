
import os
import imp
import sys
import types

import Core.Error
import Core.Types

def import_as_module(path):
    _, basename = os.path.split(path)
    path = os.path.join(path, '.cake')

    if os.path.exists(path) is False:
        raise Core.Error.CakeImportError('Component \'%s\' not found' % basename)
    module = imp.load_source(basename, path)

    return module

def print_module(module, path, indent=0):
    print ' ' * indent + path + '(' + str(type(module)) + '):'

    indent += 1
    for cname, c in module.__children.items():
        p = os.path.join(path, cname)
        print_module(c, p, indent)

def add_module_to_tree(root, module, module_path):
    if hasattr(root, '__children') is False:
        root.__children = Core.Types.Dict()

    parent_module = root
    module_path, module_name = os.path.split(module_path)
    for intermediate_module_name in module_path.split(os.path.sep):
        intermediate_module = getattr(parent_module, intermediate_module_name, None)
        if intermediate_module is None:
            intermediate_module = Core.Types.Container()
            intermediate_module.__children = Core.Types.Dict()
            # add to children dictionary for possible future morph to module
            parent_module.__children[intermediate_module_name] = intermediate_module
            # add directly to container for convenience referencing
            setattr(parent_module, intermediate_module_name, intermediate_module)

            parent_module = getattr(parent_module, intermediate_module_name)
            continue
    
    existing_module = getattr(parent_module, module_name, None)
    #if isinstance(existing_module, types.ModuleType) is True:
    #    return  
    if isinstance(existing_module, Core.Types.Container) is True:
        module.__children = existing_module.__children
    else:
        module.__children = Core.Types.Dict()

    parent_module.__children[module_name] = module
    setattr(parent_module, module_name, module)
