"""Prepare the full registered B200 release and focused current startup verification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_release_tools_v5870')
if __name__=='__main__':
    assert not ROOT.exists();receipt=read('work/analysis/lil_B200_atomic_v5869/atomic_validation_receipt.json')
    assert receipt['positive_records']==19 and receipt['negative_count']==110 and receipt['all_negatives_reject_before_mutation']
    old=Path('scripts/register_lil_B199_v5815.py').read_text(encoding='utf-8');a=old.index('        description=');b=old.index('    updated=',a)
    new="""        description='Complete V5816 plus19 whole-exchange B200 collapse/inn-recovery/rescue/thanks reviews:13 revisions/six justified retentions. All31 commands/19 preambles/12 leaves/two distinct FE/zero macros and one ending remain. All19 actual panels/73 holds match native text/source regions.172 of182 nontext samples match;ten subsequent sailing-cloud and six prompt differences remain explicit,as do eight speech-duration changes,19 shifted pairs and unequal PRNG. Queried final native components agree;no natural activation,full-route or broad simulation claim. Stranger name target remains separate.',
        note='Source/native/reference/English-content and110 semantic pre-mutation negatives approved. Registered build,clean-input patch and current startup pending. Main V4701 preserved.')
"""
    rows=[derive('scripts/register_lil_B199_v5815.py','scripts/register_lil_B200_v5871.py',{
        old[a:b]:new,'B199':'B200','lil_B199_editorial_v3':'lil_B200_editorial_v1',
        'registration_v5815':'registration_v5871','all-routes-unified-v5816':'all-routes-unified-v5872',
        'atomic_v5813c':'atomic_v5869','combined_v5756':'combined_v5816','verification_v5811':'verification_v5867',
        'V5756':'V5816',"receipt['positive_records']==31":"receipt['positive_records']==19",
        "receipt['negative_count']==101":"receipt['negative_count']==110",'==584':'==585',
        'all-routes-unified-v5756':'all-routes-unified-v5816','build_integrated_release_v5815.tmp':'build_integrated_release_v5871.tmp',
        'expected_manifest_batches=585':'expected_manifest_batches=586',
        'Registered experimental V5816:complete V5756 plus B199 once,585 expected batches/114 accepted.101 atomic negatives pass;main V4701 unchanged.':
        'Registered experimental V5872:complete V5816 plus B200 once,586 expected batches/114 accepted.110 atomic negatives pass;main V4701 unchanged.'})]
    rows.append(derive('scripts/build_lil_B199_v5816.py','scripts/build_lil_B200_v5872.py',{
        'B199':'B200','build_v5816':'build_v5872','combined_v5816':'combined_v5872',
        'registration_v5815':'registration_v5871','all-routes-unified-v5816':'all-routes-unified-v5872'}))
    rows.append(derive('scripts/verify_lil_B199_release_v5817.py','scripts/verify_lil_B200_release_v5873.py',{
        'B199':'B200','lil_B199_editorial_v3':'lil_B200_editorial_v1','release_v5817':'release_v5873',
        'combined_v5816':'combined_v5872','combined_v5756':'combined_v5816',
        'registration_v5815':'registration_v5871','build_v5816':'build_v5872','all-routes-unified-v5816':'all-routes-unified-v5872',
        'all-routes-unified-v5756':'all-routes-unified-v5816',"len(manifest['batches'])==585":"len(manifest['batches'])==586",
        'all585_manifest_batches':'all586_manifest_batches','reference_v5800':'reference_v5853','V5756':'V5816','manifest_batches=585':'manifest_batches=586'}))
    rows.append(derive('scripts/run_lil_B199_startup_v5818.py','scripts/run_lil_B200_startup_v5874.py',{
        'B199':'B200','runs_v5818':'runs_v5874','_v5818_':'_v5874_','version=5816':'version=5872'}))
    rows.append(derive('scripts/verify_lil_B199_startup_v5819.py','scripts/verify_lil_B200_startup_v5875.py',{
        'B199':'B200','startup_v5819':'startup_v5875','runs_v5818':'runs_v5874',
        'combined_v5816':'combined_v5872','combined_v5756':'combined_v5816',
        'lil_B198_runs_v5758':'lil_B199_runs_v5818','V5756':'V5816','Current5816':'Current5872'}))
    rows.append(derive('scripts/record_lil_B199_startup_view_v5819.py','scripts/record_lil_B200_startup_view_v5875.py',{
        'B199':'B200','startup_v5819':'startup_v5875','V5756':'V5816'}))
    rows.append(derive('scripts/run_lil_B199_regressions_v5816.py','scripts/run_lil_B200_regressions_v5872.py',{
        'B199':'B200','regressions_v5816':'regressions_v5872'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_registered_release_tools.json',dict(tools=rows,expected_batches=586,parent_batches=585,accepted=114,
        experimental_profile='all-routes-unified-v5872',parent_profile='all-routes-unified-v5816',main_V4701_preserved=True,
        no_promotion_or_pruning_authorized=True,full_goal_complete=False))
    print('B200 registration/build/patch/current startup/regression tools prepared;586 cumulative batches expected.')
