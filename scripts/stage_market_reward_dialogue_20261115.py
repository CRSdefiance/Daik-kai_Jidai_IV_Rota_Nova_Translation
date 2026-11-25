"""Review Market letters, their instructions, and the alternative closing favors."""

from pathlib import Path
from types import FunctionType

from scripts import register_market_economy_dialogue_20261115 as parent
from scripts.review_market_stock_v755 import fragments
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES, RegisteredRuntime,
    common_message_entries, compile_layouts, digest, files, font_tools, native_layout,
    owned_deployment, owned_entries, portrait_sheets, reference, render_portrait, with_components,
)


base = parent.base
ROOT = Path('work/market_reward_dialogue_20261115_v1')
ROM, STORED = ROOT / 'Market_Reward_Dialogue_RESEARCH_ONLY.nds', ROOT / 'staged.json'
MANUSCRIPT = Path('translations/editorial_checkpoints/SharedText_20261110_v1/market_reward_dialogue_20261115_v1.json')
REVISIONS = {
    775: "And to thank you for all those popular goods, I'll write you a letter of recommendation.",
    776: "Oh, I know! Thanks for selling us so many popular goods. I'll write you a letter of introduction.",
    777: "Oh, a letter of introduction! Let me add a few words to make it a letter of recommendation.",
    778: "Oh, I know! Thanks for selling us so many popular goods. I'll write you a letter of recommendation.",
    779: "In a small town, show the letter at a palace or governor's office. You should get some market share.",
    780: "In any town, show the letter at a palace or governor's office. You should get some market share.",
    781: 'A letter of introduction works only in small towns. A letter of recommendation works in any town.',
    783: "Oh, you're selling popular goods? Thanks! Keep them coming!",
}
REFLOW = {774: "Oh, I know! I'll write you a letter of introduction to thank you for selling us those popular goods."}
PHRASES = {
    774: ('a letter of introduction', 'those popular goods.'),
    775: ('all those popular goods,', 'a letter of recommendation.'),
    776: ('so many popular goods.', 'a letter of introduction.'),
    777: ('letter of introduction!', 'Let me add a few words', 'a letter of recommendation.'),
    778: ('so many popular goods.', 'a letter of recommendation.'),
    779: ("at a palace or governor's office.", 'You should get some market share.'),
    780: ("at a palace or governor's office.", 'You should get some market share.'),
    781: ('A letter of introduction', 'only in small towns.', 'A letter of recommendation', 'works in any town.'),
    783: ('popular goods?', 'Thanks! Keep them coming!'),
}
REVIEW = {
    765: ('The trader adds a small market-share favor and assures the player they will handle it.',
          'Keep the added favor, the indefinite amount and the personal reassurance. Market share stays together.'),
    766: ('The trader closes the transaction by asking the player to come back.',
          'Come back anytime is an idiomatic invitation after each benefit or thank-you, and fits one line.'),
    774: ('An idea occurs to the trader, who offers an introduction in thanks for the popular goods.',
          'Keep the spontaneous offer and reason. The reflow keeps the letter name and the goods phrase together.'),
    775: ('The trader adds a recommendation in thanks for the large quantity of popular goods.',
          'And keeps this recommendation an added favor. All those conveys the quantity in the trader’s own voice.'),
    776: ('The trader suddenly offers an introduction in thanks for a large quantity of popular goods.',
          'Give the thanks its own sentence and retain both the size of the sale and the introduction.'),
    777: ('The trader notices an existing introduction and offers to add a note that makes it a recommendation.',
          'The opening calls out the letter the player already has. The trader adds a few words to it.'),
    778: ('The trader thinks to offer a recommendation for the large quantity of popular goods.',
          'Use the same voice as the introduction offer while keeping this distinct recommendation.'),
    779: ('In a small town, present the introduction at a palace or governor’s office for a likely share concession.',
          'Lead with the small-town limit. Show the letter makes the next action clear, and should preserves uncertainty.'),
    780: ('In any town, present the recommendation at a palace or governor’s office for a likely share concession.',
          'Lead with the expanded reach and use the same action and degree of certainty as the small-town reply.'),
    781: ('Introductions work only in small towns. Recommendations are accepted in any town.',
          'Use parallel sentences so the difference is clear after the trader upgrades the letter.'),
    782: ('After pausing to think, the trader offers a little extra because the player is selling popular goods.',
          'Keep the deliberation and the indefinite offer. The closing phrase already fits on one line.'),
    783: ('The trader reacts with surprise, thanks the player for selling popular goods and asks for continued sales.',
          'Keep the quick question and the lively closing on separate complete lines.'),
}


def encoded_changes():
    compiler = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': PHRASES})
    return compiler({n: {'english': text} for n, text in (REFLOW | REVISIONS).items()})


def original_branches(clean_arm, arm):
    spans = ((0xBBDA4, 0xBBDC8), (0xBBED4, 0xBBF04), (0xBC018, 0xBC05C), (0xBC08C, 0xBC0B8),
             (0xBC260, 0xBC2A8))
    assert all(clean_arm[a:b] == arm[a:b] for a, b in spans)
    clean, current = ([row for row in fragments(raw) if row['kind'] == 'letter_or_thanks_fragment']
                      for raw in (clean_arm, arm))
    assert clean == current and len(current) == 6
    return dict(chains=current, spans=[dict(start=a, end=b, sha256=digest(arm[a:b])) for a, b in spans])


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
    assert all(f'COMMON_MESSAGE_{n}' in credited for n in REVIEW)
    bindings = original_branches(source_arm, arm)
    edited = encoded_changes()
    deployed, installed, slots = owned_deployment(common, arm, old, edited)
    updated = with_components(ctx, arm, deployed)
    cpu, get, provider = updated.machine(arm, deployed, updated.raw, updated.plan)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    records, pages = [], []
    for n, (meaning, note) in REVIEW.items():
        s, a, b = source[n], old[n], installed[n]
        assert b'%' not in s.text + a.text + b.text
        pointer = get(0x5528C, n)
        assert bytes(cpu.mem_read(pointer, len(b.text) + 1)) == b.text + b'\0'
        before_bytes, before = native_layout(cpu, a.text, n, ())
        after_bytes, after = native_layout(cpu, b.text, n, ())
        existing = ' '.join(a.text.decode('ascii').split())
        english = REVISIONS.get(n, existing)
        assert ' '.join(after) == english and all(after)
        if n in REFLOW:
            assert english == REFLOW[n]
        if n in edited:
            assert before != after and all(any(group in line for line in after) for group in PHRASES[n]), (n, after)
            for label, body in (('before', before_bytes), ('after', after_bytes)):
                plane, _ = render_portrait(raster, arm, kanji, body)
                pages.append((f'{n} {label}', plane))
        chains = [row['IDs'] for row in bindings['chains'] if n in row['IDs']]
        records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, speaker='Trader', file_path=COMMON,
            context=('The trader adds a small share favor before the closing invitation.' if n == 765 else
                     'A Market reward or thank-you after the sale, with original follow-ups recorded in the selected chains.'),
            original_chains=chains, source_meaning=meaning, localization_note=note,
            Japanese=s.text.decode('cp932'), english=english, decision='revision' if n in REVISIONS else 'retention',
            reflow=n in edited, source_reference=reference(s), current_reference=reference(a),
            staged_reference=reference(b), source_hex=s.text.hex(), current_hex=a.text.hex(), staged_hex=b.text.hex(),
            old_native_lines=before, native_lines=after, native_formatted_hex=after_bytes.hex(),
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
        whole_parent_inverse=True, sheets=sheets, font=font, manuscript_sha256=base.digest(MANUSCRIPT)))
    print(f'Reviewed {len(records)} Market records and staged {len(edited)} changes.')


if __name__ == '__main__':
    main()
