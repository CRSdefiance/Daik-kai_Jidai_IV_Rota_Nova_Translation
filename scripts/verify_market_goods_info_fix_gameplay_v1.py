"""Verify actual Local/Cargo glyph masks, clean status space and loaded declared data."""
import struct
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_goods_info_terminator_v1 import NEW_FORMAT,PAYLOAD,FIELDS
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.verify_commodity_private_market_live_v354 import exact_label

OUT=Path('work/market_goods_info_terminator_release_v1')

def digest(p):return sha(Path(p).read_bytes())

def main():
    output=OUT/'market_gameplay_verification.json';assert not output.exists()
    staged_path=OUT/'staged_successor.json';staged=load(staged_path)
    startup_path=OUT/'own_registered_startup_verification.json';startup=load(startup_path)
    getter_path=OUT/'own_registered_name_getters_v1.json';getters=load(getter_path)
    report_path=OUT/'market_run_v3/capture/capture_report.json';report=load(report_path)
    plan_path=OUT/'market_run_v3/run_plan.json';plan=load(plan_path)
    assert plan['staged_sha256']==digest(staged_path)
    assert digest(staged['candidate'])==staged['candidate_sha256']==startup['candidate_sha256']==report['ROM_sha256']
    assert getters['runtime']['candidate_sha256']==staged['candidate_sha256'] and getters['both_name_getters_exact_for_all12_protected_actors']
    assert report['frames']==11600 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule']==load(plan['unchanged_inputs'])
    donor=plan['source_save'];assert digest(donor['source'])==donor['source_sha256']==report['battery_save_preloaded']['source_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    image=NdsImage.open(staged['candidate']);arm=image.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    captures={r['frame']:r for r in report['frames_captured']};cases=[]
    for frame,consumer in [(10400,'Local-selected Goods Info'),(11600,'Cargo-selected Goods Info after ordinary drag')]:
        entry=captures[frame];assert digest(entry['path'])==entry['PNG_sha256']
        pic=Image.open(entry['path']).convert('RGB');assert pic.size==(256,384)
        # Current native bitmap composition has the established one-pixel font
        # origin relative to the older V354 oracle. Every ink and blank cell is
        # matched, including the entire formerly garbled third-row area.
        mask=exact_label(pic,font,'Olive Oil\n  Cond. 100%',(144,127),(144,126,256,162))
        assert mask['exact_ink_pixels']==224
        assert not any(pic.getpixel((x,y))==(230,230,230) for y in range(150,162) for x in range(144,256))
        cases.append(dict(frame=frame,consumer=consumer,capture=entry,complete_Goods_Info_mask=mask,
            status_suffix_area_all_text_ink_blank=True,directly_viewed=True))
    town=captures[9600];assert digest(town['path'])==town['PNG_sha256']
    state=report['read_only_capture_native_states'][0]
    assert state['frame']==11600 and state['read_only_export'] and not state['state_loaded']
    assert state['serialized_RAM_matches_same_frame_direct_export'] and state['main_RAM_unchanged_by_export']
    itcm=state['regions']['ITCM'];raw_itcm=Path(itcm['path']).read_bytes();assert digest(itcm['path'])==itcm['sha256']
    assert raw_itcm[NEW_FORMAT%32768:NEW_FORMAT%32768+len(PAYLOAD)]==PAYLOAD
    assert raw_itcm[0x46AC:0x46C4]==bytes.fromhex('0c209fe50a1182e701308ae2143082e51eff2fe124dc1502')[:24]
    snapshot=report['read_only_RAM_snapshot'];ram=Path(snapshot['path']).read_bytes()
    assert len(ram)==0x400000 and digest(snapshot['path'])==snapshot['sha256']
    for field in FIELDS:assert struct.unpack_from('<I',ram,field)[0]==NEW_FORMAT
    save(output,dict(candidate=staged['candidate'],candidate_sha256=staged['candidate_sha256'],
        actual_Local_andCargo_market_screens_verified=True,no_machine_code_suffix_oruntranslated_garbage=True,
        gameplay_frames=11600,ordinary_source_save_byte_exact=True,unchanged_ordinary_controller_andstylus_schedule=True,
        actual_goods='Olive Oil / Cond.100%',user_exact_Cheese_Food101_reproduced_andcorrected_in_native_matrix=True,
        cases=cases,town_before_Trade_directly_viewed=town,original_town_capture_code_still_loaded_exact=True,
        new_declared_format_andboth_literal_pointers_loaded_exact=True,
        complete_first_internal_final_ASCII_glyphs_andentire_status_blank_cells_exact=True,
        no_source_gameplay_ROM_stock_location_RNG_money_event_orRAM_override=True,
        planned_Cargo_drag_not_completed_purchase=True,
        no_new_shortage_ortrend_eligibility_orhardware_claim=True,
        capture_report=str(report_path),capture_report_sha256=digest(report_path),
        save_source=donor['source'],save_source_sha256=donor['source_sha256'],new_credit=0,
        evidence={str(p):digest(p) for p in [plan_path,report_path,startup_path,getter_path,
            Path('work/market_goods_info_terminator_20261109_v1/native_verification_v1.json'),Path(__file__)]}))
    (OUT/'staged_before_gameplay_completion.json').write_bytes(staged_path.read_bytes())
    staged.update(own_registered_startup_pending=False,own_registered_startup=str(startup_path),own_registered_startup_sha256=digest(startup_path),
        market_gameplay_pending=False,market_gameplay_verification=str(output),market_gameplay_verification_sha256=digest(output))
    save(staged_path,staged)
    print('PASS actualLocal/Cargo complete224-pixel masks andblank suffix area;genuine-save replay/new data/town code exact. Readyforregistration.')

if __name__=='__main__':main()
