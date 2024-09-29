# Created with alpha.fusekit.lite 0.0.1 on 2024-09-29 13:08:50
# 

# fuse:import
import sys,os
# fuse:import

# The next line should be replaced by bprep.py in its entierity
BUILD_TARGET_IDENTIFIER="pysource","any","any",-1,{} #<target>,<arch>,<osver>,<epoch>,<flags>

from .pyinst_essentials import *

from .frontends import *
from .defines_frontends import *

# region: Example
from rich.console import Console
console = Console()

console.print('Running mode:', PYINST_PROPERTIES.running_mode, style="magenta")
console.print('  Application path  :', PYINST_PROPERTIES.application_path, style="magenta")
console.print('  Executable path   :', PYINST_PROPERTIES.executable_path, style="magenta")
console.print('  First args path   :', PYINST_PROPERTIES.first_argument, style="magenta")
console.print('  Is-Onefile        :', PYINST_PROPERTIES.isonefile, style="magenta")
console.print('  Target platform   :', PYINST_PROPERTIES.idef.target, style="magenta")
console.print('  Target arch       :', PYINST_PROPERTIES.idef.arch, style="magenta")
console.print('  Target os-version :', PYINST_PROPERTIES.idef.osver, style="magenta")
console.print('  Staged Timestamp  :', PYINST_PROPERTIES.idef.epoch_f, style="magenta")
console.print('  Flags             :', style="magenta", end="")
i = 0
for k,v in PYINST_PROPERTIES.idef.flags.items():
    if not k.startswith("_"):
        if i == 0:
            console.print(f" {k}: {v}",style="blue")
        else:
            console.print(f"                      {k}: {v}", style="blue")
        i += 1
if i == 0:
    console.print(" None", style="magenta")
# endregion: Example