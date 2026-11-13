"""Prepare B173 complete source/current,two-actor and nested-control contracts."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B173_source_tools_v4411')
OLD=Path('scripts/map_lil_B172_source_v4364.py')
NEW=Path('scripts/map_lil_B173_source_v4411.py')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    a=text.index('        if index == 11:');b=text.index('        row.update(',a)
    text=text[:a]+text[b:]
    changes={'B172':'B173','lil_B172_source_v4364':'lil_B173_source_v4411',
        'editorial_handoff_verification_v4363':'editorial_handoff_verification_v4409b',
        'lil_B171_source_v4311/all37_clean_current_complete_context':'lil_B172_source_v4364/all27_clean_current_complete_context',
        'clean_context_v4361/all27_complete_B172_exchange':'clean_context_v4410/all11_complete_B173_exchange',
        'len(known) == 5762':'len(known) == 5789','blocks[172]':'blocks[173]',
        'len(old) == 38 and len(spoken) == 27':'len(old) == 23 and len(spoken) == 11',
        'selectors = [], [2,26,201]':'selectors = [], [2,202]',
        "sum(command['word'] in [0x100,0x200,0x300,0x400] for command in old) == 0":"sum(command['word'] in [0x100,0x200,0x300,0x400] for command in old) == 4",
        'block=172':'block=173','physical_speeches=27':'physical_speeches=11','relative_sites=0':'relative_sites=4',
        'all27_clean_current_complete_context':'all11_clean_current_complete_context',
        'total_editorial_objects=27, speech_objects=27, ordinary_source_speeches=27':'total_editorial_objects=11, speech_objects=11, ordinary_source_speeches=11',
        'all27_clean_first_glosses':'all11_clean_first_glosses','source_native_commands=38':'source_native_commands=23',
        'source_relative_sites=0, source_predicates=0':'source_relative_sites=4, source_predicates=1',
        'Bind27 clean/current complete preambles and38 commands':'Bind11 clean/current complete preambles and23 structural commands',
        'B172 mapped:27 complete preambles/38 commands/no relative sites,no macros':'B173 mapped:11 complete preambles/23 structural commands/four relative sites/one predicate,no macros',
    }
    for key in changes:assert key in text,key
    text=re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)),lambda m:changes[m[0]],text)
    assert 'clean_context_v4410' in text and 'B172' not in text.replace('lil_B172_source_v4364/all27_clean_current_complete_context','')
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8',newline='\n')
    tools=[dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),successor=str(NEW),successor_sha256=sha(NEW.read_bytes()))]
    old='lil_B172_source_v4364/all27_clean_current_complete_context';new='lil_B173_source_v4411/all11_clean_current_complete_context'
    tools.append(derive('scripts/reconcile_lil_B172_voices_v4365.py','scripts/reconcile_lil_B173_voices_v4412.py',{
        'lil_B172_voices_v4365':'lil_B173_voices_v4412',old:new,'len(chosen)==3':'len(chosen)==2',
        'three source-owned':'two source-owned','::3_source_names':'::2_source_names',
        'current3_static_names':'current2_static_names','fresh3_actor_names':'fresh2_actor_names',
        'all27_dispatches_still_require_separate_proof':'all11_dispatches_still_require_separate_proof',
        '3 static names/voices pass':'2 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B172_dispatches_v4366.py','scripts/prove_lil_B173_dispatches_v4413.py',{
        'Bind54 source/current speech calls and11 exact non-relative control leaves.':'Bind22 source/current speech calls and8 exact non-relative control leaves.',
        'lil_B172_dispatches_v4366':'lil_B173_dispatches_v4413',old:new,'lil_B172_voices_v4365':'lil_B173_voices_v4412',
        'len(cases)==54 and len(leaves)==11':'len(cases)==22 and len(leaves)==8',
        'all27_source_current_dispatches_no_macros_and11_control_leaves':'all11_source_current_dispatches_no_macros_and8_control_leaves',
        'all11_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact':'all8_nonrelative_nonspeech_nonchoice_source_current_leaf_commands_exact',
        'all3_static_actors':'all2_static_actors','actual_selected_B172_IDs':'actual_selected_B173_IDs',
        '54 source/current dispatches pass:three static actors,no macros/noFE. All11 nonrelative nontext leaves exact.':'22 source/current dispatches pass:two static actors,no macros/noFE. All8 nonrelative nontext leaves exact.',
    }))
    tools.append(derive('scripts/prove_lil_B172_branches_v4367.py','scripts/prove_lil_B173_branches_v4414.py',{
        'lil_B172_branches_v4367':'lil_B173_branches_v4414',old:new,
    }))
    tools.append(derive('scripts/prove_lil_B172_entry_v4368.py','scripts/prove_lil_B173_entry_v4415.py',{
        'lil_B172_entry_v4368':'lil_B173_entry_v4415',old:new,'lil_B172_voices_v4365':'lil_B173_voices_v4412',
        'B172':'B173','in [172]':'in [173]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,source_scope=dict(block=173,speeches=11,structural_commands=23,
        selectors=[2,202],FI=0,FA=0,FO=0,relative_sites=4,predicates=1,nonrelative_leaves=8,
        A000_offsets=[720,748],predicate_offset=728,end_offsets=[762],pause=0),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B173 source/current,two voices,22 dispatches,four-relative-site and entry producers;11 clean glosses precede English.')
