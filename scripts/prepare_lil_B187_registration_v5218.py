"""Prepare cumulative registration with scene-specific meaningful negatives."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT=Path('work/analysis/lil_B187_registration_tools_v5218')
if __name__=='__main__':
    assert not ROOT.exists();source=Path('scripts/register_lil_B185_v5121.py');text=source.read_text(encoding='utf-8')
    removals=[line for line in text.splitlines(True) if 'source_bound_wrap_refinement_proof' in line and 'postscene_native_state_proof' not in line]
    removals += [line for line in text.splitlines(True) if "('lost-ordinary-boundary-reason'" in line]
    a=text.index("        description='Complete V5076");b=text.index('        note=',a)
    description="        description='Complete V5177 plus16 B187 whole-exchange reviews:7 revisions/9 justified retentions. Sailor155 progressive label remains distinct from catalogue Retainer;Shopkeeper87 and original voices4/0 are preserved. Keep cough,qualified reassurance,speculation,forgotten remedy name,reported almond ingredient,memory trigger,reported exceptional efficacy and strong sales,parallel search intentions and tentative Almonds/Malacca notice. All19 source commands,A000,C200,end and2 tailzeros remain. All16 actual panels,63 holds,115 nontext samples,12 full screens and normal return pass. Sixteen timings differ;sampled postscene/final RGB,five native groups,whole actor and measured final PRNG agree within disclosed fixture scope. No wrap exception,font or guard change.',\n"
    changes={line:'' for line in removals}
    changes.update({text[a:b]:description,'B185':'B187','registration_v5121':'registration_v5218',
        'all-routes-unified-v5122':'all-routes-unified-v5219','combined_v5076':'combined_v5177','all-routes-unified-v5076':'all-routes-unified-v5177','V5076':'V5177',
        'editorial_handoff_verification_v5082':'editorial_handoff_verification_v5183','editorial_manuscript_v5':'editorial_manuscript_v4',
        'lil_B185_layout_v2.py':'lil_B187_layout_v1.py','reference_approval_v5119':'reference_approval_v5216','loader_v5109':'loader_v5206',
        'native_approval_v5104b/all8':'native_approval_v5201/all16','actual_v5116/actual_all8':'actual_v5213/actual_all16',
        ",'source_bound_wrap_refinement_proof'":'',"len(proof['changed_records'])==8":"len(proof['changed_records'])==16",
        "'{SPEAKER:A6}Hello.'":"'{SPEAKER:9B}Hello.'",'complete_matching_observations=7':'complete_matching_observations=15',
        "('concealed-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=True))":"('false-final-RNG-inequality',doc['postscene_native_state_proof'],lambda v:v.update(PRNG_equality=False))",
        "if r['actor_ID']==164":"if r['actor_ID']==155",'wrong-progressive-couple-role':'wrong-progressive-Sailor-role','wrong-catalogue-couple-role':'wrong-catalogue-Retainer-role',
        "{'164':'Woman in a Couple'}":"{'155':'Retainer'}","{'165':'Man in a Couple'}":"{'155':'Sailor'}",
        'lost-source-reported-sales-price-fact':'lost-source-reported-efficacy-sales-fact',
        'source_explicit_reported_current_fur_sales_and_rising_prices_due_to_cold_must_be_preserved':'source_explicit_reported_remedy_effectiveness_and_strong_sales_both_must_be_preserved',
        'build_integrated_release_v5121.tmp':'build_integrated_release_v5218.tmp',
        'expected_manifest_batches=569':'expected_manifest_batches=571','positive_records=8':'positive_records=16','expected_batches=569':'expected_batches=571',
    })
    row=derive(source,'scripts/register_lil_B187_v5218.py',changes)
    result=Path(row['successor']).read_text(encoding='utf-8')
    assert 'source_bound_wrap_refinement_proof' not in result and 'ordinary-boundary' not in result
    ROOT.mkdir(parents=True);save(ROOT/'prepared_atomic_registration.json',dict(derivation=row,
        parent_profile='all-routes-unified-v5177',profile='all-routes-unified-v5219',source_metadata_name_voice_reported_remedy_and_measured_scope_negatives=True,
        no_ROM_registry_or_credit_change=True,full_goal_complete=False))
