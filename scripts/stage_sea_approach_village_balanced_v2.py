"""Refine the complete battle questions and static village line breaks."""

import inspect
import json
from pathlib import Path
from types import FunctionType

from scripts import stage_sea_approach_village_review_v1 as first
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/sea_approach_village_20261111_v2')
ROM = ROOT / first.ROM.name
PROOF = ROOT / first.PROOF.name
OUTPUT = first.OUTPUT.with_name('sea_approach_village_contextual_review_v2.json')
PHRASES = first.PHRASES | {
    1333: ("right at home. Everyone's pleased.",),
    1334: ("was delicious! Everyone's happy.",),
    1336: ('our ship repairs.',),
    1337: ('the fleet for us.',),
    1338: ('our ship repairs for us.',),
    1339: ('the ship repairs for us.',),
    1341: ('the fleet for us!',),
    1342: ('our ship repairs.',),
}
REVISIONS = {
    1300: ('Admiral! Ships from %s are fighting. Should we help them?',
           'Use a conversational question that clearly names the side to help and keeps the full question together.'),
    1302: ('Admiral! Ships from %s are in battle. Shall we help them?',
           'Keep the older voice measured and put the full offer of help together for all native faction labels.'),
    1304: ('Ships from %s are in battle. Shall we help them?',
           'Use a measured, natural question and retain the original lack of direct address.'),
    1353: ("The villagers helped us out, so we gave them %s in gold.",
           'Use the rough speaker\'s direct explanation of why the fleet gave the gold.'),
    1355: ('We gave the villagers %s in gold. Told them it was to say thanks!',
           'Use the young speaker\'s conversational follow-up and restore the spoken thanks.'),
}


def prepare_review():
    review = load(first.OUTPUT)
    assert all(digest(path) == expected for path, expected in review['evidence'].items())
    for row in review['records']:
        n = row['message_ID']
        if n in REVISIONS:
            english, note = REVISIONS[n]
            assert row['decision'] == 'revision' and row['english'].count('%s') == english.count('%s') == 1
            row.update(first_pass_English=row['english'], english=english, localization_note=note)
    review['evidence'] |= {str(path): digest(path) for path in (first.OUTPUT, first.PROOF, Path(__file__))}
    if OUTPUT.exists():
        assert load(OUTPUT) == review
    else:
        save(OUTPUT, review)


def main():
    assert not ROOT.exists()
    previous = load(first.PROOF)
    assert digest(first.ROM) == previous['research_ROM_sha256']
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in previous['contact_sheets'])
    prepare_review()
    visuals = {(row['message_ID'], row['argument']): row for row in previous['native_cases']}
    prior_stored = {row['message_ID']: bytes.fromhex(row['staged_hex']) for row in previous['stored']}
    prior_layouts = {(row['message_ID'], row['argument']): bytes.fromhex(row['display_hex'])
                     for row in previous['all_substitution_layouts']}
    compiler = FunctionType(first.compile_storage.__code__, {**first.compile_storage.__globals__, 'PHRASES': PHRASES})
    source = checked_text(inspect.getsource(first.main), {
        'display = expanded_layout(cpu, stored, group, argument) if argument else shown':
            'display = prior_layouts[n, label] if argument and stored == prior_stored[n] else ('
            'expanded_layout(cpu, stored, group, argument) if argument else shown)',
        'visible = [line.strip().decode(\'cp932\') for line in lines]':
            'visible = [line.strip().decode(\'cp932\') for line in lines]\n'
            "            if path['choice'] and label != 'long-label stress':\n"
            "                question = row['english'].rsplit('. ', 1)[-1].rsplit('! ', 1)[-1]\n"
            "                assert any(question in line for line in visible), (n, label, visible)",
        '                pixels, glyphs = render_portrait(raster, arm, kanji, display)':
            "                before = visuals.get((n, label))\n"
            "                if before and before['display_hex'] == display.hex():\n"
            "                    results.append(path | {k: before[k] for k in ('message_ID', 'argument', 'display_hex',\n"
            "                        'visible_lines', 'native_ink_sha256', 'complete_glyphs')} | {'exact_view_reused': True})\n"
            "                    images.add(display)\n"
            "                    continue\n"
            '                pixels, glyphs = render_portrait(raster, arm, kanji, display)',
        '    assert len(lookups) == len(rows) == 67':
            "    assert len(lookups) == len(rows) == 67\n"
            "    assert all(row['argument'] == 'long-label stress' for row in findings)\n"
            "    assert json.loads(json.dumps(selector)) == previous['selector'] and scope == previous['selector_scope']\n"
            "    assert font == previous['font']",
        'font=font, complete_serialized_ROM_parent_inverse=True':
            "font=font, reused_exact_viewed_pages=sum(case.get('exact_view_reused', False) for case in results),\n"
            "        first_pass_proof=str(first.PROOF), all_actual_faction_questions_stay_together=True,\n"
            "        complete_serialized_ROM_parent_inverse=True",
    })
    env = {**vars(first), **globals(), 'compile_storage': compiler, 'previous': previous,
        'prior_stored': prior_stored, 'prior_layouts': prior_layouts, 'visuals': visuals}
    exec(compile(source, __file__ + '::balanced-sea-approach-stage', 'exec'), env)
    env['main']()


if __name__ == '__main__':
    main()
