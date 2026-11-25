"""Review source-product and voyage-supply advice shared by Hans and Mikhail."""

from hashlib import sha256
from struct import unpack_from

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R4, UC_ARM_REG_R6, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save, wide_letters
from scripts.checkpoint_sailing_alert_review_v1 import BASE, GATES, branch_target
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.register_promotional_item_cards_v1 import RELEASE, base
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.research_battle_declaration_context_v991c import name
from scripts.review_source_item_cards_and_coin_v1 import ARM, CLEAN, COMMON, ROOT, WIDE_ASCII, reference


OUTPUT = ROOT / 'item_production_advice_context_v1.json'
FIRST = 3033
IDS = tuple(range(FIRST, FIRST + 24))
DISPATCH = 0x02053FE4
CALLERS = (
    ('Gallery', 0x45488, UC_ARM_REG_R4, ((0x45408, 0x45430), (0x45438, 0x45460))),
    ('Compact item screen', 0x4B224, UC_ARM_REG_R6, ((0x4AEC4, 0x4AEEC), (0x4AEF4, 0x4AF1C))),
    ('Regular Items', 0x4CE0C, UC_ARM_REG_R8, ((0x4C89C, 0x4C8C4), (0x4C8CC, 0x4C8F4))),
)
ADVISERS = {75: 'Hans', 76: 'Mikhail'}
DATA = {
    3033: ('Pumpkin Seeds', "There's a good chance these will grow around the North Sea, too.",
           'The seeds have a good chance of growing around the North Sea as well.',
           'Restore the degree of confidence and the sense that the North Sea is another possibility.'),
    3034: ('Tomato Seedling', 'I think this would do well around the Mediterranean.',
           'The seedling looks likely to grow well if introduced around the Mediterranean.',
           'Use a grower’s natural phrasing and preserve the tentative forecast. Replace the full-width I.'),
    3035: ('Banana Tree', 'It might grow in the tropics of the New World or Africa, too.',
           'The plant might also grow in the tropical parts of the New World and Africa.',
           'Restore the tropical climate condition and both regions. Keep the prediction qualified.'),
    3036: ('Beehive', None,
           'Honey made from flowers that bloom around the Mediterranean must taste good too.',
           'Retain the speaker’s speculation about flavor and the Mediterranean flowers. The line works as a light aside about the hive.'),
    3037: ('Baby Shark', None,
           'The adviser has heard that people eat shark fins in China and shark eggs around the Black Sea beyond the Mediterranean.',
           'Retain the reported food customs, the distinction between fins and eggs, and the geographical relationship. Use a consistent ASCII I.'),
    3038: ('Pepper Plant', None,
           'Southeast Asia has an ideal climate for growing pepper.',
           'Retain the natural observation and keep pepper as the crop.'),
    3039: ('Clove Plant', "Cloves should thrive in Southeast Asia. The Mediterranean, though? We might have trouble there.",
           'Southeast Asia is very well suited to cloves. The adviser pauses to consider the Mediterranean and suggests it may be difficult.',
           'Keep the change of thought and the open question about the second climate. Use punctuation for the pause.'),
    3040: ('Cinnamon Tree', None,
           'If we could produce cinnamon in the Mediterranean, we would make a great profit.',
           'Retain the conversational excitement and the conditional promise of profit.'),
    3041: ('Pimento Plant', 'If only we could sell this spice in Africa...',
           'The adviser wishes this aromatic spice could be made into a trade good in Africa.',
           'Use the item context to name the spice and keep the wish trailing off. Remove the stiff “market this aromatic product” and the full-width I.'),
    3042: ('Coffee Tree', None,
           'The New World ought to be suitable for growing coffee.',
           'Retain the confident but qualified growing advice and the named region.'),
    3043: ('Tea Plant', 'I think we could grow tea in Africa, too.',
           'It seems possible to produce tea around Africa as well.',
           'Keep the tentative recommendation and the alternative region in direct speech. Replace the full-width I.'),
    3044: ('Cacao Seeds', None,
           'This appears to grow only in the tropics. The adviser suggests trying to bring it to Africa.',
           'Retain the two-part observation and proposal. The tropical requirement and the suggested next step both read clearly.'),
    3045: ('Tobacco Plant', 'We could grow and sell this in the Mediterranean. Might make us rich, too.',
           'Growing and selling this in the Mediterranean looks promising and might make us rich.',
           'Keep the location, the plan and the gleeful speculation as a spoken follow-up.'),
    3046: ('Alchemy Book', 'We might be able to turn African ore into a new trade good.',
           'Ore from Africa might yield a new local product.',
           'Keep the clue about African ore and the uncertain new trade good. Leave the product unidentified.'),
    3047: ('Glassmaking Guide', 'Glass is prized in Africa and East Asia.',
           'Glass is valuable in Africa and East Asia.',
           'Keep both markets and render the adviser’s observation in a short spoken sentence. Replace the full-width I.'),
    3048: ('Silkworms', None,
           'Silk has long been a major trade good in East Asia.',
           'Retain the historical perspective and the importance of silk in East Asian trade.'),
    3049: ('Loom', None,
           'Textile production around the North Sea and Mediterranean still has plenty of potential to grow.',
           'Retain the plain idiom “room to grow” and both regions.'),
    3050: ('Pearl Oyster', None,
           'Pearls may be obtainable in East Asia as well.',
           'Retain the tentative suggestion and the implication that East Asia is another possible source.'),
    3051: ("Herbalist's Bible", "I hear there are plenty more unusual herbal remedies in China.",
           'The adviser has heard that China still has many unusual traditional medicinal preparations.',
           'Keep the report attributed and preserve “plenty more.” The setting and the item make the tradition clear. Replace the full-width I.'),
    3052: ('Mangosteen Seeds', 'Southeast Asia has all sorts of unusual fruit. You can make dye from the peel of this one.',
           'Southeast Asia has many unusual fruits, and the peel of the fruit under discussion yields dye.',
           'Restore the contrast between regional variety and this fruit’s specific use.'),
    3053: ('Golden Cat', "If rats get aboard, this should come in mighty handy.",
           'The item should prove especially useful if rats appear.',
           'Keep the strong recommendation conditional and give the older adviser a conversational turn of phrase.'),
    3054: ('Lime Drops', "I wouldn't set sail without some of this to ward off scurvy.",
           'This is something the adviser would always take on a voyage to guard against scurvy.',
           'Make the recommendation sound like practical experience. Keep scurvy prevention and the insistence on bringing it.'),
    3055: ("Hermes' Prayer", None,
           'Even the best sailor cannot prevail against the weather, so this should be useful.',
           'Retain the natural maxim and the confident recommendation. The source gives no detailed weather effect here.'),
    3056: ("Hua Tuo's Tonic", None,
           'The adviser admires this example of Eastern medicine and says it reportedly works particularly well against infectious disease.',
           'Retain the admiring reaction and the reported, qualified remedy claim.'),
}


def bind_advice_callers(clean, runtime):
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    names = {n: name(cpu, get, runtime.actor_root + 4 + 32 * n) for n in ADVISERS}
    assert {n: entry['name'] for n, entry in names.items()} == ADVISERS
    assert get(0xCB184) == runtime.actor_root and get(0x7F244) == 3
    seen = []

    def dispatched(machine, pc, size, unused):
        seen.append((machine.reg_read(UC_ARM_REG_R0), machine.reg_read(UC_ARM_REG_R1),
                     machine.reg_read(UC_ARM_REG_LR)))
        machine.emu_stop()

    cpu.hook_add(UC_HOOK_CODE, dispatched, begin=DISPATCH, end=DISPATCH)
    cases, bindings = [], []
    for screen, literal, index_reg, branches in CALLERS:
        assert unpack_from('<I', clean, literal)[0] == unpack_from('<I', runtime.arm, literal)[0] == FIRST
        for actor, (start, call) in zip(ADVISERS, branches, strict=True):
            code = clean[start:call + 4]
            assert code == runtime.arm[start:call + 4] and branch_target(clean, call) == DISPATCH
            bindings.append(dict(screen=screen, actor_ID=actor, first_message_ID=FIRST,
                                 dispatch=DISPATCH, call=BASE + call, literal=BASE + literal,
                                 fragment=[BASE + start, BASE + call + 4], sha256=sha256(code).hexdigest()))
            for n in IDS:
                seen.clear()
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.reg_write(UC_ARM_REG_LR, STOP)
                cpu.reg_write(index_reg, n - FIRST)
                cpu.emu_start(BASE + start, STOP, count=2000)
                obj = runtime.actor_root + 4 + 32 * actor
                assert seen == [(obj, n, BASE + call + 4)], (screen, actor, n, seen)
                cases.append(dict(screen=screen, actor_ID=actor, item_ID=n - FIRST, message_ID=n,
                                  speaker_pointer=obj, original_call=BASE + call))
    assert len(cases) == 144 and bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    runtime.calls.clear()
    return dict(native_names=names, branches=bindings, offline_native_selector_cases=cases,
                input_scope='Item index supplied to each original actor-selection branch. No menu or dialogue replay.')


def main():
    assert not OUTPUT.exists() and tuple(DATA) == IDS
    release = load(RELEASE)
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    clean_image = NdsImage.open(CLEAN)
    clean = clean_image.read_file(ARM)
    assert digest(CLEAN) == release['clean_input_sha256']
    japanese = common_message_entries(clean_image.read_file(COMMON), clean)
    directory = sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    current = owned_entries(runtime.common, runtime.arm, directory)
    ledger = load(base.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(row['file_path'], row['id']) for row in ledger[base.CONTEXT]['integrated_record_keys']}
    del ledger
    cards = {}
    for filename in ('source_item_cards_and_coin_context_v1.json', 'utility_weapon_item_cards_context_v1.json'):
        for row in load(ROOT / filename)['records']:
            if isinstance(row.get('item_ID'), int) and row['item_ID'] < len(IDS):
                cards[row['item_ID']] = row
    assert sorted(cards) == list(range(len(IDS)))
    context = bind_advice_callers(clean, runtime)
    rows = []
    for n, (item, revision, meaning, note) in DATA.items():
        card = cards[n - FIRST]
        assert card['item_name'] == item
        identifier = f'COMMON_MESSAGE_{n}'
        assert (COMMON, identifier) not in credited
        jp, en = japanese[n], current[n]
        before = en.text.decode('cp932')
        logical = ' '.join(before.translate(WIDE_ASCII).split())
        english = revision or logical
        assert english.isascii() and english == ' '.join(english.split()) and '%' not in english
        assert '%' not in jp.text.decode('cp932') and bool(revision) == (logical != english)
        rows.append(dict(id=identifier, message_ID=n, file_path=COMMON, item_ID=n - FIRST, item_name=item,
            source_reference=reference(jp), current_reference=reference(en), source_hex=jp.text.hex(),
            current_hex=en.text.hex(), source_Japanese=jp.text.decode('cp932'), current_English=before,
            related_item_description=dict(id=card['id'], source_reference=card['source_reference']),
            speaker='Hans or Mikhail', actor_IDs=list(ADVISERS), original_substitutions=[],
            context=(f'The player requests advice while viewing {item}. Both advisers use the same reply. '
                     'This is a standalone observation in the item screen, with no preceding spoken prompt.'),
            source_meaning=meaning, english=english, localization_note=note,
            current_wide_Latin=wide_letters(before), decision='revision' if revision else 'retention',
            review={gate: gate != 'formatting' for gate in GATES}))
    revisions = sum(row['decision'] == 'revision' for row in rows)
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, registered_input=runtime.receipt(),
        source_ROM_sha256=release['clean_input_sha256'], native_context=context, records=rows,
        counts=dict(records=len(rows), revisions=revisions, justified_retentions=len(rows) - revisions),
        formatting_pending=True, registered_release_pending=True, new_gameplay=False, new_credit=0,
        full_goal_complete=False))
    print(f'{len(rows)} advice records, {revisions} revisions, and 144 original caller-fragment checks.')


if __name__ == '__main__':
    main()
