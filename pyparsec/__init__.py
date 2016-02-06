class State:
    __slots__ = ('value', 'state')
    
    def __init__(self, value, state):
        self.value = value
        self.state = state
        
    def bind(self, fn):
        return fn(self.value, self.state)

    def do(self, fns):
        s = self
        for fn in fns:
            s = s.bind(fn)
        return s
        
    __rshift__ = bind
    
    def __str__(self):
        return 'State(value={0}, state={1})'.format(repr(self.value), repr(self.state))

class Parser:
    __slots__ = ('fn', )
    
    def __init__(self, fn):
        self.fn = fn

    def __call__(self, *args):
        return self.fn(*args)

    def __or__(self, other):
        @Parser
        def inner(*args):
            try:
                return self(*args)
            except:
                return other(*args)
        return inner

    def map(self, fn):
        @Parser
        def inner(value, state):
            s = self(value, state)
            return State(fn(value, s.value), s.state)
        return inner
    
    def to(self, fn):
        return self.map(lambda _, value: fn(value))

    def bind(self, other):
        return Parser(lambda *args: self(*args).bind(other))

    __rshift__ = bind

class ParseError(ValueError): pass