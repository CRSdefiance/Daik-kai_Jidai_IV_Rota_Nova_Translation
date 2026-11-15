"""Verify complete predecessor inheritance and only declared font-offset code deltas."""

import json
import struct
import subprocess
import sys
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.ascii_draw_offset_20261027_v2 import BASE, SLOT, SLOT_END
from dk4tool.patch.ascii_draw_offset_one_20261027 import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/font_offset_one_20261027')
ROM = Path('out/font_v2_draw_down_one_20261027_test.nds')
CONFIG = Path('translations/ascii_draw_offset_one_20261027_v1.json')


if __name__ == '__main__':
    cfg = json.loads(CONFIG.read_text())
    parent_path = Path(cfg['predecessor_rom'])
    old = json.loads(parent_path.with_suffix('.manifest.json').read_text())
    manifest = json.loads(ROM.with_suffix('.manifest.json').read_text())
    stack = json.loads((ROOT / 'release_stack_snapshot.json').read_text())
    live = json.loads(Path('translations/release_stack.json').read_text())
    assert sha(parent_path.read_bytes()) == cfg['predecessor_rom_sha256'] == old['candidate_sha256']
    assert sha(ROM.read_bytes()) == manifest['candidate_sha256']
    assert manifest['release_stack_sha256'] == sha((ROOT / 'release_stack_snapshot.json').read_bytes())
    assert manifest['profile'] == 'font-v2-draw-down-one-20261027'
    assert manifest['batches'] == old['batches'] + [str(CONFIG)]
    assert manifest['required_batches'] == old['required_batches']
    assert manifest['changed_paths'] == old['changed_paths']
    assert all(manifest['checks'].values())
    for key in ['canonical_baseline', 'accepted_layers', 'latest_promoted_build']:
        assert stack[key] == live[key]
    assert stack['profiles'][manifest['profile']] == live['profiles'][manifest['profile']]
    parent, candidate = NdsImage.open(parent_path), NdsImage.open(ROM)
    def files(rom):
        return {**{p: b for _, p, b in rom.iter_files()}, **dict(rom.iter_components())}
    a, b = files(parent), files(candidate)
    assert a.keys() == b.keys()
    changes = [p for p in a if a[p] != b[p]]
    assert changes == ['/__arm9__.bin']
    source, arm = a['/__arm9__.bin'], b['/__arm9__.bin']
    target, proof = apply_release(source, CONFIG)
    assert target == arm == (ROOT / 'proposed_ARM9.bin').read_bytes()
    assert GameAsciiFont.from_arm9(source).glyphs == GameAsciiFont.from_arm9(arm).glyphs
    before_sections, after_sections = MainCodeFile(source, BASE).sections, MainCodeFile(arm, BASE).sections
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before_sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in after_sections]
    assert all(bytes(before_sections[i].data) == bytes(after_sections[i].data) for i in [1, 2, 3])
    # The newly assigned slot is blank and has no original absolute-word or ARM
    # branch references in any loaded ARM9 section or ARM9 overlay unit.
    units = [(s.ramAddress, bytes(s.data), f'section{i}') for i, s in enumerate(before_sections)]
    from ndspy.code import loadOverlayTable
    overlays = loadOverlayTable(parent.rom.arm9OverlayTable, lambda fid, _: parent.rom.files[fid])
    units.extend((o.ramAddress, bytes(o.data), f'overlay{k}') for k, o in overlays.items())
    references = []
    for address, raw, name in units:
        for off in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, off)[0]
            if SLOT <= word < SLOT_END or SLOT <= (word & ~1) < SLOT_END:
                references.append([name, off, 'absolute', word])
            if word >> 25 & 7 == 5 and word >> 28 != 15:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                dest = address + off + 8 + delta * 4
                if SLOT <= dest < SLOT_END:
                    references.append([name, off, 'ARM branch', dest])
    assert not references, references
    args = [sys.executable, 'scripts/verify_release_baseline.py', manifest['base_rom'], str(ROM)]
    for path in manifest['changed_paths']:
        args += ['--allow-path', path]
    with (ROOT / 'baseline_verification.log').open('w', encoding='utf-8') as log:
        subprocess.run(args, check=True, stdout=log, stderr=subprocess.STDOUT)
    for key in ['arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode', 'arm9RamAddress', 'arm9EntryAddress']:
        assert getattr(parent.rom, key) == getattr(candidate.rom, key)
    result = dict(candidate=str(ROM), candidate_sha256=manifest['candidate_sha256'],
        predecessor=str(parent_path), predecessor_sha256=cfg['predecessor_rom_sha256'],
        profile=manifest['profile'], canonical_base=stack['canonical_baseline'],
        changed_from_predecessor=changes, proof=proof,
        improved_font_all_files_routes_artwork_Japanese_font_and_nonowned_code_preserved=True,
        all_autoload_extents_staged_payload_and_DTCM_bytes_preserved=True,
        original_helper_slot_absolute_and_ARM_branch_references=references,
        reference_units=len(units), existing_accepted_layers=len(stack['accepted_layers']),
        complete_manifest_batches=len(manifest['batches']), baseline_verifier_passed=True,
        promoted_main=stack['latest_promoted_build'], experimental_user_acceptance_pending=True)
    (ROOT / 'release_verification.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print('Release, font identity, owned code changes, helper reference census and baseline checks pass.')
    print('ROM SHA256', manifest['candidate_sha256'])
