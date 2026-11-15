"""Archive the complete Lil B299–B311 contextual comparisons with zero new credit."""
from collections import Counter
import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint

ROOT = Path('work/Lil278_B299_B311_clean_20261110')
ARCHIVE = Path('translations/editorial_checkpoints/Lil278_clean_20261110_v1')
RELEASE = Path('work/lil361_B283_B298_release_v1/registered_release_verification.json')


def main():
    manifest = ARCHIVE / 'archive_manifest.json'
    assert not manifest.exists()
    release = load(RELEASE)
    packet = load(ROOT / 'clean_source_packet.json')
    current = load(ROOT / 'current_v1/current_effective.json')
    objects = load(ROOT / 'current_objects_v1/current_objects.json')
    roles = load(ROOT / 'dynamic_roles_all_v1.json')
    names = load(ROOT / 'scoped_names_macros_reference_v1.json')
    seal = load(ROOT / 'clean_draft_seal_v1.json')
    parts = [ROOT / 'contextual_proposals_v1.json', ROOT / 'contextual_adventure_proposals_v1.json']
    documents = [load(path) for path in parts]
    assert all(d['runtime'] == current['runtime'] for d in [*documents, roles, names, objects])
    assert digest(seal['source_meanings']) == seal['source_meanings_sha256']
    assert digest(seal['independent_drafts']) == seal['independent_drafts_sha256']
    assert seal['source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure']
    assert current['current_ROM_sha256'] == objects['current_ROM_sha256'] == release['candidate_sha256']
    reuse = current['exact_native_context_reuse']
    assert reuse['exact_current_blocks'] == list(range(299, 312))
    assert reuse['complete_ARM9_font_payload_andCOMMON_exact']
    assert len(current['groups']) == 13 and sum(len(g['records']) for g in current['groups']) == 133
    assert len(objects['style_records']) == 139 and len(objects['choice_records']) == 6
    assert objects['native_style_getter_cases'] == 144
    assert len(roles['source_records']) == 141 and roles['source_selectors'] == [207, 208, 211, 214]
    assert len(names['records']) == 10 and names['original_native_name_getters'] == 20
    source = [row for group in packet['groups'] for row in group['records']]
    by_id = {r['id']: r for d in documents for r in d['records']}
    assert len(source) == len(by_id) == sum(d['records_count'] for d in documents) == 278
    rows = [by_id[r['id']] for r in source]
    for original, reviewed in zip(source, rows, strict=True):
        assert all(reviewed[k] == original[k] for k in ('id', 'source_reference', 'source_hex', 'source_Japanese'))
        assert reviewed['finding'] and reviewed['current_reference'] and reviewed['current_hex']
        assert not any(reviewed['review'].values())
        if reviewed['decision'] == 'retention':
            assert reviewed['retention_reason'] and reviewed['proposed_English'] == reviewed['current_comparison_paragraph']
    assert Counter(r['decision'] for r in rows) == {'revision': 170, 'retention': 108}
    combined = ROOT / 'all278_contextual_comparisons_v1.json'
    assert not combined.exists()
    save(combined, {**documents[0], 'records': rows, 'records_count': 278, 'complete_exchanges': 13,
        'blocks': list(range(299, 312)), 'revised': 170, 'retained': 108,
        'current_ROM': current['current_ROM'], 'current_ROM_sha256': current['current_ROM_sha256'],
        'exact_native_context_reuse': reuse,
        'evidence': {str(path): digest(path) for path in parts}})
    artifacts = {}
    for path in sorted(ROOT.rglob('*.json')):
        raw = path.read_bytes()
        packed = (ARCHIVE / path.relative_to(ROOT)).with_suffix('.json.gz')
        assert not packed.exists()
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=digest(path), archive_sha256=digest(packed))
    producers = {str(path): digest(path) for path in [Path(__file__),
        *Path('scripts').glob('*lil278*.py'), *ARCHIVE.glob('*.txt')]}
    save(manifest, dict(artifacts=artifacts, producers=producers, source_objects=278,
        complete_exchanges=13, revisions=170, retentions=108, all_five_review_gates_pending=True,
        current_references_point_to_registered_Lil361=True, exact_native_context_reuse=True,
        new_credit=0, full_goal_complete=False))
    summary = ('Lil B299–B311 has 278 source-first drafts and exact contextual comparisons across 13 exchanges. '
        'There are 170 proposed revisions and 108 justified retentions. '
        'The registered Lil361 text is bound using byte-identical runtime and block evidence. '
        'Final names and terminology, review gates, formatting, gameplay and integration are pending. '
        'The ledger has 25,105 completed reviews and 793 remaining native Lil records.')
    notes = '''# Lil B299–B311 contextual review checkpoint

''' + summary + '''

The clean Japanese glosses and independent English drafts were sealed before the current text was extracted. The archive binds each decision to its clean bytes, registered current bytes, source position and current position. The 278 records include 133 ordinary speech records, 139 physical personality alternatives and six menu captions. Exact byte comparisons establish that the previous Lil startup capture applies to these thirteen blocks and their runtime dependencies. The capture comes from Lil269 and the current text references point to registered Lil361. Native checks cover 144 personality slots and both name getters for ten scoped actors.

The snake exchange now distinguishes driving the animal away from killing it and keeps the injuries uncertain. The oasis branch restores the sandstorm, water rationing and recovery from fatigue. The river exchange keeps flood damage speculative and distinguishes looking for a bridge from trying to cross on foot. The ferry discovery and 100-gold fare remain in that second branch.

The Basra commission specifies the Indian Ocean coast, nine spices, a cargo hold of each, and one combined delivery. It keeps the 40,000-gold payment and reward, the slight market-share increase and the guildmaster's unnamed gift. The two temple errands restore six Japanese speech records across B309 and B310. A separate full-width exclamation becomes ASCII. The revised replies keep Lil's shift into forced politeness and her eventual self-correction. The directions preserve the icy sea, the peninsula and its east-coast peak, and the clan guarding the map to the Proof.

Native dispatch identifies CF as Lil in the opening context. D0, D3 and D6 resolve to the existing Sailor fallback there. Later assignments can differ. The scoped name review should preserve Matilda, Safia and Sakura as established names, Camille's given and full forms, and the distinction between Senior Monk and a specific title such as abbot. Regional name-table fields are identity metadata. The full catalogue labels remain part of the wider name review.

Continue with the exact commodity, place and Proof terminology, name decisions, and the final read-aloud pass. Then plan and verify the native layouts, stored bytes and representative gameplay before registration. Preserve the source-first seals and keep earlier builds available. The remaining storyline, shared dialogue, random scenes, player-facing prose and name review continue from the coverage ledger.

[Archived source, comparisons and verification](../translations/editorial_checkpoints/Lil278_clean_20261110_v1/archive_manifest.json)
'''
    evidence = {str(path): digest(path) for path in [manifest, combined, ROOT / 'clean_draft_seal_v1.json',
        ROOT / 'scoped_names_macros_reference_v1.json', ROOT / 'dynamic_roles_all_v1.json']}
    progress = dict(records=278, complete_exchanges=13, proposed_revisions=170, justified_retentions=108,
        native_name_getters_bound=20, all_contextual_comparisons_saved=True, all_five_gates_pending=True,
        registered_integration_pending=True, evidence=evidence, new_credit=0, full_goal_complete=False)
    checkpoint(mutation=ROOT / 'contextual_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(current_batch='Lil B299–B311 contextual comparisons saved',
            current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
            all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
            no_batch_worker_live=True, previous_goal_turn_classification='progress',
            current_goal_turn_classification='progress', guide_photos=False, new_credit=0,
            next_action='Finalize Lil B299–B311 names and terminology, then bind the native layout and gameplay checks.'),
        new_entries={'Lil_SC2_B299_B311_clean_20261110': progress},
        summary=summary, document=Path('docs/editorial_Lil278_contextual_20261110.md'), document_text=notes,
        completed=25105, protected={
            'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'],
            release['manifest']: release['manifest_sha256'],
            release['patch']: release['patch_sha256'],
            release['canonical_base']: release['canonical_sha256'],
        })
    print(f'Archived {len(artifacts)} source and comparison artifacts for 278 records. New completion credit: 0.')


if __name__ == '__main__':
    main()
