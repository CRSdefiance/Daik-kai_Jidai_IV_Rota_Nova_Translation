"""Prepare exact-parent registered release and targeted current startup tools."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_release_tools_v5814')
if __name__=='__main__':
    assert not ROOT.exists()
    old=Path('scripts/register_lil_B198_v5755.py').read_text(encoding='utf-8')
    a=old.index("        description=");b=old.index('    updated=',a)
    new="""        description='Complete V5756 plus31 whole-exchange B199 portrait/chase/found-book reviews:11 revisions/20 justified retentions. All47 commands/31 preambles/16 leaves/one FI/pause/two picture layouts/two short47xx and one ending remain. All31 actual panels/120 holds and182 sampled nontext regions match. Six speech duration changes,34 shifted pairs,six advance-prompt differences and unequal PRNG seeds remain explicit;queried final components agree. No natural activation,full-route or broad world-equivalence claim.',
        note='Source/native/reference/English-content and101 semantic pre-mutation negatives approved. Registered build,clean-input patch and current startup pending. Main V4701 preserved.')
"""
    rows=[derive('scripts/register_lil_B198_v5755.py','scripts/register_lil_B199_v5815.py',{
        old[a:b]:new,'B198':'B199','lil_B198_editorial_v2':'lil_B199_editorial_v3',
        'registration_v5755':'registration_v5815','all-routes-unified-v5756':'all-routes-unified-v5816',
        'atomic_v5754':'atomic_v5813c','combined_v5692':'combined_v5756','verification_v5751':'verification_v5811',
        'V5692':'V5756',"receipt['positive_records']==17":"receipt['positive_records']==31",
        "receipt['negative_count']==98":"receipt['negative_count']==101",'==583':'==584',
        'all-routes-unified-v5692':'all-routes-unified-v5756','build_integrated_release_v5755.tmp':'build_integrated_release_v5815.tmp',
        'expected_manifest_batches=584':'expected_manifest_batches=585',
        'Registered experimental V5756:complete V5692 plus B198 once,584 expected batches/114 accepted.98 atomic negatives pass;main V4701 unchanged.':
        'Registered experimental V5816:complete V5756 plus B199 once,585 expected batches/114 accepted.101 atomic negatives pass;main V4701 unchanged.'})]
    rows.append(derive('scripts/build_lil_B198_v5756.py','scripts/build_lil_B199_v5816.py',{
        'B198':'B199','build_v5756':'build_v5816','combined_v5756':'combined_v5816',
        'registration_v5755':'registration_v5815','all-routes-unified-v5756':'all-routes-unified-v5816'}))
    rows.append(derive('scripts/verify_lil_B198_release_v5757.py','scripts/verify_lil_B199_release_v5817.py',{
        'B198':'B199','lil_B198_editorial_v2':'lil_B199_editorial_v3','release_v5757':'release_v5817',
        'combined_v5756':'combined_v5816','combined_v5692':'combined_v5756',
        'registration_v5755':'registration_v5815','build_v5756':'build_v5816','all-routes-unified-v5756':'all-routes-unified-v5816',
        'all-routes-unified-v5692':'all-routes-unified-v5756',"len(manifest['batches'])==584":"len(manifest['batches'])==585",
        'all584_manifest_batches':'all585_manifest_batches','reference_v5733':'reference_v5800','V5692':'V5756','manifest_batches=584':'manifest_batches=585'}))
    rows.append(derive('scripts/run_lil_B198_startup_v5758.py','scripts/run_lil_B199_startup_v5818.py',{
        'B198':'B199','runs_v5758':'runs_v5818','_v5758_':'_v5818_','version=5756':'version=5816'}))
    rows.append(derive('scripts/verify_lil_B198_startup_v5759.py','scripts/verify_lil_B199_startup_v5819.py',{
        'B198':'B199','startup_v5759':'startup_v5819','runs_v5758':'runs_v5818',
        'combined_v5756':'combined_v5816','combined_v5692':'combined_v5756',
        'lil_B197_runs_v5694':'lil_B198_runs_v5758','V5692':'V5756','Current5756':'Current5816'}))
    rows.append(derive('scripts/record_lil_B198_startup_view_v5759.py','scripts/record_lil_B199_startup_view_v5819.py',{
        'B198':'B199','startup_v5759':'startup_v5819','V5692':'V5756'}))
    rows.append(derive('scripts/run_lil_B198_regressions_v5756.py','scripts/run_lil_B199_regressions_v5816.py',{
        'B198':'B199','regressions_v5756':'regressions_v5816'}))
    ROOT.mkdir(parents=True);save(ROOT/'source_locked_registered_release_tools.json',dict(tools=rows,expected_batches=585,
        parent_batches=584,accepted=114,experimental_profile='all-routes-unified-v5816',parent_profile='all-routes-unified-v5756',
        main_V4701_preserved=True,no_promotion_or_pruning_authorized=True,full_goal_complete=False))
    print('Registration/build/patch/current startup/regression tools prepared;585 cumulative batches expected.')
