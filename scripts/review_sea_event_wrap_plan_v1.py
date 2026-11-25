"""Preview balanced line breaks for sea-event phrases with awkward stock wraps."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import PROFILE
from scripts.preflight_diplomatic_outcome_wrap_v1 import preview_sheets
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, render
from scripts.probe_button_prompt_native import call
from scripts.stage_sea_event_review_v1 import BASE, EVIDENCE, OUTPUT, RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from dk4tool.dialogue.layout import format_markup


ROOT = Path('work/SharedText_20261110_v1/sea_event_wrap_plan_v1')
PROOF = ROOT / 'phrase_layout_proof.json'
DIRECT = 0x02132020
SOURCE, DEST = 0x0242C020, 0x0242D020
PROTECTED = {
    394: ("the crew has scurvy!",),
    399: ("got scurvy!",),
    401: ("we're overrun with rats!", "if we let this go on!",),
    405: ("Is the food safe?!",),
    407: ("Don't eat my food!",),
    408: ("the ship!",),
    409: ("just a moment ago...",),
    411: ("a minute ago...",),
    412: ("so clear...",),
    413: ("just so clear.",),
    414: ("just a moment ago?",),
    415: ("was just out...",),
    422: ("we won't be able to see.",),
    441: ("S-someone's swimming!",),
    443: ("S-someone's swimming!",),
    444: ("out there?",),
    446: ("S-someone's swimming!",),
    447: ("Somebody's swimming!",),
    448: ("Is someone swimming?!",),
    456: ("from the legends?",),
    461: ("suspicious bubbles",),
    462: ("weird bubbles",),
    468: ("the bubbles from the stories?",),
    476: ("the whole ship...",),
    478: ("All hands to your stations!",),
    480: ("Stay calm, everyone!", "To your stations!", "We'll steer clear!",),
}
RETAINED_BOUNDARIES = {
    396: 'The full report after the alarm needs 39 cells. The ordinary looks/like split keeps two substantial lines.',
    404: 'Help is a complete shouted appeal after the rat report, so its separate line suits the panic.',
    453: 'The ordinary legendary/mermaid boundary uses a fuller opening than the feasible alternative Could that be the. The complete creature name remains readable.',
    460: 'The surface description requires more than 35 cells. Holding Strange bubbles would add a third row ending in the water. Retain the fuller two-line plan.',
}


def main():
    assert not ROOT.exists()
    source, storage, release = map(load, (OUTPUT, EVIDENCE, RELEASE))
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert source['registered_input'] == storage['registered_input'] == runtime.receipt()
    assert storage['evidence'][str(OUTPUT)] == digest(OUTPUT)
    rows = {row['message_ID']: row for row in source['records']}
    previous = {row['message_ID']: row for row in storage['cases']}
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    cpu, _, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    pages, cases = [], []
    profile = replace(PROFILE, window_width_px=210)
    for number, phrases in PROTECTED.items():
        row = rows[number]
        old = previous[number]
        text = row['english']
        assert '_' not in text and all(text.count(phrase) == 1 for phrase in phrases)
        protected = text
        for phrase in phrases:
            protected = protected.replace(phrase, phrase.replace(' ', '_'))
        lines = format_markup(protected, profile).replace('_', ' ').split('{LB}')
        assert all(0 < len(line) <= 35 for line in lines)
        assert ' '.join(lines) == text and all(any(phrase in line for line in lines) for phrase in phrases)
        assert len(lines) == len(old['visible_lines']) + int(number == 480)
        display = (' ' + '\n  '.join(lines)).encode('ascii')
        assert display.hex() != old['display_hex']
        canaries = b'\xa5' * 16
        cpu.mem_write(SOURCE - 16, canaries + display + b'\0' + canaries)
        cpu.mem_write(DEST - 16, b'\xa5' * 288)
        call(cpu, DIRECT - BASE, (DEST, SOURCE, runtime.actor_root + 0x19E4, 0))
        assert bytes(cpu.mem_read(DEST, len(display) + 1)) == display + b'\0'
        assert bytes(cpu.mem_read(SOURCE - 16, len(display) + 33)) == canaries + display + b'\0' + canaries
        assert bytes(cpu.mem_read(DEST - 16, 16)) == bytes(cpu.mem_read(DEST + 256, 16)) == canaries
        pixels, glyphs = render(raster, runtime.arm, kanji, display)
        assert glyphs[0]['code'] == ord(text[0]) and glyphs[-1]['code'] == ord(text[-1])
        pages.append(pixels)
        cases.append(dict(message_ID=number, arguments=(), source_reference=row['source_reference'],
            current_reference=row['current_reference'], staged_reference=old['staged_reference'],
            staged_logical_English=text, protected_phrases=phrases, previous_display_hex=old['display_hex'],
            proposed_display_hex=display.hex(), lines=lines, ink_sha256=sha256(pixels).hexdigest()))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    ROOT.mkdir()
    sheets = FunctionType(preview_sheets.__code__, {**preview_sheets.__globals__, 'ROOT': ROOT})
    save(PROOF, dict(candidate_sha256=storage['research_ROM_sha256'], source_manifest=str(OUTPUT),
        old_storage_proof=str(EVIDENCE), complete_preview_count=len(cases), records=cases,
        contact_sheets=sheets(cases, pages), font=font, source_and_current_scope=storage['source_consumer_scopes'],
        ordinary_boundaries_retained=RETAINED_BOUNDARIES,
        original_literal_formatter_in_isolated_CPU=True, live_gameplay=False, new_ROM=False,
        stored_routing_and_registration_pending=True,
        evidence={str(path): digest(path) for path in (OUTPUT, EVIDENCE, Path(__file__))}))
    print(f'{len(cases)} alternative native layouts pass without changing a word.')


if __name__ == '__main__':
    main()
