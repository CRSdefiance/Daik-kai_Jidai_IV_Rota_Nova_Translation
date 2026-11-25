"""Source-bound global4000/prefix10 mapping;not a visit to Gerhard's B27 branch."""
import json
import struct
from pathlib import Path
from PIL import Image
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_name_catalog_glyphs_v278 import raster,expected_pixels
from scripts.verify_port_gameplay_v762 import cstring
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Gerhard_story_control_proof_v1857')
RUN=Path('work/analysis/Gerhard_story_control_v1856')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/Gerhard_story_control_v1856_V1841')
PACKET=Path('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')
BASE=0x02000000

if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace,journal=map(read,(RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',
        CAP/'observer/commands.json',CAP/'navigation_command_journal.json'))
    rom=Path(plan['candidate']);digest=sha(rom.read_bytes());image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin')
    assert digest==plan['candidate_sha256']==terminal['candidate_sha256']==report['ROM_sha256']
    assert terminal['terminal']and terminal['frame']==report['frames']==7160
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not any(v for k,v in report.items()if k.startswith('synthetic_'))and'battery_save_preloaded'not in report
    assert not trace['errors']and not trace['mismatches']and trace['all_host_slots_restored_and_core_file_exact']
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']]
    assert commands[-1]=={'stop':True}and journal['last_command_frame']==7160
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for r in journal['commands_received']:
        assert r['validation_passed'];c=r['command']
        if c.get('buttons'):schedule.append({'start':r['frame']+1,'duration':c['duration'],'buttons':c['buttons']})
    assert schedule==report['scripted_input_schedule']
    photos={r['frame']:r for r in report['frames_captured']}
    for r in photos.values():assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==0x400000 and sha(raw)==r['sha256']and r['read_only_export']
        if 'frame'in r:snapshots[r['frame']]=r
    a=next(r for r in trace['rows']if r['kind']=='before_command'and r['source'].get('route')==1
           and r['source'].get('block')==42 and r['source']['instruction_offset']==304)
    b=next(r for r in trace['rows']if r['kind']=='after_command'and trace['rows'][r['entry_row']]==a)
    block=IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks[42]
    assert block[304:310]==bytes.fromhex('0040ffff0010')
    text=block[310:block.index(b'\0',310)]
    assert text.strip()==b'Admiral, address the crew.'
    assert a['source']['whole_resident_payload_exact_ROM']and a['source']['actual_sha256']==sha(block)
    assert b['decoded_length']==34 and b['result_words'][0]==3
    wrapped=struct.unpack_from('<I',arm,0x54450)[0];actual_holds=[]
    for frame in(6800,6830):
        raw=Path(snapshots[frame]['path']).read_bytes();assert a['frame']<frame<b['frame']
        expanded=cstring(raw,wrapped);assert expanded==text
        pixels,events,font=raster(arm,expanded);assert pixels==expected_pixels(arm,font,events)
        visible=[e['code']for e in events if e['code']!=32]
        assert visible==[c for c in text if c not in(32,10)]
        wanted={(16+x,296+y)for y in range(64)for x in range(216)if pixels[y*216+x]==1}
        im=Image.open(photos[frame]['path']).convert('RGB')
        actual={(x,y)for y in range(296,360)for x in range(16,232)if im.getpixel((x,y))==(0,8,0)}
        assert actual==wanted
        cpu,get=get_machine(arm,raw);assert get(0x7F244)==1 and get(0x2434C,16)==16
        assert bytes(cpu.mem_read(BASE,0x400000))==raw
        actual_holds.append({'frame':frame,'capture':photos[frame]['path'],'capture_sha256':photos[frame]['PNG_sha256'],
            'RAM_sha256':sha(raw),'complete_native_independent_actual_ink_equal':True,'complete_initial_A_and_final_period':True})
    # Same native selector and actor ID with Lil's original captain2 state.
    packet=read(PACKET);lil=read('work/analysis/lil_after_Amsterdam_inventory_v1846/all336_states_and_original_town_eligibility.json')
    raw=Path(lil['snapshot']).read_bytes();cpu,get=get_machine(arm,raw)
    assert get(0x7F244)==2 and get(0x2434C,16)==16 and bytes(cpu.mem_read(BASE,0x400000))==raw
    clean=NdsImage.open('work/clean.nds');assert arm[0x2434C:0x243A0]==clean.read_file('/__arm9__.bin')[0x2434C:0x243A0]
    original=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks[27]
    current=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[27]
    eligible=[]
    for row in packet['records']:
        if row['source_presentation_prefix_hex']!='10':continue
        ja=row['source_reference']['header_offset'];now=row['current_reference']['header_offset']
        assert original[ja:ja+6]==current[now:now+6]==block[304:310]
        eligible.append(row['id'])
    assert len(eligible)==9
    next_line=next(r for r in trace['rows']if r['kind']=='before_command'and r['source'].get('route')==1
        and r['source'].get('block')==42 and r['source']['instruction_offset']==338)
    assert next_line['frame']>=b['frame']
    ROOT.mkdir(parents=True)
    save(ROOT/'original4000_prefix10_Gerhard_live_mapping.json',{'candidate':str(rom),'candidate_sha256':digest,
        'ARM9_sha256':sha(arm),'native_control_selector':0x0202434C,'selector_equal_clean_source':True,
        'mapped_source_preamble_hex':'0040ffff0010','native_actor_ID':16,
        'native_catalog_name':packet['native_speaker_catalog']['16']['native_full_name'],
        'actor16_lookup_exact_on_actual_Hodram1_and_Lil2_snapshots':True,
        'actual_SC1B42_command304_before_after':[a,b],'two_complete_actual_text_holds':actual_holds,
        'actual_Gerhard_portrait_full_nameplate_body_and_normal_next_Hodram_portrait_viewed':True,
        'normal_next_source338_and_capture7160':{'source':next_line['source'],'capture':photos[7160]},
        'all_captures_inputs4MiB_and_readonly_observer_boundaries_verified':True,
        'fixture_free_current_ROM_NewGame_no_save_savestate_RNG_or_actor_override':True,
        'B27_clean_block_sha256':sha(original),'B27_current_block_sha256':sha(current),'eligible_B27_record_IDs':eligible,
        'only_leading0x10_in_exact_B27_source_and_exact_runtime_may_be_added_to_private_profile':True,
        'not_individual_B27_Gerhard_visits_or_approval_of_revised51_texts':True,
        'no_global_profile_codec_registry_or_ROM_change':True,
        'evidence':{str(p):sha(p.read_bytes())for p in(PACKET,RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json')},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'Gerhard_source_control':'10','native_actor':16,'actual_native_matching_holds':2,
        'eligible_private_B27_prefix_records':9,'new_prose_display_approval':False},flush=True)
