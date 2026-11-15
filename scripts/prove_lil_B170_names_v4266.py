"""Bind the four original Lil/Yifa name consumers and owned scratch paths."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B167_names_v4124b as prior
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B170_names_v4266')
SOURCE=Path('work/analysis/lil_B170_source_v4260/all33_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B170_voices_v4262/current2_static_names_voices_and207_catalog_rebind.json')
if __name__=='__main__':
    assert not ROOT.exists()
    source,voice=read(SOURCE),read(VOICE)
    image=NdsImage.open(source['current_ROM'])
    arm,clean=image.read_file('/__arm9__.bin'),NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    text=inspect.getsource(prior.names)
    assert text.count('for ident in [2,4,13,23,109]:')==1
    text=text.replace('for ident in [2,4,13,23,109]:','for ident in [2,25]:').replace('all_ten_original_consumers','all_four_original_consumers')
    namespace=dict(prior.__dict__)
    exec(compile(text,__file__+'::two-source-names','exec'),namespace)
    ROOT.mkdir(parents=True)
    ctx=CurrentContext('work/analysis/lil_B170_voices_v4262/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(namespace['names'])
    ctx.machines.pop()
    assert not ctx.machines
    full={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh2_actor_names']['rows']}
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    assert len(values)==4 and {i:values[i,'full-catalogue'] for i in full}==full=={2:'Lil Argot',25:'Yifa Sol'}
    progressive={i:values[i,'progressive-nameplate'] for i in full}
    assert progressive=={2:'Lil Argot',25:'Yifa Sol'}
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in native['rows'])
    assert all(r['original_scratch_rings'] and r['original_getter_writes'] for r in native['rows'])
    save(ROOT/'four_original_name_consumers_and_owned_scratch_paths.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_four_consumer_cases=native,
        progressive_nameplate_values=progressive,full_catalogue_values=full,approved_prose_names={'2':'Lil','25':'Yifa'},
        source_19_selector_is_Yifa25_not_text_to_strip=True,source_printed_Ifa_maps_to_approved_Yifa_spelling=True,
        surname_not_added_to_source_spoken_introduction=True,source_onesan_address_does_not_establish_kinship=True,
        later_older_record0D_reaudit_stays_open=True,not_actual_B170_nameplate_observation=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(prior.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(progressive=progressive,full=full,four_original_consumers_pass=True,credit=0))
