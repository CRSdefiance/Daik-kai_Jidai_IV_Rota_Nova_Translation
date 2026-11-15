"""Compile and verify the first source-bound shipyard and fleet setup batch."""

import inspect
from pathlib import Path

from dk4tool.patch.shipyard_fleet_setup_wrap_v1 import transform
from scripts import preflight_shipyard_fleet_setup_v1 as intake
from scripts import stage_setup_save_equipment_v1 as previous
from scripts.register_setup_save_equipment_v1 import RELEASE
from scripts.review_shipyard_fleet_setup_v1 import OUTPUT as MANUSCRIPT
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path('out/shipyard_fleet_setup_staged_20261111_v1')
ROM = ROOT / 'shipyard_fleet_setup_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PREFLIGHT = intake.PROOF
RETAIN_STORED = {264, 265, 266, 283, 285}
AMENDMENTS = {
    261: {
        'english': 'It seems people in %s who follow trends are talking about this news.',
        'localization_note': 'Report what people are talking about. Keep the city, the trend-following audience and the source uncertainty together in a single sentence.',
    },
    279: {
        'english': 'Appoint %s %s as admiral?',
        'localization_note': 'Use a direct appointment question with the given name and surname in order. The preceding selection identifies the new fleet.',
    },
}
PHRASE_STARTS = {
    269: 'you want to change.',
    271: 'to serve as captain.',
    274: 'and let a sailor take command?',
    275: 'to form a regional fleet.',
    277: 'to add to the new fleet.',
}


def active_rows(manuscript):
    return {row['message_ID']: row | AMENDMENTS.get(row['message_ID'], {}) for row in manuscript['records']}


def choose_storage(prepared, rows):
    planned = {case['message_ID']: case['storage_markup'] for case in prepared['current_modal_cases']
               if case.get('complete_glyphs_bounds_and_words')}
    for n in (261, 279):
        planned[n] = rows[n]['english']
    for n, phrase in PHRASE_STARTS.items():
        text = rows[n]['english']
        assert text.endswith(' ' + phrase)
        preceding = text[:-(len(phrase) + 1)]
        assert 0 < len(preceding) <= 36 and 0 < len(phrase) <= 35
        planned[n] = preceding + '{LB} ' + phrase
    return planned


def stage():
    original = inspect.getsource(previous.stage)
    selectors = """    planned = {case['message_ID']: case['storage_markup'] for case in prepared['modal_cases']
               if case.get('complete_glyphs_bounds_and_words')}
    planned[329] = rows[329]['english']
    planned[320] = '  ' + rows[320]['english']"""
    direct = """    direct = current_copy(clone, rows[320] | {'current_hex': storage[320].hex()}, 0x0205528C)
    clone.calls.clear()
    assert direct['copied_hex'] == storage[320].hex()

"""
    source = checked_text(original, {
        'def stage():': 'def build():',
        'preflight.RELEASE': 'RELEASE',
        'preflight.MANUSCRIPT': 'MANUSCRIPT',
        "    assert prepared['modal_layout_holds'] == [329]":
            "    assert set(prepared['dynamic_layout_holds']) == {'261', '279'}",
        "    rows = {row['message_ID']: row for row in manuscript['records'] if row['message_ID'] != 318}":
            '    rows = active_rows(manuscript)',
        'assert len(rows) == 14': 'assert len(rows) == 24',
        selectors: '    planned = choose_storage(prepared, rows)',
        "prepared['modal_cases']": "prepared['current_modal_cases']",
        "        plane, lines, origins, glyphs = preflight.render(raster, font, arm, bytes.fromhex(result['native_wrapper_output_hex']))":
            "        try:\n            plane, lines, origins, glyphs = preflight.render(raster, font, arm, bytes.fromhex(result['native_wrapper_output_hex']))\n"
            "        except AssertionError as error:\n            raise ValueError((n, args, result['native_wrapper_lines'])) from error",
        direct: "    assert all(call['target'] != 0x0205528C for row in rows.values() for call in row['native_callers'])\n\n",
        'rendered_variants=confirmed, direct_320_stored_copy=direct,':
            'rendered_variants=confirmed, editorial_amendments=AMENDMENTS,',
        'Staged {len(rows)} records, {len(pages)} complete modal variants and direct chooser copy. Research only.':
            'Staged {len(rows)} records and {len(pages)} complete modal variants. Research only.',
    })
    env = {**vars(previous), **globals(), '__file__': __file__, '__name__': 'shipyard_fleet_stored_stage'}
    exec(compile(source, __file__ + '::same-native-storage-and-inverse-workflow', 'exec'), env)
    env['build']()


if __name__ == '__main__':
    stage()
