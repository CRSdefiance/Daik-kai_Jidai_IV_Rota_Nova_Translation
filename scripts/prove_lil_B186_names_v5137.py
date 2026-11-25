"""Execute every source actor's progressive and full-catalogue name consumers."""
from pathlib import Path
import inspect
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B186_names_v5137')
SOURCE=Path('work/analysis/lil_B186_source_v5132/all12_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B186_voices_v5133/current207_catalog_eight_voices_and_two_source_selectors.json')
if __name__=='__main__':
    assert not ROOT.exists();packet,voice=read(SOURCE),read(VOICE)
    assert voice['source_context_sha256']==sha(SOURCE.read_bytes())
    source=inspect.getsource(names);assert source.count('for ident in [2,4,13,23,109]:')==1
    source=source.replace('for ident in [2,4,13,23,109]:','for ident in [174,175]:')
    env=dict(names.__globals__);exec(compile(source,__file__+'::source-two-name-consumers','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B186_voices_v5133/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines
    assert len(native['rows'])==4 and all(r['text'] and r['all_actor_models_and_unowned4MiB_exact'] for r in native['rows'])
    assert {(r['actor_ID'],r['consumer']) for r in native['rows']}=={(i,c) for i in [174,175] for c in ['progressive-nameplate','full-catalogue']}
    catalogue={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh2_actor_names']['rows']}
    assert {r['actor_ID']:r['text'] for r in native['rows'] if r['consumer']=='full-catalogue'}==catalogue
    save(ROOT/'four_original_progressive_and_catalogue_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),native_four_consumer_cases=native,
        progressive_nameplate_values={r['actor_ID']:r['text'] for r in native['rows'] if r['consumer']=='progressive-nameplate'},
        full_catalogue_values=catalogue,source_owned_adapter=source,current_context_plan=str(ctx.proof_path),current_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        prose_roles_pending_manual_terminology_reconciliation=True,not_actual_B186_nameplate_observation=True,
        no_asset_ROM_emulator_or_review_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Four source-owned name consumers bound;progressive/catalogue roles remain separate. No actual scene observation or prose approval.')
