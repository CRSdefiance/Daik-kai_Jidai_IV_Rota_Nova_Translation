"""Replay the registered builder and record resident-byte write provenance."""

import contextlib
import inspect
import json
from pathlib import Path
import sys

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import build_integrated_release as builder
from scripts.inspect_patch_runtime_memory_20261027 import spans

ROOT = Path('work/patch_interaction_audit_20261027')


if __name__ == '__main__':
    source = Path('out/font_v2_square_scratch_fix_20261027_test.nds')
    target = ROOT / 'audited_reconstruction_RESEARCH_ONLY.nds'
    manifest = json.loads(source.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    assert not target.exists()
    registry = Path('translations/release_stack.json').read_bytes()
    assert sha(registry) == manifest['release_stack_sha256']
    original = NdsImage.replace_file
    records = []
    owners = {}

    def traced(image, path, data):
        if path == '/__arm9__.bin':
            before = image.read_file(path)
            old = {s.ramAddress: bytes(s.data) for s in MainCodeFile(before,0x02000000).sections}
            after = {s.ramAddress: bytes(s.data) for s in MainCodeFile(bytes(data),0x02000000).sections}
            caller = inspect.currentframe().f_back
            location = dict(file=caller.f_code.co_filename, line=caller.f_lineno, function=caller.f_code.co_name)
            ranges = []
            for address, current in after.items():
                previous = old.get(address, b'')
                changed = [i for i,b in enumerate(current) if i >= len(previous) or b != previous[i]]
                for lo,hi in spans(changed):
                    ranges.append(dict(address=address+lo, end=address+hi, newly_loaded=lo>=len(previous)))
                    for at in range(address+lo,address+hi):
                        owners[at] = len(records)
            records.append(dict(stage=len(records), caller=location, before_ARM9_sha256=sha(before),
                after_ARM9_sha256=sha(bytes(data)), resident_changed_ranges=ranges))
        return original(image,path,data)

    NdsImage.replace_file = traced
    sys.argv = ['build_integrated_release.py','--profile',manifest['profile'],'--out',str(target)]
    try:
        with (ROOT/'traced_builder_stdout.json').open('w',encoding='utf-8') as output:
            with contextlib.redirect_stdout(output):
                builder.main()
    finally:
        NdsImage.replace_file = original
    assert target.read_bytes() == source.read_bytes()
    assert Path('translations/release_stack.json').read_bytes() == registry
    provenance = []
    for at in sorted(owners):
        owner = owners[at]
        if provenance and at == provenance[-1]['end'] and owner == provenance[-1]['stage']:
            provenance[-1]['end'] += 1
        else:
            provenance.append(dict(address=at,end=at+1,stage=owner))
    result = dict(ROM_sha256=sha(target.read_bytes()), exact_registered_reconstruction=True,
        registry_sha256=sha(registry), ARM9_replacement_stages=len(records), stages=records,
        final_changed_byte_writer_ranges=provenance,
        limitation='Write provenance is distinct from runtime ownership. Mutable buffers are classified separately; unchanged zero bytes are never treated as proof of free space.')
    (ROOT/'construction_write_provenance.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('Exact registered reconstruction;',len(records),'ARM9 stages;',len(provenance),'final resident-byte writer ranges.')
