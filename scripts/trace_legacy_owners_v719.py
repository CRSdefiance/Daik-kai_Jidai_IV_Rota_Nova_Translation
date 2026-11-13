"""Resolve bounded computed references to two registered legacy resource owners."""

import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import trace_control_aliases_v688 as flow
from scripts.probe_button_prompt_native import call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/legacy_owners_v719')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
FILES = ('_pxl/winframe00.pxl', '_pxl/seamap.pxl')


def main():
    ROOT.mkdir(exist_ok=True)
    assert not (ROOT / 'constant_flow_leads.json').exists()
    controls = flow.controls()
    registry = read('work/analysis/legacy_archive_access_v384/PXL_registry_proof.json')
    rows = [r for r in registry['initialized_owners'] if r['native_filename'].lstrip('/') in FILES]
    assert len(rows) == 2
    targets = {r['native_filename'].lstrip('/'): (r['owner'], 20) for r in rows}
    original_targets = flow.TARGETS
    versions = {}
    try:
        flow.TARGETS = targets
        for name, path in (('source', Path('work/clean.nds')), ('current', ROM)):
            image = NdsImage.open(path)
            cpu = machine(image.read_file('/__arm9__.bin'))
            executed = call(cpu, 0x10E190, (), instruction_limit=100000)
            owners = []
            for filename, (owner, extent) in targets.items():
                fields = struct.unpack('<5I', cpu.mem_read(owner, extent))
                assert fields[1:3] == (owner + 4, owner + 4) and fields[4] == 0xFFFFFFFF
                actual = bytes(cpu.mem_read(fields[3], 128)).split(b'\0')[0].decode('ascii')
                assert actual == filename
                owners.append({'filename': filename, 'owner': owner, 'extent': extent,
                    'five_native_initialized_words': fields,
                    'whole_file_sha256': sha(image.read_file('/' + filename))})
            findings, statistics = flow.analyze(flow.sections(image))
            versions[name] = {'ROM': str(path), 'ROM_sha256': sha(path.read_bytes()),
                'complete_original_initializer_no_bridges_stack_saved_registers_pass': True,
                'executed_initializer_instructions': len(executed), 'native_owners': owners,
                'sections': statistics, 'owner_candidates': findings}
    finally:
        flow.TARGETS = original_targets
    proof = {'versions': versions, 'controls': controls,
        'analyzer': 'scripts/trace_control_aliases_v688.py',
        'analyzer_sha256': sha(Path('scripts/trace_control_aliases_v688.py').read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'scope': 'Aligned ARM bounded constant flow including actual startup copy pool and overlay. Unknown branches,calls,stores,conditional writes and instructions clear values. Candidate bytes need source review; no arbitrary dynamic/Thumb/reachability closure.',
        'no_ROM_asset_or_source_change': True, 'normal_consumers_not_inferred_from_registration': True,
        'full_goal_complete': False}
    save(ROOT / 'constant_flow_leads.json', proof)
    for version, result in versions.items():
        print(version, [(r['target'], hex(r['PC']), hex(r['value']), r['direct_literal_owner_load'])
            for r in result['owner_candidates']], flush=True)


if __name__ == '__main__':
    main()
