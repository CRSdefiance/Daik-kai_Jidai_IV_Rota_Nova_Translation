"""Package the exact registered ship-label candidate and preserve its handoff."""

import gzip
from pathlib import Path

from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_ship_command_release_v1 import ACTUAL, LEDGER, PROMOTED, REVIEW
from scripts.stage_ship_command_release_v1 import CLEAN, GETTERS, OUT, PARENT_REGISTRY, REGISTRY, RELEASE, STARTUP


PACKAGE = Path('releases/all_routes_editorial_20261110_ship_command_candidate')
TEST = Path('out/promotion_ready_20261110_ship_command_v1')
DOCUMENT = Path('docs/editorial_ship_command_registered_20261110.md')


def replace_checked(path, data):
    before = path.read_bytes() if path.exists() else None
    staged = path.with_name(path.name+'.ship_label.pending')
    assert not staged.exists()
    staged.write_bytes(data)
    assert (path.read_bytes() if path.exists() else None) == before
    staged.replace(path)
    assert path.read_bytes() == data


def main():
    assert not any(p.exists() for p in (PACKAGE, TEST, DOCUMENT))
    release = load(RELEASE)
    completed = load(OUT/'completion_checkpoint.json')
    assert completed['counts'] == dict(completed=25899, revised=15402, retained=10497)
    assert completed['ledger_sha256'] == digest(LEDGER) and completed['new_credit'] == 1
    assert release['registry_sha256'] == digest(REGISTRY)
    assert load(REGISTRY)['latest_promoted_build'] == load(PARENT_REGISTRY)['latest_promoted_build']
    promoted_hash = digest(PROMOTED)
    for key in ('candidate','patch','manifest','actual_ship_menu','own_registered_startup','own_registered_name_getters'):
        assert digest(release[key]) == release[key+'_sha256']
    assert release['registered_manifest_entries'] == 732 and release['passing_release_checks'] == 67
    TEST.mkdir()
    rom = TEST/'Translation_DS_All_Routes_Abandon_Ship_20261110_candidate.nds'
    apply_xdelta(CLEAN, Path(release['patch']), rom)
    assert digest(rom) == release['candidate_sha256'] == digest(release['exact_clean_reconstruction'])
    manifest = rom.with_suffix('.manifest.json')
    manifest.write_bytes(Path(release['manifest']).read_bytes())
    assert digest(manifest) == release['manifest_sha256']
    PACKAGE.mkdir()
    patch = PACKAGE/'translation.xdelta'
    patch.write_bytes(Path(release['patch']).read_bytes())
    assert digest(patch) == release['patch_sha256']
    for source, name in ((manifest,'build_manifest.json.gz'), (REGISTRY,'build_release_stack.json.gz')):
        raw = source.read_bytes()
        target = PACKAGE/name
        target.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
    proof = PACKAGE/'verification'
    proof.mkdir()
    for p in [RELEASE, STARTUP, GETTERS, ACTUAL, REVIEW, OUT/'completion_checkpoint.json',
              OUT/'registration_mutation_plan.json', Path('out/ship_command_repo_qa_v2.xml')]:
        target = proof/p.name
        target.write_bytes(p.read_bytes())
        assert digest(target) == digest(p)
    receipt = dict(profile=release['profile'], candidate=str(rom), candidate_sha256=digest(rom),
        patch=str(patch), patch_sha256=digest(patch), clean_input_sha256=digest(CLEAN),
        manifest_sha256=digest(manifest), accepted_layers=114, release_entries=732, release_checks=67,
        integrated_editorial_reviews=25899, exact_registered_candidate_reconstructed_from_clean_input=True,
        main_promoted=False, user_acceptance_pending=True)
    save(TEST/'promotion_reconstruction.json', receipt)
    save(PACKAGE/'release_manifest.json', receipt)
    notes = f"""# Cumulative testing candidate with Abandon Ship

Use the local testing ROM `{rom}` and its adjacent manifest. Apply `translation.xdelta` to the clean Japanese ROM with SHA-256 `{receipt['clean_input_sha256']}`. The expected candidate hash is `{receipt['candidate_sha256']}`. Patch SHA-256 is `{receipt['patch_sha256']}`.

The native Assign Sailors menu now displays Abandon Ship. Six complete live caption masks match the native render. Back opens the ship confirmation, and No restores the same menu while retaining the ship. The emulator test used an isolated fleet save and set one secondary ship's crew count to zero. Hardware and confirmed abandonment remain unvisited.

The candidate preserves all 731 predecessor entries and 114 accepted layers, including Rafael's tutorials, the Market Trade-screen correction and the ASCII right-bound fix. Its own cold boot, 24 protected name getters, 67 release checks and 27 selected repository tests passed. Main V4701 awaits user cold-boot acceptance.
"""
    (PACKAGE/'README.md').write_text(notes, encoding='utf-8', newline='\n')
    save(PACKAGE/'checksums.json', {p.relative_to(PACKAGE).as_posix():digest(p)
        for p in PACKAGE.rglob('*') if p.is_file()})
    pins_path = Path('translations/rom_retention_pins.json')
    pins = load(pins_path)
    for p in [rom, Path(release['candidate']), Path(release['exact_clean_reconstruction'])]:
        if not any(Path(row['path']).resolve() == p.resolve() for row in pins):
            pins.append(dict(path=str(p.resolve()), reason='Preserve registered ship command candidate or exact reconstruction. SHA256 '+digest(p)))
    pin_backup = TEST/'retention_pins.before.json'
    pin_backup.write_bytes(pins_path.read_bytes())
    staged = pins_path.with_name('rom_retention_pins.ship_label.pending.json')
    assert not staged.exists()
    save(staged, pins)
    assert pin_backup.read_bytes() == pins_path.read_bytes()
    staged.replace(pins_path)

    summary = ('Abandon Ship is registered and credited once. The native menu passed exact live caption and Back/No checks. '
        'The cumulative patch reconstructs byte for byte. The ledger credits 25,899 reviews.')
    document = f"""# Abandon Ship registered cumulative candidate

{summary}

The [test ROM](../{rom.as_posix()}) has SHA-256 `{receipt['candidate_sha256']}`. Use its adjacent manifest or apply the [clean-input patch](../{patch.as_posix()}). The candidate retains the 731 prior entries, 114 accepted layers, the Market formatter and both Market pointers, Rafael's tutorials and the ASCII right-bound correction. Main V4701 awaits user acceptance. [Package notes](../{PACKAGE.as_posix()}/README.md)

The focused 8,500-frame emulator run started from the isolated test save and set one secondary ship's existing crew field to zero. The original caller produced the Latina notice and opened Assign Sailors. Six complete normal and highlighted caption masks match the native renders. Back opened the named confirmation. No returned to a pixel-identical menu and the original ship remained assigned to the fleet. A read-only export verified the new label and previous Market literal in live ITCM. Natural crew depletion, confirmed abandonment and hardware remain unvisited. [Live evidence](../{proof.as_posix()}/ship_menu_actual_verification.json)

The 31,000-frame Maria cold boot and both getters for 12 protected names passed. The release has 732 entries and 67 passing checks. Exact references and all five editorial gates are recorded for the single new label. [Review record](../{REVIEW.as_posix()})

The preceding turn made progress by completing and pushing 30 shared notice decisions, 19 static pages and the staged ship-label proof. This turn finished the focused gameplay check and registered the exact build. Continue the 11 substitution-bearing notices and their native wrapping, then bind storage and run representative tests for the 30-message batch. Reuse the 19 viewed static pages where their dependencies match. The wider COMMON, town and random exchanges, names, UI prose and older wrap and glyph leads remain in scope. Deferred artwork and the later older-record technical re-audit remain separate.
"""
    replace_checked(DOCUMENT, document.encode('utf-8'))
    lead = ('# Current editorial checkpoint - 2026-11-10\n\n'+summary+'\n\nContinue from ['+
        DOCUMENT.stem+']('+DOCUMENT.name+'). Reuse the completed checks; earlier entries below are historical.\n\n').encode('utf-8')
    for filename in ('editorial_handoff_current.md','editorial_efficiency_workflow.md','translation_progress.md'):
        path = Path('docs')/filename
        replace_checked(path, lead+path.read_bytes())
    assert digest(PROMOTED) == promoted_hash and digest(REGISTRY) == release['registry_sha256']
    print(f'Packaged registered ship-command successor at {rom}.')


if __name__ == '__main__':
    main()
