"""Bind all301 independent drafts, preserving originals and recording source-reread refinements."""
from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_B0_B32_clean_20261109')
REFINEMENTS = {
    (19, 188): ("Those pirates were my father's men. Ever since I was a child, I learned swordsmanship and the pirate trade by watching and copying.",
        'Leave the object of watching/copying implicit as in the Japanese; do not select the crew rather than her father.'),
    (19, 217): ("I've realized that, more than becoming a great pirate, I really just wanted something to remember my father by...",
        'Preserve the comparative priority of the keepsake; do not categorically deny that she wanted to become a great pirate.'),
    (29, 119): ("If FI is on our side, we're in good hands!",
        'Localize the hundred-people confidence idiom while retaining the conditional and avoiding a new absolute safety claim.'),
    (25, 12): ("...Even a buzzing fly is quieter. Let's hurry to Veracruz.",
        'Preserve the source noise comparison and small-fly image without selecting a particular insect species.'),
}


def main():
    out = ROOT / 'all301_clean_meanings_andindependent_drafts_v1.json'
    proof = ROOT / 'all301_clean_draft_qualification_v1.json'
    assert not out.exists() and not proof.exists()
    packet_path = ROOT / 'clean_source_packet.json'
    packet = load(packet_path)
    expected = {(g['block'], r['source_record_index']): r for g in packet['groups'] for r in g['records']}
    parts = [ROOT / f'independent_drafts_{part}_v1.json' for part in ['B0_B10', 'B11_B21', 'B22_B32']]
    rows = [deepcopy(r) for path in parts for r in load(path)['records']]
    indexed = {(r['block'], r['source_record_index']): r for r in rows}
    assert len(rows) == len(indexed) == len(expected) == 301 and indexed.keys() == expected.keys()
    refinements = []
    for key, (draft, reason) in REFINEMENTS.items():
        row = indexed[key]
        refinements.append(dict(id=row['id'], source_reference=row['source_reference'],
            source_Japanese=row['source_Japanese'], previous_independent_draft=row['independent_English_draft'],
            refined_independent_draft=draft, reason=reason))
        row['independent_English_draft'] = draft
        row['source_reread_draft_refinement'] = reason
    for key, row in indexed.items():
        original = expected[key]
        assert all(row[k] == v for k, v in original.items() if k not in ['source_meaning_pending', 'localized_draft_pending'])
        assert row['source_meaning_pending'] is False and row['localized_draft_pending'] is False
        assert row['source_meaning'] and row['whole_exchange_context']
        draft = row['independent_English_draft']
        assert draft and draft.isascii() and draft == draft.strip()
        assert not any(s in draft for s in ['\n', '\r', '\t', '{LB', '{PAD}', '{ALIGN'])
        assert {t: draft.count(t) for t in row['source_macros']} == row['source_macros']
        assert set(re.findall(r'F[A-Z]', draft)) == set(row['source_macros'])
        assert row['current_English_unconsulted'] and row['independent_draft_precedes_current_English_intake']
        assert row['current_English_comparison_pending'] and not any(row['review'].values())
    evidence = {str(p): digest(p) for p in [packet_path, *parts, Path(__file__), Path('docs/name_source_review_v294.md')]}
    save(out, dict(records=rows, records_count=301, complete_exchanges=32,
        translation_policy='natural-dialogue-v2', target_locale='en-US',
        clean_source_packet=str(packet_path), clean_source_packet_sha256=digest(packet_path),
        source_meanings_andlogical_drafts_all_saved_before_current_English_intake=True,
        current_English_unconsulted=True, source_reread_refinements=refinements,
        original_draft_chunks_unchanged=True, all_five_gates_pending=True,
        scoped_names_terms_native_consumers_andcurrent_comparisons_pending=True,
        no_formatted_pages_orobserved_gameplay_approved=True,
        no_new_ROM_orcompletion_credit=True, new_credit=0, evidence=evidence))
    save(proof, dict(source_objects=301, complete_exchanges=32,
        kind_counts=dict(Counter(r['kind'] for r in rows)),
        independent_drafts=301, remaining_independent_drafts=0, source_reread_refinements=4,
        current_comparisons=0, remaining_current_comparisons=301,
        all_source_field_bindings_exact=True, all_literal_native_substitutions_exact=True,
        macro_occurrences=dict(sum((Counter(r['source_macros']) for r in rows), Counter())),
        all301=str(out), all301_sha256=digest(out),
        scoped_epithet_working_term_evidence='docs/name_source_review_v294.md',
        epithet_is_localization_inference_not_official_English_claim=True,
        all_five_gates_pending=True, new_credit=0, full_goal_complete=False, evidence=evidence))
    print('Sealed all301 clean-first drafts across32 exchanges;four source-reread refinements;tokens exact;zero credit.')


if __name__ == '__main__':
    main()
