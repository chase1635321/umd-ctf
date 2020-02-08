#!/usr/bin/python3

import sys, angr, claripy
import IPython

def main():
    p = angr.Project('hashmenot', use_sim_procedures=True)

    #state = p.factory.entry_state(args=[p.filename, symbolic_input])

    symbolic_input = claripy.BVS('sybmolic_input', 80)

    state = p.factory.entry_state(args=[p.filename], stdin=symbolic_input)

    sim = p.factory.simulation_manager(state)
    
    sim.explore(find=0x400a2b, avoid=0x400a06)
    
    if len(sim.found) > 0:
        print ("Found: {}".format(len(sim.found)))
        print(sim.found[0].solver.eval(key, cast_to=bytes))
    else:
        print("None found")

def correct(state):
    stdout = state.posix.dumps(1)
    print(str(stdout))
    return b'verified' in stdout

def incorrect(state):
    stdout = state.posix.dumps(1)
    print(str(stdout))
    return b'rejected' in stdout

    return 0

print(main())
