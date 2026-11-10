"""Bind six progressive/catalogue getters to the actual source-selected actor objects."""
from pathlib import Path
import inspect
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts.prove_lil_B167_names_v4124b import names
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/maria_B97_names_v5003')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);voice=read('work/analysis/maria_B97_voices_v5000/current207_catalog_eight_voices_and_three_Maria_selectors.json')
    text=inspect.getsource(names)
    for a,b in [('for ident in [2,4,13,23,109]:','for ident in [3,10,180]:'),('actor = root+4+32*ident','actor = root+0x19E4 if ident==3 else root+4+32*ident'),
        ('all_ten_original_consumers','all_six_original_consumers')]:assert text.count(a)==1;text=text.replace(a,b)
    env=dict(names.__globals__);exec(compile(text,str(Path(__file__))+'::three_source_actors_six_consumers','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    native=ctx.execute(env['names']);ctx.machines.pop();assert len(native['rows'])==6 and not ctx.machines
    catalog={int(i):r['current_catalog_name'] for i,r in voice['fresh_three_actor_names'].items()}
    assert {r['actor_ID']:r['text'] for r in native['rows'] if r['consumer']=='full-catalogue'}==catalog
    save(ROOT/'six_original_progressive_and_catalogue_name_consumers.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        native_six_consumer_cases=native,progressive_nameplate_values={r['actor_ID']:r['text'] for r in native['rows'] if r['consumer']=='progressive-nameplate'},full_catalogue_values=catalog,
        actual_captain3_actor_object_selected_instead_of_static_copy=True,source_owned_adapter=text,current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        actual_source_B97_nameplate_observation_not_claimed=True,source_prose_or_completion_credit_added=0,new_emulator_runs=0,full_goal_complete=False))
    print('Six original name consumers pass;captain3 special object and both static source actors preserved with owned scratch restoration.')
