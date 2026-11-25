"""Derive production sparse reconstruction for B52 with its two distinct full ends."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B52_reconstruction_tools_v8665')
    assert not root.exists()
    receipt = derive('dk4tool/patch/hodram_B49_reconstruction_v2.py', 'dk4tool/patch/hodram_B52_reconstruction_v1.py', {
        'Hodram B49 reconstruction:': 'Hodram B52 reconstruction:',
        "require(group['block']==packet['block'] and group['file_path']=='/data/SC1.DK4','file/block identity')": """require(group['block']==packet['block']==52 and group['file_path']=='/data/SC1.DK4','file/block identity')
    require(len(rows)==3 and len(packet['all_current_commands'])==14 and len(group['relative_fixups'])==4,'complete B52 command/speech/relative set')
    require([c['whole_command_hex'] for c in packet['all_current_commands'] if c['word']==0]==['00000000','00000080'],'both distinct complete source ends')
    require([c['whole_command_hex'] for c in group['all_target_commands'] if c['word']==0]==['00000000','00000080'],'both distinct complete target ends')
    require([c['offset'] for c in packet['all_current_commands'] if c['word']==0]==[166,224] and [c['offset'] for c in group['all_target_commands'] if c['word']==0]==[158,232],'normal/flagged source andtarget end addresses')""",
        'at==574 and len(before)==len(ja)==choice[\'old_length\']==26': 'at==68 and len(before)==len(ja)==choice[\'old_length\']==36',
        'old[at:at+26]==before and clean[at:at+26]==ja': 'old[at:at+36]==before and clean[at:at+36]==ja',
        "len(typed)==choice['new_length']==22": "len(typed)==choice['new_length']==32",
        "==row['compiled_hex'] and len(row['english'])": "==row['compiled_choice_label_hex'] and len(row['english'])",
        'end=at+26,old=before': 'end=at+36,old=before',
        "choice['new_offset']==518": "choice['new_offset']==72",
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=receipt, both_distinct_end_words_explicitly_bound=True,
         all_original_inverse_parity_native_extent_relative_scope_choiceorder_guards_retained=True,
         native_effect_semantics_not_invented=True, no_ROM_orcredit=True))
