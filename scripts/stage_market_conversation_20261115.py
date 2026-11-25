"""Review the Market purchase, bargaining, and price-viewing messages together."""

from hashlib import sha256
from pathlib import Path
from struct import unpack_from
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_R1, UC_ARM_REG_R6, UC_ARM_REG_SP

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_ship_class_names_20261115 as parent
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_expedition_report_wraps_20261115 import owned_deployment
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_sheets, render_portrait
from scripts.verify_release_baseline import files


base = parent.base
ROOT = Path('work/market_conversation_20261115_v2')
ARM, CLEAN = parent.stage.ARM, parent.stage.CLEAN
COMMON = '/COMMON/MESFILE.DK4'
ROM, STORED = ROOT / 'Market_Conversation_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/market_conversation_20261115_v2.json')
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
REVISIONS = {
    10: "All right. I'll cut you a break.",
    18: "There's a fee for each price check. Which town did you have in mind?",
    19: 'Could you do a bit better?',
    20: 'Can you do any better?',
    24: 'Sorry to trouble you, but could you do a bit better?',
}
PHRASES = {18: ('Which town did you have in mind?',), 24: ('do a bit better',)}
NOTES = {
    8: ('The trader asks what the customer needs.', 'Need help? fits the trader’s brisk greeting before the player chooses a service.'),
    9: ('The trader thanks the customer and asks for their continued business.', 'Thanks! Come again. preserves the warmth of the farewell after an ordinary completed trade.'),
    10: ('The trader reluctantly agrees to a small concession.', 'All right signals that the trader has yielded. Cut you a break works for ordinary bargaining on either side of the deal.'),
    11: ('The crew member politely asks if this is acceptable.', 'Will this be all right? retains the deferential yes/no question.'),
    12: ('The crew member casually checks if this is okay.', 'This okay? sounds natural as a short check with the player.'),
    13: ('The crew member politely asks if this is okay.', 'Is this okay? is conversational and slightly more formal than This okay?'),
    14: ('The crew member directly checks that the player is satisfied.', 'Good with this? keeps the direct tone heard over the existing pending Trade recap.'),
    15: ('The crew member asks whether this will suffice.', 'Will this do? preserves the slightly more formal expression and the same player decision.'),
    16: ('The crew member draws out a familiar question asking if this is good.', 'This good? keeps the voice playful and easygoing without adding a written sound to the one-line choice.'),
    17: ('The crew member courteously asks if this looks all right.', 'Does this look all right? gives this more deliberate voice a complete question.'),
    18: ('Checking prices costs a fee each time. The trader asks which town the customer wishes to check.', 'Put the per-check fee and town question on separate complete lines. The town question follows without repeating prices.'),
    19: ('The crew member politely asks for a slightly better price.', 'Do a bit better is a polite, idiomatic request about the price the trader just quoted.'),
    20: ('The crew member directly asks the trader for a more favorable price.', 'Do any better sounds like bargaining with a merchant. The subject remains the quoted amount.'),
    21: ('The crew member informally asks if the trader can do a little better on price.', 'Think you could do a little better on the price? keeps the speaker’s casual opening and measured request.'),
    22: ('The crew member familiarly asks the trader to consider a better price.', 'Couldn’t you give me a better price? preserves the familiar appeal and keeps the price explicit.'),
    23: ('The crew member bluntly asks if the trader can do better.', 'Can you do better than that? is a natural challenge to the amount on screen and preserves this voice’s directness.'),
    24: ('The crew member apologizes for asking and requests a modest improvement in the price.', 'Sorry to trouble you preserves this more courteous opening. Do a bit better refers clearly to the price on screen and stays together on the second line.'),
    25: ('The crew member presses the trader for a small concession.', 'Come on and the exclamation mark keep the lively urgency of this voice.'),
    26: ('The crew member courteously asks the trader to reconsider the amount.', 'Could you perhaps offer a better price? is deliberately restrained and courteous.'),
}
TABLES = {0x118AA0: (11, 0xFFFFFFFF, 12, 13, 14, 15, 16, 17), 0x118A80: tuple(range(19, 27))}
LOCKS = ((0x53CB0, 0x53DCC), (0x53F4C, 0x53F9C), (0x1DD38, 0x1DD54), (0xBA340, 0xBA380),
         (0xBAF04, 0xBAF2C), (0xBB448, 0xBB454), (0xBBAD0, 0xBBAE4), (0xBC0BC, 0xBC0DC),
         (0xBC25C, 0xBC270), (0x118A80, 0x118AC0))


def digest(raw):
    return sha256(raw).hexdigest()


def encoded_changes():
    compile_market = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES})
    return compile_market({n: {'english': text} for n, text in REVISIONS.items()})


def original_choices(ctx, clean):
    arm = ctx.arm
    assert all(arm[start:end] == clean[start:end] for start, end in LOCKS)
    assert unpack_from('<I', arm, 0xBC25C) == (BASE + 0x118AA0,)
    assert unpack_from('<I', arm, 0xBC26C) == (BASE + 0x118A80,)
    cpu, get, provider = ctx.machine(arm, ctx.common, ctx.raw, ctx.plan)
    voices = {}
    for index in range(207):
        actor = ctx.actor_root + 4 + 32 * index
        voice = get(0x7E988, actor)
        if voice in range(8):
            voices.setdefault(voice, (index, actor))
    assert set(voices) == set(range(8)), voices
    tables = []
    for table, expected in TABLES.items():
        assert unpack_from('<8I', arm, table) == expected
        for voice, (index, actor) in sorted(voices.items()):
            n = get(0x53F4C, actor, BASE + table)
            requested = expected[voice]
            assert n == (requested if requested != 0xFFFFFFFF else expected[0])
            tables.append(dict(table=table, voice=voice, actor_ID=index, message_ID=n))
    concessions = []
    for discounted, n in ((0, 9), (1, 10)):
        cpu.mem_write(STACK, bytes(0x20))
        cpu.mem_write(STACK + 0x10, discounted.to_bytes(4, 'little'))
        cpu.reg_write(UC_ARM_REG_SP, STACK)
        cpu.reg_write(UC_ARM_REG_R6, 0)
        cpu.emu_start(BASE + 0xBC0BC, BASE + 0xBC0D8, count=16)
        assert cpu.reg_read(UC_ARM_REG_R1) == n
        concessions.append(dict(supplied_trade_branch=discounted, message_ID=n))
    assert not provider.reads and not provider.opens
    return dict(voice_selections=tables, concession_branches=concessions,
        original_code_locks=[dict(start=a, end=b, sha256=digest(arm[a:b])) for a, b in LOCKS])


def context(n):
    if n in {8, 9, 10}:
        return 'Trader', 'Market entry, ordinary sale farewell, or the concession following successful bargaining.'
    if n == 18:
        return 'Trader', 'The player opens the Price Info service. The trader explains the fee before the town selector opens.'
    if n < 18:
        return 'Crew member', 'One voice-selected confirmation over a pending action. The same original table is shared by Trade and another confirmation caller.'
    return 'Crew member', 'One voice-selected bargaining request over the amount already on screen. The original merchant response follows.'


def main():
    assert not any(p.exists() for p in (MANUSCRIPT, STORED, ROM))
    ROOT.mkdir(parents=True, exist_ok=True)
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    source_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    arm, common = ctx.arm, ctx.common
    bindings = original_choices(ctx, source_arm)
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    credited = {r['id'] for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys'] if r['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NOTES)
    edited = encoded_changes()
    target, installed, slots = owned_deployment(common, arm, old, edited)
    updated = with_components(ctx, arm, target)
    cpu, get, provider = updated.machine(arm, target, updated.raw, updated.plan)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    records, changed, pages = [], [], []
    for n, (meaning, note) in NOTES.items():
        s, a, b = source[n], old[n], installed[n]
        assert b'%' not in s.text + a.text + b.text
        address = get(0x5528C, n)
        assert bytes(cpu.mem_read(address, len(b.text) + 1)) == b.text + b'\0'
        consumer = 0x02054014 if n in {8, 9, 10, 18} else 0x02053D24 if n < 18 else 0x02053DB8
        old_body, before = native_layout(cpu, a.text, n, (), parent=consumer)
        body, after = native_layout(cpu, b.text, n, (), parent=consumer)
        assert 1 <= len(after) <= 3 and all(after)
        if n in edited:
            assert before != after and all(any(phrase in line for line in after) for phrase in PHRASES.get(n, ())), (n, after)
            old_plane, _ = render_portrait(raster, arm, kanji, old_body)
            plane, _ = render_portrait(raster, arm, kanji, body)
            pages.extend(((f'{n} before', old_plane), (f'{n} after', plane)))
            changed.append(dict(n=n, before=before, after=after, native_output_hex=body.hex(), native_plane_sha256=digest(plane)))
        speaker, situation = context(n)
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, speaker=speaker, context=situation,
            source_meaning=meaning, localization_note=note, Japanese=s.text.decode('cp932'),
            english=REVISIONS.get(n, ' '.join(a.text.decode('ascii').split())), decision='revision' if n in edited else 'retention',
            source_reference=reference(s), current_reference=reference(a), staged_reference=reference(b), file_path=COMMON,
            source_hex=s.text.hex(), current_hex=a.text.hex(), staged_hex=b.text.hex(), native_consumer=consumer,
            native_lines=after, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(COMMON, target)
    after = files(image)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    sheets = portrait_sheets(ROOT, pages)
    draft = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(GATES), records=records, native_bindings=bindings, candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'])
    base.save(MANUSCRIPT, draft)
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'], target_ARM9_sha256=digest(arm),
        target_COMMON_sha256=digest(target), allocations=slots, whole_parent_inverse=True, native_cases=changed,
        sheets=sheets, font=font, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'Reviewed {len(records)} Market records and rendered {len(changed)} revised pages with native checks.')


if __name__ == '__main__':
    main()
