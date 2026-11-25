"""Bind all six captions in three complete original two-choice objects."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices, count_and_base
from scripts.audit_story_glyph_consistency import load, save

DOC = Path('translations/rafael_B85_B100_contextual_editorial_manuscript_v2.json')
ROOT = Path('work/analysis/Rafael261_choices_20261105')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc = load(DOC)
    rows = [deepcopy(r) for r in doc['records'] if r['kind'] == 'typed-choice-label']
    assert len(rows) == 6
    groups = {}
    for row in rows:
        assert row['source_choice_object_hex'] == row['source_command_hex']
        groups.setdefault((row['block'], row['source_command_offset']), []).append(row)
    assert set(groups) == {(85, 80), (88, 814), (91, 110)}
    ROOT.mkdir()
    inputs = []
    for (block, offset), items in groups.items():
        source, current = map(bytes.fromhex, [items[0]['source_choice_object_hex'], items[0]['current_choice_object_hex']])
        n, _ = count_and_base(source)
        assert n == len(items) == 2
        compiled = compile_choices(source, current, items, require_formatting=False)
        subset = deepcopy(doc)
        subset.update(records=items, blocks=[block], encoder='native-typed-choice-v2', physical_speech_objects=0,
            ordinary_speech_objects=0, FE_speech_objects=0, typed_choice_objects=2, typed_choice_commands=1,
            subset_of=str(DOC), subset_of_sha256=sha(DOC.read_bytes()))
        path = ROOT/f'B{block}_C{offset}_manuscript.json'
        save(path, subset)
        inputs.append(dict(block=block, source_command_offset=offset, labels=2, manuscript=str(path), manuscript_sha256=sha(path.read_bytes()),
            complete_source_object_hex=source.hex(), complete_current_object_hex=current.hex(), compiled_object_hex=compiled.hex(),
            target_bytes=len(compiled), max_caption_bytes=max(len(r['english']) for r in items)))
    save(ROOT/'source_bound_inputs.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), menus=inputs,
        native_choice_compiler_pass=True, provider_pixels_andactual_controller_pending=True, new_credit=0))
    print('Bound six captions inthree original two-choice objects;no speech controls or padding introduced.')
