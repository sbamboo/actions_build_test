from rich.console import Console
console = Console()



import sys,os

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
    running_mode = 'Frozen/executable'
    executable_path = os.path.realpath(sys.executable)
    first_argument = os.path.realpath(sys.argv[0])
else:
    try:
        app_full_path = os.path.realpath(__file__)
        application_path = os.path.dirname(app_full_path)
        running_mode = "Non-interactive (e.g. 'python myapp.py')"
        executable_path = os.path.realpath(sys.executable)
        first_argument = os.path.realpath(sys.argv[0])
    except NameError:
        application_path = os.getcwd()
        running_mode = 'Interactive'
        executable_path = os.path.realpath(sys.executable)
        first_argument = os.path.realpath(sys.argv[0])



console.print('Running mode:', running_mode, style="magenta")
console.print('  Application path  :', application_path, style="magenta")
console.print('  Executable path   :', executable_path, style="magenta")
console.print('  First args path   :', first_argument, style="magenta")