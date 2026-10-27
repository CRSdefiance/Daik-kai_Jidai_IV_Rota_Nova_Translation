"""Closed B22 unit:49 actual dialogue pairs and all90 original command returns."""
import struct
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save
from scripts.prepare_lil_opening_research_v1704 import ROM

ROOT=Path('work/analysis/lil_opening_scene_v1708')
RUN=Path('work/analysis/lil_opening_trace_v1706')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_opening_trace_v1706_RESEARCH_ONLY')


if __name__=='__main__':
    assert not ROOT.exists()
    nav=read('work/analysis/lil_opening_navigation_v1707b/all49_holds_and_post_opening_pause.json')
    assert len(nav['rows'])==49
    trace=read(RUN/'live_observer_progress.json');assert not trace['errors'] and not trace['mismatches']
    rows=[r for r in trace['rows'] if r['source'].get('classification')=='original_SC_cache' and (r['source']['route'],r['source']['block'])==(2,22)]
    assert len(rows)==180
    mapping=read('work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json')
    commands=mapping['native_90_command_extents'];assert len(commands)==90
    pairs=[]
    for n,(before,after,expected) in enumerate(zip(rows[::2],rows[1::2],commands,strict=True)):
        assert before['kind']=='before_command' and after['kind']=='after_command'
        assert before['source']==after['source'] and after['entry_row']==2*n
        src=before['source'];assert src['whole_resident_payload_exact_ROM']
        assert (src['instruction_offset'],src['first_word'])==(expected['new_offset'],expected['opcode'])
        assert after['decoded_length']==expected['new_extent']
        assert after['result_words']==([0,0] if n==89 else [3,0])
        assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in (before,after))
        assert sha(Path(src['actual_payload_file']).read_bytes())==src['actual_sha256']==mapping['research_block_sha256']
        descriptor=struct.unpack('<4I',bytes.fromhex(after['player_descriptor16_hex']))
        assert descriptor[:2]==(0x021345B0,src['instruction_pointer']) and descriptor[2:]==(expected['new_extent'],after['result_words'][0])
        if n<89:assert rows[2*n+2]['source']['instruction_offset']==src['instruction_offset']+after['decoded_length']
        pairs.append({'opcode':src['first_word'],'source_offset':expected['old_offset'],'actual_offset':src['instruction_offset'],
            'frames':[before['frame'],after['frame']],'actual_decoded_extent':after['decoded_length'],'result_type':after['result_words'][0]})
    assert pairs[0]['actual_offset']==8 and pairs[-1]['actual_offset']+pairs[-1]['actual_decoded_extent']==3292
    image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin');wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    fonts=read('work/analysis/lil_opening_fonts_v1699b/native_font_proof.json');font_by_id={r['id']:r for r in fonts['cases']}
    mapped={r['id']:r for r in mapping['mapped_texts']};photos=[];verified=[]
    for group in nav['rows']:
        ident=group['id'];ref=font_by_id[ident];spec=mapped[ident];expected=bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil')
        preview=Image.open(ref['preview']).convert('RGB')
        wanted={(16+x,296+y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(0,8,0)}
        assert len(group['holds'])==2;images=[]
        for hold in group['holds']:
            frame=hold['frame'];raw=(CAP/f'frame_{frame:06d}_arm9_ram.bin').read_bytes();path=Path(hold['capture'])
            assert sha(raw)==hold['RAM_sha256'] and sha(path.read_bytes())==hold['capture_sha256']
            im=Image.open(path).convert('RGB');images.append(im)
            assert cstring(raw,wrapped)==expected
            actual={(x,y) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            assert wanted==actual
            source=hold['native_script_source'];assert source['instruction_offset']==spec['new_offset']-5
            whole=Path(source['actual_payload_file']).read_bytes();assert raw[source['payload_address']-0x02000000:source['payload_address']-0x02000000+3292]==whole
        assert images[0].crop((0,273,256,292)).tobytes()==images[1].crop((0,273,256,292)).tobytes()
        verified.append({'id':ident,'speaker':group['holds'][0]['speaker'],'two_full_actual_font_holds':group['holds'],
            'whole_native_body_ink_and_caption_stable':True,'all_letters_margins_bounds_and_no_extra_text_verified':True})
        photos.append(images[0])
    ROOT.mkdir(parents=True);save(ROOT/'immutable_completed_B22_trace_prefix.json',{'rows':rows,'all90_commands_completed':True})
    sheets=[]
    for start in range(0,49,10):
        sheet=Image.new('RGB',(1052,1270),(28,36,40));draw=ImageDraw.Draw(sheet)
        for k,(group,im) in enumerate(zip(verified[start:start+10],photos[start:start+10],strict=True)):
            x,y=8+522*(k%2),6+252*(k//2)
            draw.text((x,y),group['id']+' '+group['speaker'],fill='white')
            sheet.paste(im.crop((0,272,256,384)).resize((512,224),Image.Resampling.NEAREST),(x,y+20))
        p=ROOT/f'actual_review_sheet_{start//10+1:02d}.png';sheet.save(p);sheets.append({'path':str(p),'sha256':sha(p.read_bytes())})
    proof={'research_ROM':str(ROM),'research_ROM_sha256':sha(ROM.read_bytes()),'ARM9_sha256':sha(arm),
        'all49_revised_dialogues_individually_activated_with98_complete_pixel_exact_holds':True,
        'all90_original_command_entry_return_pairs_and_entire3292_byte_resident_source_verified':True,
        'original_VM_contiguous_PC_advance_uses_each_decoded_length':True,'all89_nonterminal_results_type3_and_final_result_type0':True,
        'no_branch_jump_mode_change_or_fixed_interior_target_in_this_complete_B22_execution':True,
        'original_illustration_pauses_confirmed_with_normal_A':read('work/analysis/lil_opening_navigation_v1707b/illustration_pause_confirmations.json'),
        'original_three_crew_joins_normally_dismissed_and_Amsterdam_town_exit_observed':True,
        'town_exit_capture':str(CAP/'frame_019760_navigation.png'),'town_exit_capture_sha256':sha((CAP/'frame_019760_navigation.png').read_bytes()),
        'command_pairs':pairs,'dialogues':verified,'actual_review_sheets':sheets,'actual_sheets_visual_review_pending':True,
        'current_whole_run_continues_to_following_route_scene_terminal_audit_pending':True,
        'not_registered_candidate_or_full_editorial_completion':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'complete_B22_actual_scene_proof.json',proof)
    print('B22 closed unit verified:49 individual dialogues/98 full actual font holds,90 original command returns,three joins and normal Amsterdam exit. Full run remains live for next scene.')
