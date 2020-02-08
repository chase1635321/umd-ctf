import angr, sys, claripy
import IPython

def temp():
    p = angr.Project("baby2")
    simgr = p.factory.simulation_manager(p.factory.full_init_state())
    simgr.explore(find=0x004031a3)

    return simgr.found[0].solver.eval(key, cast_to=bytes))

print(str(temp()))
