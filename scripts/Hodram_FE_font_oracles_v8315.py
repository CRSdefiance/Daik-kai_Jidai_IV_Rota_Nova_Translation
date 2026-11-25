"""Local FE source painter for the exact name-only ARM9 successor; no global guard edits."""
from pathlib import Path
from types import FunctionType
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import square_shopkeeper_font_oracles_v7020 as old
from scripts import Rafael_B45_FE_source_painter_v7894 as source
from scripts.verify_village_wrap_v608 import read

CURRENT_ARM9='12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b'

def bind(image):
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==CURRENT_ARM9
    proof=read('work/analysis/Gerhard_reference_v8215/research_image_receipt.json')
    path=Path(proof['parent']);assert sha(path.read_bytes())==proof['parent_sha256']
    predecessor=NdsImage.open(path);before=predecessor.read_file('/__arm9__.bin');slot=proof['only_changed_name_span'];at=slot['offset']
    assert len(arm)==len(before) and slot['bytes']==12 and arm[at:at+12].hex()==slot['target_hex'] and arm[at+12:at+20]==before[at+12:at+20]==b'Blades\0\0'
    restored=bytearray(arm);restored[at:at+12]=bytes.fromhex(slot['current_hex']);assert bytes(restored)==before and sha(before)==old.CURRENT_ARM9
    assert image.read_file('/GRP/KANJI.FNT')==predecessor.read_file('/GRP/KANJI.FNT')
    pixels=FunctionType(old.expected_pixels.__code__,{**old.expected_pixels.__globals__,'CURRENT_ARM9':CURRENT_ARM9},argdefs=old.expected_pixels.__defaults__)
    ascii_factory=FunctionType(old.make_painter.__code__,{**old.make_painter.__globals__,'CURRENT_ARM9':CURRENT_ARM9},argdefs=old.make_painter.__defaults__)
    factory=FunctionType(source.make_source_painter.__code__,{**source.make_source_painter.__globals__,'CURRENT_ARM9':CURRENT_ARM9,'ASCII_painter':ascii_factory},argdefs=source.make_source_painter.__defaults__)
    return pixels,factory,dict(exact_target_ARM9_sha256=CURRENT_ARM9,whole12byte_name_inverse_to_previous_font_oracle_ARM9=True,protected_next8_Blades_bytes_exact=True,whole_font_file_exact=True,
        no_global_module_ororiginal_guard_mutation=True,no_historical_initialized_RAM_overlay=True,geometry_from_prior_typed_objects_not_new_actual_FE_gameplay=True,
        source_modules={str(Path(p)):sha(Path(p).read_bytes()) for p in [old.__file__,source.__file__,__file__]})
