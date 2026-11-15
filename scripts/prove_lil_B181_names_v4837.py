"""Six source-owned generic Lady name consumers with no inferred nobility."""
from pathlib import Path
import inspect
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B181_names_v4837')
SOURCE=Path('work/analysis/lil_B181_source_v4832/all10_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    source=inspect.getsource(names);assert source.count('for ident in [2,4,13,23,109]:')==1
    source=source.replace('for ident in [2,4,13,23,109]:','for ident in [166,167,168]:')
    namespace=dict(names.__globals__);exec(compile(source,__file__+'::A6-A7-name-consumers','exec'),namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B181_voices_v4833/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(namespace['names']);ctx.machines.pop();assert not ctx.machines
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    assert values=={(i,c):'Lady' for i in [166,167,168] for c in ['progressive-nameplate','full-catalogue']}
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in native['rows'])
    save(ROOT/'six_original_Lady_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),native_six_consumer_cases=native,
        approved_prose_names={'166':'Lady','167':'Lady','168':'Lady'},generic_source_roles_not_proof_of_noble_rank_marriage_or_relationship=True,
        referenced_wearer_is_source_explicit_lady_without_bound_name_rank_relation_or_gift_provenance=True,
        all4MiB_preserved_by_six_readonly_getter_paths=True,current_context_plan=str(ctx.proof_path),
        source_owned_adapter=source,new_emulator_runs=0,actual_B181_nameplate_observation=False,
        no_new_name_asset_or_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Six current Lady166/167/168 progressive/catalogue names pass;all4MiB preserved,no inferred rank or relationship.')
