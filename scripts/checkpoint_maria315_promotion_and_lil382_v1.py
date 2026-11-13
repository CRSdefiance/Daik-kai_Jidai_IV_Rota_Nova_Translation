"""Save the promotion handoff and unfinished Lil work with zero new credit."""
import ast
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil382_residual_A_clean_20261110')
PACKAGE = Path('releases/all_routes_editorial_20261110_maria315_candidate')
ARCHIVE = Path('translations/editorial_checkpoints/Lil382_clean_20261110_v1')


def main():
    assert not ARCHIVE.exists()
    releasepath = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
    release = load(releasepath)
    promotionpath = PACKAGE/'verification/promotion_reconstruction.json'
    promotion = load(promotionpath)
    assert promotion['exact_registered_candidate_reconstructed_from_clean_input']
    assert not promotion['main_promoted'] and promotion['pending_Lil382_not_in_this_ROM']
    assert digest(promotion['candidate']) == release['candidate_sha256']
    assert digest(promotion['manifest']) == release['manifest_sha256']
    report = Path('work/maria315_promotion_repository_qa_v1/pytest.xml')
    tests = ET.parse(report).getroot()[0]
    assert (tests.attrib['tests'], tests.attrib['errors'], tests.attrib['failures']) == ('27', '0', '0')
    selection = load(ROOT/'source_selection_v1.json')
    seal = load(ROOT/'clean_draft_seal_v1.json')
    assert (selection['source_objects'], selection['full_clean_context_objects'],
            selection['credited_context_objects']) == (382, 391, 9)
    assert selection['exact_disjoint_credited_keys']
    assert seal['source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure']
    for path, expected in seal['evidence'].items():
        assert digest(path) == expected, path
    drafts = load(seal['independent_drafts'])
    assert len(drafts['records']) == 382
    assert all(not any(r['review'].values()) for r in drafts['records'])
    current = load(ROOT/'current_v1/current_effective.json')
    names = load(ROOT/'scoped_names_macros_reference_v1.json')
    assert current['records'] == 364 and names['scoped_actors'] == 34
    assert names['original_native_name_getters'] == 68
    assert not (ROOT/'current_objects_v1/current_objects.json').exists()
    startup = load(ROOT/'current_context_v1/own_Lil_startup_verification.json')
    assert (startup['frames'], startup['actual_captain_getter'], startup['actual_route_word']) == (4001, 2, 2)
    # Bind the real unresolved draft mistake; sealed source-first artifacts remain immutable.
    actor = next(r for r in names['records'] if r['actor_ID'] == 20)
    assert [f['source']['text'] for f in actor['source_andcurrent_fields']][:2] == ['フェルナンド', 'ディアス']
    assert [f['current']['text'] for f in actor['source_andcurrent_fields']][:2] == ['Fernando', 'Dias']
    row = next(r for r in drafts['records'] if r['block'] == 236 and r['id'] == 'DK4_MES_B236_R0039')
    assert 'Emilio' in row['independent_English_draft']
    producers = sorted(Path('scripts').glob('*lil382*.py')) + [
        Path('scripts/prepare_lil391_source_intake_v1.py'),
        Path('scripts/extract_editorial_current_credited_context_v1.py'),
        Path('scripts/prepare_promotion_candidate_maria315_v1.py'), Path(__file__)]
    for path in producers:
        ast.parse(path.read_bytes(), filename=str(path))
    ARCHIVE.mkdir(parents=True)
    artifacts = {}
    # Preserve all historical JSON versions and complete source/current references in Git.
    # Runtime RAM/ROM/captures remain local; they are not standalone release assets.
    for path in sorted(ROOT.rglob('*.json')):
        target = ARCHIVE/path.relative_to(ROOT)
        target = target.with_suffix(target.suffix+'.gz')
        target.parent.mkdir(parents=True, exist_ok=True)
        raw = path.read_bytes()
        target.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(target.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(target), source_sha256=digest(path), archive_sha256=digest(target))
    archive_manifest = ARCHIVE/'archive_manifest.json'
    save(archive_manifest, dict(artifacts=artifacts, source_first_seal_preserved=True,
        contextual_comparison_pending=True, all_five_gates_pending=True,
        known_draft_correction=dict(id=row['id'], source_actor=20, draft='Emilio', required_name='Fernando',
            apply_in_contextual_comparison_not_by_rewriting_sealed_drafts=True),
        raw_runtime_RAM_andcaptures_remain_local=True,
        no_new_optional_scene_gameplay_coverage=True, new_credit=0, full_goal_complete=False))
    qa = PACKAGE/'verification/promotion_repository_checks.json'
    assert not qa.exists()
    save(qa, dict(tests=27, passed=27, errors=0, failures=0, terminal_exit_code=0,
        report=str(report), report_sha256=digest(report),
        parsed_producers={str(p): digest(p) for p in producers},
        unchanged_registered_ROM_proofs_reused=True, pending_Lil382_not_in_test_ROM=True))
    document = 'docs/editorial_promotion_Maria315_Lil382_checkpoint_20261110.md'
    summary = ('Promotion-ready Maria315 testing ROM reconstructed exactly from the clean-input patch; '
        '725 entries, 114 accepted layers and 60 release checks preserved; 27 fresh repository tests pass. '
        'The integrated total remains 24,093. Lil residual A has 382 sealed meanings/drafts in 30 complete source groups, '
        '364 current speech bindings and 34 scoped actors/68 getters; contextual comparisons and all five gates remain pending. '
        'No Lil382 text is shipped or credited. Main awaits user acceptance; the full goal remains active.')
    text = f'''# Promotion-ready Maria315 and saved Lil382 checkpoint — November 10, 2026

{summary}

## Testing build

Use [Translation_DS_Maria315_promotion_candidate.nds](../{Path(promotion['candidate']).as_posix()}) and its [adjacent manifest](../{Path(promotion['manifest']).as_posix()}). SHA256: `{release['candidate_sha256']}`. This freshly reconstructed testing copy is byte-identical to the registered cumulative Maria315 candidate, not a new editorial layer. [Patch package](../{PACKAGE.as_posix()}/README.md). Profile: `{release['profile']}`. The exact source input, patch and reconstruction identities are in [the reconstruction receipt](../{promotionpath.as_posix()}).

Canonical base remains `out/raphael_natural_v2_accepted_base.nds`, SHA256 `{release['canonical_sha256']}`. The registered Maria315 transaction changes only `/data/SC3.DK4` blocks 286–302 relative to Maria349; this handoff changes no internal ROM bytes. All 725 manifest entries and 114 accepted layers remain, including Rafael/tutorial work, prior shared/shop/town translations, graphics, names, the Market 16-byte format and both pointers, six-section ARM9, ASCII right bounds, source25v2 and B164R99 padding fix. The [registered release document](editorial_Maria315_B286_B302_registered_20261110.md) records all 60 passing checks and 315 reviews (162 revisions/153 retentions), seven layout improvements and glyph corrections.

Fresh repository verification passes 27 tests with exit code 0. Existing proofs for these exact bytes include the candidate's own 31,000-frame Maria/Hangzhou startup, 24 protected name getters, all 309 reviewed body pages/six captions/18 name strings and representative gameplay observing 213 bodies/pages, menus, FE returns and sailing. This packaging step claims no new gameplay or hardware testing. Cold-boot the new file and check title/New Game, your preferred storyline/early tutorial, town/Market Trade screen, dialogue names/wrapping and transitions. Record this exact filename when reporting problems. The candidate awaits explicit acceptance after testing; main remains V4701 (`dbfb4e413047e54e50dc771f48fe0e5457e40e60e0991111474185c41858052e`).

## Unfinished Lil work preserved

The next 382 eligible objects span 30 whole source groups: B0–B19, B21, B115 and B235–B242. All 391 Japanese context objects were read; nine already-credited B115 context objects remain preserved without duplicate credit. Qualified intake reuses the 6,720-position native inventory and verifies the exact 4,915 current SC2 credit bindings, leaving 1,805 remaining. All 382 clean meanings and independent drafts were sealed before current-English extraction: 364 ordinary speeches, 14 physical style alternatives and four captions. Three pre-seal refinements preserve starboard-quarter direction, shipmate rather than invented friendship, and the actual pillaging-soldiers wording.

All 364 current ordinary speech bodies are bound with strict complete source/current command maps, preserving four already-credited ordinary B115 context speeches. The first generic extractor rejected that partial ownership; its guarded versioned successor passes. Object binding for 14 style bodies/four captions failed with StopIteration before its aggregate output; diagnose the exact lookup before resuming without weakening source/native guards. Scoped name/default-macro binding passes 34 actors/68 original getters. Names, roles, item titles, stat labels and all 382 contextual comparisons remain pending. Every individual review gate is false. This batch has no new ROM, formatting approval, release registration or completion credit.

A known independent-draft error must be corrected during contextual comparison: actor 20 is clean フェルナンド・ディアス/current Fernando Dias, not Emilio. B236R39's gambling partner must be Fernando; audit context/gloss labels using actor 20 too. Preserve the sealed drafts and document the correction in the reviewed successor. Provisional Janus/Cristina/Yuris/Jam names and item/stat terminology also require source/current consumer binding. B115's Maria/Xien source controls stay intact within SC2; the Lil captain context is separate. Preserve source relationships and ranks; review alternate battle/capture outcomes in their own contexts.

The existing registered ROM received a fresh 4,001-frame captain 2/route 2 cold-boot runtime context with exactly 123,264 staged bytes and original getters. This covers the ordinary Lil opening context; it provides no gameplay coverage of the 382 optional source objects. Its original receipt retains direct_visual_review_pending, and this handoff adds no visual approval. Raw snapshot/captures stay local. All 32 JSON artifacts, including historical versions, exact source/current references and seal, are saved losslessly under [the archived checkpoint](../{archive_manifest.as_posix()}); producers are committed too. Failed producers and historical artifacts remain preserved.

Resume object binding, then contextual prose/name/role/term comparisons, fresh wrapping/glyph checks, every generated page's visual review, storage and representative gameplay before registered integration and once-only credit. The integrated total remains 24,093 = 14,343 revisions + 9,750 retentions. The native Maria census covers all 5,129 positions; Lil's 1,805 remaining objects include this 382. Shared/shop/town/random/player-facing prose, the broader 207-name review, earlier unfinished passes and early Rafael/tutorial priority remain fully in scope. Preserve all ROMs, translations, retentions and evidence. No guide photos. Deferred graphics artwork and the later older-record technical re-audit remain separate.
'''
    note = PACKAGE/'PROMOTION_CANDIDATE.md'
    assert not note.exists()
    note.write_text(f'''# Promotion-ready testing copy — November 10, 2026

Use `{Path(promotion['candidate']).as_posix()}` and its adjacent manifest. ROM SHA256: `{release['candidate_sha256']}`. Fresh clean-input reconstruction is byte-identical to the registered cumulative Maria315 release: 725 entries, 114 accepted layers and 60 release checks. Fresh repository QA: 27 passing tests. Existing startup, name-getter and representative gameplay evidence applies to these exact bytes; this handoff claims no new gameplay. Includes completed Maria dialogue, earlier Rafael/tutorial work, the Market correction, wrap/glyph fixes and all preserved layers.

Main awaits explicit acceptance after cold-boot testing. Unfinished Lil382 clean-first drafts/current bindings are saved separately and excluded from this ROM. See [the current handoff](../../{document}) for exact provenance, remaining work and known draft corrections. The full editorial goal remains active.
''', encoding='utf-8', newline='\n')
    save(PACKAGE/'checksums.json', {
        str(p.relative_to(PACKAGE)).replace('\\', '/'): digest(p)
        for p in PACKAGE.rglob('*') if p.is_file() and p.name != 'checksums.json'
    })
    evidence = {str(p): digest(p) for p in [archive_manifest, promotionpath, qa, releasepath]}
    protected = {'translations/release_stack.json': release['registry_sha256'],
        release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
        release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256']}
    checkpoint(mutation=ROOT/'promotion_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil382 clean drafts/current bindings; review gates pending.',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            current_batch_evidence=evidence, no_batch_worker_live=True, guide_photos=False,
            next_action='Resolve Lil382 object binding,then whole-exchange contextual prose/name/term review.'),
        new_entries={'Lil_SC2_residual_A_382_clean_20261110': dict(new_credit=0,
            selected_source_objects=382, complete_clean_context_objects=391, credited_context_objects_preserved=9,
            complete_exchanges=30, clean_meanings_andindependent_drafts_sealed=True,
            current_ordinary_speeches_bound=364, current_scoped_actors_bound=34, current_name_getters_bound=68,
            style_andchoice_binding_pending=True, contextual_comparison_pending=True,
            all_five_review_gates_pending=True, known_draft_name_correction='B236R39 Fernando;actor20 isnot Emilio',
            display_stored_gameplay_andregistered_integration_pending=True,
            no_batch_worker_live=True, evidence=evidence, full_goal_complete=False)},
        summary=summary, document=document, document_text=text, completed=24093, protected=protected)
    for path, item in artifacts.items():
        assert digest(path) == item['source_sha256']
    for name, expected in load(PACKAGE/'checksums.json').items():
        assert digest(PACKAGE/name) == expected
    print('PASS promotion handoff,Lil382 checkpoint andlossless32-artifact archive;zero new credit.')


if __name__ == '__main__':
    main()
