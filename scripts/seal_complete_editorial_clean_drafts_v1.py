"""Join source-first whole-exchange speech drafts and typed captions before current extraction."""
import argparse
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['packet', 'choices', 'captions', 'out']:
        parser.add_argument('--'+key, type=Path, required=True)
    parser.add_argument('--speech-drafts', type=Path, nargs='+', required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    packet, choices, captions = map(load, [args.packet, args.choices, args.captions])
    expected = {r['id']: r for g in packet['groups'] for r in g['records']}
    rows = {}
    for path in args.speech_drafts:
        partial = load(path)
        assert partial['source_packet_sha256'] == sha(args.packet.read_bytes())
        assert partial['current_SC0_English_not_consulted_in_this_intake']
        for row in partial['records']:
            key = row['id']
            assert key not in rows and key in expected
            assert all(row[k] == expected[key][k] for k in ['source_hex', 'source_reference', 'source_Japanese'])
            assert row['earlier_English_unconsulted'] and row['current_English_comparison_pending']
            rows[key] = deepcopy(row)
    assert set(rows) == set(expected) and len(rows) == packet['records']
    caption_map = {r['id']: r for r in captions['records']}
    assert len(caption_map) == len(captions['records']) == len(choices['records'])
    assert captions['current_English_unconsulted_in_this_intake']
    assert set(caption_map) == {r['id'] for r in choices['records']}
    for source in choices['records']:
        row = deepcopy(source)
        draft = caption_map[row['id']]
        assert draft['source_Japanese'] == row['source_Japanese']
        assert draft['english'].isascii() and draft['english'].strip() == draft['english']
        assert not any(c in draft['english'] for c in '\r\n\t')
        row.update(source_meaning=draft['source_meaning'], english=draft['english'],
            independent_English_draft=draft['english'], context=next(r['context'] for r in rows.values() if r['block'] == row['block']),
            review=dict(source=True, context=True, localization=False, naturalness=True, formatting=False),
            current_English_comparison_pending=True, native_complete_choice_object_binding_pending=True,
            earlier_English_unconsulted=True, new_credit=0)
        assert row['id'] not in rows
        rows[row['id']] = row
    args.out.mkdir(parents=True)
    sealed = args.out/'all_source_meanings_andindependent_drafts.json'
    save(sealed, dict(format='dk4-complete-source-first-whole-exchange-drafts-v1', translation_policy='natural-dialogue-v2', target_locale='en-US',
        file_path=packet['file_path'], clean_source_packet=str(args.packet), clean_source_packet_sha256=sha(args.packet.read_bytes()),
        clean_choice_objects=str(args.choices), clean_choice_objects_sha256=sha(args.choices.read_bytes()),
        records=list(rows.values()), source_speech_drafts=packet['records'], source_caption_drafts=len(caption_map),
        source_objects=len(rows), remaining_source_speech_orcaption_drafts=0,
        source_meanings_andlogical_drafts_sealed_before_current_ROM_English_extraction_in_this_intake=True,
        current_SC0_English_not_consulted_in_this_intake=True, no_blanket_prior_English_exposure_claim=True,
        item_titles_unbound_speakers_andformatting_pending=True, all_current_comparisons_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.packet,args.choices,args.captions,*args.speech_drafts,Path(__file__)]},
        new_credit=0, guide_photos=False, full_goal_complete=False))
    speeches = [deepcopy(r) for r in rows.values() if r['kind'] != 'typed-choice-label']
    for row in speeches:
        row['current_ROM_English_unconsulted'] = True
    save(args.out/'meanings_view.json', dict(records=speeches, meanings=len(speeches), source_packet=str(args.packet),
        source_packet_sha256=sha(args.packet.read_bytes()), all_drafts_sealed=str(sealed), all_drafts_sha256=sha(sealed.read_bytes()),
        no_blanket_prior_English_exposure_claim=True, no_source_orEnglish_wording_changed=True, new_credit=0))
    print(dict(sealed_speeches=len(speeches), sealed_captions=len(caption_map), sealed_total=len(rows), remaining_drafts=0,
        current_English_unconsulted_in_this_intake=True, new_credit=0))


if __name__ == '__main__':
    main()
