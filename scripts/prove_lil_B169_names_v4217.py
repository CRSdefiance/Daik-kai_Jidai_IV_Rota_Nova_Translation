"""Bind six original progressive/full-name pairs and all twelve owned scratch paths."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B167_names_v4124b as prior
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_names_v4217')
SOURCE = Path('work/analysis/lil_B169_source_v4211/all36_clean_current_complete_context.json')
VOICE = Path('work/analysis/lil_B169_voices_v4213/current6_static_names_voices_and207_catalog_rebind.json')
if __name__ == '__main__':
    assert not ROOT.exists()
    source, voice = read(SOURCE), read(VOICE)
    image = NdsImage.open(source['current_ROM'])
    arm, clean = image.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4] == clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8] == clean[0x541C0:0x541C8]
    text = inspect.getsource(prior.names)
    old = 'for ident in [2,4,13,23,109]:'
    assert text.count(old) == 1
    text = text.replace(old, 'for ident in [2,6,9,20,21,76]:').replace('all_ten_original_consumers', 'all_twelve_original_consumers')
    namespace = dict(prior.__dict__)
    exec(compile(text, __file__ + '::six-source-names', 'exec'), namespace)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext('work/analysis/lil_B169_voices_v4213/current_native_input.json', source['historical_snapshot_ROM'], ROOT / 'current_context')
    native = ctx.execute(namespace['names'])
    ctx.machines.pop()
    assert not ctx.machines
    full = {row['actor_ID']: row['current_catalog_name'] for row in voice['fresh6_actor_names']['rows']}
    values = {(row['actor_ID'], row['consumer']): row['text'] for row in native['rows']}
    assert len(values) == 12 and {ident: values[ident, 'full-catalogue'] for ident in full} == full
    progressive = {ident: values[ident, 'progressive-nameplate'] for ident in full}
    assert full[21] == 'Ian Dukov'
    assert {ident: progressive[ident] for ident in [2,6,9,20,76]} == {2:'Lil Argot',6:'Julio Erneco',9:'Camille Overijssel',20:'Ｆernando Dias',76:'Mikhail Letzel'}
    assert all(row['all_actor_models_and_unowned4MiB_exact'] and row['source_owned_scratch_restoration_or_readonly_path_recovers_all4MiB'] for row in native['rows'])
    assert all(row['original_scratch_rings'] and row['original_getter_writes'] for row in native['rows'])
    save(ROOT / 'twelve_original_name_consumers_and_owned_scratch_paths.json', dict(candidate=source['current_ROM'],candidate_sha256=source['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_twelve_consumer_cases=native,
        progressive_nameplate_values=progressive,full_catalogue_values=full,
        approved_prose_names={'2':'Lil','6':'Julio','9':'Camille','20':'Fernando Dias','21':'Ian','76':'Mikhail'},
        source_15_selector_is_Ian21_not_literal_control_to_strip=True,source_printable4C_is_Mikhail76_not_literal_L=True,
        original_Fernando_width_forms_preserved_without_name_asset_change=True,
        Mikhail_Letzel_is_printed_in_source_but_full_catalogue_middle_name_not_added=True,
        later_older_record0D_reaudit_stays_open=True,not_actual_B169_nameplate_observation=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,
        evidence={str(path):sha(path.read_bytes()) for path in [SOURCE,VOICE,Path(prior.__file__),Path(__file__)]},
        new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(progressive=progressive,full=full,twelve_original_consumers_pass=True,credit=0))
