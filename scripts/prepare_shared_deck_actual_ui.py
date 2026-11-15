"""Preserve a data-only research image and the inherited ordinary Refitting save route."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_Deck_actual_UI_20261104')
NATIVE=Path('work/analysis/Shared_Deck_current_native_v5_20261104/native_andstorage_verification.json')
CONNECTED=Path('work/analysis/Shared_Deck_connected_current_20261104/connected_verification.json')
PRIOR=Path('work/emulation_v193/refit_editorial_v831_after/capture_report.json')

if __name__=='__main__':
    assert not ROOT.exists()
    native,connected,prior=map(load,[NATIVE,CONNECTED,PRIOR])
    assert connected['native_sha256']==sha(NATIVE.read_bytes()) and connected['all8_complete_current_native_constructor_selector_copy_raster_andfont_cases_pass']
    sheet=native['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'] and sheet['panels']==4
    source=Path(native['runtime']['candidate']);image=NdsImage.open(source)
    assert sha(source.read_bytes())==native['runtime']['candidate_sha256']
    target_arm=Path(native['proposed_ARM9']).read_bytes();assert sha(target_arm)==native['proposed_ARM9_sha256']
    old=image.read_file('/__arm9__.bin');recovered=bytearray(target_arm)
    for p in native['plans']:
        at=p['current_offset'];recovered[at:at+p['allocation']]=old[at:at+p['allocation']]
    assert bytes(recovered)==old
    image.replace_file('/__arm9__.bin',target_arm);original=NdsImage.open(source)
    assert all(image.read_file(p)==v for _,p,v in original.iter_files())
    assert [p for p,v in original.iter_components() if image.read_file(p)!=v]==['/__arm9__.bin']
    ROOT.mkdir();rom=ROOT/'four_reviewed_Refit_panels_RESEARCH_ONLY.nds';image.save(rom)
    restored=NdsImage.open(rom);restored.replace_file('/__arm9__.bin',old);assert bytes(restored.rom.save())==source.read_bytes()
    battery=prior['battery_save_preloaded'];donor=Path(battery['source']);digest=sha(donor.read_bytes())
    assert digest==battery['source_sha256']=='febc859c5af2df6fa8023c349bb7f31b5fc15ea769fb2eea527b3a3f80521731'
    inputs=ROOT/'ordinary_Copenhagen_Refit_prefix_inputs.json';save(inputs,[r for r in prior['scripted_input_schedule'] if r['start']<13000])
    save(ROOT/'run_plan.json',dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),parent=str(source),parent_sha256=sha(source.read_bytes()),
        changed_component='/__arm9__.bin',changed_owned_panels=native['plans'],all31_pointer_values_andall_nonpanel_bytes_exact=True,
        complete_serialized_parent_inverse_exact=True,proposed_text_data_only_no_code_font_heap_orlayout_change=True,
        original_battery=str(donor),original_battery_sha256=digest,inherited_five_ship_Copenhagen_test_save_not_earned_progress=True,
        no_savestate_ornew_RAM_roster_money_location_RNG_orcondition_override=True,inputs=str(inputs),inputs_sha256=sha(inputs.read_bytes()),
        pause_at_frame=13000,actual_UI_observation_pending=True,native_sheet_directly_viewed=True,all_four_phrase_continuity_fixes_directly_viewed=True,
        not_registered_candidate_andnot_for_main_promotion=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NATIVE,CONNECTED,PRIOR,Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve four shared Refitting panel research image,source-byte inverse andordinary UI test. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);save(pins_path,pins)
    print('Pinned data-only four-panel research ROM;unmodified inherited Copenhagen battery andordinary navigation prefix bound;actual UI pending.')
