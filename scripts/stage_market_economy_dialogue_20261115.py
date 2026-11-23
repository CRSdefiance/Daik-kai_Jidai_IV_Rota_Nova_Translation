"""Review the four alternatives when opening the Market."""

from pathlib import Path
from types import FunctionType

from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R6

from scripts import register_setup_confirmation_prose_20261115 as parent
from scripts.probe_button_prompt_native import BASE
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES, RegisteredRuntime,
    common_message_entries, compile_layouts, digest, files, font_tools, native_layout,
    owned_deployment, owned_entries, portrait_sheets, reference, render_portrait, with_components,
)


base = parent.base
ROOT = Path('work/market_economy_dialogue_20261115_v1')
ROM, STORED = ROOT / 'Market_Economy_Dialogue_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/market_economy_dialogue_20261115_v1.json')
DECISIONS = {
    8: (None, 'The trader asks what the customer wants.',
        'Need help? fits the brisk greeting as the player enters the Market.'),
    771: (None,
          'The trader wants the war to end soon because it hampers business.',
          'Keep both existing sentences. They preserve the wish and its reason in the voice of a frustrated trader.'),
    772: ("The economy's picked up lately. Business is getting easier.",
          'The local economy has improved recently, making it easier to do business.',
          'Lead with the change the trader has noticed, then give the consequence in a separate spoken beat.'),
    773: ("The economy's turned sour lately. Doing business is a real struggle.",
          'The economy has gotten worse lately, and the trader complains that doing business is very difficult.',
          'Turned sour gives the trader a natural way to describe the downturn. Keep the existing real struggle for the consequence.'),
}
PHRASES = {772: ('Business is getting easier.',), 773: ('Doing business is a real struggle.',)}
SELECTOR = ((0, 771), (1, 8), (2, 8), (3, 772), (4, 773), (5, 8), (0xFFFFFFFF, 8))


def encoded_changes():
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES})
    return compiler({n: {'english': DECISIONS[n][0]} for n in PHRASES})


def market_choices(cpu, clean, arm):
    spans = ((0xBA340, 0xBA380), (0xBA470, 0xBA480))
    assert all(clean[a:b] == arm[a:b] for a, b in spans)
    cases = []
    for state, message in SELECTOR:
        cpu.reg_write(UC_ARM_REG_R0, state)
        cpu.reg_write(UC_ARM_REG_R6, 0)
        cpu.emu_start(BASE + 0xBA354, BASE + 0xBA37C, count=16)
        assert cpu.reg_read(UC_ARM_REG_R1) == message
        cases.append(dict(supplied_economy_result=state, message_ID=message))
    return dict(selector=BASE + 0xBA354, call=BASE + 0xBA37C, cases=cases,
                spans=[dict(start=a, end=b, sha256=digest(arm[a:b])) for a, b in spans])


def main():
    assert not any(path.exists() for path in (ROM, STORED, MANUSCRIPT))
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    source_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    arm, common = ctx.arm, ctx.common
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    credited = {r['id'] for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']
                if r['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in DECISIONS)
    edited = encoded_changes()
    deployed, installed, slots = owned_deployment(common, arm, old, edited)
    updated = with_components(ctx, arm, deployed)
    cpu, get, provider = updated.machine(arm, deployed, updated.raw, updated.plan)
    bindings = market_choices(cpu, source_arm, arm)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    records, pages, native_cases = [], [], []
    for n, (replacement, meaning, note) in DECISIONS.items():
        s, a, b = source[n], old[n], installed[n]
        assert b'%' not in s.text + a.text + b.text
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(b.text) + 1)) == b.text + b'\0'
        before_bytes, before = native_layout(cpu, a.text, n, ())
        after_bytes, after = native_layout(cpu, b.text, n, ())
        english = replacement or ' '.join(a.text.decode('ascii').split())
        assert ' '.join(after) == english and all(after)
        if replacement:
            assert a.text != b.text and before != after
            assert all(any(word_group in line for line in after) for word_group in PHRASES[n])
            for label, body in (('before', before_bytes), ('after', after_bytes)):
                plane, _ = render_portrait(raster, arm, kanji, body)
                pages.append((f'{n} {label}', plane))
            assert len(after) <= 3
        native_cases.append(dict(message_ID=n, before=before, after=after, formatted_hex=after_bytes.hex()))
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, speaker='Trader', file_path=COMMON,
            context='One of four opening replies at the Market. The original selector uses the local economic state before the player chooses a service.',
            source_meaning=meaning, localization_note=note, Japanese=s.text.decode('cp932'), english=english,
            decision='revision' if n in (772, 773) else 'retention', reflow=n in edited,
            source_reference=reference(s), current_reference=reference(a), staged_reference=reference(b),
            source_hex=s.text.hex(), current_hex=a.text.hex(), staged_hex=b.text.hex(), native_lines=after,
            review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(COMMON, deployed)
    after = files(image)
    assert before.keys() == after.keys() and {name for name in before if before[name] != after[name]} == {COMMON}
    ROOT.mkdir(parents=True, exist_ok=True)
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    sheets = portrait_sheets(ROOT, pages)
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), records=records, native_bindings=bindings,
        candidate_sha256=candidate, previous_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256']))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(deployed), allocations=slots,
        whole_parent_inverse=True, native_cases=native_cases, sheets=sheets, font=font,
        manuscript_sha256=base.digest(MANUSCRIPT)))
    print('Reviewed four Market opening replies and staged two revisions.')


if __name__ == '__main__':
    main()
