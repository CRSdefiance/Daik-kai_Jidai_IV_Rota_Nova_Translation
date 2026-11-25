"""Save the 254 individual source-first contextual decisions and exact evidence."""

from collections import Counter
from copy import deepcopy
import gzip
from pathlib import Path

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.save_editorial_progress_checkpoint_v10 import checkpoint
from scripts.seal_lil254_clean_v1 import ARCHIVE, ROOT


RELEASE = Path('work/lil278_B299_B311_release_v1/registered_release_verification.json')
DECISIONS = [ARCHIVE / name for name in ('B312_B315_comparisons.txt', 'B316_B319_comparisons.txt')]


def comparisons(release):
    packet_path = ROOT / 'clean_source_packet.json'
    current_path = ROOT / 'current_v1/current_effective.json'
    objects_path = ROOT / 'current_objects_v1/current_objects.json'
    seal_path = ROOT / 'clean_draft_seal_v1.json'
    role_path = ROOT / 'dynamic_roles_all_v1.json'
    name_path = ROOT / 'scoped_names_macros_reference_v1.json'
    packet, current, objects, seal, roles, names = map(load, (
        packet_path, current_path, objects_path, seal_path, role_path, name_path,
    ))
    assert seal['source_glosses_andindependent_drafts_all_saved_before_first_current_story_English_exposure']
    assert digest(seal['source_meanings']) == seal['source_meanings_sha256']
    assert digest(seal['independent_drafts']) == seal['independent_drafts_sha256']
    assert current['current_ROM_sha256'] == objects['current_ROM_sha256'] == release['candidate_sha256']
    scope = current['exact_native_context_reuse']
    blocks = list(range(312, 320))
    assert scope['exact_current_blocks'] == blocks and scope['complete_ARM9_font_payload_andCOMMON_exact']
    assert current['runtime'] == objects['runtime'] == roles['runtime'] == names['runtime']
    assert len(roles['source_records']) == 160 and roles['source_selectors'] == [207, 208, 211, 214, 215, 218]
    assert len(names['records']) == 10 and names['original_native_name_getters'] == 20
    assert len(objects['style_records']) == 158 and len(objects['choice_records']) == 8
    assert len(objects['style_objects']) == 27 and objects['native_style_getter_cases'] == 216
    assert len(objects['choice_objects']) == 3
    bound = {row['id']: row for group in current['groups'] for row in group['records']}
    bound.update({row['id']: row for row in objects['style_records'] + objects['choice_records']})
    source = [row for group in packet['groups'] for row in group['records']]
    lines = [line for path in DECISIONS for line in path.read_text(encoding='utf-8').splitlines()]
    assert len(bound) == len(source) == len(lines) == 254
    records = []
    for clean, line in zip(source, lines, strict=True):
        short_id, action, reason, *override = line.split('|')
        row = deepcopy(bound[clean['id']])
        assert short_id == 'B' + row['id'].split('_B', 1)[1]
        assert all(row[key] == clean[key] for key in ('source_hex', 'source_reference', 'source_Japanese'))
        assert row['current_reference'] and row['current_hex'] and not any(row['review'].values())
        assert action in {'D', 'K', 'E'} and len(override) == (action == 'E') and reason
        prior = row['current_comparison_paragraph']
        proposed = {'D': row['independent_English_draft'], 'K': prior, 'E': ''.join(override)}[action]
        assert proposed and proposed == proposed.strip() and proposed.isascii(), short_id
        assert not any(token in proposed for token in ('\n', '\r', '{LB', '{ALIGN', '{PAD}'))
        assert (proposed == prior) == (action == 'K'), short_id
        assert all(proposed.count(token) == count for token, count in row['source_macros'].items()), short_id
        row.update(proposed_English=proposed, decision='retention' if action == 'K' else 'revision',
                   finding=reason, retention_reason=reason if action == 'K' else None,
                   contextual_comparison_saved=True, contextual_comparison_pending=False,
                   current_English_comparison_pending=False, source_current_comparison_pending=False,
                   earlier_English_unconsulted=False, current_ROM_English_unconsulted=False,
                   names_terms_consumers_andfresh_display_approval_pending=True,
                   source_draft_provenance=str(seal_path), source_draft_provenance_sha256=digest(seal_path),
                   no_proposal_may_ship_orreceive_completion_credit_yet=True, new_credit=0)
        records.append(row)
    counts = Counter(row['decision'] for row in records)
    out = ROOT / 'all254_contextual_comparisons_v1.json'
    assert not out.exists()
    save(out, dict(
        format='dk4-scoped-contextual-comparisons-v1', translation_policy='natural-dialogue-v2',
        target_locale='en-US', records=records, records_count=len(records), complete_exchanges=len(blocks),
        blocks=blocks, revised=counts['revision'], retained=counts['retention'], runtime=current['runtime'],
        current_ROM=current['current_ROM'], current_ROM_sha256=current['current_ROM_sha256'],
        exact_native_context_reuse=scope, all_individual_findings_andretention_reasons_saved=True,
        source_clean_meanings_andindependent_drafts_preceded_current_intake=True,
        all_five_gates_still_pending=True, scoped_names_terms_fresh_native_display_andintegration_pending=True,
        new_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in
                  [packet_path, current_path, objects_path, seal_path, role_path, name_path, *DECISIONS]},
    ))
    return out, counts


def main():
    manifest = ARCHIVE / 'archive_manifest.json'
    assert not manifest.exists()
    release = load(RELEASE)
    comparison, counts = comparisons(release)
    artifacts = {}
    for path in sorted(ROOT.rglob('*.json')):
        raw = path.read_bytes()
        packed = (ARCHIVE / path.relative_to(ROOT)).with_suffix('.json.gz')
        assert not packed.exists()
        packed.parent.mkdir(parents=True, exist_ok=True)
        packed.write_bytes(gzip.compress(raw, compresslevel=9, mtime=0))
        assert gzip.decompress(packed.read_bytes()) == raw
        artifacts[str(path)] = dict(archive=str(packed), source_sha256=digest(path), archive_sha256=digest(packed))
    producers = [Path(__file__), Path('scripts/seal_lil254_clean_v1.py'),
                 Path('scripts/prepare_lil254_source_intake_v1.py'), *sorted(ARCHIVE.glob('*.txt'))]
    save(manifest, dict(artifacts=artifacts, producers={str(path): digest(path) for path in producers},
                       source_objects=254, complete_exchanges=8, revisions=counts['revision'],
                       retentions=counts['retention'], all_five_review_gates_pending=True,
                       current_references_point_to_registered_Lil278=True, new_credit=0, full_goal_complete=False))
    summary = ('Lil B312–B319 has 254 clean-source drafts and individual contextual comparisons across eight exchanges. '
               f"The comparison ledger records {counts['revision']} proposed revisions and {counts['retention']} justified retentions. "
               'Native name and control references are bound. Final terminology, prose gates and display checks remain pending. '
               'The ledger still credits 25,383 reviews.')
    notes = f"""# Lil B312–B319 contextual review checkpoint

{summary}

The eight complete exchanges include 88 ordinary records, 158 physical personality alternatives and eight menu captions. Every Japanese meaning and independent draft was sealed before the registered English was extracted. Current references bind to Lil278. All eight current blocks, ARM9, COMMON and the startup payload matched the qualified earlier Lil runtime. The original lookups also verified all 216 personality slots across 27 objects. These checks establish control and text identity for comparison.

The wolf scene now uses the singular reading consistent with Lil addressing the animal directly. The options distinguish driving it off, fighting and running. The descent scene restores the risky choice and keeps injuries uncertain. The town clues retain the city-gate restriction despite pressure from abroad and the hearsay about an illustrated map and nearby ruins. The scorpion scene distinguishes the actual sting and one-day treatment from the cactus spine and the dropped luggage. Three wordless pauses use ASCII punctuation in the proposals.

Verisa's censer dialogue preserves the established Goryeo Celadon Burner alias pending the exact item consumer check. The two B317 replies keep their clean selector 00, which is associated with Rafael in the name getter. Verify the display in its own context before assigning a different speaker. The trader exchange preserves Lil's FO company substitution, Silveira and Espinosa, the three separate outcomes, and the argument that lower unit cost can open legitimate trade to more people. The New World crop report remains hearsay.

Both name getters were checked for ten scoped actors. The initialized dispatch resolves CF to Lil, and D0, D3, D6, D7 and DA to Sailor in the saved startup context. Later assignments remain unobserved. Next, settle terminology and name decisions, run the individual prose gates, and verify native layouts and representative gameplay. The proposals are pending release and coverage credit. Lil278 remains the cumulative testing candidate. [Exact source and comparison archive](../{manifest.as_posix()})
"""
    evidence = {str(path): digest(path) for path in [manifest, comparison, ROOT / 'clean_draft_seal_v1.json',
        ROOT / 'dynamic_roles_all_v1.json', ROOT / 'scoped_names_macros_reference_v1.json']}
    progress = dict(new_credit=0, records=254, complete_exchanges=8, proposed_revisions=counts['revision'],
                    justified_retentions=counts['retention'], native_name_getters_bound=20,
                    all_contextual_comparisons_saved=True, all_five_gates_pending=True,
                    registered_integration_pending=True, evidence=evidence, full_goal_complete=False)
    checkpoint(
        mutation=ROOT / 'contextual_checkpoint_v1', batch_key='editorial_execution_priority_20261104',
        batch_updates=dict(new_credit=0, current_batch='Lil B312–B319 contextual comparisons saved',
                           current_batch_not_yet_integrated=True, current_batch_registered_andcredited_once=False,
                           all_current_batch_fifth_gates_pending=True, current_batch_evidence=evidence,
                           no_batch_worker_live=True, previous_goal_turn_classification='progress',
                           current_goal_turn_classification='progress', guide_photos=False,
                           next_action='Finalize Lil B312–B319 names and terms, prose gates and native formatting.'),
        new_entries={'Lil_SC2_B312_B319_clean_20261110': progress},
        summary=summary, document=Path('docs/editorial_Lil254_contextual_20261110.md'),
        document_text=notes, completed=25383, protected={
            'translations/release_stack.json': release['registry_sha256'],
            'translations/promoted_build.json': digest('translations/promoted_build.json'),
            release['candidate']: release['candidate_sha256'], release['manifest']: release['manifest_sha256'],
            release['patch']: release['patch_sha256'], release['canonical_base']: release['canonical_sha256'],
        },
    )
    print(f'Archived 254 comparisons and {len(artifacts)} source and native binding artifacts. {dict(counts)}.')


if __name__ == '__main__':
    main()
