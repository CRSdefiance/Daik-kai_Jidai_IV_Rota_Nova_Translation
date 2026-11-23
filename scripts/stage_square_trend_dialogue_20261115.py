"""Review the eight original Square trade-trend alternatives and stage the revisions."""

from pathlib import Path
from struct import unpack

from dk4tool.patch.town_responses_editorial import compile_template
from scripts import register_seoul_recruitment_20261115 as parent
from scripts.probe_shipyard_runtime_v759 import layout
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES,
    RegisteredRuntime, common_message_entries, digest, files, font_tools,
    owned_deployment, owned_entries, portrait_sheets, reference, render_portrait,
    with_components,
)
from scripts.probe_button_prompt_native import BASE
from scripts.verify_category_lookup_v754 import getter, string


base = parent.base
ROOT = Path('work/square_trend_dialogue_20261115_v1')
ROM, STORED = ROOT / 'Square_Trend_Dialogue_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/square_trend_dialogue_20261115_v1.json')
TOWN_PROOF = Path('translations/editorial_checkpoints/SharedText_20261110_v1/regional_town_dialogue_20261115_v1.json')

REVISIONS = {
    653: 'Sales of %s are sky-high!',
    654: 'Brought %s? Sell your stock at the Market soon!',
    655: "Let's sell %s and make a bundle!",
    732: 'This trend may last quite a while.',
    733: "The %s craze... I wonder if it's almost over.",
}
NOTES = {
    653: ('The named good is selling extremely well right now.',
          'The brisk sales boast keeps the enthusiasm. Number-neutral wording avoids splitting the old hotcakes idiom and keeps the goods name together.'),
    654: ('If the sailor has brought the named product as stock, the shopkeeper asks them to sell it soon at the Market.',
          'The quick question introduces the condition. The advice keeps the urgency and destination without implying a sale has happened. Stock works for both plural and mass goods.'),
    655: ('The merchant rallies themself to sell the product and make plenty of money.',
          'Make a bundle sounds like eager shop talk. Let’s preserves the self-rally, without implying a partner or an agreed deal.'),
    730: ('The shopkeeper expects one unspecified product in the given category to catch on soon.',
          'Something in the market keeps the product unspecified, while sure to catch on carries the shopkeeper’s confidence. The category comes from the original full-name dialogue getter.'),
    731: ('The shopkeeper personally expects this specific good to sell well.',
          'I think keeps their personal judgment, and will sell well works with the complete commodity name.'),
    732: ('The current trend looks likely to last for quite a while longer.',
          'May preserves the forecast’s uncertainty. Quite a while carries the duration as one phrase on a complete line.'),
    733: ('The shopkeeper wonders if the craze for the named good is nearing its end.',
          'Name the topic first and let the shopkeeper think aloud. The pause suits the speculation and leaves even long names intact.'),
    734: ('The shopkeeper wants to make a good profit before the trend fades and exclaims about being busy.',
          'Plenty of money and the flustered aside preserve both motives. The wording keeps the profit prospective and the busy aside personal.'),
}


def encoded_changes():
    return {n: compile_template(text, n) if n in (653, 654, 655) else b' ' + text.encode('ascii')
            for n, text in REVISIONS.items()}


def products(cpu, get):
    root = get(0xCB124) + 4
    result = {}
    for index in range(124):
        obj = root + 16 * index
        vtable, = unpack('<I', cpu.mem_read(obj, 4))
        name_getter, = unpack('<I', cpu.mem_read(vtable + 8, 4))
        result[index] = string(cpu, get(name_getter - BASE, obj))
    assert all(name and len(name) <= 19 for name in result.values()) and 'Whale Meat' in result.values()
    return result


def run_layout(cpu, n, template, arg):
    case = layout(cpu, template, n, (arg.encode('ascii'),) if arg else ())
    lines = [line.strip() for line in case['lines']]
    assert 1 <= len(lines) <= 3 and all(0 < len(line) <= 35 for line in lines), case
    if n in REVISIONS:
        assert not case['findings'] and (not arg or any(arg in line for line in lines)), (arg, case)
    case['lines'] = lines
    return case


def main():
    assert not any(path.exists() for path in (ROM, STORED, MANUSCRIPT))
    ROOT.mkdir(parents=True, exist_ok=True)
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    assert ctx.arm[0x5FB54:0x5FC84] == clean_arm[0x5FB54:0x5FC84]
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    arm, common = ctx.arm, ctx.common
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    credited = {r['id'] for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys'] if r['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NOTES)
    target, installed, slots = owned_deployment(common, arm, old, encoded_changes())
    updated = with_components(ctx, arm, target)
    cpu, get, provider = updated.machine(arm, target, updated.raw, updated.plan)
    names = products(cpu, get)
    categories = {index: string(cpu, getter(cpu, index, 0x0205FC48)) for index in range(18)}
    assert categories[6] == 'Precious Metals' and categories[11] == 'Jewelry'
    raster, _, font_proof = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    pages, records, native_cases = [], [], []
    for n, (meaning, note) in NOTES.items():
        source_row, current, staged = source[n], old[n], installed[n]
        dynamic = n in (653, 654, 655, 730, 731, 733)
        assert all(raw.count(b'%s') == int(dynamic) and raw.count(b'%') == int(dynamic)
                   for raw in (source_row.text, current.text, staged.text))
        address = get(0x5528C, n)
        assert bytes(cpu.mem_read(address, len(staged.text) + 1)) == staged.text + b'\0'
        variants = categories if n == 730 else names if dynamic else {None: ''}
        previews = {'Rice', 'Whale Meat', 'Black Glacier Sword'} if dynamic else {''}
        for index, arg in variants.items():
            case = run_layout(cpu, n, staged.text, arg)
            case.update(argument=arg, original_argument_index=index)
            native_cases.append(case)
            if n not in REVISIONS or arg not in previews:
                continue
            plane, _ = render_portrait(raster, arm, kanji, bytes.fromhex(case['formatted_hex']))
            case['native_plane_sha256'] = digest(plane)
            pages.append((f'{n} {arg or "revised"}', plane))
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, speaker='Shopkeeper',
            context='One alternative from the original Square shopkeeper trend conversation. The local trend state and random branch select the response.',
            source_meaning=meaning, localization_note=note, Japanese=source_row.text.decode('cp932'),
            english=REVISIONS.get(n, ' '.join(current.text.decode('ascii').split())),
            decision='revision' if n in REVISIONS else 'retention', file_path=COMMON,
            source_reference=reference(source_row), current_reference=reference(current), staged_reference=reference(staged),
            source_hex=source_row.text.hex(), current_hex=current.text.hex(), staged_hex=staged.text.hex(),
            review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    assert len(native_cases) == 640 and len(pages) == 13
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
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), records=records, candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256']))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(target), allocations=slots,
        whole_parent_inverse=True, native_cases=native_cases, sheets=sheets, font=font_proof,
        original_trend_selector=dict(start=0x5FB54, end=0x5FC84, sha256=digest(arm[0x5FB54:0x5FC84])),
        regional_evidence=str(TOWN_PROOF), regional_evidence_sha256=base.digest(TOWN_PROOF),
        manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'Reviewed {len(records)} Square alternatives and checked {len(native_cases)} native layouts.')


if __name__ == '__main__':
    main()
