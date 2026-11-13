"""Bind all five original short/full name consumers,including printable6D Shipwright."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B159_name_consumers_v3827 as original
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/lil_B167_names_v4124')
SOURCE = Path('work/analysis/lil_B167_source_v4118/all29_clean_current_complete_context_with_typed_choice.json')
VOICE = Path('work/analysis/lil_B167_voices_v4120/current5_static_names_voices_and207_catalog_rebind.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    source,voice = read(SOURCE),read(VOICE)
    image = NdsImage.open(source['current_ROM'])
    arm = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4] == clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8] == clean[0x541C0:0x541C8]
    text = inspect.getsource(original.names)
    assert text.count('for ident in [9,22]:') == 1
    text = text.replace('for ident in [9,22]:','for ident in [2,4,13,23,109]:')
    env = dict(original.names.__globals__)
    exec(compile(text,__file__+'::five-original-short-full-name-pairs','exec'),env)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext('work/analysis/lil_B167_voices_v4120/current_native_input.json',source['historical_snapshot_ROM'],ROOT/'current_context')
    native = ctx.execute(env['names'])
    ctx.machines.pop()
    assert not ctx.machines
    values = {(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']}
    print(values,flush=True)
    expected = {2:'Lil Argot',4:'Janus Pasar',13:'Cesare Tony',23:'Manuel Almeida',109:'Shipwright'}
    assert len(values) == 10
    assert {i:values[(i,'progressive-nameplate')] for i in expected} == expected
    full = {r['actor_ID']:r['current_catalog_name'] for r in voice['fresh5_actor_names']['rows']}
    assert {i:values[(i,'full-catalogue')] for i in expected} == full
    save(ROOT/'ten_original_Janus_Cesare_Manuel_Lil_Shipwright_name_consumers.json',dict(candidate=source['current_ROM'],
        candidate_sha256=source['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        ARM9_sha256=sha(arm),native_ten_consumer_cases=native,progressive_nameplate_values=expected,full_catalogue_values=full,
        approved_prose_names={'2':'Lil','4':'Janus','13':'Cesare','23':'Manuel','109':'Shipwright'},
        source_selector6D_is_static_actor109_not_literal_m=True,source_selector0D_is_static_actor13_not_CR=True,
        generic_source_Shipwright_nameplate_supports_role_without_inventing_personal_name=True,
        later_older_record0D_reaudit_stays_open=True,not_actual_B167_nameplate_observation=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(original.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print('Ten original name consumers pass;all4MiB owned scratch restored;no name assets changed.')
