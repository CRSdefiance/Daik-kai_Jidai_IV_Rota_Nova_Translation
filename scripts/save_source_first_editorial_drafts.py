"""Save logical English against exact clean meanings; formatting and old-English decisions remain open."""
import argparse
import re
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ['meanings', 'bindings', 'authored', 'out']:
        parser.add_argument('--' + name, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    meanings, bindings, authored = [load(p) for p in [args.meanings, args.bindings, args.authored]]
    lookup = {r['id']: r for r in meanings['records']}
    identities = {r['actor_ID']: r for r in bindings['records']}
    assert len(lookup) == len(meanings['records'])
    rows, seen = [], set()
    for ident, english, note in authored['records']:
        assert ident in lookup and ident not in seen and note.strip()
        seen.add(ident)
        source = lookup[ident]
        assert english == english.strip() and '\n' not in english and '\t' not in english
        assert not any(s in english for s in ['{LB', '{ALIGN', '{PAD}', '  ', '%'])
        # CP932 and macro parity are necessary draft checks, not native formatting approval.
        assert english.encode('cp932').decode('cp932') == english
        macros = {m: len(re.findall(r'\{MACRO:' + m + r'\}', english)) for m in ['FI', 'FA', 'FO']}
        assert macros == source['source_macros'], (ident, macros, source['source_macros'])
        actor = source['source_selector']
        speaker = next(r['text'] for r in identities[actor]['current_consumers'] if r['consumer'] == 'progressive-nameplate') if actor < 207 else 'Source-qualified embedded speaker / system panel'
        exposed = [r for r in bindings.get('incidental_legacy_dialogue_exposure', []) if r['id'] == ident]
        rows.append({**source, **dict(english=english, logical_English=english, speaker=speaker,
                         context=source['exchange_context'], localization_note=note,
                         review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
                         source_meaning_preceded_any_prior_English_exposure=True,
                         current_English_conversation_comparison_pending=True, current_reference_pending=True,
                         incidental_legacy_line_exposure=exposed,
                         earlier_English_unconsulted=not exposed,
                         native_speaker_item_terms_localization_andformatting_pending=False,
                         no_authored_ordinary_breaks_alignment_orpadding=True,
                         formatting_visual_stored_gameplay_andrelease_pending=True,
                         decision='source-first-draft-not-yet-compared', new_credit=0)})
    blocks = sorted({r['block'] for r in rows})
    for block in blocks:
        assert {r['id'] for r in rows if r['block'] == block} == {r['id'] for r in meanings['records'] if r['block'] == block}, block
    save(args.out, dict(format='dk4-clean-first-logical-English-drafts-v1', translation_policy='natural-dialogue-v2',
                        target_locale='en-US', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
                        records=rows, complete_exchange_blocks=blocks, draft_records=len(rows),
                        current_ROM=bindings['runtime']['candidate'], current_ROM_sha256=bindings['runtime']['candidate_sha256'],
                        no_prior_English_conversation_comparison=True, no_new_completion_credit=True,
                        formatting_andtechnical_approval_not_inferred_from_draft_checks=True,
                        incidental_legacy_exposure_disclosed_per_record=True,
                        evidence={str(p):sha(p.read_bytes()) for p in [args.meanings, args.bindings, args.authored, Path(__file__)]}))
    print(f'Saved{len(rows)} logical English drafts/{len(blocks)} complete exchanges; exact IDs/macros/CP932 pass; formatting, comparison and completion remain pending.')


if __name__ == '__main__':
    main()
