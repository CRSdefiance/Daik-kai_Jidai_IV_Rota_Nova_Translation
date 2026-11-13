"""Prepare cumulative B185 registration and meaningful atomic rejection cases."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B185_registration_tools_v5121')
if __name__=='__main__':
    assert not ROOT.exists();text=Path('scripts/register_lil_B184_v5075.py').read_text(encoding='utf-8')
    a=text.index("        description='Complete V5030");b=text.index('        note=',a)
    description="        description='Complete V5076 plus8 B185 whole-exchange reviews:4 revisions/4 justified retentions. Preserve the cold-weather exchange,fur-coat wish,reported current fur sales/rising prices,hearsay,wish for warmth and continuing desire. One separate Furs/Stockholm FE forecast stays prospective. Exact source/prose-bound R16 wrapping uses2 safe rows without word,font or width change. All11 source commands and9 original B22 initializers execute in paired9001-frame content boots. All8 panels,31 complete holds,115 nontext samples and26 full screens pass. Eight timings,seven later A-indicator differences and unequal final PRNG remain disclosed;final RGB,five native groups and whole actors agree.',\n"
    extras="""    mutations.extend([
        ('lost-ordinary-boundary-reason',str(DOC),lambda v:next(r for r in v['records'] if r['source_record_index']==16).pop('reviewed_ordinary_boundaries')),
        ('false-boundary-mutation-control',doc['source_bound_wrap_refinement_proof'],lambda v:v['exact_source_and_prose_mutation_controls'][0].update(rejected=False)),
    ])
"""
    changes={text[a:b]:description,'B184':'B185','lil_B184_editorial_v2':'lil_B185_editorial_v1',
        'registration_v5075':'registration_v5121','all-routes-unified-v5076':'all-routes-unified-v5122','combined_v5030':'combined_v5076',
        'editorial_handoff_verification_v5058':'editorial_handoff_verification_v5082','reference_approval_v5073':'reference_approval_v5119','loader_v5063':'loader_v5109',
        'native_approval_v5056/all9':'native_approval_v5104b/all8','actual_v5070/actual_all9':'actual_v5116/actual_all8',
        "len(proof['changed_records'])==9":"len(proof['changed_records'])==8",'all9_words_controls_and_prose_unchanged':'all8_words_controls_and_prose_unchanged',
        'eight_other_compiled_targets_exact':'seven_other_compiled_targets_exact','complete_matching_observations=8':'complete_matching_observations=7',
        "('false-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=False))":
        "('concealed-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True))",
        "('lost-household-fact',doc['actor_terminology_reconciliation'],lambda v:v.update(household_tea_is_low_not_city_or_trade_cargo_shortage=False))":
        "('lost-source-reported-sales-price-fact',doc['actor_terminology_reconciliation'],lambda v:v.update(source_explicit_reported_current_fur_sales_and_rising_prices_due_to_cold_must_be_preserved=False))",
        '    for label,path,edit in mutations:reject(label,path,edit)':extras+'    for label,path,edit in mutations:reject(label,path,edit)',
        'all-routes-unified-v5030':'all-routes-unified-v5076','V5030':'V5076','build_integrated_release_v5075.tmp':'build_integrated_release_v5121.tmp',
        'expected_manifest_batches=568':'expected_manifest_batches=569','positive_records=9':'positive_records=8','expected_batches=568':'expected_batches=569'}
    assert all(k in text for k in changes),[k for k in changes if k not in text]
    tool=derive('scripts/register_lil_B184_v5075.py','scripts/register_lil_B185_v5121.py',changes)
    ROOT.mkdir(parents=True);save(ROOT/'prepared.json',dict(tool=tool,source_reported_sales_prices_and_exact_boundary_reason_guarded=True,
        source_native_getter_addresses_not_subject_to_identifier_replacement=True,new_review_credit=0,full_goal_complete=False))
