from math import pi
from info import Info
from state import State
from transition import Transition

class FSM: 
    
    class StateTransition():
        def __init__(self, transition: Transition, target: State):
            self.transition = transition
            self.target = target
    
    
    def __init__(self, framesPerSecond, makeVideo):
        self._directionAngle = 0
        self._info = Info(framesPerSecond, makeVideo)
        self._stateMachine = {}
        self._pressSpaceBar = False
        
        
    def add(self, source: State, transition: Transition, target: State):
        trans = self._stateMachine.get(source, None)
        
        if (trans is None):
            trans = []
            
        trans.append(self.StateTransition(transition, target))    
        self._stateMachine[source] = trans
    
    
    def ready(self,  starter: State):
        self.initial = self.current = starter
        print("States: ", str(starter), end='')
    
    
    def tick(self):
        
        self._info.tick()
        
        stateTrans = self._stateMachine.get(self.current, None)
        
        if stateTrans is None:
            return self.current.tick(self._info)
        
        for st in stateTrans:
            tran = st.transition
            if (tran.evaluate(self._info)):
                target = st.target
                print("->", str(target), end='')
                self.current = target
                return target.tick(self._info)
        
        return self.current.tick(self._info)
                        
        
    def getInfo(self):
        return self._info