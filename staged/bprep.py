import os
import sys
import time
import json

def parse_arguments(args):
    # Initialize internal dictionary with default values
    internal_dict = {
        "path": None,
        "target": "any",
        "arch": "any",
        "osver": "any",
        "flags": {},
        "ienc": "utf-8"
    }

    # Iterate over arguments and parse accordingly
    if '-path' not in args:
        raise ValueError("-path <path> must be specified!")
    for i, arg in enumerate(args):
        if arg == '-path' and i + 1 < len(args):
            internal_dict["path"] = os.path.abspath(args[i + 1])
        elif arg == '-target' and i + 1 < len(args):
            internal_dict["target"] = args[i + 1]
        elif arg == '-arch' and i + 1 < len(args):
            internal_dict["arch"] = args[i + 1]
        elif arg == '-osver' and i + 1 < len(args):
            internal_dict["osver"] = args[i + 1]
        elif arg == '-ienc' and i + 1 < len(args):
            internal_dict["ienc"] = args[i + 1]
        elif arg == '-flags' and i + 1 < len(args):
            try:
                internal_dict["flags"] = json.loads(args[i + 1])
            except json.JSONDecodeError:
                print("Error: Invalid JSON string for -flags")
                sys.exit(1)

    return internal_dict

# Exclude the script name from arguments
arguments = sys.argv[1:]
res = parse_arguments(arguments)

buildstr = f'BUILD_TARGET_IDENTIFIER="{res["target"]}","{res["arch"]}","{res["osver"]}",{int(time.time())},{res["flags"]}'

if os.path.exists(res["path"]):
    new_content = ""
    with open(res["path"],'r',encoding=res["ienc"]) as f:
        content = f.read()
        f.close()

    new_lines = []
    for line in content.split("\n"):
        if line.lstrip().startswith("BUILD_TARGET_IDENTIFIER="):
            if "#" in line:
                line = buildstr + " #"+"#".join(line.split("#")[1:])
            else:
                line = buildstr
        new_lines.append(line)
    new_content = "\n".join(new_lines)

    print("Generated '" + buildstr + "' for '" + res.get("path","None") + "'")

    with open(res["path"],'w',encoding=res["ienc"]) as f2:
        f2.write(new_content)
        f2.close()

else:
    raise FileNotFoundError("File '" + res.get("path","None") + "' not found!")