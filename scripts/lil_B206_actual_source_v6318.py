"""Load terminal actual B206 path evidence with exact original command/source bindings."""
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
COMMON=[5,9,13,17,20,24,28,32,36,39,42,46,49,53]
TAILS={'buy':[68,71,75,90],'high_price':[68,71,75,97,100,103,106],'pitch_refusal':[117,120]}
OPTIONS={'buy':[0,0],'high_price':[0,1],'pitch_refusal':[1]}
SOURCE=Path('work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json')
ENGLISH=Path('work/analysis/lil_B206_English_fixture_v6312/complete_B206_English_B22_fixture.json')
RUNS={('source','buy'):'shady_man_source_run_v6262_buy',('source','high_price'):'lil_B206_current_source_run_v6316_high_price',('source','pitch_refusal'):'lil_B206_current_source_run_v6317_pitch_refusal',('English','buy'):'lil_B206_English_run_v6313_buy',('English','high_price'):'lil_B206_English_run_v6314_high_price',('English','pitch_refusal'):'lil_B206_English_run_v6315_pitch_refusal'}
def load(language,path):
    manifest=SOURCE if language=='source' else ENGLISH;fixture=read(manifest)['fixtures'][0];run=Path('work/analysis')/RUNS[language,path];terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');assert terminal['terminal'] and terminal['observer_instances']==1 and terminal['observer_host_slots_restored'];cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==plan['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert plan['explicit_B22_entry_ROM_fixture'] and plan['source_event206_not_naturally_selected'] and plan['all42_source_commands_retained'] and sha(Path(plan['fixture_manifest']).read_bytes())==plan['fixture_manifest_sha256']==sha(manifest.read_bytes())
    schedule=read(plan['original_inputs']);assert report['scripted_input_schedule']==schedule and sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'];assert [r['start'] for r in schedule if r['buttons']==['DOWN']]=={'buy':[],'high_price':[7300],'pitch_refusal':[6300]}[path]
    image=NdsImage.open(fixture['research_ROM']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;block=bank[22];assert block.hex()==fixture['fixture_block_hex'] and sha(block)==fixture['fixture_block_sha256'];photos={}
    for p in report['frames_captured']:
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];photo=Image.open(p['path']).convert('RGB');assert photo.size==(256,384);photos[p['frame']]=(p,photo)
    snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256']
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};pairs=[];speeches=[];following=[];seen=set()
    for r in trace['rows']:
        assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if r['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=r['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=r['result_words']));continue
        entry=trace['rows'][r['entry_row']];at=entry['source']['instruction_offset'];word=int.from_bytes(block[at:at+2],'little');c=commands.get(at);seen.add(at)
        if c:assert word==c['source_word'] and (r['decoded_length']==c['native_extent'] or word in [0x100,0x200,0x300,0x400])
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=word,start=entry['frame'],returned=r['frame'],decoded_length=r['decoded_length'],native_result=r['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=r['original_RNG_seed'],UI_after=r['native_UI_request_words']);pairs.append(pair)
        if at in records:
            text=records[at];assert block[at:at+text['native_extent']].hex()==text['whole_command_hex'];speeches.append(dict(id=text['id'],source_record_index=text['source_record_index'],prefix=text['source_selector'],interval=pair))
    assert [r['source_record_index'] for r in speeches]==COMMON+TAILS[path];menus=[r for r in pairs if r['word']==0x2100];assert [m['native_result'] for m in menus]==[[2,o] for o in OPTIONS[path]] and [m['source_offset'] for m in menus]==([852] if path=='pitch_refusal' else [852,1020])
    assert pairs[-1]['word']==0 and pairs[-1]['source_offset']==1518 and pairs[-1]['native_result']==[0,OPTIONS[path][-1]] and any(r['block']==120 and r['word']==0 and r['offset']==2312 for r in following)
    files=[manifest,run/'terminal.json',run/'run_plan.json',rp,tp,Path(plan['original_inputs'])];return dict(language=language,path=path,fixture=fixture,plan=plan,report=report,trace=trace,image=image,photos=photos,command_pairs=pairs,speech_intervals=speeches,menu_intervals=menus,following_commands=following,all_seen_offsets=seen,exit_frame=pairs[-1]['returned'],final_snapshot=snap,capture_report=str(rp),observer_report=str(tp),evidence={str(p):sha(p.read_bytes()) for p in files})
