"""Bind B189's A000,C200 and end without inventing predicates or relative sites."""
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B180_C200_v4784 import C200,adapter_source
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B189_controls_v5277b')
SOURCE=Path('work/analysis/lil_B189_source_v5273b/all17_clean_current_complete_context.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);group=packet['blocks'][0]
    images=[NdsImage.open(p) for p in ['work/clean.nds',packet['current_ROM']]]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[189] for im in images]
    commands=group['all_current_native_commands'];leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word']==0x4000:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=189,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(c['offset'],c['source_current_hex']) for c in leaves]==[(8,'00a0ffff012a05a1'),(764,'00c2'),(766,'00000000')]
    assert len(commands)==20 and len(blocks[0])==len(blocks[1])==772
    assert all(c['word'] in [0x4000,0xA000,0xC200,0] and not c['ancestor_0100_offsets'] for c in commands)
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B189_voices_v5274b/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    ui=next(c for c in commands if c['word']==0xC200);uis=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        uis.append(dict(version=label,**ctx.execute(C200,block,ui)));ctx.machines.pop()
    assert not ctx.machines and uis[0]['source_owned_UI_request_words']==uis[1]['source_owned_UI_request_words']==[1,2,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes']==uis[1]['source_owned_UI_writes']
    raw=bytes.fromhex(leaves[0]['source_current_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;effects=[]
    for label,image in zip(['clean','current'],images,strict=True):
        result=walk(image.read_file('/__arm9__.bin'),isolated)
        assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
        assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
        effects.append(dict(version=label,**result))
    assert effects[0]['rows']==effects[1]['rows'] and effects[0]['opaque_effect_bridges']==effects[1]['opaque_effect_bridges']
    save(ROOT/'A000_C200_single_end_and_no_relative_or_predicate_contract.json',dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),all3_source_current_nonrelative_nonspeech_leaves=leaves,
        source_C200_pairs=[dict(block=189,source_offset=764,cases=uis)],source_owned_C200_adapter=adapter_source(),
        source_A000_structural_cases=[dict(source_site=leaves[0],versions=effects,nondecode_effect_body_bridged_not_actual_game_state_execution=True)],
        no_source_relative_sites_predicates_pause_resources_presentations_or_typed_objects=True,source_declared_end_offsets=[766],
        source_A000_packed_semantics_not_inferred=True,current_native_context_plan=str(ctx.proof_path),
        current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_scene_outcomes_unexecuted=True,
        new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('B189 three exact leaves,A000 structural pair and source-derived C200 pair pass;no predicates,relative sites or gameplay claim.')
