"""Audit actual original B23 completion, all text holds and location-only provenance."""
import argparse
import json
import struct
from pathlib import Path
from PIL import Image, ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lil_Bruges_location_v1754 import apply_fixture, REQUEST
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read, save

VERSIONS={
    'initial':('lil_crew_lesson_v1756','lil_lesson_relocation_v1731',
        'lil_lesson_layout_v1725/all60_native_font_reconciliation.json',
        'lil_FE_display_v1737/actual_paper_contract_and_all9_reviewed_FE_panels.json'),
    'final':('lil_crew_final_text_v1764','lil_lessons_relocation_v1760',
        'lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json',
        'lil_Deck_label_approval_v1758/all9_current_FE_reconciliation.json')}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--version',choices=VERSIONS,required=True);args=parser.parse_args()
    name,map_name,font_name,modal_name=VERSIONS[args.version]
    ROOT=Path('work/analysis/lil_crew_scene_v1763_'+args.version);assert not ROOT.exists()
    RUN=Path('work/analysis')/name
    CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/(name+'_RESEARCH_ONLY')
    plan,terminal,report,trace,journal=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json'))
    rom=Path(plan['research_ROM']);digest=sha(rom.read_bytes());image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin')
    assert digest==plan['research_ROM_sha256']==terminal['research_ROM_sha256']==report['ROM_sha256']
    assert terminal['terminal'] and terminal['frame']==report['frames']==41420
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report
    synthetic={k:v for k,v in report.items() if k.startswith('synthetic_') and v}
    assert set(synthetic)=={'synthetic_battle_recovery_proximity_fixtures'}
    fixtures=synthetic['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==1
    assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    commands=[json.loads(s) for s in (RUN/'navigation.jsonl').read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    assert commands==[r['command'] for r in journal['commands_received']]
    assert commands[-1]=={'stop':True} and journal['last_command_frame']==41420
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
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
    fixture=fixtures[0];assert fixture['frame']==30290 and len(fixture['owned_bytes'])==16
    before=Path(snapshots[30290]['path']).read_bytes();after,recomputed=apply_fixture(arm,before,REQUEST)
    assert fixture['before_RAM_sha256']==sha(before) and fixture['after_RAM_sha256']==sha(after)
    assert {k:v for k,v in fixture.items() if k!='frame'}==recomputed
    assert all(r['address'] in fixture['owned_bytes'] for r in fixture['changes'])
    assert fixture['original_known_town_scan_returns_Bruges3_without_any_state_edit']
    mapping=read(Path('work/analysis')/map_name/'nested_source_relocation_research.json')
    block=next(b for b in mapping['blocks'] if b['block']==23)
    source=next(b for b in read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')['blocks'] if b['block']==23)
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
    rows=[r for r in trace['rows'] if r['source'].get('route')==2 and r['source'].get('block')==23]
    assert len(rows)%2==0 and rows[0]['source']['instruction_offset']==8
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
    assert pairs[-1]['word']==0 and pairs[-1]['result_words'][0]==0
    chosen=next(r for r in pairs if r['word']==0x2100);assert chosen['result_words']==[2,0]
    nav=read('work/analysis/lil_crew_navigation_v1759b/closed_B23_unit_and_next_context.json')
    assert len(nav['holds'])==30
    fonts={r['id']:r for r in read(Path('work/analysis')/font_name)['cases']}
    modals={r['id']:r for r in read(Path('work/analysis')/modal_name)['reviewed_cases']}
    text_map={r['id']:r for r in block['text_records']}
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    checks=[];pictures=[]
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
    assert sum(r['system_FE'] for r in checks)==1
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,30,10):
        sheet=Image.new('RGB',(1052,1270),(28,36,40));draw=ImageDraw.Draw(sheet)
        for k,(r,im) in enumerate(zip(checks[start:start+10],pictures[start:start+10],strict=True)):
            x,y=8+522*(k%2),6+252*(k//2);draw.text((x,y),r['id']+' speaker'+r['source_speaker_hex'],fill='white')
            sheet.paste(im.crop((0,272,256,384)).resize((512,224),Image.Resampling.NEAREST),(x,y+20))
        p=ROOT/f'actual_crew_sheet_{start//10+1:02d}.png';sheet.save(p);sheets.append({'path':str(p),'sha256':sha(p.read_bytes())})
    save(ROOT/'complete_B23_scene_and_fixture_audit.json',{
        'version':args.version,'research_ROM':str(rom),'research_ROM_sha256':digest,'terminal_frame':41420,
        'all_original_B23_command_pairs_and_mapped_branches_verified':pairs,
        'original_choice0_full_lesson_and_normal_type0_return':True,'speeches':checks,'actual_review_sheets':sheets,
        'all30_speeches60_holds_full_native_independent_actual_ink_match':True,
        'one16_coordinate_byte_fixture_no_town_event_RNG_or_outcome_fields_changed':True,
        'all_inputs_fixture_replay_PNG_hashes_and4MiB_snapshots_verified':True,
        'all_readonly_callbacks_zero_errors_mismatches_host_restored':True,
        'unreturned_at_end_outside_completed_B23':trace['unreturned_at_capture_end'],
        'source_V1756_plan_fixture_path_metadata_erratum':'Actual import and recorded fixture hash are1754;its slash-path metadata says1752c.',
        'docking_prompt_capture':photos[30920],'choice_menu_capture':photos[32210],'terminal_capture':photos[41420],
        'original_both_early_FE_branches_skipped_after_completed_wind_lesson_same_texts_verified_in_B120':True,
        'visual_review_pending':True,'registered_release_and_other_choice_path_pending':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in (RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',CAP/'capture_report.json',CAP/'observer/commands.json')},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'version':args.version,'B23_commands':len(pairs),'speeches':30,'complete_actual_holds':60,'only_coordinate_fixture_bytes':16},flush=True)
