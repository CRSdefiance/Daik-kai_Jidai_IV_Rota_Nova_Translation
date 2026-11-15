"""Bind Sera's room responses to clean source and stage their native layouts."""

from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.register_sea_approach_village_review_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.research_battle_declaration_context_v991c import name, ptr, text
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT as MANUSCRIPTS, reference
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case, portrait_sheets, render_portrait
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/sera_assignment_20261111_v1')
ROM = ROOT / 'sera_assignment_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_sera_assignment_verification.json'
OUTPUT = MANUSCRIPTS / 'sera_assignment_contextual_review.json'
IDS = (1357, 1358, 1359, 1360)
ACTOR = 24
FLAGS = 0x02276F90
SPANS = ((0x13450, 0x13720), (0x15DE4, 0x15ED0), (0x23C60, 0x23CE4), (0x53FE4, 0x54058))
DATA = {
    1357: ("料理、私すごく得意\nきっと、おいしい", "I'm a really good cook. It'll taste great.",
        'Sera says she is very good at cooking and is confident the food will taste good.',
        'The player selects Sera for the Galley. The original eligibility checks pass and Sera responds before the assignment is written.',
        "Use Sera's plain, confident voice. Keep the second sentence prospective and use ordinary ASCII for both leading I glyphs."),
    1358: ("私に、部屋くれる…？\nうれしい♪", "A room for me...? I'm so happy!",
        'Sera asks if she is being given a room and expresses her delight.',
        'The player selects Sera for a Cabin. The original eligibility checks pass. She hesitates in pleased surprise before accepting the room.',
        "Keep the tentative question and Sera's simple delight. The punctuation carries the original musical tone."),
    1359: ("私、それムリ…\nごめんなさい…", None,
        'Sera says she cannot take on the selected duty and apologizes.',
        'The selected room is outside her eligible duties, and her language flag is set. Sera apologizes and the original handler returns to room selection.',
        'The existing clipped response conveys both the inability and the apology. It fits her direct, hesitant speech in this branch.'),
    1360: ("…。（コトバ、よくわからない。）", "... (I don't understand the language very well.)",
        'After a silence, Sera thinks that she does not understand the language well.',
        'The player tries assigning Sera before the original language flag is set. The assignment fails. Sera pauses and her thought appears in parentheses.',
        'Retain the silence and parenthetical thought. Keep the source qualification very well and use ordinary ASCII I. The source leaves the language unnamed.'),
}
PHRASES = {1357: ("I'm a really good cook.", "It'll taste great."), 1360: ('the language very well.)',)}


def clean_contract(clean, arm, runtime):
    for lo, hi in SPANS:
        assert clean[lo:hi] == arm[lo:hi], hex(lo)
    assert branch_target(clean, 0x1351C) == branch_target(clean, 0x13668) == 0x02053FE4
    assert [word(clean, p) for p in (0x136F4, 0x136F8, 0x13708, 0x13664)] == [1357, 1358, 1359, 0x03A01E55]
    assert word(clean, 0x13704) == FLAGS and word(clean, 0x15ECC) == FLAGS
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    actor = runtime.actor_root + 4 + ACTOR * 32
    identity = name(cpu, get, actor)
    assert identity['name'] == 'Sera'
    rooms = {n: text(cpu, ptr(cpu, get(0x7B3C, n))).decode('cp932') for n in (2, 12, 15)}
    assert rooms == {2: 'Deck', 12: 'Cabin', 15: 'Galley'}
    original = bytes(cpu.mem_read(FLAGS + 4, 4))
    matrix = []
    for flag in (0, 1):
        get(0x23C8C, FLAGS, 2, flag)
        assert get(0x23C60, FLAGS, 2) == flag * 4
        for room, label in rooms.items():
            result = get(0x15DE4, ACTOR, room)
            assert result == int(flag and room in (12, 15))
            matrix.append(dict(language_bit=flag, room=room, label=label, original_eligibility=result))
    cpu.mem_write(FLAGS + 4, original)
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return dict(actor_ID=ACTOR, actor=identity, room_labels=rooms, native_eligibility=matrix,
        clean_current_callers=[0x0201351C, 0x02013668], consumer=0x02053FE4,
        language_flag_object=FLAGS, language_flag_bit=2,
        clean_current_spans=[dict(start=BASE + lo, stop=BASE + hi, sha256=sha256(arm[lo:hi]).hexdigest()) for lo, hi in SPANS])


def rebuild_components(arm, common, rows, storage):
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    target_common, target_arm, rebound, packing = repack(common, arm, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    assert packing['changed_visible_templates'] == [1357, 1358, 1360]
    assert target_arm[:DIRECTORY_OFFSET] == arm[:DIRECTORY_OFFSET]
    assert target_arm[TABLE_END:] == arm[TABLE_END:]
    return target_arm, target_common, rebound, packing


def main():
    assert not ROOT.exists() and not OUTPUT.exists()
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    assert digest(CLEAN) == release['clean_input_sha256']
    clean = NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = load('translations/editorial_review_current_v1.json')
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {row['id'] for row in ledger['contextual_story_natural_dialogue_pass_v1871']['integrated_record_keys']
                if row['file_path'] == COMMON}
    assert not {f'COMMON_MESSAGE_{n}' for n in IDS} & credited
    del ledger
    contract = clean_contract(clean_arm, runtime.arm, runtime)
    rows = {}
    for n, (source_text, revision, meaning, context, note) in DATA.items():
        jp, old = source[n], current[n]
        assert source_text == jp.text.decode('cp932')
        before = old.text.decode('cp932')
        english = revision or before
        assert english.isascii() and english == ' '.join(english.split())
        assert (english != before) == bool(revision)
        assert b'%s' not in jp.text and '%' not in english
        row = dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON, source_reference=reference(jp),
            current_reference=reference(old), source_hex=jp.text.hex(), current_hex=old.text.hex(),
            source_Japanese=source_text, current_English=before, english=english, source_meaning=meaning,
            context=context, speaker='Sera', actor_ID=ACTOR, original_substitutions=[],
            localization_note=note, decision='revision' if revision else 'retention',
            review={gate: gate != 'formatting' for gate in GATES})
        row['original_current_native_lookup'] = current_copy(runtime, row, BASE + 0x5528C)
        runtime.calls.clear()
        rows[n] = row
    compiler = FunctionType(compile_layouts.__code__, {**compile_layouts.__globals__, 'PHRASES': PHRASES})
    storage = compiler(rows)
    arm, common, rebound, packing = rebuild_components(runtime.arm, runtime.common, rows, storage)
    staged = with_components(runtime, arm, common)
    raster, _, font = font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    lookups, cases, pages = [], [], []
    for n, row in rows.items():
        stored = storage[n]
        looked_up = current_copy(staged, row | {'current_hex': stored.hex()}, BASE + 0x5528C)
        staged.calls.clear()
        lookups.append(dict(message_ID=n, source_reference=row['source_reference'], current_reference=row['current_reference'],
            staged_reference=reference(rebound[n]), staged_hex=stored.hex(), original_stored_lookup=looked_up))
        native = portrait_case(staged, row, dict(consumer=0x02053FE4, table=n, original_role_argument=None), stored, ACTOR)
        display = native.pop('display')
        assert display == stored and b' '.join(display.split()).decode('ascii') == row['english']
        lines = [line.strip() for line in display.decode('ascii').split('\n')]
        assert 1 <= len(lines) <= 2
        assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(n, ()))
        pixels, glyphs = render_portrait(raster, arm, kanji, display)
        assert glyphs[0]['code'] == ord(row['english'][0]) and glyphs[-1]['code'] == ord(row['english'][-1])
        assert sum(item['code'] == ord('I') for item in glyphs) == row['english'].count('I')
        pages.append((n, pixels))
        cases.append(native | dict(message_ID=n, visible_lines=lines, display_hex=display.hex(),
            native_ink_sha256=sha256(pixels).hexdigest(), complete_glyphs=len(glyphs)))
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    assert NdsImage.open(ROM).read_file(ARM) == arm and NdsImage.open(ROM).read_file(COMMON) == common
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, records=list(rows.values()),
        registered_input=runtime.receipt(), source_ROM=str(CLEAN), source_ROM_sha256=release['clean_input_sha256'],
        native_context=contract, counts={'revision': 3, 'retention': 1}, formatting_pending=True,
        registered_release_pending=True, new_gameplay=False, new_credit=0, full_goal_complete=False))
    save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        target_ARM9_sha256=sha256(arm).hexdigest(), target_COMMON_sha256=sha256(common).hexdigest(),
        stored=lookups, storage=packing, selector=dict(original_portrait_selector_unchanged=True,
            ARM9_changes_limited_to_COMMON_offsets=True), native_cases=cases, contact_sheets=portrait_sheets(ROOT, pages),
        font=font, complete_serialized_ROM_parent_inverse=True, actual_gameplay=False, new_credit=0,
        evidence={str(path): digest(path) for path in (OUTPUT, RELEASE, Path(__file__))}))
    print('Four stored records and native pages passed, with the original renderer and assignment code intact.')


if __name__ == '__main__':
    main()
