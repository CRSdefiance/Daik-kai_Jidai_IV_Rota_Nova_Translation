"""Require actual opcode/extents as well as paired control offsets and results."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B176_actual_word_guards_v4593b')
assert not ROOT.exists()
tool=derive('dk4tool/patch/lil_B176_editorial_v1.py','dk4tool/patch/lil_B176_editorial_v2.py',{
    "and version['selected_B22_command_pairs'][-1]['original_source_offset']==386":
        "and version['selected_B22_command_pairs'][-1]['original_source_offset']==386\n            and version['selected_B22_command_pairs'][-1]['word']==0 and version['selected_B22_command_pairs'][-1]['extent']==4",
    "and version['source_C200']['original_source_offset']==384 and version['source_C200']['result_words']==[3,0]":
        "and version['source_C200']['original_source_offset']==384 and version['source_C200']['result_words']==[3,0]\n            and version['source_C200']['word']==0xC200 and version['source_C200']['extent']==2",
    "and version['source_A000'][0]['result_words']==[3,0]":
        "and version['source_A000'][0]['result_words']==[3,0]\n            and version['source_A000'][0]['word']==0xA000 and version['source_A000'][0]['extent']==8",
})
ROOT.mkdir(parents=True)
save(ROOT/'source_derivation.json',dict(tool=tool,initial_compiler_unexecuted_and_preserved=True,
    reason='Bind every claimed actual A000,C200 and end opcode/extent directly before registration negatives.',
    no_registry_builder_ROM_orledger_change=True,full_goal_complete=False))
