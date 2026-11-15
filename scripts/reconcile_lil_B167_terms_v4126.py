"""Bind six sail terms to current reviewed Refit prose and active component-label bytes."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_terms_v4126')
SOURCE = Path('work/analysis/lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json')
REVIEW = Path('translations/refit_contextual_final_review_v1.json')
CONFIG = Path('translations/refit_contextual_spritsail_release_v1.json')
TERMS = {'四角帆':('square sail',1287),'三角帆':('lateen sail',1285),
    '上帆':('topsail',1286),'斜帆':('staysail',1288),'船首帆':('spritsail',1268),'船尾帆':('jigger spanker',1269)}

if __name__ == '__main__':
    assert not ROOT.exists()
    source,review,config=map(read,[SOURCE,REVIEW,CONFIG])
    image=NdsImage.open(source['current_ROM'])
    assert sha(Path(source['current_ROM']).read_bytes())==source['current_ROM_sha256']
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    blocks=IlnkContainer.parse(common).blocks
    byid={r['id']:r for r in review['records']}
    bound=[]
    for jp,(en,native_id) in TERMS.items():
        row=byid[f'COMMON_MESSAGE_{native_id}']
        ref=row['integrated_reference']
        value=bytes.fromhex(row['integrated_hex'])
        assert blocks[ref['block']][ref['offset']:ref['offset']+len(value)]==value
        assert en in row['english'].lower() and all(row['review'].values())
        bound.append(dict(source_term=jp,approved_English=en,current_COMMON_message_ID=native_id,
            current_reference=ref,current_complete_bytes_sha256=sha(value),reviewed_English=row['english'],
            reviewed_final_record=row['id'],reviewed_final_file=str(REVIEW),reviewed_final_sha256=sha(REVIEW.read_bytes())))
    for native_id in [1280,1282]:
        row=byid[f'COMMON_MESSAGE_{native_id}'];ref=row['integrated_reference'];value=bytes.fromhex(row['integrated_hex'])
        assert blocks[ref['block']][ref['offset']:ref['offset']+len(value)]==value
    planpath=Path(config['payload_plan'])
    plan=read(planpath)
    patch=plan['ARM9_patch']
    assert (patch['offset'],patch['end'])==(0x133234,0x133240)
    assert arm[patch['offset']:patch['end']]==bytes.fromhex(patch['target_hex'])==b'Spritsail\0\0\0'
    assert struct.unpack_from('<I',arm,patch['sole_exact_label_pointer_reference'])[0]==0x02000000+patch['offset']
    label=b'Jigger Spanker\0'
    at=arm.find(label)
    assert at>=0 and arm.find(label,at+1)<0
    pointer=struct.pack('<I',0x02000000+at)
    references=[n for n in range(0,len(arm)-3,4) if arm[n:n+4]==pointer]
    assert references
    ROOT.mkdir(parents=True)
    save(ROOT/'six_sail_terms_current_Refit_bodies_and_Spritsail_Jigger_labels.json',dict(
        candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),
        source_context_sha256=sha(SOURCE.read_bytes()),current_COMMON_sha256=sha(common),current_ARM9_sha256=sha(arm),
        six_sail_terms_bound_to_complete_current_reviewed_copies=bound,
        both_current_bow_stern_size_restriction_help_copies_exact=True,
        active_Spritsail_component_label_patch=patch,active_Spritsail_pointer_exact=True,
        Jigger_Spanker_label=dict(offset=at,text=label[:-1].decode(),exact_current_pointer_references=references),
        Spritsail_is_existing_reviewed_contextual_UI_spelling_not_new_official_localization_claim=True,
        earlier_title_crop_metadata_offsets_not_reused_as_current_label_addresses=True,
        source_square_lateen_orientation_wind_tradeoffs_and_causal_explanations_preserved=True,
        source_staysail_overlap_small_ship_spritsail_large_ship_jigger_and_multi_mast_wind_facts_not_simplified_away=True,
        do_not_import_extra_Refit_sail_compatibility_or_performance_stats_not_spoken_in_B167=True,
        no_added_numeric_wind_angles_speeds_mast_limits_fees_or_lesson_rewards=True,
        no_new_native_calls_or_actual_display_coverage=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,REVIEW,CONFIG,planpath,Path('docs/glossary.md'),Path(__file__)]},
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('B167 six sail terms bound to exact current reviewed Refit prose;active Spritsail/Jigger labels and pointers verified;no credit.')
