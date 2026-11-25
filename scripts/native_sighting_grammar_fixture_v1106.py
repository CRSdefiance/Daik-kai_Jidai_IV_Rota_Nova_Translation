"""Bind the original position/prerequisite fixture to exact metadata-only V1105."""
from pathlib import Path
from types import FunctionType
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import native_sighting_context_v1087b as original
from scripts.verify_village_wrap_v608 import read


def apply_fixture(arm,raw,request):
    config=read('translations/sighting_grammar_editorial_release_v1.json')
    assert sha(arm)==config['target_arm9_sha256']
    assert request=={'sighting_context':'compassReady8'}
    old_arm=NdsImage.open('out/all_routes_combined_v1086_candidate.nds').read_file('/__arm9__.bin')
    assert sha(old_arm)==config['source_arm9_sha256']
    plan=read('work/analysis/sighting_grammar_release_v1104/repack_plan.json')
    restored=bytearray(arm)
    for at,size in plan['metadata_fields']:restored[at:at+size]=old_arm[at:at+size]
    assert bytes(restored)==old_arm
    def mapped_read(path):
        if str(path)=='translations/sighting_editorial_release_v1.json':return {'target_arm9_sha256':config['target_arm9_sha256']}
        return read(path)
    function=FunctionType(original.apply_fixture.__code__,{**original.apply_fixture.__globals__,'read':mapped_read},
        argdefs=original.apply_fixture.__defaults__)
    result,proof=function(arm,raw,request)
    proof.update(adapter_sha256=sha(Path(__file__).read_bytes()),
        source_fixture_sha256=sha(Path(original.__file__).read_bytes()),
        entire_original_ARM9_except_new_message_metadata_exact=True,
        native_geometry_getters_renderer_labels_and_all_nonmessage_data_unchanged=True)
    return result,proof
