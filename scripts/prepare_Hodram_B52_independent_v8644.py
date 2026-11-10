"""Independent command-atom B52 reconstruction; does not call the sparse producer/compiler."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B52_independent_tools_v8644');assert not root.exists()
    result=derive('scripts/verify_Hodram_B49_reconstruction_v8402.py','scripts/verify_Hodram_B52_reconstruction_v8644.py',{
        'Hodram_B49_independent_v8402':'Hodram_B52_independent_v8644','Hodram_B49_relocation_v8398':'Hodram_B52_relocation_v8642','hodram_B49_editorial_manuscript_v2':'hodram_B52_editorial_manuscript_v3',
        'work/analysis/Hodram_B49_choice_binding_v8387b/current_with_choices.json':'work/analysis/Hodram_B52_current_v8631/current_effective.json',
        '.blocks[49]':'.blocks[52]','len(commands)==36 and len(speeches)==14':'len(commands)==14 and len(speeches)==3','len(original)==26 and len(value)==22':'len(original)==36 and len(value)==32','len(fixups)==8':'len(fixups)==4','blocks[49]=result':'blocks[52]=result','36 disjoint command atoms':'14 disjoint command atoms','Independently rebuild B49':'Independently rebuild B52','Independent36-command-atom':'Independent14-command-atom','8 offsets recomputed':'4 offsets recomputed',
    })
    root.mkdir(parents=True);save(root/'derivation.json',dict(tool=result,all_native_high_integer_constants_andmultiplicity_preserved=True,separate_command_atoms_andindependent_typed_object_andrelative_offsets=True,whole_block_archive_andcomplete_clean_current_inverses_required=True,no_ROM_native_probe_registry_orcredit_change=True,new_credit=0,full_goal_complete=False))
