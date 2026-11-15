"""Bind six source-owned Barkeep/Patron/Retainer name consumers without guessed ownership."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B167_names_v4124b as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B179_names_v4713')
SOURCE=Path('work/analysis/lil_B179_source_v4708/all14_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B179_voices_v4709/current3_static_names_voices_and207_catalog_rebind.json')

if __name__=='__main__':
    assert not ROOT.exists()
    source,voice=read(SOURCE),read(VOICE);image=NdsImage.open(source['current_ROM'])
    arm,clean=image.read_file('/__arm9__.bin'),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    text=inspect.getsource(prior.names);anchor='for ident in [2,4,13,23,109]:';assert text.count(anchor)==1
    text=text.replace(anchor,'for ident in [92,96,152]:');namespace=dict(prior.__dict__)
    exec(compile(text,__file__+'::5C-60-98-native-names','exec'),namespace)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B179_voices_v4709/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(namespace['names']);ctx.machines.pop();assert not ctx.machines
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    expected={92:'Barkeep',96:'Patron',152:'Retainer'}
    full={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh3_actor_names']['rows']}
    assert len(values)==6 and {i:values[i,'full-catalogue'] for i in full}==full==expected
    progressive={i:values[i,'progressive-nameplate'] for i in full};assert progressive==full
    assert len(native['rows'])==6
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in native['rows'])
    readonly=[r for r in native['rows'] if r['ownership_mode']=='original-read-only-name-pointer-without-scratch-ring']
    assert all(not r['original_scratch_rings'] and not r['original_getter_writes'] for r in readonly)
    save(ROOT/'six_original_Barkeep_Patron_Retainer_name_consumers.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_six_consumer_cases=native,
        full_catalogue_values=full,progressive_nameplate_values=progressive,approved_prose_names={str(k):v for k,v in expected.items()},
        source_5C_60_98_are_static_Barkeep92_Patron96_Retainer152_not_literal_halfwidth_prose=True,
        readonly_consumer_count=len(readonly),source_owned_scratch_consumer_count=len(native['rows'])-len(readonly),
        server_address_master_is_tavern_Barkeep_not_new_rank_relationship_or_proper_name=True,
        Retainer_label_adds_no_named_lord_faction_rank_or_personal_relationship=True,
        FE254_is_impersonal_fashion_news_without_static_actor=True,no_new_name_asset_or_relationship_invented=True,
        not_actual_B179_nameplate_observation=True,later_older_record0D_reaudit_stays_open=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(prior.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(progressive=progressive,full=full,readonly_paths=len(readonly),source_owned_scratch_paths=6-len(readonly),FE_static_getter_calls=0,credit=0))
