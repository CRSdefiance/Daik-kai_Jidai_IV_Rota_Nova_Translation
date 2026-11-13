"""Derive the B174 source/current, four-actor, branch and entry proofs."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B174_source_tools_v4453')
OLD='lil_B173_source_v4411/all11_clean_current_complete_context'
NEW='lil_B174_source_v4453/all33_clean_current_complete_context'

if __name__=='__main__':
    assert not ROOT.exists()
    tools=[]
    tools.append(derive('scripts/map_lil_B173_source_v4411.py','scripts/map_lil_B174_source_v4453.py',{
        'Bind11 clean/current complete preambles and23 structural commands':'Bind33 clean/current complete preambles and45 structural commands',
        'lil_B173_source_v4411':'lil_B174_source_v4453',
        'editorial_handoff_verification_v4409b/verified_handoff.json':'promotion_v4452/promotion_receipt.json',
        'lil_B172_source_v4364/all27_clean_current_complete_context':'lil_B173_source_v4411/all11_clean_current_complete_context',
        'lil_B173_clean_context_v4410/all11_complete_B173_exchange':'lil_B174_clean_context_v4451/all33_complete_B174_exchange',
        'prior, history, gloss = map(read, [PRIOR, HISTORY, GLOSS])':
            "prior, history, gloss = map(read, [PRIOR, HISTORY, GLOSS])\n    promotion=read('translations/promoted_build.json')\n    assert promotion['profile']=='all-routes-unified-v4445' and promotion['rom_sha256']==prior['rom_sha256']\n    prior.update(candidate=promotion['rom'],candidate_sha256=prior['rom_sha256'])\n    assert sha(Path('translations/release_stack.json').read_bytes())==prior['updated_files']['translations/release_stack.json']",
        'len(known) == 5789':'len(known) == 5800','blocks[173]':'blocks[174]',
        'len(old) == 23 and len(spoken) == 11':'len(old) == 45 and len(spoken) == 33',
        'selectors = [], [2,202]':'selectors = [], [2,14,26,201]',
        "glosses[f'DK4_MES_B173_R{index:04d}']":"glosses[f'DK4_MES_B174_R{index:04d}']",
        'block=173':'block=174','physical_speeches=11':'physical_speeches=33',
        'all11_clean_current_complete_context.json':'all33_clean_current_complete_context.json',
        'total_editorial_objects=11, speech_objects=11, ordinary_source_speeches=11':
            'total_editorial_objects=33, speech_objects=33, ordinary_source_speeches=33',
        'source_native_commands=23':'source_native_commands=45','all11_clean_first_glosses':'all33_clean_first_glosses',
        'historical_snapshot_is_Lil_London_not_selected_B173':'historical_snapshot_is_Lil_London_not_selected_B174',
        'B173 mapped:11 complete preambles/23 structural commands':'B174 mapped:33 complete preambles/45 structural commands',
    }))
    tools.append(derive('scripts/reconcile_lil_B173_voices_v4412.py','scripts/reconcile_lil_B174_voices_v4454.py',{
        OLD:NEW,'lil_B173_voices_v4412':'lil_B174_voices_v4454','two source-owned':'four source-owned',
        'len(chosen)==2':'len(chosen)==4','::2_source_names':'::4_source_names',
        'current2_static_names':'current4_static_names','fresh2_actor_names':'fresh4_actor_names',
        'all11_dispatches_still_require_separate_proof':'all33_dispatches_still_require_separate_proof',
        '2 static names/voices pass':'4 static names/voices pass',
    }))
    tools.append(derive('scripts/prove_lil_B173_dispatches_v4413.py','scripts/prove_lil_B174_dispatches_v4455.py',{
        OLD:NEW,'lil_B173_dispatches_v4413':'lil_B174_dispatches_v4455','lil_B173_voices_v4412':'lil_B174_voices_v4454',
        'Bind22 source/current speech calls':'Bind66 source/current speech calls',
        'len(cases)==22':'len(cases)==66','all11_source_current_dispatches':'all33_source_current_dispatches',
        'all2_static_actors':'all4_static_actors','actual_selected_B173_IDs':'actual_selected_B174_IDs',
        '22 source/current dispatches pass:two static actors':'66 source/current dispatches pass:four static actors',
    }))
    tools.append(derive('scripts/prove_lil_B173_branches_v4414.py','scripts/prove_lil_B174_branches_v4456.py',{
        OLD:NEW,'lil_B173_branches_v4414':'lil_B174_branches_v4456',
    }))
    tools.append(derive('scripts/prove_lil_B173_entry_v4415.py','scripts/prove_lil_B174_entry_v4457.py',{
        OLD:NEW,'lil_B173_entry_v4415':'lil_B174_entry_v4457','lil_B173_voices_v4412':'lil_B174_voices_v4454',
        'B173':'B174','in [173]':'in [174]',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT/'source_derivation.json',dict(tools=tools,scope=dict(block=174,speeches=33,
        structural_commands=45,selectors=[2,14,26,201],relative_sites=4,predicates=1,
        conditional_food_aside='DK4_MES_B174_R0069',A000_offsets=[2068,2076],C200_offset=2084,end=2086),
        no_ROM_registry_ledger_orcredit_change=True,full_goal_complete=False))
    print('Prepared B174 source/current, four static voices,66 dispatches, four relative sites and entry proofs.')
