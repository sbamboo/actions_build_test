class ExampleTkinterFrontEnd(FrontEndSchemaReciever):
    def __init__(self):
        super().__init__()

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
        
    def terminate(self):
        '''Terminates any "second-window" applications and stops eventual listeners. (Called on expected-stop of schema-reciever)'''
        self._terminate()
        
    def clear(self):
        '''Clears the frontend.'''
        self._clear()