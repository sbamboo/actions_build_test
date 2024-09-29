# Created with alpha.fusekit.lite 0.0.1 on 2024-09-30 01:39:18
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
example_schema = FrontEndSchema(
    {
        "id": "example1",
        "properties": {
            "title": "Example UI"
        },
        "content": {
            "pyinstprops.running_mode": PYINST_PROPERTIES.running_mode,
            "pyinstprops.application_path": PYINST_PROPERTIES.application_path,
            "pyinstprops.executable_path": PYINST_PROPERTIES.executable_path,
            "pyinstprops.first_argument": PYINST_PROPERTIES.first_argument,
            "pyinstprops.isonefile": PYINST_PROPERTIES.isonefile,
            "pyinstprops.target.platform": PYINST_PROPERTIES.idef.target,
            "pyinstprops.target.arch": PYINST_PROPERTIES.idef.arch,
            "pyinstprops.target.osver": PYINST_PROPERTIES.idef.osver,
            "pyinstprops.timestamp": PYINST_PROPERTIES.idef.epoch_f,
            "pyinstprops.flags": PYINST_PROPERTIES.idef.flags
        },
        "callbacks": {
            "external.window.exit": lambda r: (
                r.host.terminate(),
                exit()
            )
        }
    }
)

example_frontend_host = FrontEndSchemaHost()
example_frontend_host.assemble("cli", ExampleCliFrontEnd())
example_frontend_host.assemble("tkinter", ExampleTkinterFrontEnd())
example_frontend_host.launch("cli")
example_frontend_host.display(example_schema, "cli")
# endregion: Example