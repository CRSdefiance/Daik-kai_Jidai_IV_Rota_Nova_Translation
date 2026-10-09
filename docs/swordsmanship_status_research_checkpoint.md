# Swordsmanship/HP research: integrated into V157

This research is integrated into complete experimental combined V157. See
[V157 checkpoint](all_routes_unified_v157_checkpoint.md) for exact identities,
native proofs, changed bytes, regression results and remaining gameplay limits.

Initial research proved a 144×12 local bitmap but had not traced parent cropping.
That was insufficient: the actual parent crops 60/60/24-pixel regions. Natural
unpositioned English crosses crop boundaries, and the state crop cuts words.

The final formatter generates two twelve-cell numeric columns followed by the
whole state. The view is 156×12; the third crop is 36 pixels at parent x66.
Both native constructors, actual image metadata and primary three-crop dispatch
execute in bounded native checks. Complete pixels and CPU-composed captured
requests pass for both actors, modes, numeric extremes and every state. All
local and paired parent sheets were inspected before formatting approval.

The variadic-stack hazard is reproduced and guarded by a twelve-byte tail helper.
Safe SDK/ARM7 loading and arenas pass; original DTCM and inherited helpers remain
exact. ITCM ends at 01FF9FEC and aligns to overlay boundary 01FFA000. Further
resident helpers require separate proven allocation.

Full skill/equipment inputs, clearing, registration, surrounding art and GPU
submission remain explicit contracts. Physical cold boot/gameplay are pending.
No canonical acceptance or full-goal completion is claimed.
