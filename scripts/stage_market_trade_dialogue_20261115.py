"""Review the Market’s trade, investment, stock, and contract replies."""

from itertools import product
from pathlib import Path
from types import FunctionType

from dk4tool.patch.market_contract_editorial import INVESTMENT
from scripts import register_market_reward_dialogue_20261115 as parent
from scripts.review_market_contract_v758 import context_cases
from scripts.review_market_stock_v755 import fragments
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES, RegisteredRuntime,
    common_message_entries, compile_layouts, digest, files, font_tools, native_layout,
    owned_deployment, owned_entries, portrait_sheets, reference, render_portrait, with_components,
)
from scripts.stage_square_trend_dialogue_20261115 import products
from scripts.verify_market_context_v753 import SPANS, selections


base = parent.base
ROOT = Path('work/market_trade_dialogue_20261115_v2')
ROM, STORED = ROOT / 'Market_Trade_Dialogue_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/market_trade_dialogue_20261115_v2.json')
REVISIONS = {
    754: 'Paying double this time may let us buy more of certain goods.',
    755: 'Looks like paying double this time will get us more of some goods.',
    756: 'I think paying double this time will get us more of some goods.',
    757: 'Looks like paying double right now gets us more of some goods.',
    758: 'It seems paying double this time will get us more of certain goods.',
    759: 'If we pay double this time, I bet we can buy lots more of some goods!',
    760: 'Paying double this time appears to let us buy more of certain goods.',
    762: "You need market share to trade. You still want to invest? That's generous of you. How much will you put in?",
    764: "You don't have enough money. This isn't a charity. You'll have to pay to take a look.",
}
REFLOW = {763: "You're going to invest? I knew you were different from the rest! How much will you put in?"}
PHRASES = {
    754: ('Paying double this time', 'buy more of certain goods.'),
    755: ('paying double this time', 'more of some goods.'),
    756: ('paying double this time', 'more of some goods.'),
    757: ('paying double right now', 'more of some goods.'),
    758: ('paying double this time', 'more of certain goods.'),
    759: ('pay double this time', 'lots more of some goods!'),
    760: ('Paying double this time', 'buy more of certain goods.'),
    762: ('You need market share to trade.', 'You still want to invest?', "That's generous of you.", 'How much will you put in?'),
    763: ('different from the rest!', 'How much will you put in?'),
    764: ("This isn't a charity.", "You'll have to pay to take a look."),
}
GROUPS = {
    'merchant_follow_up': (745,), 'investment': (746, 747, 748, 762, 763),
    'purchase_refusal': (749, 753), 'extra_stock_advice': tuple(range(754, 761)),
    'trade_contract': (761,), 'paid_viewing_refusal': (764,), 'stock_and_favors': (767, 768, 769, 770),
}
NOTES = {
    745: ('The trader asks whether the customer needs anything else.', 'Keep the concise follow-up when the customer returns to the service menu.'),
    746: ('The trader asks whether the customer was only browsing.', 'Keep the disappointed but conversational question after the player enters a zero amount.'),
    747: ('The trader thanks the player and promises to put the investment to good use.', 'Keep the natural thanks, the promise and the trader’s use of we.'),
    748: ('The amount is too little. The trader asks the player to return after earning more.', 'Keep the surprise, apology and invitation to return in that order.'),
    749: ('The cargo holds are full, and the trader asks the player to buy less.', 'Keep the reason and the practical response together.'),
    753: ('The buyer lacks enough money to complete the purchase.', 'Keep the plain warning without adding a scold.'),
    754: ('A polite adviser suspects that double payment this time would buy larger quantities of certain goods.', 'May let us preserves uncertainty. Buy more is how a crew member would describe the quantity.'),
    755: ('A conversational adviser suspects the trader will sell more of some goods if paid double this time.', 'Looks like keeps the casual observation and some goods keeps the restriction.'),
    756: ('A conversational adviser thinks double payment might buy more of some goods this time.', 'I think keeps the tentative personal observation.'),
    757: ('A rougher adviser says double payment might buy more of some goods right now.', 'Keep the immediacy of right now and the casual Looks like.'),
    758: ('A measured adviser suspects the seller will part with more of certain goods for double payment this time.', 'It seems preserves the measured observation. More of certain goods keeps the offer limited.'),
    759: ('An upbeat adviser thinks double payment could buy a lot more of some goods this time.', 'I bet and lots more keep the enthusiasm and the emphasis on quantity.'),
    760: ('A polite adviser believes paying double this time might buy more of certain goods.', 'The condition comes first and it appears keeps the measured tone.'),
    761: ('The trader apologizes and tells the player to sign a contract at the supplied facility before returning.', 'Keep the courteous request and both steps. The original native format keeps each of the supplied building names whole.'),
    762: ('The trader notes the player cannot trade without market share, expresses surprise and praises the offer, then asks how much.', 'Give the prerequisite, surprise, appreciation and amount question their own spoken beats.'),
    763: ('The trader recognizes a prospective investment, flatters the player and asks for an amount.', 'Keep the existing flattery and give the amount question a complete line.'),
    764: ('The trader bluntly refuses the fee-based viewing because the player cannot pay.', 'Keep the charity rebuke and put the condition for getting a look on one line.'),
    767: ('The trader recognizes both goods, which sell quickly and often run out.', 'Keep the recognition, both substitutions in order, and the idiom that explains the stockouts.'),
    768: ('The trader thanks the seller. Demand for the named good often leaves the shop out of stock.', 'Keep the gratitude, the complete supplied name and the reason the delivery helps.'),
    769: ('The trader offers a favor because the two goods being sold are popular.', 'Sweeten the deal keeps the trader’s enthusiasm and the vague nature of the favor.'),
    770: ('The trader hesitates and then offers a favor for supplying the named popular good.', 'Keep the hesitation, the vague favor and the strong demand for the good.'),
}


def encoded_changes():
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES})
    edited = compiler({n: {'english': text} for n, text in (REFLOW | REVISIONS).items() if n > 761})
    edited.update({n: b' ' + text.encode('ascii') for n, text in REVISIONS.items() if n <= 761})
    return edited


def original_context(clean_arm, arm):
    assert [i for a, b in SPANS for i in range(a, b) if clean_arm[i] != arm[i]] == [0xBCA3C]
    assert int.from_bytes(arm[0xBCA3C:0xBCA40], 'little') == INVESTMENT
    clean_decisions, current_decisions = map(selections, (clean_arm, arm))
    assert clean_decisions == current_decisions
    clean, current = map(context_cases, (clean_arm, arm))
    assert clean['voice_index_cases'] == current['voice_index_cases'] and clean['advice_predicate_cases'] == current['advice_predicate_cases']
    old_stock, stock = ([r for r in fragments(raw) if r['kind'] in ('one_product', 'two_products')] for raw in (clean_arm, arm))
    assert old_stock == stock and len(stock) == 24
    facility = [bytes.fromhex(r['argument_hex']).decode('ascii') for r in current['contract_facility_cases']]
    assert facility == ["Governor's Office", 'Palace']
    return dict(investment_and_viewing=current_decisions, contract_and_advice=current, stock=stock, facility_names=facility)


def check_pages(ctx, arm, common, source, old, installed, bindings, edited):
    updated = with_components(ctx, arm, common)
    cpu, get, provider = updated.machine(arm, common, updated.raw, updated.plan)
    names = sorted(set(products(cpu, get).values()), key=lambda name: (len(name), name))
    sample = tuple(dict.fromkeys((names[0], 'Tea', 'Whale Meat', names[-2], names[-1])))
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    pages, records = [], []
    for group, ids in GROUPS.items():
        for n in ids:
            s, a, b = source[n], old[n], installed[n]
            args = tuple((name,) for name in bindings['facility_names']) if n == 761 else (
                tuple(product(sample, repeat=a.text.count(b'%s'))) if n >= 767 else ((),))
            cardinality = len(args[0])
            assert all(raw.count(b'%s') == raw.count(b'%') == cardinality for raw in (s.text, a.text, b.text))
            pointer = get(0x5528C, n)
            assert bytes(cpu.mem_read(pointer, len(b.text) + 1)) == b.text + b'\0'
            english = REVISIONS.get(n, ' '.join(a.text.decode('ascii').split()))
            assert n not in REFLOW or english == REFLOW[n]
            consumer = 0x02053DB8 if group == 'extra_stock_advice' else 0x02054014
            layouts = []
            for values in args:
                raw, after = native_layout(cpu, b.text, n, values, parent=consumer)
                assert ' '.join(after) == (english % values if values else english), (n, values, after)
                assert all(after)
                if n == 761:
                    assert any(values[0] in line for line in after), (values, after)
                if n in edited:
                    before_raw, before = native_layout(cpu, a.text, n, values, parent=consumer)
                    assert before != after and all(any(ph in line for line in after) for ph in PHRASES.get(n, values)), (n, after)
                    for side, rendered in (('before', before_raw), ('after', raw)):
                        plane, _ = render_portrait(raster, arm, kanji, rendered)
                        pages.append((f'{n} {" ".join(values)} {side}'.replace('  ', ' '), plane))
                layouts.append(dict(arguments=list(values), native_lines=after, formatted_hex=raw.hex()))
            meaning, note = NOTES[n]
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=COMMON,
                speaker='Fleet adviser' if group == 'extra_stock_advice' else 'Trader', context=group.replace('_', ' '),
                source_meaning=meaning, localization_note=note, Japanese=s.text.decode('cp932'), english=english,
                decision='revision' if n in REVISIONS else 'retention', reflow=n in edited,
                source_reference=reference(s), current_reference=reference(a), staged_reference=reference(b),
                source_hex=s.text.hex(), current_hex=a.text.hex(), staged_hex=b.text.hex(), layout_cases=layouts,
                native_consumer=consumer, review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert provider.reads and bytes(cpu.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    return records, pages, font, sample


def main():
    assert not any(path.exists() for path in (ROM, STORED, MANUSCRIPT))
    release = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256'] and base.digest(CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    source_arm = clean.read_file(ARM)
    source = common_message_entries(clean.read_file(COMMON), source_arm)
    arm, common = ctx.arm, ctx.common
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    credited = {r['id'] for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys'] if r['file_path'] == COMMON}
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in NOTES)
    bindings = original_context(source_arm, arm)
    edited = encoded_changes()
    deployed, installed, slots = owned_deployment(common, arm, old, edited)
    records, pages, font, sample = check_pages(ctx, arm, deployed, source, old, installed, bindings, edited)
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
        sampled_stock_names=list(sample), groups=GROUPS, candidate_sha256=candidate,
        previous_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256']))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=release['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(deployed), allocations=slots,
        whole_parent_inverse=True, sheets=sheets, font=font, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'Reviewed {len(records)} Market records and staged {len(edited)} changes.')


if __name__ == '__main__':
    main()
