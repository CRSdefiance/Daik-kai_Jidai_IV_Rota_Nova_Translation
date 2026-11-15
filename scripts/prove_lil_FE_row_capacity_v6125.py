"""Measure original FE text capacity separately from its228-pixel bitmap width."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_current_font_oracles_v6122 import make_painter
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_FE_row_capacity_v6125')
if __name__=='__main__':
    assert not ROOT.exists();doc=read('translations/lil_B204_editorial_manuscript_v2.json');image=NdsImage.open(doc['current_ROM']);paint,cal=make_painter(image);cases=[]
    for size in range(34,42):
        text=bytes(65+i%26 for i in range(size));r=paint(text);events=[e for e in r['events'] if e['code']!=32]
        assert bytes(e['code'] for e in events)==text
        rows={y:[e for e in events if e['y']==y] for y in sorted({e['y'] for e in events})}
        assert all([e['x'] for e in v]==list(range(0,len(v)*6,6)) for v in rows.values())
        assert [len(v) for v in rows.values()]==([size] if size<=36 else [36,size-36])
        cases.append(dict(chars=size,rows=[dict(y=y,characters=len(v),first_x=v[0]['x'],final_x=v[-1]['x']) for y,v in rows.items()],all_chars_native_return_and_canaries_complete=True,complete_native_independent_logical_plane_sha256=sha(r['logical']),physical_plane_sha256=sha(r['physical'])))
    ROOT.mkdir(parents=True);save(ROOT/'original228px_descriptor_native36_ASCII_row_capacity.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],ARM9_sha256=sha(image.read_file('/__arm9__.bin')),typed_geometry_calibration=cal,cases=cases,original_bitmap_width_px=228,native_observed_row_ASCII_characters=36,native_observed_text_capacity_px=216,thirty_seventh_ASCII_glyph_wraps_to_y12_at_x0=True,all_input_chars_one_page_returns_independent_planes_and_canaries_complete=True,old_host228_plan_for_B204_R66_failed_before_complete_return_and_is_unapproved=True,failed_current_native_verifier='scripts/verify_lil_B204_fonts_v6124.py',corrected_host_budget216_required_before_all20_native_checks=True,no_ROM_native_viewport_font_clip_pair_phase_or_words_changed=True,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Eight complete FE native probes:228px descriptor,36 printable ASCII glyphs per row;37th wraps.216px planning required;no native or prose change.')
