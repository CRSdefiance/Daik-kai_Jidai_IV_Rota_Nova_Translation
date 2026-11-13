"""Derive the single-write nested compiler while preserving original native-number constants."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B214_atomic_tools_v6729');OUTPUT=Path('dk4tool/patch/lil_B214_editorial_v1.py')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();original=Path('dk4tool/patch/lil_B209_editorial_v3.py');body=original.read_text('utf8').split('def apply_release(',1)[1];body='def apply_release('+body
    changes={
        'B209':'B214','dk4-lil-B209-editorial-release-v3':'dk4-lil-B214-editorial-release-v1',
        "all20_five_individual_gates_true=True,actual_objects=6,actual_pages=8,actual_complete_body_name_holds=25,offline_only_objects=14":"all17_five_individual_gates_true=True,actual_objects=9,actual_pages=9,actual_complete_body_holds=29,actual_complete_name_holds=29,offline_only_objects=8",
        "all20_five_gates_and_exact_reference_obligations_approved=True,all_names_controls_slots_aliases_relative_spans_bounds_and_native_pages_bound=True,actual6_objects8_pages25_body_name_holds_not_all20_gameplay=True,all12_timing12_RNG_two_duration187_broader_RGB_and_final_state_limits_preserved=True,original_event209_dependency85_not_natural_activation_or_earned_progress=True":"all17_five_gates_and_exact_references_approved=True,all_names_controls_slots_aliases_eight_relatives_bounds_and_single_pages_bound=True,actual9_objects9_pages29_body29_name_holds_and8_offline_objects_explicit=True,observed_results_UI_timing_RNG_durations_later_samples_final_components_equal_with_scope=True,original_event214_dependency87_not_natural_activation_or_earned_progress=True",
        'dk4-source-bound-nested-relocation-map-v1':'dk4-lil-B214-source-relocation-map-v1',
        "len(rows)==len(set(ids))==20 and Counter(r['editorial_decision'] for r in rows)=={'revise':17,'retain-wording':3} and Counter(r['kind'] for r in rows)=={'progressive':5,'typed-4100-actor-style-alternative':15}":"len(rows)==len(set(ids))==17 and Counter(r['editorial_decision'] for r in rows)=={'revise':12,'retain-wording':5} and Counter(r['kind'] for r in rows)=={'progressive':10,'typed-4100-actor-style-alternative':7}",
        'blocks[209]':'blocks[214]',"spec['block']==209":"spec['block']==214","row['block']==209":"row['block']==214","r['block']==209":"r['block']==214",'block=209':'block=214',
        '(1148,1148,1148,0,1336,1334,2)':'(1316,1316,1314,2,1304,1302,2)','block[1144:]==bytes(4)':'block[1310:]==bytes(6)',
        "refs={r['id']:r for r in spec['text_records']}":"refs={r['id']:r for r in spec['all_object_references']}",
        "controls['relocated_dispatch_cases']":"controls['dispatch_cases']",
        'Source D0 role1 speaker,automatic original actor voice style ':'Source D0 role1 speaker, automatic original actor voice style ',
        "{2:'Lil Argot',11:'Jam Jack Ludwyan',12:'Yukihisa Genjo Shiraki'}":"{2:'Lil Argot',4:'Janus Pasar',23:'Manuel Almeida'}",
        "row['compiled_stored_alternative_hex']==row['compiled_hex'][2:]":"row['compiled_hex'].startswith('d0')",
        "rowcount==6 and sum(r['actual_record_observed'] for r in rows)==6":"rowcount==11 and sum(r['actual_record_observed'] for r in rows)==9",
        "len(spec['actor_style_commands'])==2":"len(spec['actor_style_commands'])==1",'len(patches)==7':'len(patches)==11',
        'pieces.append(block[last:])':'pieces.append(block[last:1314])','mapped(1148)==1334':'mapped(1314)==1302',
        '[(694,512,4,702),(698,768,338,1040),(1036,256,54,1094),(1090,256,0,1094)]':'[(890,512,4,898),(894,768,4,902),(898,256,68,970),(966,256,0,970),(1172,512,4,1180),(1176,768,4,1184),(1180,256,118,1302),(1298,256,0,1302)]',
        'len(target)==1336':'len(target)==1304','len(commands)==18':'len(commands)==27',
        'dict(source_offset=1144,target_offset=1330,extent=4)':'dict(source_offset=1310,target_offset=1298,extent=4)','target[1330:]':'target[1298:]','len(cases)==20':'len(cases)==40',
        "struct.pack_into('<H',inverse,4,1140)":"struct.pack_into('<H',inverse,4,1306)",
        'bytes(inverse)==block':'bytes(inverse)+block[1314:]==block','newblocks[209]':'newblocks[214]',
        'source_bytes=1148,target_bytes=1336,source_logical_end=1148,target_logical_end=1334,relative_operands=4,source_commands=18':'source_bytes=1316,target_bytes=1304,source_logical_end=1314,target_logical_end=1302,relative_operands=8,source_commands=27',
        'all5_preambles2_D0_objects15_bodies16_slots_and_aliases_preserved':'all10_preambles_one_D0_object_seven_bodies_eight_slots_and_aliases_preserved',
        'native22_pages_actual6_objects8_pages25_holds_offline14_explicit':'native17_pages_actual9_objects9_pages29_holds_offline8_explicit',
        'all_timing_RNG_broader_RGB_and_final_state_limits_retained':'all_observed_equality_and_final_scope_limits_retained'
    }
    planned=checked_text(body,changes);text='"""Atomic B214 compiler: all gates precede the sole archive write."""\nfrom dk4tool.patch.lil_B214_atomic_support_v1 import *\n\n'+planned;compile(text,str(OUTPUT),'exec');OUTPUT.write_text(text,'utf8');ROOT.mkdir(parents=True)
    save(ROOT/'source_locked_atomic_compiler.json',dict(source=str(original),source_sha256=sha(original.read_bytes()),target=str(OUTPUT),target_sha256=sha(OUTPUT.read_bytes()),changes=changes,original_native_high_numbers_and_multiplicity_preserved=True,sole_archive_write_after_all_obligations=True,source1316_full_inverse_target1304_and_original_typed_aliases=True,no_ROM_registry_ledger_or_credit_change=True,full_goal_complete=False));print('B214 atomic nested compiler prepared; positive reconstruction and independent semantic negatives pending.')
