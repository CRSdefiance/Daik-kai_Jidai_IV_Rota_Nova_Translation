"""Verify the complete integrated successor and exclusive ownership of five approved glyphs."""

import json
import subprocess
import sys
from pathlib import Path

from ndspy.code import MainCodeFile
from dk4tool.patch.ascii_draw_offset_20261027_v2 import BASE
from dk4tool.patch.ascii_punctuation_all_20261027 import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.prepare_ascii_punctuation_all_20261027 import ROOT, ROM, CONFIG, PROFILE, save


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
    assert manifest['profile'] == PROFILE
    assert manifest['batches'] == old['batches'] + [str(CONFIG)]
    assert manifest['required_batches'] == old['required_batches']
    assert manifest['changed_paths'] == old['changed_paths']
    assert all(manifest['checks'].values())
    for key in ['canonical_baseline', 'accepted_layers', 'latest_promoted_build']:
        assert stack[key] == live[key]
    assert stack['profiles'][PROFILE] == live['profiles'][PROFILE]
    parent, candidate = NdsImage.open(parent_path), NdsImage.open(ROM)
    def files(rom):
        return {**{p: b for _, p, b in rom.iter_files()}, **dict(rom.iter_components())}
    a, b = files(parent), files(candidate)
    assert a.keys() == b.keys()
    changes = [p for p in a if a[p] != b[p]]
    assert changes == ['/__arm9__.bin']
    source, arm = a['/__arm9__.bin'], b['/__arm9__.bin']
    expected, proof = apply_release(source, CONFIG)
    assert expected == arm == (ROOT / 'proposed_ARM9.bin').read_bytes()
    owned = {i for span in proof['glyph_spans'] for i in range(span['offset'], span['offset'] + 11)}
    byte_changes = [i for i, (x, y) in enumerate(zip(source, arm)) if x != y]
    assert len(source) == len(arm) and set(byte_changes) <= owned
    before, after = MainCodeFile(source, BASE).sections, MainCodeFile(arm, BASE).sections
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before] == [(s.ramAddress, len(s.data), s.bssSize) for s in after]
    assert all(bytes(before[i].data) == bytes(after[i].data) for i in range(1, len(before)))
    for key in ['arm9OverlayTable', 'arm7OverlayTable', 'iconBanner', 'name', 'idCode', 'arm9RamAddress', 'arm9EntryAddress']:
        assert getattr(parent.rom, key) == getattr(candidate.rom, key)
    args = [sys.executable, 'scripts/verify_release_baseline.py', manifest['base_rom'], str(ROM)]
    for path in manifest['changed_paths']:
        args += ['--allow-path', path]
    with (ROOT / 'baseline_verification.log').open('w', encoding='utf-8') as log:
        subprocess.run(args, check=True, stdout=log, stderr=subprocess.STDOUT)
    save(ROOT / 'release_verification.json', dict(candidate=str(ROM), candidate_sha256=manifest['candidate_sha256'],
        profile=PROFILE, canonical_base=stack['canonical_baseline'], predecessor=str(parent_path),
        predecessor_sha256=cfg['predecessor_rom_sha256'], proof=proof,
        changed_from_predecessor=changes, changed_ARM9_byte_count=len(byte_changes),
        only_approved_five_bitmaps_changed=True,
        painter_Y_plus1_line_spacing_and_all_code_byte_identical=True,
        all_other_files_glyphs_artwork_Japanese_font_and_autoload_sections_preserved=True,
        existing_accepted_layers=len(stack['accepted_layers']), complete_manifest_batches=len(manifest['batches']),
        baseline_verifier_passed=True, promoted_main=stack['latest_promoted_build'],
        experimental_user_acceptance_pending=True))
    print('Exclusive five-glyph ownership, complete stack, unchanged code/spacing and baseline: PASS')
    print('ROM SHA256', manifest['candidate_sha256'])
