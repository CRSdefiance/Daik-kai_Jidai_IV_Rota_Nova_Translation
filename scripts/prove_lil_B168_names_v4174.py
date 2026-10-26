"""Bind eight original progressive/full-name pairs and their owned or read-only paths."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B167_names_v4124b as prior
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B168_names_v4174')
SOURCE=Path('work/analysis/lil_B168_source_v4168/all54_clean_current_complete_context.json')
VOICE=Path('work/analysis/lil_B168_voices_v4170/current8_static_names_voices_and207_catalog_rebind.json')
if __name__=='__main__':
    assert not ROOT.exists();source,voice=map(read,[SOURCE,VOICE]);image=NdsImage.open(source['current_ROM'])
    arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    text=inspect.getsource(prior.names);old='for ident in [2,4,13,23,109]:';assert text.count(old)==1
    text=text.replace(old,'for ident in [2,6,9,20,76,87,165,166]:').replace('all_ten_original_consumers','all_sixteen_original_consumers')
    env=dict(prior.__dict__);exec(compile(text,__file__+'::eight-source-names','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B168_voices_v4170/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines
    full={r['actor_ID']:r['current_catalog_name'] for r in voice['fresh8_actor_names']['rows']}
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    assert len(values)==16 and {i:values[i,'full-catalogue'] for i in full}==full
    progressive={i:values[i,'progressive-nameplate'] for i in full}
    assert {i:progressive[i] for i in [2,6,9,20,76]}=={2:'Lil Argot',6:'Julio Erneco',9:'Camille Overijssel',20:'Ｆernando Dias',76:'Mikhail Letzel'}
    assert all(r['all_actor_models_and_unowned4MiB_exact'] and r['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for r in native['rows'])
    save(ROOT/'sixteen_original_name_consumers_and_owned_or_readonly_paths.json',dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_sixteen_consumer_cases=native,progressive_nameplate_values=progressive,full_catalogue_values=full,approved_prose_names={'2':'Lil','6':'Julio','9':'Camille','20':'Fernando Dias','76':'Mikhail'},generic_87_165_166_roles_bound_to_original_getters_without_personal_name_or_age_invention=True,source_printable57_4C_A5_A6_selectors_preserved=True,original_Fernando_width_forms_preserved_without_name_asset_change=True,Mikhail_middle_name_only_in_source_full_catalogue_not_added_to_spoken_introduction=True,later_older_record0D_reaudit_stays_open=True,not_actual_B168_nameplate_observation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(prior.__file__),Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(progressive=progressive,full=full,sixteen_original_consumers_pass=True,credit=0))
