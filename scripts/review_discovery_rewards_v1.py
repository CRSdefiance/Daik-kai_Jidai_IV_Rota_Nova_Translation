"""Bind discovery, recovery, acquisition and associated choices to original callers."""

import struct
from hashlib import sha256
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import review_setup_save_equipment_v1 as previous
from scripts.register_shipyard_fleet_setup_v1 import RELEASE
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference


OUTPUT = previous.OUTPUT.with_name('discovery_rewards_context_v1.json')
DATA = {
    288: ('Power increased by %s.',
          'Power, the displayed faction statistic, increased by the supplied amount.',
          'Four original notices pass the already formatted increase after a power-changing event.',
          'Express the amount as the change in Power. The full-width digits are produced by the game.'),
    292: ('It seems people in %s who follow trends are talking about this discovery.',
          'The discovery appears to be a topic of conversation among people who follow trends in the named city.',
          'The original discovery-report routine reads the name of the city that is discussing the discovery.',
          'Match the parallel local-news notice and preserve the qualified report, the city and its trend-following audience.'),
    297: ('Discovered %s.',
          'The game reports the discovery of the named place.',
          'Two original approach routines pass the settlement name from the selected model before proceeding to docking.',
          'The short current system notice fits discovery and leaves docking to the following prompt.'),
    298: ('Stop Auto Move?',
          'The game asks whether to stop automatic travel.',
          'Pressing the stop control during an active route opens this original yes/no confirmation. No leaves the route running. Yes requests manual sailing.',
          'Use the established Auto Move label and match the on-screen Stop Auto Move command.'),
    299: ("You can't assign crew here.",
          'A crew assignment cannot be made in this location.',
          'The Deck handler rejects a room that fails the original room predicate before it checks the selected actor’s qualifications.',
          'Name the action as a crew assignment. Keep the location-based reason distinct from the skill and language restrictions.'),
    301: ('You recovered %s gold from captured ships.',
          'The game reports the amount of money obtained from captured vessels.',
          'The original victory branch combines capture proceeds and passes the native formatted amount before crediting the player.',
          'Name the source of the gold. Captured ships describes the category of proceeds without supplying an exact ship count.'),
    302: ("Any trade goods you don't load will be discarded. Continue?",
          'Trade goods that have not been loaded will be discarded. The player is asked whether to proceed.',
          'The original cargo state 3 opens this yes/no branch. States 0 and 1 select the separate cargo-still-aboard prompt 268.',
          'State the consequence before asking for confirmation. Keep the distinction from cargo remaining aboard.'),
    303: ('You recovered %s barrels of food and %s barrels of water from captured ships.',
          'The captured ships yielded the supplied number of barrels of food and barrels of water.',
          'The original victory path computes two quantities separately and passes food first and water second.',
          'Restore barrels for both resources and make clear where the supplies came from.'),
    305: ('The nation awarded you %s gold.',
          'The player received the named monetary amount as a national reward.',
          'The original victory accounting selects this separate reward after computing the amount. It is distinct from the money recovered from ships.',
          'Keep the national award in a direct sentence and preserve the project’s gold terminology.'),
    311: ('You received %s gold.',
          'The player obtained the supplied amount of gold coins.',
          'The native event credits the player with the computed amount before reading this message.',
          'Complete the status sentence and keep the amount and gold unit. The source does not name the provenance of the award.'),
    313: ('Splish, splash!',
          'A small creature makes two quick splashing or flopping sounds.',
          'The shark scene plays this impersonal sound twice after the crew comments on the encounter and before they ask what to do with the creature.',
          'Use a light repeated sound appropriate for the small shark. Keep this as an impersonal effect.'),
    314: ('You got a baby shark!',
          'The player obtained the young shark.',
          'The scene explores what to do with the shark, including raising it. The original keep branch adds item 4 immediately after this notice.',
          'Use the established Baby Shark item term. The player already encountered the shark, so the line reports acquisition.'),
    340: ('You got %s!',
          'The player acquired the named item.',
          'The original item-acquisition branch passes the name returned by the item model after recording the transfer.',
          'Use a short, natural acquisition notice that also reads well with uncommon item names.'),
    341: ('%s joined!',
          'The named person joined the group.',
          'The original recruitment branch loads the message, then passes the composed character name to the separate raw-template notice wrapper.',
          'Keep the direct acknowledgement. It already names the recruit without inventing a position or restating the preceding exchange.'),
}
UNBOUND = {
    287: 'This exclamatory discovery entry is distinct from the positively bound settlement message 297.',
    296: 'This variable confirmation requires its native caller and argument. The full-width I remains a rendering lead.',
    300: 'The source chooses an attack opponent. Its original DS caller is still unbound.',
    304: 'The source forbids attacking a city occupied by an ally. The original DS caller is still unbound.',
}


def build_review():
    load, digest = previous.load, previous.digest
    assert not OUTPUT.exists()
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256'] and digest(release['candidate']) == release['candidate_sha256']
    clean_rom, current_rom = (NdsImage.open(path) for path in (CLEAN, release['candidate']))
    clean, arm = clean_rom.read_file(ARM), current_rom.read_file(ARM)
    source = common_message_entries(clean_rom.read_file(COMMON), clean)
    common = current_rom.read_file(COMMON)
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    current = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    inventory = load(previous.CALLS)
    assert inventory['source_rom_sha256'] == release['clean_input_sha256']
    context = FunctionType(previous.callers.__code__, {**previous.callers.__globals__, 'DATA': DATA, 'LEGACY_CONTEXT': {}})
    bindings = context(clean, arm, inventory)
    assert bindings.keys() == DATA.keys()
    spans = ((0x134BC, 0x134E0), (0x836C0, 0x836F4), (0x72174, 0x721C0), (0x722A0, 0x722C8),
             (0x71B90, 0x71BE8), (0x71C4C, 0x71CD8), (0x2BC24, 0x2BC58), (0x7EA8C, 0x7EADC))
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in spans)
    assert struct.unpack_from('<I', clean, 0x71C98)[0] == 0xE3A00004
    ledger = load(previous.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    done = {row['id'] for row in ledger[previous.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}

    def exact(n):
        jp, en = source[n], current[n]
        return dict(id=f'COMMON_MESSAGE_{n}', file_path=COMMON, message_ID=n,
            source_reference=reference(jp), source_hex=jp.text.hex(), clean_Japanese=jp.text.decode('cp932'),
            current_reference=reference(en), current_hex=en.text.hex(), current_English=en.text.decode('cp932'),
            native_callers=bindings.get(n, []), new_credit=0)

    records = []
    for n, (english, meaning, situation, note) in DATA.items():
        row = exact(n)
        assert row['id'] not in done
        count = row['clean_Japanese'].count('%s')
        assert count == english.count('%s') == row['current_English'].count('%s')
        records.append(row | dict(english=english, speaker='System', source_meaning=meaning, context=situation,
            localization_note=note, native_substitution_count=count,
            decision='retention' if english == ' '.join(row['current_English'].split()) else 'revision',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    supporting = [exact(n) for n in (268, 289, 290, 291, 293, 294, 295, 306, 307, 308, 309, 310, 312)]
    assert all(row['id'] in done for row in supporting)
    previous.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, credited_context=supporting,
        shark_exchange_context=[exact(n) for n in range(2425, 2454)],
        unbound=[exact(n) | dict(context=note) for n, note in UNBOUND.items()],
        clean_current_spans=[dict(runtime_address=previous.BASE + lo, exact_hex=clean[lo:hi].hex()) for lo, hi in spans],
        registered_predecessor=release['candidate'], registered_predecessor_sha256=release['candidate_sha256'],
        clean_ROM_sha256=release['clean_input_sha256'], new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, previous.CALLS, __file__)}))
    print('Reviewed 14 original caller-bound notices and read the full shark exchange for context.')


if __name__ == '__main__':
    build_review()
