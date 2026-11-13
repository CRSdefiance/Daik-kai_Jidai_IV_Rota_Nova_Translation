"""Two isolated filename fixtures for standalone title GPU compatibility."""
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

PARENT = Path('out/all_routes_combined_v546_candidate.nds')
ROOT = Path('work/analysis/standalone_resource_compatibility_v550')
OUT = ROOT/'fixtures'
STRING_OFFSET = 0x134BC8
ORIGINAL = b'/evstill/evstill%03u.pxl\0'
PATHS = ('/_pxl/logo.pxl','/_pxl/startmenu0.pxl')


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    digest = sha(PARENT.read_bytes())
    assert digest == '499e0ad767b1badf899ab6873ad787f171651035c7d6316012af2b8afc8c77d3'
    parent = NdsImage.open(PARENT)
    before = {p:data for _,p,data in parent.iter_files()}|dict(parent.iter_components())
    source = before['/__arm9__.bin']
    assert source[STRING_OFFSET:STRING_OFFSET+len(ORIGINAL)] == ORIGINAL
    assert NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')[STRING_OFFSET:STRING_OFFSET+len(ORIGINAL)] == ORIGINAL
    for path in PATHS:
        arm = bytearray(source)
        packet = path.encode('ascii')+b'\0'
        assert len(packet)<=len(ORIGINAL)
        packet = packet.ljust(len(ORIGINAL),b'\0')
        arm[STRING_OFFSET:STRING_OFFSET+len(ORIGINAL)] = packet
        assert arm[:STRING_OFFSET] == source[:STRING_OFFSET]
        assert arm[STRING_OFFSET+len(ORIGINAL):] == source[STRING_OFFSET+len(ORIGINAL):]
        fixture = NdsImage.open(PARENT)
        fixture.replace_file('/__arm9__.bin',bytes(arm))
        destination = OUT/(Path(path).stem+'_RESEARCH_ONLY.nds')
        assert not destination.exists()
        fixture.save(destination)
        saved = NdsImage.open(destination)
        after = {p:data for _,p,data in saved.iter_files()}|dict(saved.iter_components())
        assert after.keys()==before.keys()
        assert [p for p in before if before[p]!=after[p]] == ['/__arm9__.bin']
        proof = {'parent':str(PARENT),'parent_sha256':digest,'research_ROM':str(destination),
                 'research_ROM_sha256':sha(destination.read_bytes()),'source_path':path,
                 'research_only':True,'not_playable_distribution_or_registered_candidate':True,
                 'only_changed_component':'/__arm9__.bin','filename_format_offset':STRING_OFFSET,
                 'original_filename_format_hex':ORIGINAL.hex(),'replacement_literal_path_hex':packet.hex(),
                 'all_ARM_instructions_section_extents_and_all_other_bytes_exact':True,
                 'all_original_SC0_instruction_operands_prose_and_other_ROM_files_exact':True,
                 'borrowed_original_event_still_consumer_not_original_title_scene':True,
                 'original_title_scene_reachability_not_proven':True,'production_ROM_changed':False}
        destination.with_suffix('.fixture.json').write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    inputs=Path('work/analysis/village_card_gpu_v549/fixtures/opening_inputs.json').read_bytes()
    (OUT/'opening_inputs.json').write_bytes(inputs)
    assert sha(PARENT.read_bytes())==digest
    print('Two research-only filename fixtures prepared; all route instructions and production graphics exact.')


if __name__ == '__main__':
    main()
