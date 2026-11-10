"""Focused original whole-load/cache/parent tests preserve the distinct CS0101 header."""
import inspect
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_header_v7684')
SOURCE=Path('work/analysis/maria_B207_current_v7670/all18_complete_Maria_clean_current_refs_CS0101_before_new_prose.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE)
    ltext=checked_text(inspect.getsource(loader.run),{
        'for route in range(4):':'for route in (3,):',
        'for action, word in enumerate(words):':'for action, word in enumerate(words):\n            if word != 0x20CF: continue',
        'assert all_actions == 1312 and loaded == 1307':'assert all_actions == loaded == 1',
        "'all_archive_blocks_selected_once': len(scripts)":"'focused_selected_archive_blocks': loaded",
        "print(f'{label} route{route}: {len(scripts)} complete native SC loads/cache hits; {kinds[0]} null actions.', flush=True)":"print(f'{label} route{route}: one focused B207 whole load/cache hit.', flush=True)",
    })
    ptext=checked_text(inspect.getsource(parent.run),{
        'for route in range(4):':'for route in (3,):',
        'assert len(old_blocks) == len(blocks)':'assert len(old_blocks) == 1 and 207 in old_blocks',
        "'all_blocks_bound_to_V727_complete_native_loader_payloads': len(blocks)":"'focused_B207_bound_to_complete_native_loader_payload': 1",
        'for index, block in enumerate(blocks):':'for index, block in enumerate(blocks):\n                if index != 207: continue',
        'assert len(cases) == 2614':'assert len(cases) == 2',
        "print(f'{label} route{route}: {len(blocks) * 2} original handoffs and first instruction reads pass.', flush=True)":"print(f'{label} route{route}: two focused B207 parent modes and first reads pass.', flush=True)",
    })
    le,pe=dict(loader.__dict__),dict(parent.__dict__)
    exec(compile(ltext,__file__+'::focused-original-loader','exec'),le);exec(compile(ptext,__file__+'::focused-original-parent','exec'),pe)
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    assert sha(Path(packet['current_ROM']).read_bytes())==packet['current_ROM_sha256']
    arms=[im.read_file('/__arm9__.bin') for im in images]
    for a,b in [(0x23E94,0x23F84),(0x23F4C,0x24134),(0x24134,0x24230),(0x2A510,0x2A530)]:assert arms[0][a:b]==arms[1][a:b]
    ROOT.mkdir(parents=True);versions=[]
    for label,image in zip(['clean-Japanese','current-English'],images,strict=True):
        block=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks[207]
        assert block[:8].hex()=='43530101b4050000' and len(block)==1468
        loads=le['run'](image,label);parents=pe['run'](image,label,loads)
        assert loads['complete_SC_loads_and_cache_hits']==1 and len(parents['native_handoff_and_first_read_cases'])==2
        lp,pp=ROOT/(label+'_whole_load.json'),ROOT/(label+'_parent_modes.json');save(lp,loads);save(pp,parents)
        versions.append(dict(label=label,ROM_sha256=sha(image.source.read_bytes()),block_sha256=sha(block),header_hex=block[:8].hex(),whole_load=str(lp),whole_load_sha256=sha(lp.read_bytes()),parent_modes=str(pp),parent_modes_sha256=sha(pp.read_bytes()),both_native_modes_begin_at_full_payload_plus8=True))
    save(ROOT/'distinct_CS0101_two_fresh_loads_four_parent_modes.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),versions=versions,source_owned_loader_adapter=ltext,source_owned_parent_adapter=ptext,all_native_high_constants_andmultiplicity_preserved=True,complete_CS0101_header_not_normalized_orassumed_CS0001=True,two_whole_block_loads_andcache_hits=2,four_native_parent_modes=4,only_original_SDK_IO_bridged=True,guarded_header_payload_metadata_tail_andexecuted_instructions_exact=True,not_full_header_semantics_orUI_orordinary_event_activation=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(loader.__file__),Path(parent.__file__),Path(__file__)]},full_goal_complete=False))
