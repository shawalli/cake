
import subprocess

import Core.Types

def execute(commandline, shell=True):
    ret = {
        'command' : '',
        'stdout' : '',
        'stderr' : '',
        'return_code' : '',
    }

    if isinstance(commandline, Core.Types.ListTypes) is True:
        commandline = ' '.join(commandline)
    ret['command'] = commandline

    process = subprocess.Popen(
        commandline,
        shell=shell,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)
    
    stdout, stderr = process.communicate()
    ret['stdout'] = stdout
    ret['stderr'] = stderr
    ret['return_code'] = process.returncode

    return ret
