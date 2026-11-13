"""Bind B97's eight exact leaves,633E resource and4820/4700 descriptor boundaries."""
import inspect,struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_maria_native_context_v4999 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_controls_v5005')
SOURCE=Path('work/analysis/maria_B97_source_v4998/all32_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);g=packet['blocks'][0]
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[97] for im in images]
    commands=g['all_current_native_commands'];leaves=[]
    for a,b in zip(g['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=97,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['source_current_hex']) for r in leaves]==[(8,'0060'),(10,'2046a280'),(14,'3e63'),(1750,'00a0ffff0f000073'),(1884,'2048b0a8'),(1888,'00a0ffff0100b030'),(1896,'0047'),(1898,'00000000')]
    assert len(commands)==40 and len(blocks[0])==len(blocks[1])==1904
    assert all(not c['ancestor_0100_offsets'] for c in commands)
    assert 8+struct.unpack_from('<H',blocks[0],4)[0]==1902 and blocks[0][1902:]==bytes(2)
    resource_text=inspect.getsource(resource_base.control630A)
    for a,b in [("value=bytes.fromhex('0a63')","value=bytes.fromhex('3e63')"),('[0x02386EFC,10,2,1]','[0x02386EFC,62,2,1]')]:
        assert a in resource_text;resource_text=resource_text.replace(a,b)
    re=dict(resource_base.__dict__);exec(compile(resource_text,__file__+'::resource633E','exec'),re)
    picture_text=inspect.getsource(picture_base.picture)
    assert '[0x4821,0x4822,0x4823,0x4700]' in picture_text
    picture_text=picture_text.replace('[0x4821,0x4822,0x4823,0x4700]','[0x4820,0x4700]')
    pe=dict(picture_base.__dict__);exec(compile(picture_text,__file__+'::picture4820','exec'),pe)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B97_voices_v5000/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    resource=[]
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:resource.append(ctx.execute(re['control630A'],previous,result));ctx.machines.pop()
    pictures=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        for c in commands:
            if c['word'] in [0x4820,0x4700]:pictures.append(dict(version=label,**ctx.execute(pe['picture'],block,c)));ctx.machines.pop()
    assert len(resource)==10 and len(pictures)==4 and not ctx.machines
    for a,b in zip(pictures[:2],pictures[2:],strict=True):assert a['original_picture_boundary_calls']==b['original_picture_boundary_calls'] and a['source_command_hex']==b['source_command_hex']
    structural=[]
    for row in [r for r in leaves if r['word'] in [0x6000,0x4620,0xA000]]:
        raw=bytes.fromhex(row['source_current_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),isolated)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
            assert len(result['rows'])==1 and result['rows'][0]['word']==row['word'] and result['rows'][0]['native_extent']==row['native_extent']
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row,versions=versions,isolated_synthetic_cursor8_not_original_site=True,nondecode_callees_explicit_zero_return_unexecuted_boundaries=True))
    assert len(structural)==4
    save(ROOT/'eight_source_leaves_resource633E_item4820_hide_and_two_effects.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all8_exact_source_current_leaves=leaves,resource633E_ten_guarded_boundary_cases=resource,picture4820_and_hide4700_four_source_current_cases=pictures,setup_and_two_A000_eight_isolated_structural_cases=structural,source_logical_end=1902,source_stored_bytes=1904,source_declared_end_offset=1898,source_item_descriptor=pictures[0]['original_picture_boundary_calls'][0]['descriptor'],source_item_layout=pictures[0]['original_picture_boundary_calls'][0]['layout'],no_source_predicates_relative_operands_typed_objects_or_pause_pairs=True,resource_picture_effect_bodies_not_executed_and_no_earned_recruitment_or_tablet_claim=True,source_owned_adapters=dict(resource633E=resource_text,picture4820=picture_text,structural_walk=inspect.getsource(walk)),current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(exact_leaves=8,resource_boundary_cases=10,picture_and_hide_cases=4,structural_pairs=4,credit=0))
