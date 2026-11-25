"""Prepare registered B203 integration,clean-input patch and current startup checks."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_release_tools_v6049')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read('work/analysis/lil_B203_atomic_v6048/atomic_validation_receipt.json')
    assert receipt['positive_records']==22 and receipt['negative_count']==76 and receipt['all_negatives_reject_before_mutation']
    source=Path('scripts/register_lil_B202_v5997.py').read_text(encoding='utf-8');a=source.index('        description=');b=source.index('    updated=',a)
    description="""        description='Complete V5998 plus22 clean-Japanese whole-exchange B203 cordyceps/book-offer/companion-interest/1000-to100 gold reviews:nine revisions/13 justified retentions. All31 commands/22 preambles/nine leaves,21 progressive/one FE FI notice,zero choices/relative sites and one end remain.22 actual English panels/86 complete holds match source regions and original command paths/results;the generated acquisition notice matches at8350. One speech duration differs by1frame;23 shifted command pairs and18 later prompt samples differ,with zero interval RNG differences and matching queried final groups/whole actor/PRNG. No broad simulation,natural activation or complete payment/item-effect claim. Mikhail progressive/catalogue middle-field distinction,Mysterious Old Man source label and unspoken item18 title scope remain bound.207-name and following B43/source-item/Local Product leads stay open.',
        note='Native/source/reference/actual English scope and76 pre-mutation semantic negatives approved. Registered cumulative build,clean-input patch and current startup pending. Main V4701 preserved.')
"""
    tools=[derive('scripts/register_lil_B202_v5997.py','scripts/register_lil_B203_v6049.py',{
        source[a:b]:description,'B202':'B203','lil_B202_editorial_v4':'lil_B203_editorial_v1',
        'registration_v5997':'registration_v6049','all-routes-unified-v5998':'all-routes-unified-v6050','atomic_v5996d':'atomic_v6048',
        'combined_v5947':'combined_v5998','verification_v5981':'verification_v6033','V5947':'V5998',
        "receipt['positive_records']==19":"receipt['positive_records']==22","receipt['negative_count']==69":"receipt['negative_count']==76",
        "len(parent_manifest['batches'])==589":"len(parent_manifest['batches'])==590",'all-routes-unified-v5947':'all-routes-unified-v5998',
        'build_integrated_release_v5997.tmp':'build_integrated_release_v6049.tmp','expected_manifest_batches=590':'expected_manifest_batches=591',
        'Registered experimental V5998:complete V5947 plus B202 once,590 expected batches/114 accepted.69 atomic negatives pass;main V4701 unchanged.':'Registered experimental V6050:complete V5998 plus B203 once,591 expected batches/114 accepted.76 atomic negatives pass;main V4701 unchanged.',
    })]
    tools.append(derive('scripts/build_lil_B202_v5998.py','scripts/build_lil_B203_v6050.py',{
        'B202':'B203','build_v5998':'build_v6050','combined_v5998':'combined_v6050','registration_v5997':'registration_v6049','all-routes-unified-v5998':'all-routes-unified-v6050',
    }))
    tools.append(derive('scripts/verify_lil_B202_release_v5999.py','scripts/verify_lil_B203_release_v6051.py',{
        'B202':'B203','lil_B202_editorial_v4':'lil_B203_editorial_v1','release_v5999':'release_v6051',
        'combined_v5998':'combined_v6050','combined_v5947':'combined_v5998','registration_v5997':'registration_v6049','build_v5998':'build_v6050',
        'all-routes-unified-v5998':'all-routes-unified-v6050','all-routes-unified-v5947':'all-routes-unified-v5998',
        "len(manifest['batches'])==590":"len(manifest['batches'])==591",'all590_manifest_batches':'all591_manifest_batches','reference_v5985':'reference_v6037','V5947':'V5998','manifest_batches=590':'manifest_batches=591',
        "and all(manifest['checks'].values())":"and len(manifest['checks'])==18 and all(manifest['checks'].values())",
        'all_earlier_profiles_and_V4701_promotion_unchanged=True':'all_earlier_profiles_and_V4701_promotion_unchanged=True,all18_registered_release_checks_pass=True',
    }))
    tools.append(derive('scripts/run_lil_B202_regressions_v5998.py','scripts/run_lil_B203_regressions_v6050.py',{'B202':'B203','regressions_v5998':'regressions_v6050'}))
    tools.append(derive('scripts/run_lil_B202_startup_v6000.py','scripts/run_lil_B203_startup_v6052.py',{
        'B202':'B203','runs_v6000':'runs_v6052','_v6000_':'_v6052_','version=5998':'version=6050',
    }))
    tools.append(derive('scripts/verify_lil_B202_startup_v6001.py','scripts/verify_lil_B203_startup_v6053.py',{
        'B202':'B203','startup_v6001':'startup_v6053','runs_v6000':'runs_v6052','combined_v5998':'combined_v6050','combined_v5947':'combined_v5998',
        'lil_B201_runs_v5949':'lil_B202_runs_v6000','V5947':'V5998','Current5998':'Current6050',
    }))
    tools.append(derive('scripts/record_lil_B202_startup_view_v6001.py','scripts/record_lil_B203_startup_view_v6053.py',{
        'B202':'B203','startup_v6001':'startup_v6053','V5947':'V5998',
    }))
    tools.append(derive('scripts/pin_lil_B202_v6002.py','scripts/pin_lil_B203_v6054.py',{
        'B202':'B203','retention_v6002':'retention_v6054','release_v5999':'release_v6051','V5998':'V6050',
    }))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_release_and_startup_tools.json',dict(tools=tools,profile='all-routes-unified-v6050',parent_profile='all-routes-unified-v5998',expected_manifest_batches=591,accepted_layers=114,full_goal_complete=False))
    print('B203 registered-build/patch/regression/startup tools prepared;591 cumulative batches expected.')
