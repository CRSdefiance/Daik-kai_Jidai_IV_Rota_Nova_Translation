"""Save complete-menu logical English captions; native menu formatting remains unapproved."""
import argparse
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load, save


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for key in ['meanings', 'authored', 'out']:
        parser.add_argument('--' + key, type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    meanings, authored = load(args.meanings), load(args.authored)
    assert authored['target_locale'] == 'en-US'
    source_objects = Path(meanings['source_choice_objects'])
    assert sha(source_objects.read_bytes()) == meanings['source_choice_objects_sha256']
    lookup = {r['id']:r for r in meanings['records']}
    clean = NdsImage.open('work/clean.nds')
    blocks = {}
    rows, seen = [], set()
    for ident, english, note in authored['records']:
        assert ident in lookup and ident not in seen and note.strip()
        seen.add(ident)
        source = lookup[ident]
        file = source['file_path']
        if file not in blocks:
            blocks[file] = IlnkContainer.parse(clean.read_file(file)).blocks
        block = blocks[file][source['block']]
        raw = bytes.fromhex(source['source_hex'])
        at = source['source_reference']['offset']
        assert block[at:at + len(raw)] == raw and raw.decode('cp932') == source['source_Japanese']
        assert english.strip() == english and not any(x in english for x in ['\n','\t','  ','{','}','%'])
        assert english.encode('cp932').decode('cp932') == english
        rows.append({**source, **dict(english=english, logical_English=english, speaker='Hodram / player choice',
                     context=source['exchange_context'], localization_note=note,
                     review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False),
                     all_five_review_gates_pending=False, localized_caption_andnative_formatting_pending=True,
                     no_authored_ordinary_breaks_alignment_orpadding=True,
                     source_meaning_anddraft_precede_prior_English_comparison=True,
                     current_English_conversation_comparison_pending=True, current_reference_pending=True,
                     decision='source-first-draft-not-yet-compared', new_credit=0)})
    objects = {(r['file_path'],r['block'],r['source_command_offset']) for r in rows}
    for file, block, at in objects:
        assert {r['id'] for r in rows if (r['file_path'],r['block'],r['source_command_offset']) == (file,block,at)} == {r['id'] for r in meanings['records'] if (r['file_path'],r['block'],r['source_command_offset']) == (file,block,at)}
    save(args.out, dict(format='dk4-clean-first-logical-caption-drafts-v1', translation_policy='natural-dialogue-v2',
                        target_locale='en-US', review_gates=['source','context','localization','naturalness','formatting'],
                        records=rows, complete_choice_objects=len(objects), captions=len(rows),
                        native_layout_highlights_andstored_checks_pending=True, new_credit=0,
                        evidence={str(p):sha(p.read_bytes()) for p in [args.meanings,args.authored,source_objects,Path(__file__)]}))
    print(f'Saved{len(rows)} captions/{len(objects)} complete menus;exact source/CP932/logical prose pass;native formatting andcomparison remain open.')


if __name__ == '__main__':
    main()
