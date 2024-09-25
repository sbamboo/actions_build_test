# FuseKit - Lite

# Deffinitions
config = {
    "format": 0,
    "tool-id": "alpha.fusekit.lite",
    "tool-ver": "0.0.1",
    "tool-desc": "Placeholder tool, switch to fuse when ready.",

    "proj-name": "example",

    "builds-dir": "./../staged/",

    "main-file": "./../src/__init__.py",
    
    "esm": { # EmbedableSourceModule
        "output-dir": "./../staged/esm/%pn",
        "output-main-file": "__init__.py"
    },

    "fused": { # %1: FileName, %2: FileExt
        "output-file": "./../staged/fused/%pn.%2"
    },

    "file": { # id to use in include to spec this opts
        
    },

    "post-fuse-content": {
        "leading": [
            "# Created with %fi %fv on %d",
            "# ",
            ""
        ],
        "trailing": ""
    },

    "recursive-parsing-depth": -1, # -1 Set depth to inf

    "flags": ["--rem-builds"]
}

# Imports
import os, shutil, sys, json
from datetime import datetime

# Setup Vars
parent = os.path.dirname(os.path.abspath(__file__))
namespace = "fuse"
encoding = "utf-8"

# Handle flags
if len(sys.argv) > 1:
    ioffset = 0
    for i,x in enumerate(sys.argv[1:]):
        if x.strip() == "-c":
            ioffset = i+1
            p = f(x[i+1])
            if os.path.exists(p):
                n = json.loads(open(p,'r',encoding=encoding).read())
                for k,v in n.items():
                    if k in config.keys():
                        if type(config[k]) == "dict":
                            config[k].update(v)
                        elif type(config[k]) in ["list","tuple"]:
                            config[k].extend(v)
                        else:
                            config[k] = v
                    else:
                        config[k] = v
            break
    config["flags"].extend(sys.argv[1+ioffset:])

# !EXTERNAL LIBRARY INCLUSIONS!
def fprint(s): print(s)

# Setup
def f(s,isdir:bool=False,tags:dict={}):
    if s.lstrip().startswith("./"):
        t = os.path.abspath(s.replace("./",parent+"/",1))
    elif s.lstrip().startswith(".\\"):
        t = os.path.abspath(s.replace(".\\",parent+"/",1).replace("\\","/"))
    else: t = s
    for tagk,tagv in tags.items():
        t = t.replace(tagk,tagv)
    if isdir == True:
        if not os.path.exists(t):
            os.makedirs(t)
    else:
        if not os.path.exists(os.path.dirname(t)):
            os.makedirs(os.path.dirname(t))
    return t

def fdatetime(format_string="%Y-%m-%d %H:%M:%S"):
    """
    "%Y-%m-%d %H:%M:%S" (e.g., "2023-08-24 14:45:30")
    """
    current_time = datetime.now()
    formatted_time = current_time.strftime(format_string)
    return formatted_time

# Main Parser
def parse(mode:str,content:str,fileOpts:dict={},inputParent=parent,outputParent=parent,encoding="utf-8",_currentRecursiveDepthIndex:int=None,_callIsARecursion=False,_recursionStack=[],_recusiveIncludeAllowence=True,_recursiveName="") -> str:
    """Parses a string and returns the parsed content.\nModes: 'esm'/'fuse'"""
    lines = content.split("\n")
    switch_exclude = False
    switch_import = False
    switch_exclude_fuse = False
    switch_exclude_esm = False
    switch_dot = False
    switch_dot_fuse = False
    switch_dot_esm = False
    new_lines = []
    for i,line in enumerate(lines):
        switch_dotthis_perline = False
        shorthand = line.replace(" ","")

        # switches
        if shorthand.startswith("#"+namespace+":import"):
            switch_import = not switch_import

        elif shorthand.startswith("#"+namespace+":exclude.fuse"):
            switch_exclude_fuse = not switch_exclude_fuse
            if (not switch_exclude_fuse) == True:
                if mode == "fuse": continue

        elif shorthand.startswith("#"+namespace+":exclude.esm"):
            switch_exclude_esm = not switch_exclude_esm
            if (not switch_exclude_esm) == True:
                if mode == "esm": continue

        elif shorthand.startswith("#"+namespace+":dot"):
            switch_dot = not switch_dot

        elif shorthand.startswith("#"+namespace+":dot.fuse"):
            switch_dot_fuse = not switch_dot_fuse
            if (not switch_dot_fuse) == True:
                if mode == "fuse": continue

        elif shorthand.startswith("#"+namespace+":dot.esm"):
            switch_dot_esm = not switch_dot_esm
            if (not switch_dot_esm) == True:
                if mode == "esm": continue

        elif shorthand.startswith("#"+namespace+":exclude"):
            switch_exclude = not switch_exclude
            if (not switch_exclude) == True: continue

        elif shorthand.endswith("#"+namespace+":exclude.this"):
            continue
        elif shorthand.endswith("#"+namespace+":exclude.this.fuse"):
            if mode == "fuse": continue
        elif shorthand.endswith("#"+namespace+":exclude.this.esm"):
            if mode == "esm": continue

        elif shorthand.endswith("#"+namespace+":dot.this.fuse"):
            if mode == "fuse": switch_dotthis_perline = True
        elif shorthand.endswith("#"+namespace+":dot.this.esm"):
            if mode == "esm": switch_dotthis_perline = True
        elif shorthand.endswith("#"+namespace+":dot.this"):
            switch_dotthis_perline = True

        # skipper (switch_exclude)
        if switch_exclude == True or (mode == "fuse" and switch_exclude_fuse == True) or (mode == "esm" and switch_exclude_esm == True):
            continue

        # switch_dot
        if switch_dot == True or (mode == "fuse" and switch_dot_fuse == True) or (mode == "esm" and switch_dot_esm == True) or switch_dotthis_perline == True:
            if shorthand.startswith("import"):
                pref = line.split("import")[0]
                nex_ = "import".join(line.split("import")[1:]).lstrip()
                line = pref+"import ."+nex_
            elif shorthand.startswith("from"):
                pref = line.split("from")[0]
                nex_ = "import".join(line.split("from")[1:]).lstrip()
                line = pref+"from ."+nex_

        if shorthand.startswith("#"+namespace+""):    
            # include
            if shorthand.startswith("#"+namespace+":include"):
                if line.lstrip().startswith("# fuse:include"):
                    prefixIndentation = line.split("# fuse:include")[0]
                elif line.lstrip().startswith("#fuse:include"):
                    prefixIndentation = line.split("#fuse:include")[0]
                if _recusiveIncludeAllowence == False:
                    if ("--mute-warns" not in config["flags"]): fprint("{f.darkyellow}Warn: Reached the max recusion limit of "+str(config["recursive-parsing-depth"])+", won't traverse further then "+_recursiveName+"!{r}")
                else:
                    args = "include".join(line.split("include")[1:]).lstrip(" ").split(" ")
                    opts = {}
                    incl_lines = []
                    orgpath = args[0]
                    if args[0] in fileOpts.keys():
                        opts = fileOpts[args[0]]
                        args[0] = f(opts["path"])
                    else:
                        args[0] = f(args[0])
                    # Handle non-exit
                    if not os.path.exists(args[0]):
                        fprint("{f.red}Skipped include for "+os.path.basename(args[0])+", file not found!{r}")
                        new_lines.append(line+" $fuse.skipped.notFound")
                        continue
                    # Create shortpath and longpath
                    shortpath = os.path.splitext(args[0].replace("\\","/").replace(inputParent.replace("\\","/").rstrip("/"),"").lstrip("/"))[0]
                    shortpath_pathsafe = shortpath.replace("/",os.sep)
                    longpath = f(args[0]).replace("\\","/")
                    extension = os.path.splitext(longpath)[-1]
                    # orgpath is meant for comment include
                    if opts.get("write-as") != None:
                        if opts["write-as"] == "$shortpath":
                            orgpath = shortpath
                        elif opts["write-as"] == "$longpath":
                            orgpath = longpath
                        else:
                            orgpath = opts["write-as"]
                    # read
                    with open(args[0], 'r', encoding=encoding) as file:
                        content = file.read()
                    if _currentRecursiveDepthIndex < 0:
                        next_currentRecursiveDepthIndex = _currentRecursiveDepthIndex
                    else:
                        next_currentRecursiveDepthIndex = _currentRecursiveDepthIndex-1
                    if _currentRecursiveDepthIndex != 0:
                        longpathDirname = os.path.dirname(longpath)
                        if os.path.basename(args[0]) in _recursionStack:
                            raise RecursionError(formatting_inst.parse("{f.darkred}")+f"Attempted include of '{longpath}', but its already in the recursion stack!\n(NewestEntry:{_recursionStack[-1]}, lineI:{i})"+formatting_inst.parse("{r}"))
                        _recursionStack.append(os.path.basename(args[0]))
                        content = parse(mode=mode,content=content,fileOpts=fileOpts,inputParent=longpathDirname,outputParent=outputParent,encoding=encoding,_currentRecursiveDepthIndex=next_currentRecursiveDepthIndex,_callIsARecursion=True,_recursionStack=_recursionStack,_recusiveIncludeAllowence=_recusiveIncludeAllowence,_recursiveName=shortpath)
                    else:
                        content = parse(mode=mode,content=content,fileOpts=fileOpts,inputParent=longpathDirname,outputParent=outputParent,encoding=encoding,_currentRecursiveDepthIndex=next_currentRecursiveDepthIndex,_callIsARecursion=True,_recursionStack=_recursionStack,_recusiveIncludeAllowence=False,_recursiveName=shortpath)
                    incl_lines = content.split("\n")
                    # apply opts
                    if (opts.get("remove-leading-comments") == True) or (opts.get("remove-leading-comments") == "on-fuse" and mode.lower() == "fuse") or (opts.get("remove-leading-comments") == "on-esm" and mode.lower() == "esm"):
                        in_lead_comm = True
                        new_incl_lines = []
                        for incl_line in incl_lines:
                            if incl_line.startswith("#") and in_lead_comm == True and (not incl_line.replace(" ","").startswith("#region")) and (not incl_line.replace(" ","").startswith("#endregion")) and (not incl_line.replace(" ","").startswith("#fuse")): pass
                            else:
                                in_lead_comm = False
                                new_incl_lines.append(incl_line)
                        incl_lines = new_incl_lines
                    if (not opts.get("skip-include-regions") == True) and mode != "esm":
                        commentpath = "./"+shortpath+extension
                        if opts.get("custom-comment-path") != None:
                            commentpath = opts.get("custom-comment-path").replace("%s",shortpath).replace("%l",longpath).replace("%o",orgpath)
                        incl_lines = [
                            f"#region [fuse.include: {commentpath}]",
                            *incl_lines,
                            f"#endregion [fuse.include: {commentpath}]"
                        ]
                    # Apply
                    if mode == "esm":
                        # Indent Carryover
                        if "--experiments.esm-indent-carryover" in config["flags"] and prefixIndentation != "":
                            incl_lines = [prefixIndentation+x for x in incl_lines]
                        if opts.get("custom-esm-import") != None:
                            line = opts["custom-esm-import"].replace("%s",shortpath).replace("%l",longpath).replace("%o",orgpath)
                        else:
                            line = f"from .{shortpath.replace("/",".")} import *"
                        # Indent Carryover
                        if not "--no-indent-carryover" in config["flags"] and prefixIndentation != "":
                            line = prefixIndentation+line
                        # Write
                        writing_outputpath = os.path.join(outputParent,shortpath_pathsafe)+".py"
                        if not os.path.exists(os.path.dirname(writing_outputpath)): os.makedirs(os.path.dirname(writing_outputpath))
                        with open(writing_outputpath, 'w', encoding=encoding) as incl_file:
                            incl_file.write("\n".join(incl_lines))
                    elif mode == "fuse":
                        # Indent Carryover
                        if not "--no-indent-carryover" in config["flags"] and prefixIndentation != "":
                            incl_lines = [prefixIndentation+x for x in incl_lines]
                        new_lines.extend(incl_lines)
                        continue
        # Append
        new_lines.append(line)
    # Post fuse content
    if _callIsARecursion == False:
        if config.get("post-fuse-content") != None:
            if config["post-fuse-content"].get("leading") != None:
                new_lines = [*[x.replace("%fi",config["tool-id"]).replace("%fv",config["tool-ver"]).replace("%d",fdatetime()) for x in config["post-fuse-content"]["leading"]],*new_lines]
            if config["post-fuse-content"].get("trailing") != None:
                new_lines.extend([x.replace("%fv",config["tool-ver"]).replace("%d",fdatetime()) for x in config["post-fuse-content"]["trailing"]])
    # Return
    if ("--remove-type-hints" in config["flags"]):
        return strip_type_hints( '\n'.join(new_lines) )
    else:
        return '\n'.join(new_lines)


def parse_file(mode:str,filepath:str,newpath:str=None,fileOpts:dict={},encoding="utf-8") -> str:
    """Reads a file, parses it and writes the new content, returns the choosen path."""
    with open(filepath, 'r', encoding=encoding) as file:
        content = file.read()
    output_path = newpath if newpath != None else filepath
    if config["recursive-parsing-depth"] == 0:
        _crdi = config["recursive-parsing-depth"]
        _alow = False
    else:
        _crdi = config["recursive-parsing-depth"]-1
        _alow = True
    parsed_content = parse(mode,content,fileOpts,os.path.dirname(filepath),os.path.dirname(output_path),encoding,_currentRecursiveDepthIndex=_crdi,_callIsARecursion=False,_recursionStack=[os.path.basename(filepath),os.path.basename(newpath)],_recusiveIncludeAllowence=_alow,_recursiveName=os.path.basename(filepath))
    with open(output_path, 'w', encoding=encoding) as file:
        file.write(parsed_content)
        file.close()
    return output_path

# Rem builds?
if "--rem-builds" in config.get("flags"):
    p = f(config["builds-dir"])
    if os.path.exists(p): shutil.rmtree(p)

# Read main and ensure out
mainFile_p = f(config["main-file"],False)
tags = {
    "%1": os.path.splitext(os.path.basename(mainFile_p))[0],
    "%2": os.path.splitext(os.path.basename(mainFile_p))[1].lstrip("."),
    "%pn": config["proj-name"]
}
esmOut_p = f(config["esm"]["output-dir"],True,tags)
fusedOut_p = f(config["fused"]["output-file"],False,tags)

# SourceEmbedableModule
parse_file("esm",mainFile_p,os.path.join(esmOut_p,config["esm"]["output-main-file"]),config["file"],encoding=encoding)
# Fused
parse_file("fuse",mainFile_p,fusedOut_p,config["file"],encoding=encoding)

fprint("Done! Wrote to "+os.path.abspath(config["builds-dir"])+"!\n"+"ESM: "+os.path.join(esmOut_p,config["esm"]["output-main-file"])+"\nFUSED: "+fusedOut_p)

pfts = config.get("post-fuse-test-script")
if pfts != None:
    pfts = f(pfts)
    if os.path.exists(pfts):
        os.system(f"{sys.executable} {pfts}")