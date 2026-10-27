"""Bind ten Lil/Camille/Angel/Snake/Dandy name consumers without a FE actor lookup."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B167_names_v4124b as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_names_v4508')
SOURCE=Path('work/analysis/lil_B175_source_v4503/all32_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B175_voices_v4504/current5_static_names_voices_and207_catalog_rebind.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,voice=map(read,[SOURCE,VOICE]);image=NdsImage.open(source['current_ROM'])
    arm,clean=image.read_file('/__arm9__.bin'),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    text=inspect.getsource(prior.names);anchor='for ident in [2,4,13,23,109]:'
    assert text.count(anchor)==1;text=text.replace(anchor,'for ident in [2,9,183,184,185]:')
    namespace=dict(prior.__dict__);exec(compile(text,__file__+'::five-source-actors','exec'),namespace)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B175_voices_v4504/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(namespace['names']);ctx.machines.pop();assert not ctx.machines
    full={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh5_actor_names']['rows']}
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']};assert len(values)==10
    assert {i:values[i,'full-catalogue'] for i in full}==full=={2:'Lil Argot',9:'Camille Marinus Overijssel',183:'Angel',184:'Snake',185:'Dandy'}
    progressive={i:values[i,'progressive-nameplate'] for i in full}
    assert progressive=={2:'Lil Argot',9:'Camille Overijssel',183:'Angel',184:'Snake',185:'Dandy'}
    owned=[r for r in native['rows'] if r['actor_ID'] in [2,9]];readonly=[r for r in native['rows'] if r['actor_ID'] in [183,184,185]]
    assert len(owned)==4 and all(r['original_scratch_rings'] and r['original_getter_writes'] for r in owned)
    assert len(readonly)==6 and all(r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring' and not r['original_scratch_rings'] and not r['original_getter_writes'] for r in readonly)
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in native['rows'])
    save(ROOT/'ten_original_name_consumers_owned_and_readonly_paths.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_ten_consumer_cases=native,
        full_catalogue_values=full,progressive_nameplate_values=progressive,approved_prose_names={'2':'Lil','9':'Camille','183':'Angel','184':'Snake','185':'Dandy'},
        FE254_is_anonymous_null_actor_paper_not_a_static_name_or_guessed_woman_identity=True,
        source_B7_B8_B9_are_static_actors183184185_not_literal_halfwidth_prose=True,
        Camille_catalogue_middle_name_not_imported_into_source_given_name_addresses=True,
        source_diminutive_group_address_does_not_require_narrating_Camille_as_a_girl=True,
        no_new_asset_spelling_or_source_rank_relationship_invented=True,later_older_record0D_reaudit_stays_open=True,not_actual_B175_nameplate_observation=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(prior.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(progressive=progressive,full=full,owned_name_paths=4,readonly_paths=6,FE_static_getter_calls=0,credit=0))
