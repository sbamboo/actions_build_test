#fuse:include ./libs/fuse_legacy_ui.py
#fuse:exclude
from libs.fuse_legacy_ui import EventHandler,EventReciever
#fuse:exclude

# Define the main frontend-engine aswell as the class that frontends should inherit from

class FrontEndSchema(dict):
    """
    A `FrontEndSchema` is a dictionary that follows a specific structure,
    that when sent to a `FrontEndSchemaReciever` tells it how to display stuff.

    A `FrontEndSchema` also contains an `EventHandler` under '<FrontEndSchema>.events'

    Example:
    {
        "id": "example",          # REQUIRED FIELD
        "properties": {
            "title": "Example UI"
        },
        "content": {
            "config.backgroundColor": "red",           # The "config" namespace is reserved for configurations,
                                                       # in this example makes the "global" backgroundColor red.
            "components.*.pxperspace": 5,              # The "components" namespace is reserved for modifying components,
                                                       # the frontend must define this behaviour but can call '<FrontEndSchema>.applyComponentsContent(<key>,<value>)' or '<FrontEndSchema>.auto()'
            "text1": "Hello this is example text!",    # Content should generally just have friendly-names,
            "textbox1.content": "Hello world!"         # but may have namespaced names for readability.
        },
        "components: {
            "text1": {
                "type": "labeled_text",
                "label": "Running mode",
                "content": "content.text1" # The "content" namespace is reserved here to fetch fields from content,
                                           # the frontend must define this behaviour but can call '<FrontEndSchema>.getContentValue(<key>)' or '<FrontEndSchema>.auto()'
            }
        },
        "callbacks": {
            "external.window.exit": exit(), # For when a possible "second-window" exits
            "next": next_schema_method(),   # Method to change to next schema
            "exit": exit()                  # Regular callback called "exit"
        }
    }

    Reserved callbacks are:
      `external.window.exit`
      `external.window.minimize`
      `external.window.maximize`

    NOTE! Reserved callbacks still have to be handled by `FrontEndSchemaReciever`

    Callbacks can call methods of the schema object if its an instance of `FrontEndSchema`:
    Using "schema.generic.<method>"
    Context can be sent using "schema.generic.<method>;<str>".
    NOTE! Only one string can be sent as context, the string will be sent as first argument.
          THE FRONTEND MUST IMPLEMENT SCHEMA-CALLBACKS, THE FRONTEND MAY CALL `<FrontEndSchema>.callGenericMethod(<methodNameWithOptionalContext>)` OR IMPLEMENT IT ITSELF!

    NOTE! The frontend may call '<FrontEndSchema>.auto()' to handle genericMethods, contentValues and componentContent.

    NOTE! Callbacks can contain lambda function, theese are recommended to take one param being the `FrontEndSchemaReciever`
          the frontend can call '<FrontEndSchema>.callLambdaCallback(<key>)' which will send the reciever as first arg,
          as long as it is set for the schema using '<FrontEndSchema>.setReciever(<reciever>)'.
    """
    def __init__(self, predict={}, **kwargs):
        super().__init__(**kwargs)
        for k,v in predict.items():
            self[k] = v
        self.reciever = None
        self.events = EventHandler()

    def setReciever(self, reciever):
        self.reciever = reciever

    def callGenericMethod(self, method):
        if not method.startswith("schema.generic."):
            raise ValueError("Methods must be called via schema.generic.<method>")
        method = method.replace("schema.generic.","",1)
        if ";" in method:
            context = method.split(";")[-1]
        if not hasattr(self,method):
            raise AttributeError(f"'{method}' is not a method of this schema!")
        if not callable(self.method):
            raise AttributeError(f"'{method}' exists on this schema but is a method!")
        if context != None:
            return getattr(self,method)(context)
        else:
            return getattr(self,method)()

    def applyComponentsContent(self, key, value):
        if not key.startswith("components."):
            raise ValueError("Components content must use the syntax 'components.<typeOrWildCard>.<property>'")
        if self.get("components") != None:
            key = key.replace("components.","",1)
            type_,prop_ = key.split(".")
            if type_ == "*":
                for k in self["components"].keys():
                    self["components"][k][prop_] = value
            else:
                for k in self["components"].keys():
                    if self["components"][k].get("type") == type_:
                        self["components"][k]["type"] = type_

    def getContentValue(self, key):
        if not key.startswith("content."):
            raise ValueError("Content values must be gotten via 'content.<key>'")
        key = key.replace("content.","",1)
        if self.get("content") != None:
            return self["content"].get(key)

    def auto(self):
        if self.get("content") != None:
            for k,v in self["content"].items():
                if k.startswith("components."):
                    self.applyComponentsContent(key,value)
        if self.get("components") != None:
            for k in self["components"].items():
                for prop,val in self["components"][k].items():
                    if val.starswith("content."):
                        self["components"][k][prop] = self.getContentValue(val)
        if self.get("callbacks") != None:
            for k,v in self["callbacks"].items():
                if v.starswith("schema.generic."):
                    self["callbacks"][k] = lambda: self.callGenericMethod(v)
    
    def callLambdaCallback(self,key):
        if self.get("callbacks") != None:
            if key in self["callbacks"].keys():
                return self["callbacks"][key](self.reciever)

class FrontEndSchemaReciever():
    def __init__(self):
        self.host = None     # The 'host' to the reciever
        self.assembled = False # Whether or not the reciever has been assembled
        self.active = False    # Whether or not the reciever can be assumed to be "visible"
        self.assembly_options = None
        self.active_options = None

    # Core Implementations
    def _on_assemble(self,host,**assembly_options):
        self.host = host
        self.assembled = True
        self.assembly_options = assembly_options

    def _on_destroy(self):
        self.terminate()
        self.host = None
        self.assembled = False
        self.assembly_options = None

    def _launch(self,**active_options):
        if self.assembled == False:
            raise Exception("FrontEndSchemaReciever must be assembled before launch!")
        self.active_options = active_options
        self.active = True

    def _display(self,schema):
        if self.active == False:
            raise Exception("FrontEndSchemaReciever must be active before displaying anything!")
        pass

    def _terminate(self):
        self.active_options = None
        self.active = False

    def _clear(self):
        pass

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

class FrontEndSchemaHost():
    def __init__(self,frontends={}):
        self.frontends = frontends

    def assemble(self, name, reciever, **assembly_options):
        if name in self.frontends.keys():
            raise Exception(f"Name '{name}' is already registered for this host!")
        self.frontends[name] = reciever
        reciever.on_assemble(self,**assembly_options)
    
    def destroy(self, name):
        if name not in self.frontends.keys():
            raise KeyError(f"Name '{name}' is not registered with this host!")
        self.frontends[name].on_destroy()
        del self.frontends[name]


    def launch(self, name="*", **active_options):
        if name == "*":
            for reciever in self.frontends.values():
                reciever.launch(**active_options)
        else:
            if name not in self.frontends.keys():
                raise KeyError(f"Name '{name}' is not registered with this host!")
            self.frontends[name].launch(**active_options)

    def display(self, schema, name="*", __strict_schemas=True):
        if not isinstance(schema,FrontEndSchema) and __strict_schemas == True:
            raise TypeError("Schemas should be of the 'FrontEndSchema' type, to disable check, pass '__strict_schemas=False'!")
        if schema.get("id") == None:
            raise ValueError("The 'id' field is required for schemas!")
        if name == "*":
            for reciever in self.frontends.values():
                reciever.display(schema)
        else:
            if name not in self.frontends.keys():
                raise KeyError(f"Name '{name}' is not registered with this host!")
            self.frontends[name].display(schema)

    def terminate(self, name="*"):
        if name == "*":
            for reciever in self.frontends.values():
                reciever.terminate()
        else:
            if name not in self.frontends.keys():
                raise KeyError(f"Name '{name}' is not registered with this host!")
            self.frontends[name].terminate()
