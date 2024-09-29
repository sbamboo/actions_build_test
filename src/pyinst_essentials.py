#fuse:import
import datetime
#fuse:import

#fuse:exclude
BUILD_TARGET_IDENTIFIER="pysource","any","any",-1,{}
#fuse:exclude

class PropertiesDict(dict):
    def __init__(self, __raising=False, **kwargs):
        super().__init__(**kwargs)
        self.__raising = __raising
    def __getattr__(self, name):
        if name in dir(self):
            attr = getattr(super(), name, None)
            if callable(attr):
                print("BONK")
        try:
            return self[name]
        except KeyError:
            if self.__raising == True:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            else:
                return None
    def __setattr__(self, name, value):
        self[name] = value
    def __delattr__(self, name):
        try:
            del self[name]
        except KeyError:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")

class PyInstallerProperties():
    def __init__(self,idef):
        # Get paths
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
        # Set properties
        self.idef = PropertiesDict()
        #<target>,<arch>,<osver>,<epoch>,<flags>
        self.idef.target = idef[0]
        self.idef.arch = idef[1]
        self.idef.osver = idef[2]
        self.idef.epoch = idef[3]
        # flags
        self.idef.flags = PropertiesDict()
        for k,v in idef[4].items():
            self.idef.flags[k] = v
        self.isonefile = True if self.idef.flags.onefile == True else False
        # info
        self.running_mode = running_mode
        self.application_path = application_path
        self.executable_path = executable_path
        self.first_argument = first_argument
        # format
        self.idef.epoch_f = self.epoch_to_str(self.idef.epoch) if self.idef.epoch not in [-1,None,""] else f'{self.idef.epoch}'

    def epoch_to_str(self,epoch,format="%Y-%m-%d %H:%M:%S"):
        # Convert epoch to datetime object
        dt_object = datetime.datetime.fromtimestamp(epoch)
        # Format
        return dt_object.strftime(format)

# Make instance
PYINST_PROPERTIES = PyInstallerProperties(BUILD_TARGET_IDENTIFIER)