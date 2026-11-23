"""Review the remaining legacy COMMON wording and bind its current evidence."""

import re
from hashlib import sha256
from pathlib import Path
from struct import pack, unpack_from

from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_market_conversation_20261115 as current
from scripts.checkpoint_legacy_common_35_v1 import actor_data
from scripts.probe_button_prompt_native import BASE, machine
from scripts.review_sound_bgm_titles_v1 import reference


base = current.base
ROOT = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
OUTPUT = ROOT / 'legacy_dialogue_review_20261115_v1.json'
IDS = (*range(100, 112), *range(113, 118), 119, 124, 284, 287, 300, 304, 318, *range(330, 334), 750, 751, 752)
GATES = ('source', 'context', 'localization', 'naturalness', 'formatting')
REVISIONS = {
    101: ('%s, %s, and %s. Is that right?', 'Read back the three selected skills as a single list and preserve their order.'),
    102: ('Set the volume for music and sound effects.', 'Spell out music and sound effects in the help sentence.'),
    113: ("There aren't enough free blocks. Saving game data requires four.", 'Restore the shortage, the four-block requirement and the game-data distinction.'),
    114: ("There aren't enough free blocks. Saving system data requires one.", 'Restore the shortage and the distinct one-block requirement for system data.'),
    117: ('The game data is corrupted.', 'Use a complete sentence. The source reports corruption, without the separate DS slot label.'),
    119: ('Save the ending data to the memory card?', 'Ask one complete question and retain the storage device named in this copy.'),
    304: ("An allied faction holds this town. You can't attack it.", 'Say who holds the town and make clear that the attempted attack is unavailable.'),
    330: ('Music is %s. Change it to %s?', 'Keep the current and proposed settings in order and spell out the music label.'),
    331: ('Sound effects are %s. Change them to %s?', 'Name the exact setting and keep agreement across both clauses.'),
    333: ('Quick Guide auto-display is %s. Change it to %s?', 'Keep automatic display distinct from the guide itself and preserve both states.'),
    750: ('Are you sure you want to start over?', 'Restore the trader’s insistence on confirmation.'),
    751: ('What a hassle.', 'Give the standalone complaint a natural spoken shape.'),
    752: ("I'm busy. Spare me the jokes.", 'Keep both the impatience and the explicit complaint about joking around.'),
}
MEANINGS = {
    100: ('Select three skills you are good at.', 'Choose three skills you excel at is a clear and concise character-setup instruction.'),
    101: ('Asks whether the three substituted skills are acceptable.', ''),
    102: ('Explains that the music and sound-effect volumes can be set.', ''),
    103: ('Asks the player to enter their birthday.', 'Enter your birthday is a natural, direct calendar instruction.'),
    104: ('A Portuguese boy drawn to sailing goes to sea at a friend’s urging. The route is recommended to new players.', ''),
    105: ('After Sweden regains independence, its admiral leads a privateer fleet and wants it to become the strongest in the world.', ''),
    106: ('A business-minded Dutch girl and Camille, her childhood friend and partner, set sail to make their fortune.', ''),
    107: ('A woman admiral of Ming leads her private fleet against wokou raids in defiance of the country’s isolation law.', ''),
    108: ('The player is short of the four free blocks needed for game saves and can choose to begin anyway.', 'Keep the four-block requirement, the temporary inability to save and the start-anyway question.'),
    109: ('The player is short of the free block needed for system data and can choose to begin anyway.', 'Keep system data and its one-block requirement distinct from game data.'),
    110: ('The player is short of the five free blocks needed to save and can choose to begin anyway.', 'Keep the five-block threshold and the explicit decision to continue.'),
    111: ('Game data is missing and therefore cannot be loaded.', 'There’s no game data to load conveys the absence and failed load in one natural sentence.'),
    113: ('There is insufficient space to save game data, which requires four free blocks.', ''),
    114: ('There is insufficient space to save system data, which requires one free block.', ''),
    115: ('There is insufficient space to save, which requires five free blocks.', 'The English gives the reason and the exact number in two plain sentences.'),
    116: ('The memory card is being checked. Do not insert or remove it or the controller.', 'Keep the whole instruction and both devices as written in the clean source.'),
    117: ('The game data is corrupted.', ''),
    119: ('Asks whether the player wants to save ending data to the memory card.', ''),
    124: ('The memory card can be formatted during saving. Asks whether to start the game.', 'Keep the timing of formatting and the decision to start as separate sentences.'),
    284: ('The fleet is operating at a loss, and the player lacks the money to pay its debt.', ''),
    287: ('Announces the discovery of the place or thing inserted in the one name slot.', 'We’ve discovered preserves the announcement and enthusiasm without restricting the name slot.'),
    300: ('Asks the player to select whom to attack.', 'Choose an opponent to attack states the decision directly.'),
    304: ('An allied faction occupies the town, so it cannot be attacked.', ''),
    318: ('Quitting will lose the exhibition data. Asks the player whether to proceed.', ''),
    330: ('States the current music setting and asks whether to switch to the second state.', ''),
    331: ('States the current sound-effect setting and asks whether to switch to the second state.', ''),
    332: ('States the current vibration setting and asks whether to switch to the second state.', 'The existing two clauses preserve the setting and distinguish present and requested states.'),
    333: ('States whether the Quick Guide displays automatically and asks whether to switch that setting.', ''),
    750: ('Asks for confirmation that the player really wants to start over.', ''),
    751: ('The speaker mutters that this is a nuisance.', ''),
    752: ('The speaker says they are busy and tells the player to stop joking.', ''),
}
GROUPS = (
    ('Character setup', 'Skill selection, skill confirmation, sound help and birthday entry. The tested DS editor uses its own headings and COMMON 120.', tuple(range(100, 104))),
    ('Captain chooser', 'Four alternative introductory biographies. The DS chooser displays the registered four ARM9 texts.', tuple(range(104, 108))),
    ('Saving and loading', 'Separate warnings and confirmations for game data, system data, available space and the ending save.', (*range(108, 112), *range(113, 118), 119, 124)),
    ('Fleet and discovery', 'Separate replies for fleet debt, discovery, selecting an attack target and denying an attack on allied territory.', (284, 287, 300, 304)),
    ('Exhibition quit', 'A data-loss warning before confirming departure from an exhibition session.', (318,)),
    ('Settings', 'Alternative confirmations for music, sound effects, vibration and automatic Quick Guide display.', tuple(range(330, 334))),
    ('Market trader', 'A restart question or an irritated reply. The source storage alone gives no sequence or reply condition.', (750, 751, 752)),
)


def reject_graphics_collision(arm):
    """Execute the literal use of 318 through its actual table lookup and write."""
    cpu = machine(arm)
    target = 0x04000488
    cpu.mem_map(0x04000000, 0x1000)
    assert unpack_from('<I', arm, 0xF57A4) == (318,)
    assert unpack_from('<2I', arm, 0x692E8) == (0x0214599C, target)
    assert unpack_from('<I', arm, 0x14599C + 4 * 318) == (0x06001000,)
    executed, writes = [], []
    cpu.hook_add(UC_HOOK_CODE, lambda _, address, size, data: executed.append(address))
    cpu.hook_add(UC_HOOK_MEM_WRITE, lambda _, access, address, size, value, data: writes.append((address, size, value)))
    cpu.emu_start(BASE + 0xF56AC, BASE + 0xF56B4, count=16)
    assert executed == [BASE + i for i in (0xF56AC, 0xF56B0, 0x692D4, 0x692D8, 0x692DC, 0x692E0, 0x692E4)]
    assert writes == [(target, 4, 0x06001000)]
    assert cpu.reg_read(UC_ARM_REG_R0) == unpack_from('<I', cpu.mem_read(target, 4))[0] == 0x06001000
    return dict(literal_address=BASE + 0xF57A4, literal_value=318, executed=executed, graphics_register=target,
                graphics_parameter=0x06001000)


def main():
    assert not OUTPUT.exists()
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    source, candidate = map(base.NdsImage.open, (current.stage.CLEAN, current.ROM))
    arm_path, common_path = current.stage.ARM, current.stage.COMMON
    clean, arm = (rom.read_file(arm_path) for rom in (source, candidate))
    common = candidate.read_file(common_path)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    ja = common_message_entries(source.read_file(common_path), clean)
    en = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    ledger = base.load(base.LEDGER)
    pending = ledger['pending_shared_consumer_checkpoint_20261114']['remaining_legacy_keys']
    assert tuple(pending) == IDS and set(IDS) == MEANINGS.keys()
    last, chooser, debt, quit_notice, load_notice = [ROOT / name for name in (
        'legacy_common_35_checkpoint_v1.json', 'common_104_107_chooser_owner_comparison_v1.json',
        'fleet_debt_disband_20261115_v2.json', 'exhibition_quit_warning_20261115_v2.json',
        'continue_legacy_calls_20261115_v1.json')]
    previous = {row['message_ID']: row for row in base.load(last)['records']}
    approved = {row['id']: row for row in base.load(chooser)['records']}
    debt_draft = base.load(debt)['debt_warning']
    quit_draft = base.load(quit_notice)['exhibition_warning']
    previous_load = base.load(load_notice)
    assert all(sha256(arm[row['start'] - BASE:row['end'] - BASE]).hexdigest() == row['sha256']
               for row in previous_load['verified_code_spans'])
    assert arm[0xEF068:0xEF06C] == bytes.fromhex('1eff2fe1')
    assert en[111].text.hex() == previous_load['records'][0]['current_hex']
    revised = REVISIONS | {
        284: (debt_draft['staged_draft'], 'Carry forward the source-faithful warning from the earlier preview.'),
        318: (quit_draft['english'], 'Carry forward the verified ASCII draft, preserving the loss of exhibition data.'),
    }
    for n in range(104, 108):
        row = approved[f'COMMON_MESSAGE_{n}']
        assert ja[n].text.decode('cp932') == row['clean_COMMON_text']
        revised[n] = (row['current_chooser_English'], 'Use the corresponding approved chooser biography and its established names.')
    records = []
    for speaker, context, choices in GROUPS:
        for n in choices:
            s, c = ja[n], en[n]
            assert previous[n]['clean_hex'] == s.text.hex() and previous[n]['current_hex'] == c.text.hex()
            logical = ' '.join(c.text.decode('cp932').split())
            meaning, reason = MEANINGS[n]
            english, note = revised.get(n, (logical, reason))
            macros = re.findall(rb'%[a-z]', s.text)
            assert macros == re.findall(rb'%[a-z]', c.text) == re.findall(rb'%[a-z]', english.encode('ascii'))
            assert note and english and '{' not in english and '\n' not in english
            records.append(dict(id=f'COMMON_MESSAGE_{n}', message_ID=n, file_path=common_path, speaker=speaker,
                context=context, source_meaning=meaning, localization_note=note, Japanese=s.text.decode('cp932'),
                previous_English=c.text.decode('cp932'), english=english, decision='draft revision' if n in revised else 'wording retention',
                source_reference=reference(s), current_reference=reference(c), source_hex=s.text.hex(), current_hex=c.text.hex(),
                current_copy_extent_bytes=c.copy_end - c.block_offset, draft_text_bytes=len(english.encode('ascii')),
                preserved_format_arguments=[token.decode('ascii') for token in macros],
                review=dict.fromkeys(GATES, True) | {'formatting': False}, original_display_ownership='open'))
    assert tuple(row['message_ID'] for row in records) == IDS
    assert len(revised) == 19 and len(records) - len(revised) == 12
    graphics = reject_graphics_collision(clean)
    assert reject_graphics_collision(arm) == graphics
    addr, old_actor = actor_data(clean)
    _, new_actor = actor_data(arm)
    assert old_actor[12:] == new_actor[12:] and unpack_from('<I', old_actor, 12) == (750,)
    references = {str(p): base.digest(p) for p in (current.RELEASE, last, chooser, debt, quit_notice, load_notice, Path(__file__))}
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=list(GATES), candidate_sha256=release['candidate_sha256'], clean_sha256=release['clean_input_sha256'],
        common_sha256=release['target_COMMON_sha256'], records=records, graphics_collision_318=graphics,
        actor_collision_750=dict(record_address=addr, field_address=addr + 12, value=750), evidence=references,
        reused_non_display_111=dict(known_path='Continue warning', sink=BASE + 0xEF068, proven_code_spans_match=True),
        draft_revisions=len(revised), wording_retentions=len(records) - len(revised), observed_gameplay_added=False,
        registered_ROM_changed=False, new_editorial_credit=0))
    print('Bound all 31 legacy records to the current ROM and recorded 19 draft revisions and 12 wording retentions.')


if __name__ == '__main__':
    main()
