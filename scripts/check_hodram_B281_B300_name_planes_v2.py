"""Resume name planes with the unchanged original renderer module, preserving the failed bridge."""
from types import FunctionType
from scripts import check_hodram_B281_B300_name_planes_v1 as previous

env={**previous.env,'previous':previous.previous.env['previous'],
     'OUT':previous.ROOT/'name_planes_v2','INPUT':previous.ROOT/'name_plane_inputs_v2','__file__':__file__}
main=FunctionType(previous.env['main'].__code__,env)
if __name__=='__main__':main()
