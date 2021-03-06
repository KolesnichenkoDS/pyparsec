from . import *
import functools, re

def string(s):
    @Parser
    def inner(value, state):
        if state[:len(s)] == s:
            return State(s, state[len(s):])
        raise ParseError(repr(state))
    return inner

def regex(r):
    @Parser
    def inner(value, state):
        try:
            m = re.compile(r).match(state).group()
            return State(m, state[len(m):])
        except:
            raise ParseError(repr(state))
    return inner

def repeat(p, min=0, max=None):
    @Parser
    def inner(_, state):
        s = State([], state)
        while max == None or max > 0:
            try:
                s = s.bind(p.map(lambda l, v: l + [v]))
            except:
                if min < 1: return s
                raise ParseError(repr(state))
    return inner

def ignore(p):
    @Parser
    def inner(value, state):
        return State(value, state).bind(p.map(lambda val, _: val))
    return inner
    
def maybe(p):
    @Parser
    def inner(value, state):
        try:
            return p(value, state)
        except:
            return State(value, state)
    return inner

def lazy(f):
    @Parser
    def inner(value, state):
        return (f() if callable(f) else eval(f))(value, state)
    return inner

def append(p):
    return p.map(lambda l, v: l + [v])
    
def oneof(*ps):
    return functools.reduce(lambda p1, p2: p1 | p2, ps)
    
def seq(*ps):
    return functools.reduce(lambda p1, p2: p1 >> p2, ps)

digits = regex(r'\d+')

spaces = regex(r'\s+')

spaces0 = regex(r'\s*')