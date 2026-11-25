"""Keep complete phrases in the stored sailing alerts and verify the scoped change."""

from dataclasses import replace
from hashlib import sha256
import inspect
from pathlib import Path
import re
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.layout import format_markup
from dk4tool.patch import sea_event_static_wrap_v1 as wrap
from dk4tool.patch.sailing_alert_static_wrap_v1 import NEW_TABLES, transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import PROFILE
from scripts.preflight_diplomatic_outcome_wrap_v1 import preview_sheets
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_sailing_alert_review_v1 import ARM, BASE, COMMON, OUTPUT, RELEASE, crew_case
from scripts.stage_sailing_alert_review_v1 import PROOF as ORDINARY
from scripts.stage_sea_event_balanced_wrap_v2 import verify_scope as verify_sea_event_scope
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/sailing_alerts_20261111_v2')
ROM = ROOT / 'sailing_alerts_balanced_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_sailing_alert_balanced_verification.json'
PHRASES = {
    488: ("Admiral, we've got trouble!", "There's an epidemic!"),
    491: ("An epidemic's broken out!", "This'll be trouble."),
    493: ("Admiral, the wind's died.", "There's nothing we can do."),
    495: ("Oh, the wind's died...", "I guess we'll have to wait a while."),
    496: ("There's not a breath of wind.", "We're becalmed.", "Let's sit tight."),
    497: ("Tch. The wind's gone dead.", "Guess we'll have to wait."),
    498: ("...We're becalmed, Admiral.", "Nothing we can do without wind."),
    499: ("The wind's gone...", "Nothing we can do.", "Let's just", "take it easy while we wait."),
    500: ("is wait for it to pick up again.",),
    502: ("Watch out!",),
}


def verify_scope(arm):
    scoped = SimpleNamespace(**vars(wrap))
    scoped.TABLES = wrap.TABLES | {wrap.QUEUED: (*NEW_TABLES, *wrap.TABLES[wrap.QUEUED])}
    code = checked_text(inspect.getsource(verify_sea_event_scope), {
        '0x021187E0,': 'generic_table, 0x021187E0,',
        'assert selected == 13': 'assert selected == 16',
    })
    env = {**verify_sea_event_scope.__globals__, 'wrap': scoped, 'generic_table': 0x021187C0}
    exec(compile(code, __file__ + '::extended-queued-scope', 'exec'), env)
    return env['verify_scope'](arm)


def compile_breaks(rows):
    profile = replace(PROFILE, window_width_px=210)
    storage = {n: row['english'].encode('ascii') for n, row in rows.items()}
    for n, phrases in PHRASES.items():
        logical = rows[n]['english']
        text = logical
        assert '_' not in text and all(text.count(phrase) == 1 for phrase in phrases)
        for phrase in phrases:
            text = text.replace(phrase, phrase.replace(' ', '_'))
        lines = format_markup(text, profile).replace('_', ' ').split('{LB}')
        assert 2 <= len(lines) <= 3 and all(0 < len(line) <= 35 for line in lines)
        assert ' '.join(lines) == logical
        assert all(any(phrase in line for line in lines) for phrase in phrases)
        stored = (' ' + '\n  '.join(lines)).encode('ascii')
        assert not re.search(rb'%|F[AIOU]|IC', stored)
        storage[n] = stored
    return storage


def main():
    assert not ROOT.exists()
    source, ordinary, release = map(load, (OUTPUT, ORDINARY, RELEASE))
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert source['registered_input'] == ordinary['registered_input'] == runtime.receipt()
    assert ordinary['evidence'][str(OUTPUT)] == digest(OUTPUT)
    assert digest(ordinary['research_ROM']) == ordinary['research_ROM_sha256']
    assert all(digest(sheet['path']) == sheet['sha256'] for sheet in ordinary['crew_contact_sheets'])

    rows = {row['message_ID']: row for row in source['records']}
    storage = compile_breaks(rows)
    target_arm, owner = transform(runtime.arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(runtime.common, target_arm, rows, storage)
    assert len(packing['changed_visible_templates']) == 28 and packing['all_41_blocks_fit_8KiB']
    scope = verify_scope(arm)
    staged = with_components(runtime, arm, common)
    groups = {n: group for group in source['exact_native_crew_groups']
              for n in range(group['first_ID'], group['last_ID'] + 1)}
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    cases, changed, pages = [], [], []
    for old in ordinary['crew_cases']:
        n = old['message_ID']
        names = old['arguments']
        native = crew_case(staged, rows[n], groups[n], names[0].encode('ascii') if names else None)
        new_hex = native['formatted_hex']
        if n in PHRASES:
            assert new_hex == storage[n].hex() and new_hex != old['native']['formatted_hex']
            pixels, glyphs = render(raster, arm, kanji, storage[n])
            logical = rows[n]['english'].encode('ascii')
            assert glyphs[0]['code'] == logical[0] and glyphs[-1]['code'] == logical[-1]
            case = old | dict(native=native, glyphs=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest(),
                protected_phrases=PHRASES[n], previous_display_hex=old['native']['formatted_hex'],
                visible_lines=[line.strip() for line in storage[n].decode('ascii').split('\n')])
            changed.append(case)
            pages.append(pixels)
        else:
            assert new_hex == old['native']['formatted_hex']
            case = old | dict(native=native, unchanged_display_reuses_exact_ink=True)
        cases.append(case)
    assert len(cases) == 45 and len(changed) == len(PHRASES) == 10
    stored = []
    for n, row in rows.items():
        lookup = current_copy(staged, row | {'current_hex': storage[n].hex()}, BASE + 0x5528C)
        staged.calls.clear()
        stored.append(dict(message_ID=n, source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=reference(rebound[n]),
            staged_hex=storage[n].hex(), original_stored_lookup=lookup))
    assert next(r for r in stored if r['message_ID'] == 97)['staged_hex'] == (
        next(r for r in ordinary['stored'] if r['message_ID'] == 97)['staged_hex'])
    assert arm[0x7E2E8:0x7E5C4] == runtime.arm[0x7E2E8:0x7E5C4]

    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert sha256(image.rom.save()).hexdigest() == release['candidate_sha256']
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    assert NdsImage.open(ROM).read_file(COMMON) == common and NdsImage.open(ROM).read_file(ARM) == arm
    sheets = FunctionType(preview_sheets.__code__, {**preview_sheets.__globals__, 'ROOT': ROOT})
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        stored=stored, storage=packing, selector=owner, selector_scope=scope, complete_serialized_ROM_parent_inverse=True,
        crew_cases=cases, floating_expansions_inherited_from=str(ORDINARY), fresh_crew_contact_sheets=sheets(changed, pages),
        fresh_crew_pages=10, exact_crew_pages_reused=35, font=font, new_gameplay=False, new_credit=0,
        evidence={str(path): digest(path) for path in (OUTPUT, ORDINARY, Path(__file__))}))
    print(f"{len(stored)} stored templates, 45 portrait expansions and {scope['tested']} selector cases pass.")


if __name__ == '__main__':
    main()
