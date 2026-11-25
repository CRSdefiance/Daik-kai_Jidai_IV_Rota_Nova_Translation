"""Bind shared actual Lil panel/menu/return rules;no individual Seville claim."""
import struct
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster,expected_pixels
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Seville_sampling_v2721b')
ACTUAL=Path('work/analysis/lil_Hamburg_revised_audit_v1967b/revised_Hamburg79_choice_join_and_three_access_fixture_audit.json')
DOC=Path('translations/lil_seville_encounter_editorial_manuscript_v3.json')
FE=Path('work/analysis/lil_Seville_FE_v2713/current_FE_macro_font_and_typed_paper_proof.json')
CHOICE=Path('work/analysis/lil_Seville_choice_v2714/original_choice_decoder_VM_geometry_and_native_pixels.json')
REFERENCE=Path('work/analysis/lil_Seville_reference_census_v2720/all69_commands28_relative_sites_and_shipped_entry_census.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(DOC);actual=read(ACTUAL);im=NdsImage.open(doc['current_ROM']);old=NdsImage.open(actual['candidate']);clean=NdsImage.open('work/clean.nds');arm,oldarm=im.read_file('/__arm9__.bin'),old.read_file('/__arm9__.bin')
    assert sha(Path(actual['candidate']).read_bytes())==actual['candidate_sha256']
    assert all(actual[k] for k in ['all79_activated_revised_speeches158_holds_complete_native_independent_actual_glyphs','both_revised_choice_labels_two_actual_holds_complete_native_ink_and_bounds','native_menu_geometry_and_fixed_margins_calibrated_before_revised_pixels','normal_docking_B74_entry_and_Hamburg_return_not_overridden','all_inputs_capture_hashes4MiB_snapshots_and_three_access_footprints_verified','all_readonly_observer_boundaries_and_host_restoration_pass'])
    assert IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[74]==IlnkContainer.parse(old.read_file('/data/SC2.DK4')).blocks[74]
    for path in ['/GRP/KANJI.FNT','/data/EV2.DK4']:assert im.read_file(path)==old.read_file(path)
    nowfont,oldfont=GameAsciiFont.from_arm9(arm),GameAsciiFont.from_arm9(oldarm)
    for c in range(32,127):assert nowfont.decode(chr(c)).tobytes()==oldfont.decode(chr(c)).tobytes()
    spans=[(0x2425C,0x243A0),(0x54020,0x54450),(0x5473C,0x54984),(0x2A1D8,0x2A530),(0x51FC0,0x52030),(0x52E40,0x52F50),(0xD5404,0xD55A0)]
    for a,b in spans:assert arm[a:b]==oldarm[a:b]
    oldsections,newsections=MainCodeFile(oldarm,0x02000000).sections,MainCodeFile(arm,0x02000000).sections
    config_path=Path('translations/primary_town_services_editorial_release_v1.json');config=read(config_path)
    plan_path=Path('work/analysis/town_services_runtime_v2080/runtime_plan.json');plan=read(plan_path)
    deps={str(k).replace('\\','/'):v for k,v in config['dependencies'].items()};assert sha(plan_path.read_bytes())==deps[str(plan_path).replace('\\','/')]
    patch=next(p for p in plan['patches'] if p['address']==0x01FF9CE4);assert patch['section']==1 and len(bytes.fromhex(patch['target_hex']))==96
    at=patch['address']-oldsections[1].ramAddress
    assert oldsections[1].data[at:at+96]==bytes.fromhex(patch['source_hex']) and newsections[1].data[at:at+96]==bytes.fromhex(patch['target_hex'])
    restored=bytearray(newsections[1].data);restored[at:at+96]=bytes.fromhex(patch['source_hex']);assert restored==oldsections[1].data
    assert all(oldsections[i].data==newsections[i].data for i in [2,4])
    owned_ITCM_delta=dict(owner='registered primary_town_services_editorial release',config=str(config_path),config_sha256=sha(config_path.read_bytes()),plan=str(plan_path),plan_sha256=sha(plan_path.read_bytes()),address=patch['address'],bytes=96,source_hex=patch['source_hex'],target_hex=patch['target_hex'],all_other_ITCM_bytes_exact=True,parent=plan['modal_parent'],literal_IDs=plan['modal_literal_IDs'])
    delta=[i for i,(a,b) in enumerate(zip(oldsections[3].data[:-48],newsections[3].data[:-48],strict=True)) if a!=b];assert delta in [[],list(range(0x5D4,0x5DC))]
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return im
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    selected=[next(r for r in actual['revised_speech_observations'] if r['prefix_hex']==p) for p in ['02','10']];holds=[];pictures=[];evidence={str(ACTUAL):sha(ACTUAL.read_bytes()),str(DOC):sha(DOC.read_bytes()),str(FE):sha(FE.read_bytes()),str(CHOICE):sha(CHOICE.read_bytes()),str(REFERENCE):sha(REFERENCE.read_bytes()),'docs/editorial_testing_scope_v1870.md':sha(Path('docs/editorial_testing_scope_v1870.md').read_bytes())}
    wrapped=struct.unpack_from('<I',arm,0x54450)[0]
    for record in selected:
        for hold in record['holds']:
            capture=Path(hold['capture']);rp=Path(str(capture).replace('_navigation.png','_arm9_ram.bin'));raw=rp.read_bytes();assert sha(raw)==hold['RAM_sha256'] and sha(capture.read_bytes())==hold['capture_sha256'] and hold['complete_native_independent_actual_ink_equal']
            stream=hold['source'];payload=im.read_file('/data/SC2.DK4');block=IlnkContainer.parse(payload).blocks[74];offset=stream['payload_address']-0x02000000;assert raw[offset:offset+len(block)]==block and sha(block)==stream['actual_sha256']
            body=raw[wrapped-0x02000000:].split(b'\0')[0];pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events);rgb=Image.open(capture).convert('RGB')
            for index,color in [(1,(0,8,0)),(15,(98,97,98))]:
                expected={(16+i%216,296+i//216) for i,v in enumerate(pixels) if v==index};seen={(x,y) for y in range(296,360) for x in range(16,232) if rgb.getpixel((x,y))==color};assert expected==seen
            holds.append(dict(id=record['id'],frame=hold['frame'],capture=str(capture),capture_sha256=hold['capture_sha256'],RAM=str(rp),RAM_sha256=hold['RAM_sha256'],resident_expanded_body_hex=body.hex(),current_complete_native_ink_gray_and_blank_masks_equal=True,not_Seville_or_current_gameplay=True))
            evidence[str(capture)]=hold['capture_sha256'];evidence[str(rp)]=hold['RAM_sha256']
        pictures.append(dict(label='Historical B74 '+record['prefix_hex']+'; not Seville',capture=record['holds'][0]['capture']))
    assert len(holds)==4
    menu_holds=actual['revised_choice']['holds'];assert len(menu_holds)==2 and all(h['menu_proof'] for h in menu_holds)
    for hold in menu_holds:assert sha(Path(hold['capture']).read_bytes())==hold['capture_sha256'];evidence[hold['capture']]=hold['capture_sha256']
    pictures.append(dict(label='Historical two-choice menu; not Seville',capture=menu_holds[0]['capture']))
    fe=read(FE);assert fe['historical_calibration']['complete_current_native_ink_and_blank_mask_equal'];pictures.append(dict(label='Historical FE calibration; not Seville',capture=fe['historical_calibration']['capture']))
    last=actual['original_native_town_and_event_transitions'][-1];assert last['original_town_ID']==5 and last['original_event_completion_flags']['74']==1 and last['all4MiB_unchanged_by_queries']
    reference=read(REFERENCE);assert reference['all69_clean_current_target_commands_and28_relative_sites_reexecuted'] and reference['original_block_index_loader_and_parent_contract_verified_for336_blocks_two_modes']
    choice=read(CHOICE);assert choice['six_original_VM_selection_and_cancel_cases_pass'] and choice['stored_option_indices_and_original_selection_return_values_preserved']
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(pictures):
        x,y=i%2*256,i//2*410;draw.text((x+2,y+3),p['label'][:42],fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'historical_shared_panels_not_Seville.png';sheet.save(sp)
    save(ROOT/'representative_rule_reconciliation.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(arm),evidence=evidence,historical_progressive_holds=holds,historical_menu_holds=menu_holds,historical_FE_hold=fe['historical_calibration'],historical_Hamburg_return=last,
        all4_historical_progressive_holds_freshly_match_current_full_ink_gray_blank_masks=True,all95_current_ASCII_glyph_bitmaps_equal_historical=True,historical_B74_whole_source_block_equal_current=True,original_presenter_return_choice_VM_and_text_render_spans_historical_current_exact=True,current_deployed_payload_delta=delta,registered_owned_ITCM_wrapper_delta=owned_ITCM_delta,
        previous_three_access_fixtures=actual['exact_fixture_replays'],inherited_synthetic_travel_and_funds_not_earned=True,no_new_fixture_or_event_RNG_health_result_mutation=True,
        policy_resolution='User representative-sampling policy applies. All20Seville source/prose objects use established ordinary54020progressive,FE5473Cmode1paper,andnative2100two-choice consumers. Five ordinary actor IDs andall source headers are bound;current native macro alignment andall target fonts/geometry/return values are checked. Current font andcontrol code freshly reproduce four preserved historical Lil/Gerhard holds;whole B74data andASCII glyphs match. Existing source-audited two-label menu/default0andnormal Hamburg return remain representative samples,withinherited three travel/funds access fixtures explicitly unearned. Current FEcold typed-object reconstruction separately matches a preserved actual tutorial hold. Complete native source/target walks,relative branches andall336block/two-parent-mode loads prove relocation andunchanged control paths. No distinct new translation-specific display/control finding requires an individual Seville conditional orJanus/Valdes portrait visit. Individual Seville activation andchoice1gameplay remain unclaimed;frozen earlier proof fields marking those unobserved visits pending are not reinterpreted as completion claims. Registered cumulative build/exact patch/required current startup are still mandatory.',
        no_open_translation_specific_display_or_control_finding=True,individual_Seville_visits_not_required_for_reusable_rules=True,actual_Seville_IDs=[],actual_Janus4_or_Valdes31_nameplate_observations=[],new_emulator_runs=0,registered_release_and_startup_still_pending=True,
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('4historical Lil/Gerhard holds freshly match current native ink/gray/blank masks;two-label menu/FE/normal-return rules source-bound. User representative policy resolves20display/control scope;no Seville visit,new fixture orrelease claim.')
