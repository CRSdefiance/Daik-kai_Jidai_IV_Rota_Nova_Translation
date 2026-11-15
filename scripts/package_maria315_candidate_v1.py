"""Package the registered cumulative candidate as an exactly reconstructable clean-input patch."""
import ast
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/maria315_B286_B302_release_v1')
EDITORIAL = Path('work/Maria_B286_B302_clean_20261110')
OUT = Path('releases/all_routes_editorial_20261110_maria315_candidate')


def main():
    assert not OUT.exists()
    release = load(ROOT/'registered_release_verification.json')
    complete = load(ROOT/'completion_checkpoint.json')
    assert (release['registered_manifest_entries'], release['accepted_layers'], release['passing_release_checks']) == (725, 114, 60)
    assert complete['counts'] == dict(completed=24093, revised=14343, retained=9750)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert digest('translations/release_stack.json') == release['registry_sha256']
    for key in ['candidate', 'manifest', 'patch']:
        assert digest(release[key]) == release[key+'_sha256']
    assert Path(release['candidate']).read_bytes() == Path(release['exact_clean_reconstruction']).read_bytes()
    old = load(ROOT/'release_stack_before_Maria315.json')
    assert old['latest_promoted_build'] == load('translations/release_stack.json')['latest_promoted_build']
    reportpath = Path('work/maria315_repository_qa_v1/pytest.xml')
    tests = ET.parse(reportpath).getroot()[0]
    assert (tests.attrib['tests'], tests.attrib['errors'], tests.attrib['failures']) == ('27', '0', '0')
    producers = sorted(set(Path('scripts').glob('*maria315*.py')) | {Path('dk4tool/patch/maria315_release_v1.py')})
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    semantic = EDITORIAL/'registered_semantic_checks_v1/qualification.json'
    OUT.mkdir()
    verification = OUT/'verification'
    verification.mkdir()
    (OUT/'translation.xdelta').write_bytes(Path(release['patch']).read_bytes())
    for src, name in [(release['manifest'], 'build_manifest.json.gz'), ('translations/release_stack.json', 'build_release_stack.json.gz')]:
        raw = Path(src).read_bytes()
        packed = gzip.compress(raw, compresslevel=9, mtime=0)
        assert gzip.decompress(packed) == raw
        (OUT/name).write_bytes(packed)
    proofs = [ROOT/'registered_release_verification.json', ROOT/'own_registered_startup_verification.json',
        ROOT/'own_registered_name_getters_v1.json', ROOT/'completion_checkpoint.json',
        EDITORIAL/'gameplay_review_v1.json', EDITORIAL/'offline_display_approval_v1.json',
        EDITORIAL/'final_layout_delta_v1.json', semantic]
    for src in proofs:
        (verification/src.name).write_bytes(src.read_bytes())
    save(verification/'actor0_scope_negatives.json', load(EDITORIAL/'actor0_scope_negatives_v1/qualification.json'))
    save(verification/'repository_checks.json', dict(selected_tests=27, passing_tests=27, errors=0, failures=0,
        terminal_exit_code=0, test_report=str(reportpath), test_report_sha256=digest(reportpath),
        active_batch_producers_parsed={str(p): digest(p) for p in producers},
        production_scope_rejection_tests=8, actor0_scope_rejection_tests=2,
        source_qualification=str(semantic), exact_native_stored_actual_andregistered_guards_pass=True,
        all_historical_failed_producers_preserved=True))
    save(OUT/'release_manifest.json', dict(profile=release['profile'], status='registered-candidate-awaiting-user-acceptance',
        candidate=release['candidate'], candidate_sha256=release['candidate_sha256'], clean_input_sha256=release['clean_input_sha256'],
        patch='translation.xdelta', patch_sha256=release['patch_sha256'], build_manifest_sha256=release['manifest_sha256'],
        release_stack_sha256=release['registry_sha256'], entries=725, accepted_layers=114, passing_release_checks=60,
        integrated_editorial_records=24093, main_promoted=False, full_goal_complete=False))
    text = f'''# Combined editorial candidate — Maria B286–B302

This cumulative testing candidate includes every accepted layer through the final315 native Maria story objects, plus earlier Rafael/tutorial work, the Market Trade-screen correction, speaker-name work and the registered ASCII right-bound correction. Main remains V4701 pending your cold-boot testing and explicit acceptance. The earlier Maria349 testing ROM and package are preserved.

Local ROM: `{release['candidate']}`. Its adjacent manifest preserves exact registered provenance. Apply `translation.xdelta` to the clean Japanese ROM with SHA256 `{release['clean_input_sha256']}`. Expected output SHA256: `{release['candidate_sha256']}`. Patch SHA256: `{release['patch_sha256']}`. Reconstruction is verified byte for byte; historical work-folder artifacts are unnecessary to apply this patch. The build contains725 manifest entries,114 accepted layers and60 passing release checks.

This batch adds315 contextual reviews:162 revisions,153 justified retentions and14 scoped name reviews. Corrections include self-reference, reported uncertainty, the guardian's reversed discovery, the Sextant being handed over rather than received, and Charles having mentioned the monk's book rather than written it. The review preserves tone, humor, cultural context and the original Rafael/Lil speaker controls. One full-width Latin I and two full-width question reactions are corrected. Seven layouts improve, including six phrase wraps and a complete warning/question reclaimed onto one page without shortening prose.

All309 final body pages,six captions and18 name strings were directly reviewed and pass native/stored checks. Four disclosed initialized emulator samples observe213 distinct bodies/pages,allthree two-choice menus/both highlight indices,six captions,17 effective voice4 alternatives,all13 system-message A returns andfour returns to sailing. The other96 body variants have offline native/stored coverage. These samples concatenate conditional alternatives and do not establish natural activation, original rewards/outcomes/geography/chronology, exhaustive playthroughs orhardware behavior. Allchanged paragraphs fit one page; no new multipage behavior is claimed.

The candidate's own31,000-frame startup reaches Hangzhou. Its six checkpoints and24 protected name getters pass. All27 selected repository tests,eight production scope rejections andtwo actor0 allowlist rejections pass. Exact first/internal/final characters,controls,substitutions,pagination,bounds,allocation,320 relocated branch cases,309 native lookups,303 archive loads and606 handoffs are checked.

The ledger credits24,093 contextual reviews:14,343 revisions and9,750 retentions. The exact native Maria source census now covers all5,129 positions; native Lil remainder is1,805. Shared/shop/town/random/player-facing prose andthe broader name review remain separate scope. The full editorial goal stays active,including earlier unfinished contextual passes. No guide photos. Deferred artwork andthe later older-record technical re-audit remain separate.

The gzip files preserve exact build-time manifest/registry bytes. `verification/` contains release,startup,getter,gameplay,offline-display,layout,source-scope andrepository receipts. Preserve existing ROMs,translations,retentions,drafts andevidence. The coverage ledger uses Git LFS; run `git lfs pull` after cloning.
'''
    (OUT/'README.md').write_text(text, encoding='utf-8', newline='\n')
    save(OUT/'checksums.json', {str(p.relative_to(OUT)).replace('\\', '/'): digest(p) for p in OUT.rglob('*') if p.is_file()})
    assert digest(OUT/'translation.xdelta') == release['patch_sha256']
    print('Packaged725-entry cumulative candidate andexact clean-input patch;main unchanged.')


if __name__ == '__main__':
    main()
