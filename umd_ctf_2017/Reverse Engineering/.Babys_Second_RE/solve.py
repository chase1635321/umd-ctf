#!/usr/bin/python3

import sys, angr, claripy
import IPython

def main():
    p = angr.Project('baby2', use_sim_procedures=True)

    symbolic_input = claripy.BVS('sybmolic_input', 200)
    state = p.factory.entry_state(args=[p.filename, symbolic_input])

    sim = p.factory.simulation_manager(state)
    
    #sim.explore(find=0x004031a3)
    sim.explore(find=correct, avoid=incorrect)
    
    print ("Found: {}".format(len(sim.found)))
    if len(sim.found) > 0:
        print(sim.found[0].solver.eval(key, cast_to=bytes))

def correct(state):
    stdout = state.posix.dumps(1)
    print(str(stdout))

    if b'Correct' in stdout:
        print("FOUND IT")

    return b'Correct' in stdout

def incorrect(state):
    stdout = state.posix.dumps(1)
    print(str(stdout))
    return b'WRONG' in stdout

    return 0

print(main())
