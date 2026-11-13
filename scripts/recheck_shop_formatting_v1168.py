"""Recheck the photographed shop defect in registered V1166;no new scene claim."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.duel_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster as original_raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save


def main():
    target=Path('work/analysis/duel_release_v1165/photographed_shop_formatting.json')
    assert not target.exists()
    path=Path('out/all_routes_combined_v1166_candidate.nds')
    assert sha(path.read_bytes())=='19109464a37c8acfe7ccf802fed712cc0bd413600b304546668fb5475801ac26'
    rom=NdsImage.open(path);common=rom.read_file('/COMMON/MESFILE.DK4');arm=rom.read_file('/__arm9__.bin')
    prior_path=Path('work/analysis/dialogue_formatting_user_recheck_v1027c/COMMON676_677.json')
    prior=read(prior_path);entries=current_entries(common,arm);cpu=prepared(arm)
    class CurrentFont:
        @staticmethod
        def open(requested):
            assert str(requested)=='out/all_routes_combined_v255_candidate.nds'
            return rom
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':CurrentFont},argdefs=original_raster.__defaults__)
    results=[]
    for row in prior['entries']:
        n=row['id'];assert entries[n].text.hex()==row['template_hex']
        formatted,lines=native_layout(cpu,entries[n].text,n,())
        assert formatted.hex()==row['native_formatted_hex'] and lines==row['lines']
        assert all(line==line.strip() and '  ' not in line for line in lines)
        assert 'Discover' not in ' '.join(lines) and len(lines)<=4
        pixels=raster(arm,formatted,0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000)
        assert pixels==independent_font(arm,rom.read_file('/GRP/KANJI.FNT'),lines)
        results.append({'id':n,'lines':lines,'original_native_wrapping_exact_to_repaired_reference':True,
            'complete228x64_native_and_independent_font_equal':True,'no_authored_indent_internal_gap_or_stray_Discover':True})
    capture=Path(prior['earlier_actual_capture']);assert sha(capture.read_bytes())==prior['earlier_actual_capture_sha256']
    target.parent.mkdir(parents=True,exist_ok=True)
    save(target,{'candidate':str(path),'candidate_sha256':sha(path.read_bytes()),'entries':results,
        'reference':str(prior_path),'reference_sha256':sha(prior_path.read_bytes()),
        'earlier_actual_V747_capture':str(capture),'capture_sha256':sha(capture.read_bytes()),
        'earlier_capture_visually_reviewed':True,'new_V1166_shop_scene_activation_claimed':False,
        'global_formatting_audit_still_open':True,'producer_sha256':sha(Path(__file__).read_bytes())})
    print('V1166:676/677 exact repaired bytes,original native wrapping and whole font planes pass;no new shop activation claimed.')


if __name__=='__main__':main()
