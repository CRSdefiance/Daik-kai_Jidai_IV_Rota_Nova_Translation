"""Publish the registered cumulative clean-input patch and an exact local testing copy."""
import ast
import gzip
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/lil269_B243_B282_release_v1')
EDITORIAL = Path('work/Lil269_B243_B282_clean_20261110')
OUT = Path('releases/all_routes_editorial_20261110_lil269_candidate')
TEST = Path('out/promotion_ready_20261110_lil269_v1')


def main():
    assert not OUT.exists() and not TEST.exists()
    rp = ROOT / 'registered_release_verification.json'
    release = load(rp)
    complete = load(ROOT / 'completion_checkpoint.json')
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (727, 114, 62)
    assert complete['counts'] == dict(completed=24744, revised=14704, retained=10040)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    registry = Path('translations/release_stack.json')
    assert digest(registry) == release['registry_sha256']
    assert load(ROOT / 'release_stack_before_Lil269.json')['latest_promoted_build'] == load(registry)['latest_promoted_build']
    for key in ['candidate', 'manifest', 'patch', 'own_registered_startup', 'own_registered_name_getters', 'exact_record_bindings']:
        assert digest(release[key]) == release[key + '_sha256'], key
    manifest = load(release['manifest'])
    assert len(manifest['batches']) == 727 and len(manifest['checks']) == 62 and all(v is True for v in manifest['checks'].values())
    report = Path('work/lil269_repository_qa_v1_pytest.xml')
    suites = list(ET.parse(report).getroot().iter('testsuite'))
    assert sum(int(s.get('tests', 0)) for s in suites) == 27
    assert all(int(s.get(k, 0)) == 0 for s in suites for k in ['errors', 'failures', 'skipped'])
    producers = sorted(set(Path('scripts').glob('*lil269*.py')) | {Path('dk4tool/patch/lil269_release_v1.py')})
    for p in producers:
        ast.parse(p.read_bytes(), filename=str(p))
    visual = ROOT / 'own_startup_visual_v1/direct_visual_review.json'
    assert load(visual)['all_six_original_captures_andexact_composite_directly_viewed']
    TEST.mkdir()
    rom = TEST / 'Translation_DS_All_Routes_Lil269_20261110_candidate.nds'
    clean = Path('work/clean.nds')
    assert digest(clean) == release['clean_input_sha256']
    apply_xdelta(clean, Path(release['patch']), rom)
    assert rom.read_bytes() == Path(release['candidate']).read_bytes() == Path(release['exact_clean_reconstruction']).read_bytes()
    adjacent = rom.with_suffix('.manifest.json')
    adjacent.write_bytes(Path(release['manifest']).read_bytes())
    OUT.mkdir()
    verification = OUT / 'verification'
    verification.mkdir()
    patch = OUT / 'translation.xdelta'
    patch.write_bytes(Path(release['patch']).read_bytes())
    for p, name in [(Path(release['manifest']), 'build_manifest.json.gz'), (registry, 'build_release_stack.json.gz')]:
        raw = p.read_bytes()
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        assert gzip.decompress(packed) == raw
        (OUT / name).write_bytes(packed)
    proofs = [rp, ROOT / 'completion_checkpoint.json', ROOT / 'own_registered_startup_verification.json',
        ROOT / 'own_registered_name_getters_v1.json', visual, EDITORIAL / 'gameplay_review_v1.json',
        EDITORIAL / 'offline_display_approval_v1.json', EDITORIAL / 'final_layout_delta_v2.json']
    for p in proofs:
        (verification / p.name).write_bytes(p.read_bytes())
    for p, name in [(EDITORIAL / 'registered_semantic_checks_v1/qualification.json', 'production_scope_rejections.json'),
        (EDITORIAL / 'loaders_v1/verification.json', 'native_loaders.json'),
        (EDITORIAL / 'stored_catalogue_all_v1/all_stored_effective_body_bindings.json', 'stored_catalogue.json')]:
        (verification / name).write_bytes(p.read_bytes())
    (verification / 'repository_pytest.xml').write_bytes(report.read_bytes())
    save(verification / 'repository_checks.json', dict(selected_tests=27, passing_tests=27, errors=0, failures=0,
        terminal_exit_code=0, report=str(report), report_sha256=digest(report), production_scope_rejections=8,
        active_producers_parsed={str(p): digest(p) for p in producers}))
    receipt = dict(candidate=str(rom), candidate_sha256=digest(rom), manifest=str(adjacent), manifest_sha256=digest(adjacent),
        registered_release=str(rp), registered_release_sha256=digest(rp),
        clean_input=str(clean), clean_input_sha256=digest(clean), patch=str(patch), patch_sha256=digest(patch),
        exact_registered_candidate_reconstructed_from_clean_input=True, release_entries=727, accepted_layers=114,
        release_checks=62, integrated_editorial_records=24744, main_promoted=False, user_acceptance_pending=True,
        new_editorial_credit=0, new_gameplay_claim=False, full_goal_complete=False,
        producer=str(Path(__file__)), producer_sha256=digest(__file__))
    save(TEST / 'promotion_reconstruction.json', receipt)
    save(verification / 'promotion_reconstruction.json', receipt)
    save(OUT / 'release_manifest.json', dict(profile=release['profile'], status='registered-candidate-awaiting-user-acceptance',
        candidate=str(rom), candidate_sha256=digest(rom), clean_input_sha256=release['clean_input_sha256'],
        patch='translation.xdelta', patch_sha256=digest(patch), build_manifest_sha256=release['manifest_sha256'],
        release_stack_sha256=release['registry_sha256'], entries=727, accepted_layers=114,
        passing_release_checks=62, integrated_editorial_records=24744, main_promoted=False, full_goal_complete=False))
    text = f'''# Cumulative testing candidate — Lil269

Local ROM: `{rom}`, with its adjacent manifest. This registered successor preserves all726 predecessor entries and114 accepted layers, including Rafael/tutorial localization, prior storyline/shared work, Market Trade-screen correction, names and the ASCII right-bound repair. Main remains V4701 pending your cold-boot testing and explicit acceptance. Earlier ROMs remain preserved.

Apply `translation.xdelta` to the clean Japanese ROM SHA-256 `{release['clean_input_sha256']}`. Expected output SHA-256: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Both the registered reconstruction and this new testing copy match byte for byte. The patch can be applied independently of historical work folders. The gzip files preserve exact build-time manifest and registry bytes.

The new269 reviews cover40 complete Lil SC2 groups B243-B282:104 revisions and165 individually justified retentions, with25 scoped name reviews. They restore untranslated expedition instructions, Indian Ocean directions, source uncertainty and character/name details across town, figurehead, riddle and wanted-person exchanges. Sixteen final layouts change and one page is reclaimed without shortening prose. The confirmed riddle truncation is repaired with the qualified record-specific FE reserve; its complete final question is visible. Fonts, physical widths, speaker/layout controls and substitutions remain preserved.

All262 bodies/264 native pages, seven captions and24 name strings pass native and direct visual review. Stored checks pass264 pages (117 fresh parity-sensitive/147 exact reuse),990 relative branch cases,262 effective-body lookups,336 SC2 loads/cache hits and672 parent handoffs. Three disclosed initialized emulator samples observe139 bodies/141 pages, both effective personality tables, allseven captions, two page turns,21 FE returns, the three-choice Right cursor and two-choice No cursor with following A returns. All18 actual body/menu/transition sheets were viewed. The123 remaining body variants have offline native/stored coverage, including14 other personality alternatives.

These initialized samples concatenate conditional alternatives and preserve a qualified Lil B22 host. Original optional conditions, branch outcomes, reward/stat effects, geography, chronology, free sailing, full-route playthroughs and hardware remain unvisited. Numeric menu return values and cancellation are separately checked offline. Full catalogue UI layouts and future role assignments are not inferred from name-string tests.

The exact cumulative candidate also passes its own31,000-frame Maria/Hangzhou cold boot, six directly viewed captures,24 protected name getters,27 fresh repository tests and eight production-scope rejections. Its existing isolated system unlock is disclosed and unearned.

The ledger now credits24,744 contextual reviews:14,704 revisions and10,040 retentions. Native Lil scope has1,154 positions remaining; the full shared/shop/town/random/player-facing and broader name review stays active. Preserve earlier translations, justified retentions, ROMs and evidence. No guide photos are required. Deferred graphics artwork and the later older-record technical re-audit remain separate.

After cloning, run `git lfs pull` for the coverage ledger. Cold-boot this exact filename and check title/New Game, Rafael/tutorial, town/Market Trade, names, wrapping and transitions. Report the filename with any issues.
'''
    (OUT / 'README.md').write_text(text, encoding='utf-8', newline='\n')
    pins = Path('translations/rom_retention_pins.json')
    before = pins.read_bytes()
    values = load(pins)
    for p in [Path(release['candidate']), Path(release['exact_clean_reconstruction']), rom]:
        if not any(Path(v['path']).resolve() == p.resolve() for v in values):
            values.append(dict(path=str(p.resolve()), reason='Preserve Lil269 cumulative testing candidate or exact reconstruction. SHA256 ' + digest(p)))
    (TEST / 'retention_pins.before.json').write_bytes(before)
    pending = pins.with_name('rom_retention_pins.Lil269_package.pending.json')
    assert not pending.exists()
    save(pending, values)
    assert pins.read_bytes() == before
    os.replace(pending, pins)
    save(OUT / 'checksums.json', {str(p.relative_to(OUT)).replace('\\', '/'): digest(p)
        for p in OUT.rglob('*') if p.is_file()})
    assert digest(registry) == release['registry_sha256']
    print('Packaged727-entry cumulative candidate and exact clean-input patch; main awaits acceptance.')
    print(rom)
    print(digest(rom))


if __name__ == '__main__':
    main()
