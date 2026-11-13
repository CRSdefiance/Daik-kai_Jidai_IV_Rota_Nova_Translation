"""Bind active own-RAM label tables, actual skill pixels and room references; reject stale-string inference."""
import struct
from pathlib import Path
from PIL import Image
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/HELP_active_skill_labels_20261105')
RELEASE=Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json')
SKILLS=[('生命力','Vigor'),('統率力','Command'),('操船術','Sailing'),('測量術','Survey'),('会計術','Finance'),
    ('剣闘術','Swords'),('命中力','Aim'),('説得力','Speech'),('謀略術','Guile'),('観察力','Observe')]
ATTRIBUTES=[('体力','Stamina'),('敏捷','Agility'),('魅力','Charm'),('知力','Wits'),('精神','Spirit'),('運勢','Luck')]
MOODS=[('ハイ','Excited'),('元気','Good'),('リラックス','Relaxed'),('通常','Normal'),('不機嫌','Upset'),('混乱','Confused')]
CONDITIONS=[('健康','Healthy'),('疲労','Tired'),('軽傷','Hurt'),('重傷','Wounded'),('瀕死','Dying'),('疾病','Sick'),('死亡','Dead')]

if __name__=='__main__':
    out=ROOT/'active_terms_binding_v1.json';assert not out.exists()
    release=load(RELEASE);startup_path=RELEASE.with_name('own_registered_startup_verification.json');startup=load(startup_path)
    own_report_path=Path(startup['capture_report']);own_report=load(own_report_path);snapshot=own_report['read_only_RAM_snapshot'];ram=Path(snapshot['path']).read_bytes()
    assert not release['own_registered_startup_pending']and release['clean_input_patch_byte_exact']
    assert sha(ram)==snapshot['sha256']and len(ram)==4194304
    image=NdsImage.open(release['candidate']);arm=image.read_file('/__arm9__.bin');clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert sha(Path(release['candidate']).read_bytes())==release['candidate_sha256']
    code=MainCodeFile(arm,0x2000000)
    def active_string(address):
        if 0x2000000<=address<0x2400000:return ram[address-0x2000000:].split(b'\0',1)[0]
        for section in code.sections:
            at=address-section.ramAddress
            if 0<=at<len(section.data):return bytes(section.data[at:]).split(b'\0',1)[0]
        raise AssertionError('Unmapped active label '+hex(address))
    tables=[]
    for table,rows,group in [(0x148398,ATTRIBUTES,'Attributes'),(0x1483e4,SKILLS,'Skills'),(0x1483b0,MOODS,'Mood'),(0x1483c8,CONDITIONS,'Physical condition')]:
        assert arm[table:table+4*len(rows)]==ram[table:table+4*len(rows)]
        cases=[]
        for i,(jp,en)in enumerate(rows):
            field=table+4*i;p=struct.unpack_from('<I',clean,field)[0];q=struct.unpack_from('<I',ram,field)[0]
            assert 0x2000000<=p<0x2400000
            source=clean[p-0x2000000:].split(b'\0',1)[0];current=active_string(q)
            assert source==jp.encode('cp932')and current==en.encode('ascii'),(group,i,source,current)
            cases.append(dict(index=i,pointer_field=field,source_pointer=p,current_pointer=q,Japanese=jp,English=en,
                source_hex=source.hex(),current_hex=current.hex(),own_RAM_table_exact_to_current_ROM=True))
        tables.append(dict(group=group,table=table,records=cases))
    assert arm[0x7e070:0x7e108]==clean[0x7e070:0x7e108]
    old_status=Path('work/analysis/condition_labels_v387/native_proof.json');assert load(old_status)['all512_selector_values_and_original_fallbacks_guards_ABI_pass']
    prior_binding_path=Path('work/analysis/Shared_HELP_T103_T132_clean_20261104/native_roles_rooms_andskills_v1.json');prior_binding=load(prior_binding_path)
    rooms=[]
    for label in prior_binding['stored_room_skill_andcommand_labels']:
        at=label['offset']
        if not 0x12ff50<=at<=0x130014:continue
        needle=struct.pack('<I',0x2000000+at);fields=[i for i in range(0,len(clean)-3,4)if clean[i:i+4]==needle]
        assert len(fields)==1
        field=fields[0];q=struct.unpack_from('<I',ram,field)[0]
        assert arm[field:field+4]==ram[field:field+4]and active_string(q)==label['English'].encode('ascii')
        rooms.append(dict(source_label=label,pointer_field=field,current_pointer=q,current_text=active_string(q).decode('ascii'),
            original_aligned_reference_current_pointer_andown_RAM_string_bound=True))
    assert len(rooms)==21
    run=load(ROOT/'run_plan_v1.json');report_path=ROOT/'capture_v1/capture_report.json';report=load(report_path)
    assert report['ROM_sha256']==run['ROM_sha256']==sha(Path(run['ROM']).read_bytes())and report['frames']==8600
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not any(v for k,v in report.items()if k.startswith('synthetic_'))
    assert sha(Path(run['battery']).read_bytes())==run['battery_sha256']and report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    assert NdsImage.open(run['ROM']).read_file('/__arm9__.bin')==arm
    for frame in report['frames_captured']:assert sha(Path(frame['path']).read_bytes())==frame['PNG_sha256']
    capture=next(r for r in report['frames_captured']if r['frame']==8600);picture=Image.open(capture['path']).convert('RGB');pixels=picture.load();font=GameAsciiFont.from_arm9(arm);masks=[]
    for jp,term in SKILLS:
        points=set()
        for i,c in enumerate(term):
            glyph=font.decode(c);points.update((i*6+x,y)for y in range(11)for x in range(6)if glyph.getpixel((x,y)))
        first=next(iter(points));matches=[];color=(230,230,230)
        for y in range(260,348):
            for x in range(256-len(term)*6):
                if pixels[x+first[0],y+first[1]]!=color:continue
                if all(pixels[x+dx,y+dy]==color for dx,dy in points):
                    actual={(dx,dy)for dy in range(11)for dx in range(len(term)*6)if pixels[x+dx,y+dy]==color}
                    if actual==points:matches.append((x,y))
        assert len(matches)==1,(term,matches)
        masks.append(dict(English=term,Japanese=jp,x=matches[0][0],y=matches[0][1],width=len(term)*6,height=11,
            complete_ink_pixels=len(points),all_ink_andblank_cells_andfirst_final_letters_exact=True))
    old_ui=Path('work/analysis/skill_terms_v463/UI_term_proof.json');assert load(old_ui)['actual_native_skill_labels']==[en for jp,en in SKILLS]
    save(out,dict(verified_release=str(RELEASE),verified_release_sha256=sha(RELEASE.read_bytes()),current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],
        current_ARM9_sha256=sha(arm),source_ARM9_sha256=sha(clean),own_startup=str(startup_path),own_startup_sha256=sha(startup_path.read_bytes()),own_RAM=snapshot,
        active_label_tables=tables,active_room_references=rooms,actual_capture_report=str(report_path),actual_capture_report_sha256=sha(report_path.read_bytes()),
        actual_skill_capture=capture,actual_all10_complete_skill_masks=masks,all_four_individual_navigation_frames_directly_viewed=True,
        historical_active_skill_order_andlabels_confirmed=str(old_ui),historical_active_skill_order_andlabels_proof_sha256=sha(old_ui.read_bytes()),
        condition_selector_code_clean_exact_reusing_prior512_cases=str(old_status),condition_selector_prior_proof_sha256=sha(old_status.read_bytes()),
        inactive_original_Health_Social_Tactics_strings_are_not_active_skill_names=True,
        supersedes_static_skill_label_inference_in_prior_binding=str(prior_binding_path),prior_binding_sha256=sha(prior_binding_path.read_bytes()),
        Help30_topics_requiring_correction=[116,117,118,121,126],Help33_required_term='Speech',Help66_Command_confirmed_active=True,
        physical_Health_heading_distinct_from_Vigor_skill=True,Dead_is_native_extra_state_not_added_to_six_state_source_Help=True,
        original_battery_preserved_no_new_RAM_code_location_fixture_or_savestate=True,
        alternate_moods_conditions_andall_rooms_not_newly_visited=True,no_new_Rafael_progress_full_story_orhardware_claim=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    print('Active tables bound:Vigor/Speech/Guile,all10 actual complete skill masks,6 attributes,13 conditions and21 room references. Correct Help30;Command remains valid.')
