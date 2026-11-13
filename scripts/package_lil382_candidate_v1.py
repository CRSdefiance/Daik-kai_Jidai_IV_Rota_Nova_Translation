"""Publish a checksum-bound clean-input patch and an identical local testing ROM."""
import ast
import gzip
import os
import xml.etree.ElementTree as ET
from pathlib import Path
from dk4tool.patch.xdelta import apply_xdelta
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/lil382_residual_A_release_v1')
EDITORIAL=Path('work/Lil382_residual_A_clean_20261110')
OUT=Path('releases/all_routes_editorial_20261110_lil382_candidate')
TEST=Path('out/promotion_ready_20261110_lil382_v1')


def main():
    assert not OUT.exists() and not TEST.exists()
    rp=ROOT/'registered_release_verification.json';release=load(rp)
    complete=load(ROOT/'completion_checkpoint.json')
    assert (release['registered_manifest_entries'],release['accepted_layers'],release['passing_release_checks'])==(726,114,61)
    assert complete['counts']==dict(completed=24475,revised=14600,retained=9875)
    assert release['clean_input_patch_byte_exact'] and not release['own_registered_startup_pending']
    registry=Path('translations/release_stack.json');assert digest(registry)==release['registry_sha256']
    assert load(ROOT/'release_stack_before_Lil382.json')['latest_promoted_build']==load(registry)['latest_promoted_build']
    for key in ['candidate','manifest','patch','own_registered_startup','own_registered_name_getters','exact_record_bindings']:
        assert digest(release[key])==release[key+'_sha256']
    reportpath=Path('work/lil382_repository_qa_v3/pytest.xml')
    tests=ET.parse(reportpath).getroot()[0]
    assert (tests.attrib['tests'],tests.attrib['errors'],tests.attrib['failures'])==('27','0','0')
    producers=sorted(set(Path('scripts').glob('*lil382*.py'))|{Path('dk4tool/patch/lil382_release_v1.py'),Path('dk4tool/script/reviewed_credited_context_rebuild_v1.py')})
    for p in producers:ast.parse(p.read_bytes(),filename=str(p))
    visual=load(ROOT/'own_startup_visual_v1/direct_visual_review.json')
    assert visual['all_six_original_captures_andexact_composite_directly_viewed']
    OUT.mkdir();v=OUT/'verification';v.mkdir()
    patch=OUT/'translation.xdelta';patch.write_bytes(Path(release['patch']).read_bytes())
    for p,name in [(Path(release['manifest']),'build_manifest.json.gz'),(registry,'build_release_stack.json.gz')]:
        raw=p.read_bytes();packed=gzip.compress(raw,compresslevel=9,mtime=0);assert gzip.decompress(packed)==raw;(OUT/name).write_bytes(packed)
    proofs=[rp,ROOT/'completion_checkpoint.json',ROOT/'own_registered_startup_verification.json',ROOT/'own_registered_name_getters_v1.json',
            ROOT/'own_startup_visual_v1/direct_visual_review.json',EDITORIAL/'gameplay_review_v1.json',EDITORIAL/'offline_display_approval_v1.json',
            EDITORIAL/'final_layout_delta_v1.json',EDITORIAL/'credited_context_rebuild_qualification_v1.json']
    for p in proofs:(v/p.name).write_bytes(p.read_bytes())
    for p,name in [(EDITORIAL/'registered_semantic_checks_v1/qualification.json','production_scope_rejections.json'),
                   (EDITORIAL/'loaders_v1/verification.json','native_loaders.json'),
                   (EDITORIAL/'stored_catalogue_all_v1/all_stored_effective_body_bindings.json','stored_catalogue.json')]:
        (v/name).write_bytes(p.read_bytes())
    save(v/'repository_checks.json',dict(selected_tests=27,passing_tests=27,errors=0,failures=0,terminal_exit_code=0,
        report=str(reportpath),report_sha256=digest(reportpath),production_scope_rejections=8,credited_context_rejections=5,
        active_producers_parsed={str(p):digest(p) for p in producers},
        earlier_temp_directory_setup_errors_preserved='work/lil382_repository_qa_v1 and v2; corrected isolated existing-parent temp folder in v3'))
    TEST.mkdir();rom=TEST/'Translation_DS_Lil382_promotion_candidate.nds'
    clean=Path('work/clean.nds');assert digest(clean)==release['clean_input_sha256']
    apply_xdelta(clean,patch,rom)
    assert rom.read_bytes()==Path(release['candidate']).read_bytes()==Path(release['exact_clean_reconstruction']).read_bytes()
    manifest=rom.with_suffix('.manifest.json');manifest.write_bytes(Path(release['manifest']).read_bytes())
    receipt=dict(candidate=str(rom),candidate_sha256=digest(rom),manifest=str(manifest),manifest_sha256=digest(manifest),
        registered_release=str(rp),registered_release_sha256=digest(rp),clean_input=str(clean),clean_input_sha256=digest(clean),
        patch=str(patch),patch_sha256=digest(patch),exact_registered_candidate_reconstructed_from_clean_input=True,
        release_entries=726,accepted_layers=114,release_checks=61,integrated_editorial_records=24475,
        main_promoted=False,user_acceptance_pending=True,new_editorial_credit=0,new_gameplay_claim=False,full_goal_complete=False,
        producer=str(Path(__file__)),producer_sha256=digest(__file__))
    save(TEST/'promotion_reconstruction.json',receipt);save(v/'promotion_reconstruction.json',receipt)
    save(OUT/'release_manifest.json',dict(profile=release['profile'],status='registered-candidate-awaiting-user-acceptance',
        candidate=str(rom),candidate_sha256=digest(rom),clean_input_sha256=release['clean_input_sha256'],patch='translation.xdelta',
        patch_sha256=digest(patch),build_manifest_sha256=release['manifest_sha256'],release_stack_sha256=release['registry_sha256'],
        entries=726,accepted_layers=114,passing_release_checks=61,integrated_editorial_records=24475,main_promoted=False,full_goal_complete=False))
    text=f'''# Cumulative testing candidate — Lil382

Local ROM: `{rom}`. This registered successor includes all earlier accepted work through Maria315, including Rafael and tutorial localization, the Market Trade-screen correction, speaker-name fixes and the ASCII right-bound correction. All 725 predecessor entries and 114 accepted layers are preserved. Main remains unchanged pending your cold-boot testing and explicit acceptance.

Apply `translation.xdelta` to the clean Japanese ROM with SHA-256 `{release['clean_input_sha256']}`. Expected output: `{release['candidate_sha256']}`. Patch SHA-256: `{release['patch_sha256']}`. Both reconstructions were verified byte for byte. The patch can be applied without historical work folders. The gzip files preserve exact build-time manifest and registry bytes.

This batch completes 382 contextual reviews in 30 Lil SC2 groups: 257 dialogue revisions and 125 justified retentions, plus 34 scoped name reviews. It restores source meaning in the Aziza exchange, naval directions, gambling opponent, Francisca's glass rose, Gabriel's escape and other crew, letter and quest exchanges. Thirty final layouts improve; five pages are reclaimed without shortening prose. Twelve records with mixed-width punctuation are normalized. All source speaker controls, substitutions and the nine already credited B115 context objects are preserved.

All 378 bodies across 386 native pages, four captions and 42 name strings pass native and direct visual review. Storage, allocation, 555 relocated branch cases, 378 lookups, 336 SC2 loads and 672 handoffs pass. Three initialized emulator samples observe 211 bodies across 217 pages, six page turns, two personality selections, two FE message returns and both default menu returns. All four captions and 24 actual contact sheets are reviewed. The 167 other bodies, including 12 other personality alternatives and the Frozen Rose handover notice, have offline native/stored coverage. Requested DOWN inputs occurred before menu opening; only index 0 was observed. Both cursor styles and native return indices are separately checked offline. The hosts reach resupply and the following native steering tutorial; free sailing is not claimed.

The candidate's own 31,000-frame Maria startup reaches Hangzhou and passes 24 protected name getters. This is separate from the Lil content samples. All 27 selected repository tests, eight production-scope rejections and five credited-context rejections pass. The first two test attempts had temporary-directory setup errors; the passing third run uses an isolated folder with an existing parent. No product test assertion was waived.

These are disclosed initialized content samples, not natural event activation or exhaustive playthroughs. Original optional conditions, rewards, branch outcomes, geography, chronology and hardware behavior remain unvisited. Full catalogue UI layouts and future dynamic role assignments are not inferred from name-string proofs.

The ledger credits 24,475 contextual reviews: 14,600 revisions and 9,875 retentions. Native Lil story scope has 1,423 positions remaining; shared shop/town/random dialogue, other player-facing prose and the broader name review remain in scope. Preserve earlier translations, retentions, ROMs and evidence. The full goal remains active; no guide photos are required. Deferred artwork and the later older-record technical re-audit remain separate. The coverage ledger uses Git LFS; run `git lfs pull` after cloning.
'''
    (OUT/'README.md').write_text(text,encoding='utf-8',newline='\n')
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    for p in [Path(release['candidate']),Path(release['exact_clean_reconstruction']),rom]:
        if not any(Path(x['path']).resolve()==p.resolve() for x in values):values.append(dict(path=str(p.resolve()),reason='Preserve Lil382 cumulative testing candidate or exact reconstruction. SHA256 '+digest(p)))
    (TEST/'retention_pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Lil382_package.pending.json');assert not pending.exists();save(pending,values);assert pins.read_bytes()==before;os.replace(pending,pins)
    save(OUT/'checksums.json',{str(p.relative_to(OUT)).replace('\\','/'):digest(p) for p in OUT.rglob('*') if p.is_file()})
    assert digest(registry)==release['registry_sha256']
    print('Packaged 726-entry cumulative candidate and exact clean-input patch; main awaits acceptance.')
    print(rom);print(digest(rom))


if __name__=='__main__':main()
