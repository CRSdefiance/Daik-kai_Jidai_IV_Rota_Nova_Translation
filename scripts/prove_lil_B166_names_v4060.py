"""Bind the original Manuel, Fernando and Camille name consumers with owned scratch restoration."""
import inspect,unicodedata
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B159_name_consumers_v3827 as original
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B166_names_v4060')
SOURCE=Path('work/analysis/lil_B166_source_v4054/all44_clean_current_complete_context_with_typed_choice.json')
VOICE=Path('work/analysis/lil_B166_voices_v4056/current4_static_names_voices_and207_catalog_rebind.json')
if __name__=='__main__':
    assert not ROOT.exists();v=read(SOURCE);image=NdsImage.open(v['current_ROM']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x7ED88:0x7EDD4]==clean[0x7ED88:0x7EDD4] and arm[0x541C0:0x541C8]==clean[0x541C0:0x541C8]
    text=inspect.getsource(original.names);assert text.count('for ident in [9,22]:')==1;text=text.replace('for ident in [9,22]:','for ident in [9,20,23]:');env=dict(original.names.__globals__);exec(compile(text,__file__+'::three-original-name-pairs','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B166_voices_v4056/current_native_input.json',v['historical_snapshot_ROM'],ROOT/'current_context');native=ctx.execute(env['names']);ctx.machines.pop();assert not ctx.machines
    values={(r['actor_ID'],r['consumer']):r['text'] for r in native['rows']};assert len(values)==6
    assert values[(9,'progressive-nameplate')]=='Camille Overijssel' and values[(9,'full-catalogue')]=='Camille Marinus Overijssel'
    assert values[(23,'progressive-nameplate')]==values[(23,'full-catalogue')]=='Manuel Almeida'
    assert all(unicodedata.normalize('NFKC',values[(20,kind)])=='Fernando Dias' for kind in ['progressive-nameplate','full-catalogue'])
    save(ROOT/'six_original_Manuel_Fernando_Camille_name_consumers.json',dict(candidate=v['current_ROM'],candidate_sha256=v['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),ARM9_sha256=sha(arm),native_six_consumer_cases=native,approved_prose_names={'23':'Manuel Almeida','20':'Fernando Dias','9':'Camille'},original_name_values=[dict(actor_ID=i,consumer=k,text=t) for (i,k),t in values.items()],source_selector17_is_static_actor23_and14_is_static_actor20=True,original_Fernando_width_forms_preserved_without_name_asset_change=True,later_older_record0D_reaudit_stays_open=True,not_actual_B166_nameplate_observation=True,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),source_owned_adapter=text,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,VOICE,Path(original.__file__),Path(__file__)]},new_emulator_runs=0,source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print([dict(actor=i,consumer=k,text=t) for (i,k),t in values.items()]);print('Six original name consumers pass;all4MiB owned scratch restored;no assets changed.')
