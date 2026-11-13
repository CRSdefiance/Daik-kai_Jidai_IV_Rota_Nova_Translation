"""Bind two predicates,ten relative sites,three opaque effects,C200 and the end."""
from pathlib import Path
import inspect
import itertools
import struct

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts.prove_lil_B182_predicate500_v4883 import probe500 as probe
from scripts.prove_lil_B182_C200_v4883 import C200,adapter_source as C200_adapter_source
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B182_controls_v4883')
SOURCE=Path('work/analysis/lil_B182_source_v4878/all8_clean_current_complete_context.json')
BRANCH=Path('work/analysis/lil_B182_branches_v4881/original_relative_skip_operand_proof.json')

if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);branch=read(BRANCH);group=packet['blocks'][0]
    assert branch['source_context_sha256']==sha(SOURCE.read_bytes()) and len(branch['cases'])==100
    assert len(branch['operands_requiring_adjustment_when_resizing'])==10
    images=[NdsImage.open('work/clean.nds'),NdsImage.open(packet['current_ROM'])]
    blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[182] for im in images]
    original_arm,current_arm=[im.read_file('/__arm9__.bin') for im in images]
    assert all(original_arm[a:b]==current_arm[a:b] for a,b in [(0x29428,0x294D4),(0x904CC,0x9050C),(0x34674,0x34690)])
    commands=group['all_current_native_commands'];assert len(commands)==25
    leaves=[]
    for a,b in zip(group['all_clean_native_commands'],commands,strict=True):
        if a['word'] in [0x4000,0x100,0x200,0x300,0x400]:continue
        assert a['offset']==b['offset'] and a['whole_command_hex']==b['whole_command_hex']
        leaves.append(dict(block=182,offset=a['offset'],word=a['word'],native_extent=a['native_extent'],source_current_hex=a['whole_command_hex']))
    assert [(r['offset'],r['source_current_hex']) for r in leaves]==[
        (512,'0080fffff4010000'),(532,'00a0ffff014700a1'),(544,'0080fffff4010000'),
        (564,'00a0ffff014800a1'),(576,'00a0ffff014600a1'),(630,'00c2'),(632,'00000000')]
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/lil_B182_voices_v4879/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    predicates=[]
    for command in [c for c in commands if c['word']==0x8000]:
        for label,block in zip(['clean','current'],blocks,strict=True):
            predicates.append(dict(version=label,**ctx.execute(probe,block,command)));ctx.machines.pop()
    assert len(predicates)==4
    for offset in [512,544]:
        pair=[r for r in predicates if r['offset']==offset];assert pair[0]['native_result']==pair[1]['native_result']
    ui=next(c for c in commands if c['word']==0xC200);uis=[]
    for label,block in zip(['clean','current'],blocks,strict=True):
        uis.append(dict(version=label,**ctx.execute(C200,block,ui)));ctx.machines.pop()
    assert not ctx.machines and uis[0]['source_owned_UI_request_words']==uis[1]['source_owned_UI_request_words']==[1,2,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes']==uis[1]['source_owned_UI_writes']
    structural=[]
    for row in [r for r in leaves if r['word']==0xA000]:
        raw=bytes.fromhex(row['source_current_hex']);isolated=b'CS\0\1'+struct.pack('<H',len(raw))+bytes(2)+raw;versions=[]
        for label,image in zip(['clean','current'],images,strict=True):
            result=walk(image.read_file('/__arm9__.bin'),isolated)
            assert result['error'] is None and result['stopped_offset']==result['logical_end']==len(isolated)
            assert len(result['rows'])==1 and result['rows'][0]['word']==0xA000 and result['rows'][0]['native_extent']==8
            versions.append(dict(version=label,**result))
        assert versions[0]['rows']==versions[1]['rows'] and versions[0]['opaque_effect_bridges']==versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row,versions=versions,isolated_offset8_not_original_cursor=True,
            nondecode_effect_body_bridged_zero_return_not_actual_game_state_execution=True))
    by_at={c['offset']:c for c in commands};speeches={r['source_reference']['header_offset']:r for r in packet['records']}
    def path(values):
        cursor,last=8,0;visited=[];spoken=[];effects=[];ui_sites=[];used=[]
        while True:
            assert cursor in by_at and cursor not in visited
            c=by_at[cursor];visited.append(cursor);word=c['word']
            if word==0:
                return dict(hypothetical_predicate_results=list(values),actual_used_predicate_results=used,
                    command_offsets=visited,spoken_record_indices=spoken,A000_offsets=effects,C200_offsets=ui_sites,
                    source_end_offset=cursor,not_VM_effect_body_or_gameplay_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                tested_last=last if last in [0,1,2,3,0xFFFFFFFF] else 3
                match=[r for r in branch['cases'] if r['version']=='current' and r['offset']==cursor and r['last_choice_or_result']==tested_last]
                assert len(match)==1;cursor=match[0]['original_next_command_offset'];continue
            if word==0x8000:
                value=values[[512,544].index(cursor)];last=value;used.append(dict(offset=cursor,value=value))
            elif word==0x4000:spoken.append(speeches[cursor]['source_record_index'])
            elif word==0xA000:effects.append(cursor)
            elif word==0xC200:ui_sites.append(cursor)
            cursor+=c['native_extent']
    values=sorted({0,1,2,3,0xFFFFFFFF,*[r['native_result'][1] for r in predicates]})
    paths=[path(pair) for pair in itertools.product(values,repeat=2)]
    assert all(p['source_end_offset']==632 and p['C200_offsets']==[630] for p in paths)
    assert set.union(*(set(p['A000_offsets']) for p in paths))=={532,564,576}
    assert all(len(p['A000_offsets'])==1 for p in paths)
    expected=[r['source_record_index'] for r in packet['records']]
    assert all(p['spoken_record_indices']==expected for p in paths)
    save(ROOT/'two_predicates_three_A000_C200_ten_relative_sites_and_single_end.json',dict(
        candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),
        all7_source_current_nonrelative_nonspeech_leaves=leaves,source_predicate_cases=predicates,
        both_source_raw_operand_values=500,predicate_result_not_assumed_boolean_or_plot_semantics=True,
        exact_source500_threshold_and_original_RNG_ownership_proof='work/analysis/lil_B182_predicate500_v4883/all16_original500_predicate_RNG_ownership_cases.json',
        threshold500_uses_original_bounded1000_draw_and_three_native_result_classes=True,
        unforced_current_opening_predicate_results={str(r['offset']):r['native_result'][1] for r in predicates if r['version']=='current'},
        source_C200_pairs=[dict(block=182,source_offset=630,cases=uis)],source_A000_structural_cases=structural,
        source_A000_hex_by_offset={str(r['source_site']['offset']):r['source_site']['source_current_hex'] for r in structural},
        source_A000_packed_semantics_not_inferred=True,hypothetical_predicate_result_paths=paths,
        all8_speeches_all_three_alternative_effects_single_C200_and_end_structurally_bound=True,
        source_declared_end_offsets=[632],source_pause_resume_pairs=[],no_source_2000_pause_2100_4100_or_resources=True,
        current_native_context_plan=str(ctx.proof_path),current_native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        source_owned_adapters=dict(predicate=inspect.getsource(probe),C200=C200_adapter_source(),effect_walk=inspect.getsource(walk)),
        actual_scene_outcomes_or_earned_fashion_state_unexecuted=True,new_emulator_runs=0,new_review_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(predicates=4,A000_source_current_pairs=3,C200_pairs=1,structural_paths=len(paths),
        unforced_results={str(r['offset']):r['native_result'][1] for r in predicates if r['version']=='current'},actual_B182=False,credit=0),flush=True)
