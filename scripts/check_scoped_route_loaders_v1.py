"""Run original complete archive/cache/parent checks for the explicit changed story bank."""
import argparse
from collections import Counter
import inspect
from pathlib import Path
import struct
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import trace_event_script_sources_v727 as loader
from scripts import verify_script_handoff_v732 as parent
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['reconstruction','out']:
        ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--route',type=int,choices=range(4),required=True)
    ap.add_argument('--expected-changed-blocks',type=int,required=True)
    args=ap.parse_args()
    assert not args.out.exists()
    rebuilt=load(args.reconstruction)
    assert len(rebuilt['changed_blocks'])==args.expected_changed_blocks
    assert rebuilt['full_clean_current_block_archive_andserialized_NDS_inverses_exact']
    assert digest(rebuilt['research_ROM'])==rebuilt['research_ROM_sha256']
    image=NdsImage.open(rebuilt['research_ROM'])
    doc=load(rebuilt['manuscript'])
    assert doc['file_path']==f'/data/SC{args.route}.DK4'
    blocks=IlnkContainer.parse(image.read_file(doc['file_path'])).blocks
    evpath=f'/data/EV{args.route}.DK4'
    ev=image.read_file(evpath)
    assert ev[:2]==b'VE' and struct.unpack_from('<I',ev,4)[0]==len(ev)-96
    begin,end=struct.unpack_from('<2I',ev,0x4C)
    assert 0<=begin<=end<=len(ev)-96 and (end-begin)%2==0
    words=struct.unpack_from(f'<{(end-begin)//2}H',ev,96+begin)
    kinds=Counter((w>>12)&3 for w in words)
    assert not kinds[1] and not kinds[3]
    assert [w&4095 for w in words if (w>>12)&3==2]==list(range(len(blocks)))
    loader_source=checked_text(inspect.getsource(loader.run),{
        'for route in range(4):':f'for route in [{args.route}]:',
        'assert all_actions == 1312 and loaded == 1307':f'assert all_actions == {len(words)} and loaded == {len(blocks)}',
    })
    parent_source=checked_text(inspect.getsource(parent.run),{
        'for route in range(4):':f'for route in [{args.route}]:',
        'assert len(cases) == 2614':f'assert len(cases) == {2*len(blocks)}',
        'all_blocks_bound_to_V727_complete_native_loader_payloads':
            'all_blocks_bound_to_fresh_complete_native_loader_payloads',
    })
    env,penv=dict(vars(loader)),dict(vars(parent))
    exec(compile(loader_source,__file__+'::same-native-loaders-explicit-source-bank','exec'),env)
    exec(compile(parent_source,__file__+'::same-native-parent-handoffs-explicit-source-bank','exec'),penv)
    args.out.mkdir(parents=True)
    label=f'SC{args.route}-reviewed-storage-research'
    loaded=env['run'](image,label)
    loadpath=args.out/'native_loads.json';save(loadpath,loaded)
    modes=penv['run'](image,label,loaded)
    modepath=args.out/'native_parent_modes.json';save(modepath,modes)
    save(args.out/'verification.json',dict(reconstruction=str(args.reconstruction),reconstruction_sha256=digest(args.reconstruction),
        research_ROM=rebuilt['research_ROM'],research_ROM_sha256=rebuilt['research_ROM_sha256'],route=args.route,
        original_EV_action_count=len(words),original_EV_null_actions=kinds[0],whole_archive_loads_andcache_hits=len(blocks),
        parent_cases=2*len(blocks),EV_file=evpath,EV_sha256=__import__('hashlib').sha256(ev).hexdigest(),
        loads=str(loadpath),loads_sha256=digest(loadpath),modes=str(modepath),modes_sha256=digest(modepath),
        source_owned_loader_adapter=loader_source,source_owned_parent_adapter=parent_source,
        all_native_executed_instructions_current_ROM_exact=True,
        all_loaded_payloads_cache_metadata_neighbors_andparent_first_reads_exact=True,
        controlled_native_route_inputs_not_optional_event_activation=True,other_routes_not_replayed=True,
        actual_gameplay=False,new_credit=0,
        evidence={str(p):digest(p) for p in [args.reconstruction,Path(loader.__file__),Path(parent.__file__),Path(__file__)]}))
    print(dict(route=args.route,actions=len(words),loads=len(blocks),parent_cases=2*len(blocks),all_pass=True))


if __name__=='__main__':
    main()
