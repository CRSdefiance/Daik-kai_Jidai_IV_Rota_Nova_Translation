"""Preserve every source distinction while resolving three failed prose plans."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_phrase_flow_v4227')
INPUT = Path('translations/lil_B169_editorial_manuscript_v1.json')
OUTPUT = Path('translations/lil_B169_editorial_manuscript_v2.json')
OLD = Path('dk4tool/dialogue/lil_B169_layout_v1.py')
NEW = Path('dk4tool/dialogue/lil_B169_layout_v2.py')
CHANGES = {
    32: ("You're throwing me off... Mikhail... I mean, Mikhail Letzel, the great naturalist! About the Proof of Conquest...",
         'The complete exchange supplies Mikhail as the cause of Camille\'s fluster. The idiomatic opening preserves the disrupted train of thought, initial Mikhail address, self-correction, exact spoken full name, flattering naturalist address and unfinished Proof question. No degree or rank is invented.'),
    41: ("They're treasures scattered across the seas. Those who rule the seas are said to claim them. Much remains a mystery...",
         'Move the hearsay construction around the same sea-ruler claim. Preserve scattered treasures, seas, reported rather than asserted entitlement and continuing mystery; add no numerical requirement, military-only rule or immediate award.'),
    167: ("Life is all give-and-take. It's a small price compared with the value of the treasure we're after.",
          'The idiomatic maxim preserves the all-encompassing give-and-take claim. Keep the relative value comparison and shared we treasure search; no price, gift or particular exchange is supplied.'),
}

if __name__ == '__main__':
    assert not ROOT.exists() and not OUTPUT.exists() and not NEW.exists()
    doc = deepcopy(read(INPUT))
    source = OLD.read_text(encoding='utf-8')
    pairs = [('about','the'), ('much','remains'), ('touch','me'), ('talk','sense'), ('collecting','all'), ('all','those'), ('be','useful'), ('small','price')]
    insertion = '\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset(' + repr(pairs) + ')\n'
    assert source.count('\ndef _word(value):') == 1
    NEW.write_text(source.replace('\ndef _word(value):', insertion + '\ndef _word(value):'), encoding='utf-8', newline='\n')
    changes = []
    for row in doc['records']:
        index = row['source_record_index']
        if index not in CHANGES:
            continue
        body, reason = CHANGES[index]
        previous = row['english']
        row['english'] = previous.split('}', 1)[0] + '}' + body
        row['localization_note'] += ' Phrase-flow refinement: ' + reason
        row['phrase_flow_previous_english'] = previous
        row['phrase_flow_refinement_reason'] = reason
        assert row['editorial_decision'] == 'revise' and not row['review']['formatting']
        assert not any(token in body for token in ['{LB','{PAD','{ALIGN','\n','  '])
        changes.append(dict(id=row['id'],source_hex=row['source_hex'],source_meaning=row['source_meaning'],previous=previous,english=row['english'],reason=reason))
    assert len(changes) == 3
    doc.update(previous_manuscript=str(INPUT), previous_manuscript_sha256=sha(INPUT.read_bytes()),
               phrase_flow_formatter=str(NEW), phrase_flow_formatter_sha256=sha(NEW.read_bytes()))
    ROOT.mkdir(parents=True)
    save(OUTPUT, doc)
    save(ROOT / 'three_meaning_preserving_refinements_and_additional_phrase_boundaries.json', dict(
        manuscript=str(OUTPUT), manuscript_sha256=sha(OUTPUT.read_bytes()), changes=changes,
        old_formatter=str(OLD), old_formatter_sha256=sha(OLD.read_bytes()),
        new_formatter=str(NEW), new_formatter_sha256=sha(NEW.read_bytes()), additional_protected_pairs=pairs,
        all36_decisions_and17_justified_retentions_preserved=True,
        no_weak_ending_protected_name_or_native_guard_waiver=True,
        source_controls_macros_meanings_all_retained=True, new_emulator_runs=0,
        source_prose_or_completion_credit_added=0, full_goal_complete=False,
        producer_sha256=sha(Path(__file__).read_bytes())))
    # Preserve both earlier producers and the failed complete layout proof.
    plan = Path('scripts/plan_lil_B169_layout_v4224.py').read_text(encoding='utf-8')
    plan = plan.replace('lil_B169_layout_v1','lil_B169_layout_v2').replace('lil_B169_layout_v4224','lil_B169_layout_v4228')
    plan = plan.replace("INPUT=Path('translations/lil_B169_editorial_manuscript_v1.json')", "INPUT=Path('translations/lil_B169_editorial_manuscript_v2.json')")
    plan = plan.replace("OUTPUT=Path('translations/lil_B169_editorial_manuscript_v2.json')", "OUTPUT=Path('translations/lil_B169_editorial_manuscript_v3.json')")
    planned = Path('scripts/plan_lil_B169_layout_v4228.py')
    assert not planned.exists()
    planned.write_text(plan, encoding='utf-8', newline='\n')
    native = Path('scripts/verify_lil_B169_fonts_v4225.py').read_text(encoding='utf-8')
    native = native.replace('lil_B169_layout_v1','lil_B169_layout_v2').replace('lil_B169_fonts_v4225','lil_B169_fonts_v4229').replace('lil_B169_editorial_manuscript_v2.json','lil_B169_editorial_manuscript_v3.json')
    proof = Path('scripts/verify_lil_B169_fonts_v4229.py')
    assert not proof.exists()
    proof.write_text(native, encoding='utf-8', newline='\n')
    print('Three full-meaning refinements and eight stronger phrase boundaries; all36 decisions preserved, no credit.')
