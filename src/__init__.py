# fuse:import
import sys,os
# fuse:import

# The next line should be replaced by bprep.py in its entierity
BUILD_TARGET_IDENTIFIER="pysource","any","any",-1,{} #<target>,<arch>,<osver>,<epoch>,<flags>

# fuse:include ./pyinst_essentials.py

# fuse:include ./frontends.py
# fuse:include ./defines_frontends.py

# region: Example
# fuse:exclude
from frontends import *
from frontends.cli import *
from frontends.tkinter import *
# fuse:exclude
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