"""Revised B120 wind path: all executed commands and complete actual text holds."""
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_revised_wind_v1744')
RUN = Path('work/analysis/lil_lessons_revised_v1741')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lessons_revised_v1741_RESEARCH_ONLY')

if __name__ == '__main__':
    assert not ROOT.exists()
    plan, terminal, report, trace = map(read, (RUN/'run_plan.json', RUN/'terminal.json',
        CAP/'capture_report.json', CAP/'observer/commands.json'))
    rom = Path(plan['research_ROM'])
    digest = sha(rom.read_bytes())
    assert digest == plan['research_ROM_sha256'] == terminal['research_ROM_sha256'] == report['ROM_sha256']
    assert terminal['terminal'] and report['frames'] == terminal['frames'] == 29930
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == read(plan['inputs'])
    assert sha(Path(plan['inputs']).read_bytes()) == plan['inputs_sha256']
    assert not trace['errors'] and trace['mismatches'] == 0 and not trace['unreturned_at_capture_end']
    assert trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    previous = read('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711/observer/commands.json')
    selected = lambda t: [r for r in t['rows'] if r['source'].get('route') == 2 and r['source'].get('block') == 120]
    rows, old_rows = selected(trace), selected(previous)
    assert len(rows) == len(old_rows) == 82
    relocation = read('work/analysis/lil_lesson_relocation_v1731/nested_source_relocation_research.json')
    block = next(b for b in relocation['blocks'] if b['block'] == 120)
    patches = sorted([{'start':r['old_offset'], 'end':r['old_offset']+r['old_length'], 'delta':r['new_length']-r['old_length']}
                      for r in block['text_records']+block['choice_commands']], key=lambda r:r['start'])
    def mapped(at):
        delta=0
        for p in patches:
            if at < p['start']: break
            assert not p['start'] < at < p['end']
            if at == p['start']: return at+delta
            delta += p['delta']
        return at+delta
    command_pairs=[]
    for i,(a,b,oa,ob) in enumerate(zip(rows[::2],rows[1::2],old_rows[::2],old_rows[1::2],strict=True)):
        assert a['kind']=='before_command' and b['kind']=='after_command'
        assert a['source']==b['source'] and b['entry_row']==trace['rows'].index(a)
        src=a['source']; old=oa['source']
        assert src['whole_resident_payload_exact_ROM'] and src['actual_sha256']==block['research_block_sha256']
        assert sha(Path(src['actual_payload_file']).read_bytes())==src['actual_sha256']
        assert src['first_word']==old['first_word'] and src['instruction_offset']==mapped(old['instruction_offset'])
        assert b['result_words']==ob['result_words']
        assert src['instruction_offset']+b['decoded_length']==mapped(old['instruction_offset']+ob['decoded_length'])
        if i+1<len(rows)//2:
            assert rows[2*i+2]['source']['instruction_offset']==src['instruction_offset']+b['decoded_length']
        command_pairs.append({'source_offset':old['instruction_offset'],'actual_offset':src['instruction_offset'],
            'word':src['first_word'],'frames':[a['frame'],b['frame']],
            'source_decoded_length':ob['decoded_length'],'actual_decoded_length':b['decoded_length'],
            'result_words':b['result_words'],'all_results_and_mapped_destinations_match_original_path':True})
    assert command_pairs[0]['actual_offset']==8 and command_pairs[-1]['result_words']==[0,1]
    assert command_pairs[-1]['actual_offset']+command_pairs[-1]['actual_decoded_length']==block['research_logical_end']
    choice=next(r for r in command_pairs if r['word']==0x2100)
    assert choice['result_words']==[2,1]
    branch=next(r for r in command_pairs if r['source_offset']==0x454)
    assert branch['word']==0x300 and branch['actual_decoded_length']==180
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw=Path(r['path']).read_bytes()
        assert len(raw)==r['bytes']==0x400000 and sha(raw)==r['sha256'] and r['read_only_export']
        snapshots[r.get('frame',29930)]=r
    photos={}
    for r in report['frames_captured']:
        p=Path(r['path']); assert sha(p.read_bytes())==r['PNG_sha256']
        assert Image.open(p).size==(256,384)
        photos[r['frame']]=r
    fonts=read('work/analysis/lil_lesson_layout_v1725/all60_native_font_reconciliation.json')
    native={r['id']:r for r in fonts['cases']}
    modal={r['id']:r for r in read('work/analysis/lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json')['reviewed_cases']}
    by_offset={r['new_offset']-5:r for r in block['text_records']}
    arm=NdsImage.open(rom).read_file('/__arm9__.bin')
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    checks=[]; pictures=[]
    for a,b in zip(rows[::2],rows[1::2],strict=True):
        if a['source']['first_word']!=0x4000: continue
        spec=by_offset[a['source']['instruction_offset']]; ref=native[spec['id']]
        panel=ref['consumer']=='original_FE_modal_548A8'
        preview_path=Path(modal[spec['id']]['display_preview'] if panel else ref['preview'])
        preview=Image.open(preview_path).convert('RGB')
        width=228 if panel else 216
        assert preview.size==(width,64)
        wanted={(16+x,296+y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(0,8,0)}
        holds=sorted(f for f in photos if a['frame']+120<=f<b['frame'])[-2:]
        assert len(holds)==2,(spec['id'],a['frame'],b['frame'])
        verified=[]
        for frame in holds:
            photo=photos[frame]; im=Image.open(photo['path']).convert('RGB')
            actual={(x,y) for y in range(296,360) for x in range(16,16+width) if im.getpixel((x,y))==(0,8,0)}
            assert actual==wanted,(spec['id'],frame,len(wanted-actual),len(actual-wanted))
            raw=Path(snapshots[frame]['path']).read_bytes(); src=a['source']; at=src['payload_address']-0x02000000
            assert sha(raw[at:at+src['payload_bytes']])==block['research_block_sha256']
            if not panel:
                assert cstring(raw,wrapped)==bytes.fromhex(spec['target_hex'])[1:].replace(b'FI',b'Lil')
            verified.append({'frame':frame,'capture':photo['path'],'capture_sha256':photo['PNG_sha256'],
                             'RAM_sha256':snapshots[frame]['sha256'],'complete_native_independent_ink_plane_exact':True})
        checks.append({'id':spec['id'],'system_FE':panel,'speaker_prefix_hex':spec['target_hex'][:2],
            'source_offset':spec['old_offset']-5,'actual_offset':spec['new_offset']-5,'two_complete_actual_holds':verified,
            'no_leading_trailing_letters_missing_no_overflow_extra_ink_or_extra_page':True})
        pictures.append(Image.open(photos[holds[-1]]['path']).convert('RGB'))
    assert len(checks)==22 and sum(r['system_FE'] for r in checks)==6
    ROOT.mkdir(parents=True)
    sheets=[]
    for start in range(0,len(checks),10):
        sheet=Image.new('RGB',(1052,1270),(28,36,40)); draw=ImageDraw.Draw(sheet)
        for k,(r,im) in enumerate(zip(checks[start:start+10],pictures[start:start+10],strict=True)):
            x,y=8+522*(k%2),6+252*(k//2)
            draw.text((x,y),r['id']+(' SYSTEM' if r['system_FE'] else ' speaker'+r['speaker_prefix_hex']),fill='white')
            sheet.paste(im.crop((0,272,256,384)).resize((512,224),Image.Resampling.NEAREST),(x,y+20))
        p=ROOT/f'actual_revised_wind_sheet_{start//10+1:02d}.png'; sheet.save(p)
        sheets.append({'path':str(p),'sha256':sha(p.read_bytes())})
    save(ROOT/'actual_revised_wind_branch_proof.json',{
        'research_ROM':str(rom),'research_ROM_sha256':digest,'terminal_frame':29930,
        'all41_original_command_pairs_mapped_and_same_path_results':command_pairs,
        'all22_executed_speeches44_holds_complete_native_independent_actual_pixels':checks,
        'all6_revised_FE_panels_actual_full_ink_matches_prior_composition_contract':True,
        'actual_wind_option1_selected_native_result2_1_and_mapped_relative_skip180':True,
        'normal_original_type0_scene_end_confirmed_with_unused_prior_choice1_word':True,
        'all262_readonly_callbacks_zero_errors_mismatches_host_restored':True,
        'all_capture_input_and4MiB_snapshot_hashes_verified':True,
        'actual_review_sheets':sheets,'visual_review_pending':True,
        'choice_menu_capture':photos[26330], 'terminal_capture':photos[29930],
        'other_B120_alternatives_B23_and_registered_release_pending':True,
        'no_preloaded_save_savestate_or_gameplay_fixture':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'observer/commands.json')},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Revised B120 wind path:41 mapped command pairs,22 dialogues/44 full-pixel holds,6 actual FE panels,choice1 and normal scene end pass.',flush=True)
