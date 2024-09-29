#fuse:include ../libs/fuse_legacy_ui.py

class ExampleCliFrontEnd(FrontEndSchemaReciever):
    def __init__(self):
        super().__init__()
        self._console = Console()
        self._text = Text(self._console.terminal)

    # Overridable Implementations
    def on_assemble(self,host,**assembly_options):
        '''Called on assemble, can do eventuall background-setup.'''
        self._on_assemble(host)

    def on_destroy(self):
        '''Called on destroy, should terminate and clean up.'''
        self.terminate()
        self._on_destroy()

    def launch(self,**active_options):
        '''Launches "second-window" applications and starts eventual listeners. (Called on expected-init of schema-reciever)'''
        self._launch(**active_options)

    def display(self,schema):
        '''Requests a schema to be displayed.'''
        self._display(schema)
        ml = 0
        for k in schema["content"].keys():
            if len(k) > ml: ml = len(k)
        for k,v in schema["content"].items():
            s = "{f.magenta}"+str(k)+((ml-len(k))*" ")+"{f.darkgray} : {f.magenta}"+str(v)+"{r}"
            print(self._text.parse(s))

    def terminate(self):
        '''Terminates any "second-window" applications and stops eventual listeners. (Called on expected-stop of schema-reciever)'''
        self._terminate()