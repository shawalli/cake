#!/usr/bin/env python2.7

import os
import argparse

import Core
import Core.Component
import Core.FS.RootDir
import Core.Types

def parse_args(args):
    usage = '$(prog)s [--workspace=PATH] [-c|-d] [--component=PATH] [target-platform]'
    p = argparse.ArgumentParser(usage=usage)

    p.add_argument('--workspace', type=str, metavar='PATH', help='Bases your workspace somewhere else. Default workspace will be at one level above top crate directory.')
    p.add_argument('--component', type=str, metavar='PATH', default='.crate', help='Patch to component to make. Default is workspace-level component.')
    clean = p.add_mutually_exclusive_group()
    clean.add_argument('-c', dest='clean', action='store_true', default=False, help='Clean the build environment.')
    clean.add_argument('-d', dest='distclean', action='store_true', default=False, help='Clean the build environment for a specific component and target platform.')

    args, platform = p.parse_known_args(args)

    if len(platform) > 1:
        raise Exception('Only one platform should be specified.')
    elif len(platform) == 0:
        platform = ['host']
    args.platform = platform[0]

    return args

def process_args(args):
    new_args = argparse.Namespace()

    if args.clean is True:
        new_args.clean='all'
    elif args.distclean is True:
        new_args.clean='dist'
    else:
        new_args.clean='none'

    new_args.platform = args.platform
    new_args.component = os.path.abspath(args.component)

    if args.workspace is not None:
        ws = os.path.abspath(os.path.normpath(args.workspace))
        if os.path.exists(ws) is False or os.path.isdir(ws) is False:
            raise argparse.ArgumentError('provided workspace path is not an existing directory')
        os.chdir(ws)
        new_args.workspace = ws
    else:
        new_args.workspace = os.path.abspath(os.getcwd())

    return new_args

# construct platform by pulling out any options that match a naming scheme in platforms/
# 1. see if component .crate exists; throw error if not.
# 2. go through all imported components, adding them as modules for use later
def main(args):
    args = parse_args(args)
    args = process_args(args)

    root_dir = Core.FS.RootDir(args.workspace)
    relpath = root_dir.relpath(args.component)

    Core.modules = Core.Types.Container()

    component = Core.Component.import_as_module(args.component)

    Core.Component.add_module_to_tree(Core.modules, component, relpath)
    Core.Component.print_module(Core.modules, '.')
