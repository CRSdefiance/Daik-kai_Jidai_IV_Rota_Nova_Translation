"""Refine the emergency layouts after reviewing their first native contact sheets."""

from hashlib import sha256
import inspect
from pathlib import Path
from types import FunctionType

from dk4tool.patch import ship_emergency_wrap_v1 as wrap
from scripts import stage_ship_emergency_review_v1 as first
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/ship_emergency_20261111_v2')
ROM = ROOT / 'ship_emergency_balanced_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_ship_emergency_balanced_verification.json'
OUTPUT = first.OUTPUT.with_name('ship_emergency_contextual_review_v2.json')
RELEASE = first.RELEASE
STATIC = {(0x02053DB8, 0x27C): (0x02118620, 0x021185E0, 0x02118580), (0x02054014, 0x274): (609,)}
DYNAMIC = {(0x02053F40, 0x274): (0x02118600, 0x021185C0)}
PHRASES = first.PHRASES | {
    576: ("We're in trouble!", "This ship's taking on water!", 'Looks like the bottom', "of the hull's damaged."),
}
REVISIONS = {
    580: ("There's a leak aboard %s! The bottom of its hull looks damaged.",
          "Use the ship's name in the alarm and keep the likely damage as a separate, direct observation."),
    581: ("Admiral, they say %s has a leak! Think the hull's damaged underneath?",
          "Keep the secondhand report and the speaker's question about damage at the bottom of the hull."),
    582: ("Admiral, word is %s has sprung a leak! Must be damage to the bottom of its hull.",
          "Keep the rough speaker's hearsay and the inference that the bottom of the hull is damaged."),
}
BREAKS = {610: '. ', 611: '... ', 612: '. ', 613: '? '}


def prepare_review():
    source = load(first.OUTPUT)
    assert all(digest(path) == expected for path, expected in source['evidence'].items())
    for row in source['records']:
        n = row['message_ID']
        if n not in REVISIONS:
            continue
        english, note = REVISIONS[n]
        assert row['english'] != english and row['english'].count('%s') == english.count('%s') == 1
        row.update(first_pass_English=row['english'], english=english, localization_note=note)
    source['evidence'] |= {str(first.OUTPUT): digest(first.OUTPUT), str(Path(__file__)): digest(__file__)}
    if OUTPUT.exists():
        assert load(OUTPUT) == source
    else:
        save(OUTPUT, source)


def qualified_storage(rows, manuscript):
    strings = {n: row['english'].encode('ascii') for n, row in rows.items() if row['original_substitutions']}
    labels = [row['English'] for row in manuscript['arguments']['supplies']]
    both, activity = [row['English'] for row in manuscript['arguments']['automatic_travel_literals']]
    assert rows[587]['english'] == "It's all right. We put the fire out!"
    strings[587] = b" It's all right.\n  We put the fire out!"
    for n, delimiter in BREAKS.items():
        first_line, second_line = rows[n]['english'].rsplit(delimiter, 1)
        first_line += delimiter.rstrip()
        assert first_line.count('%s') == second_line.count('%s') == 1
        assert ' '.join((first_line, second_line)) == rows[n]['english']
        for supply in (*labels, both):
            assert 0 < len(first_line % supply) <= 35 and 0 < len(second_line % activity) <= 35
        strings[n] = (' ' + first_line + '\n  ' + second_line).encode('ascii')
    return strings


def verify_scope(arm):
    run = FunctionType(first.verify_scope.__code__, {**first.verify_scope.__globals__, 'DYNAMIC': DYNAMIC, 'STATIC': STATIC})
    scope = run(arm)
    assert scope['compiled_literal'] == 8 and scope['dynamic_paragraph'] == 10
    return scope


def main():
    assert not ROOT.exists()
    prepare_review()
    ordinary = load(first.PROOF)
    assert digest(first.ROM) == ordinary['research_ROM_sha256']
    assert all(digest(path) == expected for path, expected in ordinary['evidence'].items())
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in ordinary['contact_sheets'])
    reused = {bytes.fromhex(row['display_hex']): (row['native_ink_sha256'], row['complete_glyphs'])
              for row in ordinary['native_cases']}
    assembly = FunctionType(wrap.assembly.__code__, {**wrap.assembly.__globals__, 'DYNAMIC': DYNAMIC, 'STATIC': STATIC})
    transform = FunctionType(wrap.transform.__code__, {**wrap.transform.__globals__, 'assembly': assembly})
    source = checked_text(inspect.getsource(first.main), {
        "storage.update({n: row['english'].encode('ascii') for n, row in rows.items() if row['original_substitutions']})":
            'storage.update(qualified_storage(rows, review))',
        'assert display == storage[n], (n, display)':
            'assert display == (storage[n] % arguments if arguments else storage[n]), (n, display)',
        '            if display not in images:\n':
            '            if display in reused:\n                images[display] = reused[display]\n'
            '            if display not in images:\n',
        'rendered_unique_pages=len(pages), contact_sheets=':
            'rendered_unique_pages=len(pages), reused_exact_pages=len(images) - len(pages),'
            ' first_pass_proof=str(first.PROOF), contact_sheets=',
        '(OUTPUT, Path(__file__))': '(OUTPUT, first.PROOF, Path(__file__))',
    })
    env = {**vars(first), **globals(), 'transform': transform, 'reused': reused}
    exec(compile(source, __file__ + '::balanced-emergency-stage', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
