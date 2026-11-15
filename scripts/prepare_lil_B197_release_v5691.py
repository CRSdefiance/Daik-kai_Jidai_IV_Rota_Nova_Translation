"""Prepare registration,cumulative build,clean patch and fresh startup successors."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B197_release_tools_v5691')
if __name__=='__main__':
    assert not ROOT.exists()
    source=Path('scripts/register_lil_B196_v5636.py').read_text(encoding='utf-8')
    start=source.index('        description=');end=source.index('        note=',start)
    description="        description='Complete V5637 plus24 contextual B197 objects:16 revisions/eight justified retentions. Preserve Ian/Alluring Woman voices,Indian classic/celestial maiden/sage,8500 gold,purchase then romantic rebuff,delegated personal apology/gift,and common Ian Charm notice. One2200 proposal/refusal/delegation menu,six relative sites,39 commands,11 exact leaves and one common end remain.21 distinct speech panels/35 observations/128 native holds/all three visible options and normal returns are captured. Retain59 timing/82 later RGB and explicit RNG/state differences without broad simulation equivalence,natural activation,earned affordability,full-route or hardware claims.',\n"
    rows=[derive('scripts/register_lil_B196_v5636.py','scripts/register_lil_B197_v5691.py',{
        source[start:end]:description,'lil_B196_editorial_v3':'lil_B197_editorial_v1','B196':'B197','V5580':'V5637',
        'registration_v5636':'registration_v5691','all-routes-unified-v5637':'all-routes-unified-v5692',
        'atomic_v5635c':'atomic_v5690','combined_v5580':'combined_v5637',
        "receipt['positive_records']==36 and receipt['negative_count']>=90":"receipt['positive_records']==24 and receipt['negative_count']>=80",
        'verification_v5633':'verification_v5675',"len(parent_manifest['batches'])==579":"len(parent_manifest['batches'])==581",
        "registry['profiles']['all-routes-unified-v5580']":"registry['profiles']['all-routes-unified-v5637']",
        "parent_profile='all-routes-unified-v5580'":"parent_profile='all-routes-unified-v5637'",
        'build_integrated_release_v5636.tmp':'build_integrated_release_v5691.tmp','positive_records=36':'positive_records=24'})]
    rows.append(derive('scripts/build_lil_B196_v5637.py','scripts/build_lil_B197_v5692.py',{
        'B196':'B197','build_v5637':'build_v5692','combined_v5637':'combined_v5692','registration_v5636':'registration_v5691','all-routes-unified-v5637':'all-routes-unified-v5692'}))
    rows.append(derive('scripts/verify_lil_B196_release_v5638.py','scripts/verify_lil_B197_release_v5693.py',{
        'lil_B196_editorial_v3':'lil_B197_editorial_v1','B196':'B197','release_v5638':'release_v5693','combined_v5637':'combined_v5692','combined_v5580':'combined_v5637',
        'registration_v5636':'registration_v5691','build_v5637':'build_v5692',
        'all-routes-unified-v5637':'all-routes-unified-v5692','all-routes-unified-v5580':'all-routes-unified-v5637',
        "len(manifest['batches'])==581":"len(manifest['batches'])==583",'reference_v5619':'reference_v5677',
        'all581_manifest_batches':'all583_manifest_batches','V5580':'V5637','manifest_batches=581':'manifest_batches=583'}))
    rows.append(derive('scripts/run_lil_B196_startup_v5639.py','scripts/run_lil_B197_startup_v5694.py',{
        'B196':'B197','runs_v5639':'runs_v5694','_v5639_':'_v5694_','version=5637':'version=5692'}))
    rows.append(derive('scripts/verify_lil_B196_startup_v5640.py','scripts/verify_lil_B197_startup_v5695.py',{
        'work/analysis/lil_B195_runs_v5582':'work/analysis/lil_B196_runs_v5639','B196':'B197','startup_v5640':'startup_v5695','runs_v5639':'runs_v5694',
        'combined_v5637':'combined_v5692','combined_v5580':'combined_v5637','V5580':'V5637','Current5637':'Current5692'}))
    rows.append(derive('scripts/record_lil_B196_startup_view_v5640.py','scripts/record_lil_B197_startup_view_v5695.py',{
        'B196':'B197','startup_v5640':'startup_v5695','V5580':'V5637'}))
    rows.append(derive('scripts/run_lil_B196_regressions_v5637.py','scripts/run_lil_B197_regressions_v5692.py',{
        'B196':'B197','regressions_v5637':'regressions_v5692'}))
    ROOT.mkdir(parents=True);save(ROOT/'prepared_registration_release_and_startup.json',dict(tools=rows,
        profile='all-routes-unified-v5692',parent_profile='all-routes-unified-v5637',expected_manifest_batches=583,accepted_layers=114,
        source_locked_atomic_compiler='dk4tool.patch.lil_B197_editorial_v1',registration_requires_positive_and_all_semantic_negatives=True,
        startup_runs_should_be_serial_after_prior_concurrent_memory_failure=True,
        preserve_every_ROM_and_main_V4701=True,no_registry_or_ROM_or_ledger_mutation_by_preparation=True,full_goal_complete=False))
