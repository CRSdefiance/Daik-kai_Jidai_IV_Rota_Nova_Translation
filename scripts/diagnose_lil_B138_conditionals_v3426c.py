"""Locate the exact failing conditional without assuming the query caused it."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.prove_lil_crew_items_controls_v3114 import predicate
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B138_conditional_diagnostic_v3426c')
SOURCE=Path('work/analysis/lil_remaining_B138_B140_source_v3422/next44_B138_clean_current_context.json')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);packet=read(SOURCE);image=NdsImage.open(packet['current_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    text=inspect.getsource(predicate);needle="assert values[0]==2 and values[1] in [0,1] and extent==command['native_extent']";assert text.count(needle)==1
    text=text.replace(needle,"save(DIAGNOSTIC,dict(command=command,values=list(values),extent=extent,event_calls=calls)); "+needle)
    env={**predicate.__globals__,'save':save,'DIAGNOSTIC':None};exec(compile(text,str(Path(__file__))+'::captured-predicate','exec'),env)
    ctx=CurrentContext('work/analysis/lil_B138_voices_v3425/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context');results=[]
    for b in packet['blocks']:
        for c in b['all_current_native_commands']:
            if c['word'] not in [0x8000,0x8100]:continue
            p=ROOT/f'conditional_{c["offset"]:04X}.json';env['DIAGNOSTIC']=p
            try:result=ctx.execute(env['predicate'],blocks[b['block']],c);passed=True
            except AssertionError:result=None;passed=False
            finally:ctx.machines.pop()
            observed=read(p);results.append(dict(offset=c['offset'],word=c['word'],original_assertions_pass=passed,observed=observed,result=result))
    save(ROOT/'all11_original_assertion_results.json',dict(cases=results,instrumented_source=text,producer_sha256=sha(Path(__file__).read_bytes()),first_query_only_diagnostic_did_not_reproduce_failure=True,previous_diagnostic_preserved=True,no_RAM_fixtures_or_source_changes=True,full_goal_complete=False))
    print([dict(offset=r['offset'],word=hex(r['word']),passed=r['original_assertions_pass'],values=r['observed']['values'],extent=r['observed']['extent'],expected_extent=r['observed']['command']['native_extent'],command_hex=r['observed']['command']['whole_command_hex']) for r in results])
