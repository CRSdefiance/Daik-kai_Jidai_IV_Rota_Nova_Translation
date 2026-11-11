"""Review the original faction, level-up, and four-panel epilogue notices."""

import inspect
import struct
from hashlib import sha256

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import review_setup_save_equipment_v1 as previous
from scripts.register_discovery_rewards_v1 import RELEASE
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text


OUTPUT = previous.OUTPUT.with_name('faction_and_epilogue_context_v1.json')
DATA = {
    334: ("%s is under attack by %s's fleet!",
          'The named town is under attack by a fleet belonging to the second named faction.',
          'The Sea View branch checks the town and excludes the special attacker index 21 before reading the town and attacking faction labels in that order.',
          'Retain the urgent wording. The town comes first and the fleet belongs to the faction named by the second substitution. Verify wrapping with long labels.'),
    335: ('%s leveled up!',
          'The named crew member gained a level.',
          'This modal result follows the original level calculation, calls the same given-name getter as the distinct floating level-up notice, and plays the original effect before display.',
          'Use the same wording and single exclamation point as the registered floating notice. Keep the modal and floating displays distinct.'),
    337: ('%s has disbanded.',
          'The named company or faction has dissolved.',
          'The dissolution handler displays the faction name through the original raw-template notice before branching on whether the faction is the player’s.',
          'Use the same disband verb as the fleet interface. The completed result applies to an entire faction here, with its own name supplied by the game.'),
    342: ('After leading %s for many years, %s...',
          'The named person led the named faction for many years. Their fate is given on the next panel.',
          'The first panel of the original epilogue passes the player’s faction name and then the composed character name. The following panel completes the sentence.',
          'Use an active verb and remove the redundant title. Keep the source pause because the game waits on this separate opening panel before revealing the fate.'),
    343: ('passed away after a full and eventful life.',
          'The leader died at the end of their natural lifespan after a life full of upheaval.',
          'The second epilogue panel completes the opening sentence about the named leader. It is immediately followed by the historical overview.',
          'Retain the dignified wording and lowercase opening. “Full” carries the sense of a natural lifespan and “eventful” suits this retrospective without naming new events.'),
    344: ('From the Middle Ages into the early modern era, the Age of Discovery transformed the world.',
          'From the Middle Ages into the early modern era, the Age of Discovery brought great change to the world.',
          'The third epilogue panel moves from the individual’s life to the historical period before the final panel turns to the legends it left behind.',
          'Give the historical panel its own complete sentence. The original pause remains in the game’s panel transition, and the next sentence still refers back to the Age of Discovery.'),
    345: ('Its many legends will live on, passed down to each new generation.',
          'The period left many legends that will be told and passed down to a new generation.',
          'This is the final narrator panel after the historical overview. The original ending routine continues only after the panel is dismissed.',
          'Keep the closing image of legends handed down to new generations. Use ordinary ASCII I and a period to close the narration.'),
}
UNBOUND = {
    330: 'Two string substitutions describe the current and proposed BGM settings. The exact DS consumer remains unbound.',
    331: 'Two string substitutions describe the current and proposed sound-effects settings. The exact DS consumer remains unbound.',
    332: 'Two string substitutions describe current and proposed vibration settings. A DS caller for this entry remains unbound.',
    333: 'Two string substitutions describe current and proposed automatic display of the Quick Guide. The separate DS Sailing Help literal is not a caller for this entry.',
    336: 'This two-argument generic statistic increase remains unbound. The neighboring modal and floating level notices use distinct original callers and only a name.',
}
SPANS = ((0x4833C, 0x483A4), (0x7E364, 0x7E3A8), (0x3A3DC, 0x3A454), (0x3E1EC, 0x3E294))
LITERALS = {0x48A2C: 334, 0x7E5B0: 335, 0x3A608: 337, 0x3E334: 342, 0x3E338: 343, 0x3E33C: 345}


def build_review():
    load, digest = previous.load, previous.digest
    assert not OUTPUT.exists()
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256']
    assert digest(release['candidate']) == release['candidate_sha256']
    clean_rom, current_rom = map(NdsImage.open, (CLEAN, release['candidate']))
    clean, arm = (rom.read_file(ARM) for rom in (clean_rom, current_rom))
    source = common_message_entries(clean_rom.read_file(COMMON), clean)
    common = current_rom.read_file(COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    current = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    inventory = load(previous.CALLS)
    assert inventory['source_rom_sha256'] == release['clean_input_sha256']
    # Stop the modal caller witness before the separately registered floating-notice code.
    caller_source = checked_text(inspect.getsource(previous.callers), {
        "end = row['file_offset'] + 12": "end = row['file_offset'] + (8 if number == 335 else 12)",
    })
    env = previous.callers.__globals__ | {'DATA': DATA, 'LEGACY_CONTEXT': {}}
    exec(compile(caller_source, __file__ + '::original-modal-caller-windows', 'exec'), env)
    callers = env['callers'](clean, arm, inventory)
    assert callers.keys() == DATA.keys()
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in SPANS)
    assert all(struct.unpack_from('<I', clean, offset)[0] == expected
               and clean[offset:offset + 4] == arm[offset:offset + 4]
               for offset, expected in LITERALS.items())
    assert [callers[n][0]['call'] for n in range(342, 346)] == list(range(0x0203E25C, 0x0203E275, 8))
    assert all(callers[n][0]['target'] == 0x020546B8 for n in DATA if n != 337)
    assert callers[337][0]['target'] == 0x0205528C
    assert struct.unpack_from('<I', clean, 0x3A428)[0] == 0xEB0068C3
    callers[337][0]['raw_notice_wrapper'] = 0x0205473C
    callers[337][0]['raw_notice_call_PC'] = 0x0203A428
    ledger = load(previous.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    done = {row['id'] for row in ledger[previous.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}

    def exact(n):
        jp, en = source[n], current[n]
        return dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, message_ID=n,
            source_reference=reference(jp), source_hex=jp.text.hex(), clean_Japanese=jp.text.decode('cp932'),
            current_reference=reference(en), current_hex=en.text.hex(), current_English=en.text.decode('cp932'),
            native_callers=callers.get(n, []), new_credit=0)

    records = []
    for n, (english, meaning, situation, note) in DATA.items():
        row = exact(n)
        assert row['id'] not in done
        count = row['clean_Japanese'].count('%s')
        assert count == english.count('%s') == row['current_English'].count('%s')
        records.append(row | dict(english=english, speaker='Narrator' if n >= 342 else 'System',
            source_meaning=meaning, context=situation, localization_note=note, native_substitution_count=count,
            decision='retention' if english == ' '.join(row['current_English'].split()) else 'revision',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    supporting = [exact(n) for n in (97, 316, 338, 339, 340, 341)]
    assert all(row['id'] in done for row in supporting)
    previous.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, credited_context=supporting, unbound=[exact(n) | {'context': note} for n, note in UNBOUND.items()],
        epilogue_original_state=3, epilogue_original_substate=1, epilogue_sequence=list(range(342, 346)),
        separate_ending_movie_and_save_state=4,
        clean_current_spans=[dict(runtime_address=previous.BASE + lo, exact_hex=clean[lo:hi].hex()) for lo, hi in SPANS],
        registered_predecessor=release['candidate'], registered_predecessor_sha256=release['candidate_sha256'],
        clean_ROM_sha256=release['clean_input_sha256'], new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, previous.CALLS, __file__)}))
    print('Reviewed seven caller-bound notices, including the complete four-panel epilogue.')


if __name__ == '__main__':
    build_review()
