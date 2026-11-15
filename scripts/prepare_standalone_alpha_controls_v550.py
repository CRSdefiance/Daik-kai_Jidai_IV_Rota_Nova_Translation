"""Palette-specific colour-key controls for diagnostic title compositing, not production art."""
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_standalone_title_gpu_v550 import OUT, PATHS


def main():
    for path in PATHS:
        stem = Path(path).stem
        original = OUT/(stem+'_RESEARCH_ONLY.nds')
        parent = NdsImage.open(original)
        metadata = json.loads(original.with_suffix('.fixture.json').read_text(encoding='utf-8'))
        assert metadata['research_ROM_sha256'] == sha(original.read_bytes())
        before = {p:data for _,p,data in parent.iter_files()}|dict(parent.iter_components())
        pxl = PxlImage.from_bytes(before[path])
        assert (pxl.width,pxl.height,pxl.bits_per_pixel) == (256,192,8)
        prefix = before[path][:pxl.pixels_offset]
        keys = [i for i,colour in enumerate(pxl.palette) if colour[:3] == (0,0,0)]
        assert len(keys) == 1
        key = keys[0]
        pxl.indices[:] = bytes([key])*49152
        blank = pxl.to_bytes()
        assert len(blank)==len(before[path]) and blank[:pxl.pixels_offset]==prefix
        parent.replace_file(path,blank)
        suffix = '_ZERO_KEY_CONTROL_RESEARCH_ONLY.nds' if key == 0 else f'_KEY{key}_CONTROL_RESEARCH_ONLY.nds'
        destination = OUT/(stem+suffix)
        if not destination.exists():
            parent.save(destination)
        saved = NdsImage.open(destination)
        after = {p:data for _,p,data in saved.iter_files()}|dict(saved.iter_components())
        assert before.keys()==after.keys()
        assert [p for p in before if before[p]!=after[p]] == [path]
        proof = {'research_only':True,'not_playable_distribution_or_registered_candidate':True,
                 'parent_fixture':str(original),'parent_fixture_sha256':sha(original.read_bytes()),
                 'source_path':path,'control_ROM':str(destination),'control_ROM_sha256':sha(destination.read_bytes()),
                 'all_source_pixel_indices_replaced_with_transparent_colour_entry':key,
                 'source_header_flags_palette_extent_and_file_length_exact':True,
                 'all_other_files_components_and_native_instructions_exact_parent_fixture':True,
                 'not_a_translation_or_a_production_graphics_change':True}
        metadata_path = destination.with_suffix('.fixture.json')
        if metadata_path.exists():
            existing = json.loads(metadata_path.read_text(encoding='utf-8'))
            assert existing['control_ROM_sha256'] == proof['control_ROM_sha256']
            assert existing['parent_fixture_sha256'] == proof['parent_fixture_sha256']
        else:
            metadata_path.write_text(json.dumps(proof,indent=2)+'\n',encoding='utf-8')
    print('Two palette-specific controls verified; original headers/palettes and all native code exact.')


if __name__ == '__main__':
    main()
