"""Audit the complete fixture-free original B120 default-response path."""
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_sailing_choice0_audit_v1772')
RUN=Path('work/analysis/lil_sailing_choice0_v1770')
NAV=Path('work/analysis/lil_sailing_navigation_v1771')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_sailing_choice0_v1770_RESEARCH_ONLY')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal,nav=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json',NAV/'closed_B120_unit_and_next_context.json'))
    rom=Path(plan['research_ROM']);digest=sha(rom.read_bytes());arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==terminal['research_ROM_sha256']==report['ROM_sha256']==nav['research_ROM_sha256']
    assert terminal['terminal'] and terminal['frame']==report['frames']==nav['terminal_frame_requested']==27850
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert terminal['no_gameplay_fixture_save_or_ROM_runtime_edit']
    assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    commands=[json.loads(s) for s in (RUN/'navigation.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    assert commands==[r['command'] for r in journal['commands_received']]
    assert commands[-1]=={'stop':True} and journal['last_command_frame']==27850
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    assert all(r['start']<=22930 for r in schedule)
    for r in journal['commands_received']:
        assert r['validation_passed'];command=r['command']
        if command.get('buttons') or command.get('touch'):
            event={'start':r['frame']+1,'duration':command['duration'],'buttons':command.get('buttons',[])}
            if command.get('touch'):event['touch']=command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    photos={}
    for r in report['frames_captured']:
        assert sha(Path(r['path']).read_bytes())==r['PNG_sha256'] and Image.open(r['path']).size==(256,384)
        photos[r['frame']]=r
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(r['path']).read_bytes()
        assert len(data)==r['bytes']==0x400000 and sha(data)==r['sha256'] and r['read_only_export']
        if 'frame' in r:snapshots[r['frame']]=r
    block=next(b for b in read('work/analysis/lil_lessons_relocation_v1760/nested_source_relocation_research.json')['blocks'] if b['block']==120)
    source=next(b for b in read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')['blocks'] if b['block']==120)
    patches=sorted([{'start':r['old_offset'],'end':r['old_offset']+r['old_length'],'delta':r['new_length']-r['old_length']}
                    for r in block['text_records']+block['choice_commands']],key=lambda r:r['start'])
    def mapped(at):
        delta=0
        for p in patches:
            if at<p['start']:break
            assert not p['start']<at<p['end']
            if at==p['start']:return at+delta
            delta+=p['delta']
        return at+delta
    native={mapped(r['offset']):r for r in source['all_nested_native_commands']}
    edges={r['new_offset']:r for r in block['relative_skip_fixups']}
    rows=[r for r in trace['rows'] if r['source'].get('route')==2 and r['source'].get('block')==120]
    assert len(rows)==60 and rows[0]['source']['instruction_offset']==8
    pairs=[];last=0
    for i,(a,b) in enumerate(zip(rows[::2],rows[1::2],strict=True)):
        assert a['kind']=='before_command' and b['kind']=='after_command' and a['source']==b['source']
        assert trace['rows'][b['entry_row']]==a
        src=a['source'];old=native[src['instruction_offset']]
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==block['research_block_sha256']
        assert sha(Path(src['actual_payload_file']).read_bytes())==src['actual_sha256']
        assert src['first_word']==old['word']
        if src['first_word'] in (0x100,0x200,0x300):
            edge=edges[src['instruction_offset']]
            take=src['first_word']==0x100 or (src['first_word']==0x200 and last==0) or (src['first_word']==0x300 and last==1)
            next_at=edge['new_matched_skip_target'] if take else edge['new_unmatched_next']
            assert src['instruction_offset']+b['decoded_length']==next_at
        else:
            assert src['instruction_offset']+b['decoded_length']==mapped(old['offset']+old['native_extent'])
        if b['result_words'][0]==2:last=b['result_words'][1]
        if i+1<len(rows)//2:assert rows[2*i+2]['source']['instruction_offset']==src['instruction_offset']+b['decoded_length']
        pairs.append({'source_offset':old['offset'],'actual_offset':src['instruction_offset'],'word':old['word'],
            'decoded_length':b['decoded_length'],'frames':[a['frame'],b['frame']],'result_words':b['result_words']})
    assert pairs[-1]['word']==0 and pairs[-1]['result_words']==[0,0]
    assert pairs[-1]['actual_offset']+pairs[-1]['decoded_length']==block['research_logical_end']
    chosen=next(r for r in pairs if r['word']==0x2100);assert chosen['result_words']==[2,0]
    assert len(nav['choices'])==1 and nav['choices'][0]['normal_A_selects_original_default_option0']
    assert len(nav['holds'])==14
    fonts={r['id']:r for r in read('work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json')['cases']}
    modals={r['id']:r for r in read('work/analysis/lil_Deck_label_approval_v1758/all9_current_FE_reconciliation.json')['reviewed_cases']}
    text_map={r['id']:r for r in block['text_records']}
    wrapped=struct.unpack_from('<I',arm,0x54450)[0];checks=[];pictures=[]
    for group in nav['holds']:
        spec=text_map[group['id']];ref=fonts[group['id']];panel=group['system_FE'];width=228 if panel else 216
        preview=Image.open(modals[group['id']]['display_preview'] if panel else ref['preview']).convert('RGB')
        assert preview.size==(width,64)
        wanted={(16+x,296+y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(0,8,0)}
        active=next((a,b) for a,b in zip(rows[::2],rows[1::2],strict=True) if a['source']['instruction_offset']==spec['new_offset']-5)
        holds=[]
        for original_hold in group['holds']:
            frame=original_hold['frame'];assert active[0]['frame']<frame<active[1]['frame']
            p=photos[frame];raw=Path(snapshots[frame]['path']).read_bytes();im=Image.open(p['path']).convert('RGB')
            actual={(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y))==(0,8,0)}
            assert actual==wanted,(group['id'],frame,len(wanted-actual),len(actual-wanted))
            src=active[0]['source'];at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==block['research_block_sha256']
            if not panel:assert cstring(raw,wrapped)==bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil')
            holds.append({'frame':frame,'capture':p['path'],'capture_sha256':p['PNG_sha256'],
                          'RAM_sha256':snapshots[frame]['sha256'],'whole_native_independent_actual_ink_equal':True})
        assert len(holds)==2
        checks.append({'id':group['id'],'system_FE':panel,'source_speaker_hex':spec['target_hex'][:2],
            'two_complete_actual_holds':holds,'complete_first_last_letters_bounds_and_no_extra_pages':True})
        pictures.append(Image.open(holds[1]['capture']).convert('RGB'))
    ids={r['id'] for r in checks};assert {'DK4_MES_B120_R0134','DK4_MES_B120_R0137'}<=ids
    assert [r['id'] for r in checks if r['system_FE']]==['DK4_MES_B120_R0186']
    assert ids=={text_map_id for text_map_id,spec in text_map.items() if spec['new_offset']-5 in {r['actual_offset'] for r in pairs if r['word']==0x4000}}
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(checks),10):
        sheet=Image.new('RGB',(1052,1270),(28,36,40));draw=ImageDraw.Draw(sheet)
        for k,(r,im) in enumerate(zip(checks[start:start+10],pictures[start:start+10],strict=True)):
            x,y=8+522*(k%2),6+252*(k//2);draw.text((x,y),r['id']+' speaker'+r['source_speaker_hex'],fill='white')
            sheet.paste(im.crop((0,272,256,384)).resize((512,224),Image.Resampling.NEAREST),(x,y+20))
        p=ROOT/f'actual_sailing_choice0_sheet_{start//10+1:02d}.png';sheet.save(p);sheets.append({'path':str(p),'sha256':sha(p.read_bytes())})
    save(ROOT/'complete_B120_choice0_scene_audit.json',{
        'research_ROM':str(rom),'research_ROM_sha256':digest,'ARM9_sha256':sha(arm),'terminal_frame':27850,
        'all30_original_B120_command_pairs_and_mapped_branches_verified':pairs,
        'original_choice0_and_normal_type0_return':True,'speeches':checks,'actual_review_sheets':sheets,
        'all14_speeches28_holds_full_native_independent_actual_ink_match':True,
        'R134_and_R137_now_individually_visited':True,'no_preloaded_save_savestate_or_gameplay_fixture':True,
        'all_inputs_PNG_hashes_and4MiB_snapshots_verified':True,
        'readonly_callback_count':trace['callbacks'],'all_readonly_callbacks_zero_errors_mismatches_host_restored':True,
        'unreturned_at_end':trace['unreturned_at_capture_end'],
        'choice_menu_capture':photos[nav['choices'][0]['frame']],'terminal_capture':photos[27850],
        'visual_review_pending':True,'registered_release_pending':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',CAP/'capture_report.json',CAP/'observer/commands.json',NAV/'closed_B120_unit_and_next_context.json')},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'B120_commands':len(pairs),'speeches':len(checks),'complete_actual_holds':28,'fixture_free':True},flush=True)
