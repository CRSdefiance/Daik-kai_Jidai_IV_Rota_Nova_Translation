"""Review the complete baby-shark exchange, captain variants, and decision menu."""

import struct
from hashlib import sha256
from pathlib import Path

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts.audit_story_glyph_consistency import load, save
from scripts.checkpoint_mutiny_review_v1 import arm_immediate, pointer_aliases
from scripts.checkpoint_sailing_alert_review_v1 import BASE, branch_target, caller_binding, word
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.register_faction_and_epilogue_v1 import RELEASE
from scripts.register_shared_notices_v1 import CONTEXT, LEDGER
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, ROOT, reference


OUTPUT = ROOT / 'shark_encounter_context_v1.json'
MENU = 0x119114
START, STOP = 0x71B18, 0x71D54
GROUPS = (
    (0x1167A0, 0x71D08, 0x71BBC, 0x71BC0, (2426, 2427, 2429, 2428),
     'The admiral agrees after Al comments on the fight. The shark splashes again before Al asks what to do.'),
    (0x116660, 0x71D10, 0x71BD8, 0x71BDC, (2431, 2432, 2433, 2434),
     'The admiral hesitates to kill so small a shark. Al interprets the hesitation as a plan to release it.'),
    (0x116520, 0x71D1C, 0x71BF8, 0x71BFC, (2444, 2445, 2446, 2447),
     'The admiral invites Samwell to speak after he interrupts Al’s warning.'),
    (0x1164D0, 0x71D38, 0x71C64, 0x71C68, (2437, 2438, 2439, 2440),
     'The admiral confirms the player’s decision to raise the shark. Al grumbles before the acquisition notice.'),
)
SINGLES = {
    2425: (17, 0x71BA8, 0x71BB0, 0x71D00, 'Al opens the exchange after the shark fight.'),
    2430: (17, 0x71BD0, 0x71BD4, 0x71D0C, 'Al asks the admiral to decide after the two splashes.'),
    2435: (17, 0x71BE4, 0x71BE8, 0x71D14, 'Al responds to the admiral’s hesitation by protesting the idea of release.'),
    2436: (17, 0x71C58, 0x71C60, 0x71D34, 'After Samwell cheers the decision to raise it, Al asks if the admiral is serious.'),
    2441: (17, 0x71C6C, 0x71C74, 0x71D3C, 'Al reluctantly accepts the admiral’s decision to raise it and mutters a warning.'),
    2442: (17, 0x71CDC, 0x71CE4, 0x71D4C, 'On the kill branch, Al approves and gives his reason.'),
    2443: (22, 0x71BF0, 0x71BF4, 0x71D18, 'Samwell interrupts the argument with a proposal.'),
    2448: (22, None, 0x71C08, None, 'Samwell wonders if sharks are edible and might become a new trade good.'),
    2449: (22, 0x71C10, 0x71C14, 0x71D20, 'Samwell follows up by proposing they raise this shark and see.'),
    2450: (17, 0x71C1C, 0x71C20, 0x71D24, 'Al rebukes Samwell for ignoring how dangerous sharks are.'),
    2451: (17, 0x71C28, 0x71C2C, 0x71D28, 'Al dismisses Samwell’s idea and urges the admiral to kill the shark before the player chooses.'),
    2452: (22, 0x71C4C, 0x71C54, 0x71D30, 'Samwell cheers when the player chooses to raise it.'),
    2453: (22, 0x71CE8, 0x71CF0, 0x71D50, 'On the kill branch, Samwell mourns the meal that might have been.'),
}
CAPTAINS = ('Rafael', 'Hodram', 'Lil', 'Maria')
SPEAKERS = {17: 'Al Ferid Shin', 22: 'Samwell da Khan'}
DATA = {
    2425: ('That thing put up quite a fight...', 'A weary opening about the struggle that just ended.'),
    2426: ('Yeah, it sure did.', 'Rafael’s warm agreement answers Al’s comment about the fight.'),
    2427: ('Yeah. It did.', 'Hodram gives a short, steady assent.'),
    2428: ('Yes, it did.', 'Maria agrees in a composed tone. The original table selects this for Maria.'),
    2429: ('Sure did.', 'Lil answers casually. The original table selects this for Lil.'),
    2430: ('Admiral, what should we do with it?', 'Retain the natural question, the rank of the person addressed, and Al’s attention to the shark.'),
    2431: ("A shark may be a monster, but killing one this small... I don't know.",
           'Rafael trails off rather than announcing a decision. Keep both his concession and hesitation.'),
    2432: ("Shark or no shark, I don't like the idea of killing anything this small.",
           'Hodram is plainspoken. His discomfort applies even to a shark.'),
    2433: ("Look how small this shark is. It'd be cruel to kill it...",
           'Lil points out the size before appealing to pity. Preserve both thoughts and her trailing hesitation.'),
    2434: ("It may be a shark, but I can't bear to take the life of something so small.",
           'Maria frames the objection as taking a small creature’s life, in her slightly more formal voice.'),
    2435: ("So you're going to let it go?! You've got to be kidding! Think what could happen once it's grown!",
           'Al jumps from reluctance to kill it to fear that they might release it. No actual release occurs in this branch.'),
    2436: ('What?! Are you serious?', 'Retain the two short, startled questions as Al reacts to the player’s choice.'),
    2437: ("Yeah. I can't wait to see what happens.", 'Rafael confirms and looks forward to seeing how the experiment goes.'),
    2438: ("Yes. I'm serious.", 'Retain Hodram’s firm wording. Replace the accidental full-width I with the normal glyph.'),
    2439: ("Yeah. No idea how it'll turn out, though...", 'Lil agrees without knowing what the result will be. Keep the uncertainty.'),
    2440: ('Yes.', 'Restore Maria’s complete assent on its own panel. The old “All” is the first half of an English phrase assigned to two speakers.'),
    2441: ("Just don't blame me for what happens later... (Grumble, grumble.)",
           'Restore Al’s separate warning and muttering. His first word no longer completes Maria’s line.'),
    2442: ("It's for the best in the long run. There's no room for pity.",
           'Al explains why he approves of the choice before rejecting mercy. Preserve both thoughts.'),
    2443: ('Hey, can I say something?', 'Retain Samwell’s casual interruption. Replace the accidental full-width I.'),
    2444: ("What's up?", 'Rafael invites the interruption without assuming something has gone wrong.'),
    2445: ('What is it?', 'Retain Hodram’s brief, direct invitation to continue.'),
    2446: ('What?', 'Retain Lil’s short, informal response to the interruption.'),
    2447: ('Yes? What is it?', 'Retain Maria’s polite opening and invitation to continue.'),
    2448: ("I've got a hunch you can eat shark. It might even make a new trade good.",
           'Samwell gives both ideas as speculation. Retain trade good as the game’s established term.'),
    2449: ("So why don't we raise this one and see?", 'Samwell proposes raising this shark to test the idea. Match the action in the following menu.'),
    2450: ("What are you talking about? You don't know how dangerous sharks are!",
           'Restore Al’s rebuke and the accusation that Samwell doesn’t understand the danger.'),
    2451: ("You catch a shark, you kill it. Admiral, don't listen to him. Let's kill it and be done with it!",
           'Restore Al’s rule of thumb and his direct appeal to disregard Samwell’s proposal and act immediately.'),
    2452: ("That's more like it! Oh, this is going to be fun. I can't wait!",
           'Samwell’s enthusiastic approval and anticipation contrast with Al’s disbelief on the next panel.'),
    2453: ('Aw, there goes a good meal... What a waste.',
           'Samwell mourns the meal he might have had. Keep the comic disappointment and the unrealized opportunity.'),
}
MENU_TEXT = (
    ('飼う', 'Raise It', 'Raise the young shark to test Samwell’s idea. The original branch awards the Baby Shark item.'),
    ('殺す', 'Kill It', 'Kill the shark as Al urges. The original branch displays Al’s approval and Samwell’s regret.'),
)


def exact_menu(clean, arm):
    caller = caller_binding(clean, arm, 0x71C30, 0x71C40, 0x71D2C, BASE + MENU, 0x51E7C)
    assert pointer_aliases(clean, BASE + MENU) == pointer_aliases(arm, BASE + MENU) == [0x71D2C]
    assert word(clean, 0x71C34) == 0xE3A01002
    records = []
    for i, (japanese, english, context) in enumerate(MENU_TEXT):
        field = MENU + 4 * i
        ptr = word(clean, field)
        offset = ptr - BASE
        raw = japanese.encode('cp932') + b'\0'
        assert word(arm, field) == ptr
        assert clean[offset:offset + len(raw)] == arm[offset:offset + len(raw)] == raw
        assert pointer_aliases(clean, ptr) == pointer_aliases(arm, ptr) == [field]
        ref = dict(pointer_field=BASE + field, literal_offset=offset, terminator_offset=offset + len(raw) - 1)
        records.append(dict(id=f'ARM9_SHARK_CHOICE_{i}', file_path=ARM, choice_index=i, source_reference=ref,
            current_reference=ref, source_hex=raw.hex(), current_hex=raw.hex(), source_Japanese=japanese,
            current_English=japanese, english=english, speaker='Shark decision menu', context=context,
            source_meaning=context, localization_note='Use the original action as a short English choice caption.',
            decision='revision', review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    return dict(original_consumer=0x02051E7C, caller=caller, result_branches=[0x02071C4C, 0x02071CDC], records=records)


def main():
    assert not OUTPUT.exists()
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256']
    runtime = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    clean_rom = NdsImage.open(CLEAN)
    clean, arm = clean_rom.read_file(ARM), runtime.arm
    assert clean[START:STOP] == arm[START:STOP]
    assert clean[0x71DF4:0x71E70] == arm[0x71DF4:0x71E70]
    assert branch_target(clean, 0x71E4C) == BASE + START
    assert word(clean, 0x71E24) == 0xEA000008 and word(clean, 0x71C98) == 0xE3A00004
    assert branch_target(clean, 0x71B44) == branch_target(clean, 0x71B78) == 0x0207DB14
    assert word(clean, 0x71B2C) == 0xE3500016 and word(clean, 0x71B60) == 0xE3500011
    for address, register, actor_id in ((0x71B3C, 5, 22), (0x71B70, 6, 17)):
        instruction = word(clean, address)
        assert instruction & 0xFFFFF000 == (0x12800000 | register << 12)
        assert arm_immediate(0xE3A00000 | (instruction & 0xFFF)) == actor_id * 32
    assert word(clean, 0x71CFC) == 0x19E4 and branch_target(clean, 0x71B98) == 0x0204A368
    cpu, get, _ = runtime.machine(arm, runtime.common, runtime.raw, runtime.plan)
    names = {n: bytes(cpu.mem_read(get(0x7EA8C, runtime.actor_root + 4 + n * 32), 64)).split(b'\0')[0].decode('cp932')
             for n in SPEAKERS}
    assert names == SPEAKERS
    runtime.calls.clear()
    source = common_message_entries(clean_rom.read_file(COMMON), clean)
    current = owned_entries(runtime.common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = load(LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    credited = {(row['file_path'], row['id']) for row in ledger[CONTEXT]['integrated_record_keys']}
    bindings, groups = {}, []
    for table, literal, pc, call, slots, context in GROUPS:
        assert struct.unpack_from('<4I', clean, table) == struct.unpack_from('<4I', arm, table) == slots
        assert pointer_aliases(clean, BASE + table) == pointer_aliases(arm, BASE + table) == [literal]
        native = caller_binding(clean, arm, pc, call, literal, BASE + table, 0x53BD8)
        group = dict(table=BASE + table, table_slots=slots, consumer=0x02053BD8, context=context, native_caller=native)
        groups.append(group)
        for captain, n in enumerate(slots):
            bindings[n] = dict(speaker=CAPTAINS[captain], captain_index=captain, context=context, native_caller=native)
    for n, (actor, pc, call, literal, context) in SINGLES.items():
        if pc is None:
            instruction = word(clean, call - 4)
            assert (instruction >> 12) & 15 == 1 and arm_immediate(instruction) == n
            assert branch_target(clean, call) == 0x02053FE4
            native = dict(call_PC=BASE + call, consumer=0x02053FE4, message_ID=n,
                          exact_instruction_and_call_hex=clean[call - 4:call + 4].hex())
        else:
            native = caller_binding(clean, arm, pc, call, literal, n, 0x53FE4)
        bindings[n] = dict(speaker=names[actor], original_actor_ID=actor, context=context, native_caller=native)

    def row(n):
        jp, en = source[n], current[n]
        return dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, message_ID=n, source_reference=reference(jp),
            current_reference=reference(en), source_hex=jp.text.hex(), current_hex=en.text.hex(),
            clean_Japanese=jp.text.decode('cp932'), current_English=en.text.decode('cp932'))

    records = []
    for n, (english, note) in DATA.items():
        record = row(n) | bindings[n]
        assert (COMMON, record['id']) not in credited
        assert english.isascii() and '%' not in english and '%' not in record['clean_Japanese']
        old = ' '.join(record['current_English'].replace('Ｉ', 'I').split())
        records.append(record | dict(english=english, localization_note=note,
            decision='retention' if english == old else 'revision',
            fullwidth_I_corrected='Ｉ' in record['current_English'],
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    assert tuple(row['message_ID'] for row in records) == tuple(range(2425, 2454))
    menu = exact_menu(clean, arm)
    assert all((ARM, choice['id']) not in credited for choice in menu['records'])
    context = [row(n) for n in (313, 314)]
    assert all((COMMON, record['id']) in credited for record in context)
    save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        registered_input=runtime.receipt(), records=records, captain_tables=groups, original_choice_menu=menu,
        original_speakers=names, previously_credited_system_context=context,
        original_common_sequence=[2425, 313, [2426, 2427, 2429, 2428], 313, 2430, [2431, 2432, 2433, 2434],
            2435, 2443, [2444, 2445, 2446, 2447], 2448, 2449, 2450, 2451],
        raise_sequence=[2452, 2436, [2437, 2438, 2439, 2440], 2441, 314], kill_sequence=[2442, 2453],
        exact_original_function_hex=clean[START:STOP].hex(), clean_source_battle_call=0x02071E4C,
        clean_source_battle_model=36, live_gameplay=False, new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, Path(__file__))}))
    print('Reviewed the full shark encounter, all four captain variants, and both original decision captions.')


if __name__ == '__main__':
    main()
