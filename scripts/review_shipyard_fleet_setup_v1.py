"""Review the original shipyard and regional fleet setup exchanges."""

import struct
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import review_setup_save_equipment_v1 as previous
from scripts.register_setup_save_equipment_v1 import RELEASE
from scripts.seal_shared_text_source_v1 import ARM, CLEAN, COMMON, reference


OUTPUT = previous.OUTPUT.with_name('shipyard_fleet_setup_context_v1.json')
DATA = {
    261: ("This news seems to be making the rounds among people in %s who follow the latest trends.",
          "This news seems to be a topic of conversation among people who follow trends in the named city.",
          "The original report first marks the local news, then supplies the city name from the selected city's getter.",
          "Replace the unrelated placeholder with a report of what people are talking about. Keep the qualified claim and the interest group."),
    262: ("You have too many ships!",
          "The player already owns too many ships.",
          "Both ordinary and copy-build entry checks stop the purchase when the ship ownership table has no room.",
          "Restore a complete warning confined to the ownership limit. Leave shipyard availability to 263."),
    263: ("No ships can be built here!",
          "No ships are available to build in this city.",
          "The yard has passed the ownership check but the original town-specific build list is empty.",
          "Restore the complete local availability warning from the Japanese. Keep it independent of funds and ownership."),
    264: ("Not enough money!",
          "The player does not have enough money.",
          "The Buy branch compares the current funds against the offered price and returns to selection after showing this warning.",
          "The short current warning suits the failure and preserves the emphatic source. Keep its simple distinction from the other yard refusals."),
    265: ("Buy this ship?",
          "The game asks whether to purchase the selected ship.",
          "The original confirmation follows ship selection and the affordability check. Yes proceeds to purchase, and No leaves the purchase unmade.",
          "The current question is natural and clearly identifies the selected ship."),
    266: ("Give your ship a name!",
          "The player is asked to name the ship.",
          "The original purchase path opens the ship name entry and can repeat this prompt during its naming loop.",
          "The current friendly imperative fits the naming screen. Keep it distinct from the purchase and acceptance prompts."),
    268: ("There's still cargo aboard. Continue?",
          "Cargo is still on board. The game asks whether to proceed.",
          "The cargo check selects this generic confirmation for the residual-cargo states 0 and 1. State 3 has the separate discard warning 302.",
          "Use ordinary spoken English and keep the fact that cargo is still aboard. The other branch gives the more specific consequence."),
    269: ("Choose the ship whose captain you want to change.",
          "Select the ship whose captain will be changed.",
          "The original ship chooser opens before candidate selection. A flagship selection can first produce the room warning and confirmation.",
          "Keep this clear instruction. Generate wraps for the full sentence at the native modal width."),
    270: ("A sailor will take command.",
          "The captaincy will be entrusted to someone subordinate.",
          "The original fallback detects that the current captain uses a generic sailor ID and shows a result instead of asking to relieve a named officer.",
          "State the result in plain language. The original fallback and the companion prompt support sailor without inventing a named officer."),
    271: ("Choose a crew member to serve as captain.",
          "Choose a navigator to appoint as captain.",
          "The original candidate list opens after ship selection and any flagship warning.",
          "Keep the established crew wording for the selectable officers. Describe what the chosen person will do rather than assigning a rank before selection."),
    272: ("Changing the flagship may remove crew from their room assignments.",
          "Changing the flagship can cause crew members assigned to ship rooms to lose their assignments.",
          "The original flagship checks present the warning immediately before the generic yes/no question 273.",
          "Keep the possibility and the affected room assignments. The warning concerns assignments aboard ship."),
    273: ("Continue?",
          "The game asks the player to confirm proceeding.",
          "Four original callers use this separate yes/no question after the flagship warning 272.",
          "Restore the short standalone confirmation. The current stored prefix belongs to the different captain-removal question 274."),
    274: ("Relieve the captain and let a sailor take command?",
          "Relieve the captain and put a subordinate sailor in charge?",
          "This is the original confirmation when the player has left the crew chooser with a named captain still on the ship.",
          "Restore the full choice and distinguish a sailor taking command from the earlier warning about room assignments."),
    275: ("You need 100,000 gold to form a regional fleet.",
          "Creating a regional fleet requires 100,000 gold coins.",
          "The formation routine checks current funds against the original 100000 literal before it opens admiral selection.",
          "Use a direct explanation with the exact cost and the established regional fleet term."),
    276: ("You already have seven fleets!",
          "There are already seven fleets.",
          "The original empty fleet-slot lookup returns its sentinel and ends formation before the player can select an admiral.",
          "Say who has the fleets in a complete sentence. The warning preserves the source count."),
    277: ("Choose which ships to add to the new fleet.",
          "Select the ships to include in the new fleet.",
          "The original flow asks for ships after the admiral is accepted. It populates the new fleet from the available ships.",
          "Restore the purpose of selection so the player knows why the list opened."),
    278: ("Choose an admiral for the new fleet.",
          "Choose the admiral of the new fleet.",
          "The original admiral list opens before the name confirmation and ship selection.",
          "Identify the new fleet explicitly and preserve the rank the source uses."),
    279: ("Make %s %s the new fleet's admiral?",
          "Make the person identified by these two name parts the admiral?",
          "The original Yes/No call receives the selected crew member's given name and surname in that order.",
          "Put the two name parts together as a name and identify the job. Remove the invented association implied by 'of'."),
    280: ("Choose a fleet to reorganize.",
          "Choose which fleet to organize.",
          "The original fleet-list helper selects this when its mode is 0. The reorganize path can then ask whether to change orders.",
          "Use a clear instruction suited to an existing fleet. Replace the unrelated storage fragment."),
    281: ("Choose a fleet to disband.",
          "Choose the fleet to disband.",
          "The same list helper selects this when its mode is 1. The original flow later asks for confirmation in 285.",
          "Use the same disband wording as the confirmation. The current storage contains an unrelated fragment."),
    282: ("Choose orders and a target city for the fleet.",
          "The fleet must be given orders and a city to target.",
          "The formation handler repeats its order-and-city menu while the original status remains the unset sentinel.",
          "Make the missing requirements actionable. Target city covers the distinct patrol, attack, base and port-call routes."),
    283: ("Change this fleet's orders?",
          "The game asks whether to change the newly organized fleet's orders.",
          "The native reorganize flow asks this after setting up the selected fleet's ships. Yes opens orders; No skips that menu.",
          "The current question is concise and identifies the selected fleet."),
    285: ("Disband this fleet?",
          "The game asks whether to disband the selected fleet.",
          "The original confirmation follows fleet selection. No returns without disbanding; Yes shows the separate dock result.",
          "The current question is natural. Keep the effect on individual ships in the follow-up."),
    286: ("We'll put all the ships in the dock.",
          "Each ship will be left in dock.",
          "The original follow-up plays only after the player confirms disbandment and immediately precedes the dock transfer.",
          "Make the destination clear and account for every ship. Use the established dock term."),
}
HOLD = {
    284: ("This fleet is in the red, and you don't have enough money to cover its debt.",
          "The fleet is running a deficit and the player does not have enough money to pay off its debt.",
          "The current storage is unrelated. The DS disband routine's adjacent call to 0203FA9C returns immediately; no source-qualified caller for 284 has been established."),
}


def original_bindings(clean, arm, inventory):
    additional = [(264, 0x63518), (280, 0x5A4E8), (281, 0x5A4E8), (282, 0x5A854)]
    rows = [*inventory['calls'], *(dict(message_id=n, file_offset=at, runtime_address=previous.BASE + at,
        target=0x020546B8, argument_register='r0', component='arm9') for n, at in additional)]
    env = {**previous.callers.__globals__, 'DATA': DATA, 'LEGACY_CONTEXT': {}}
    bindings = FunctionType(previous.callers.__code__, env)(clean, arm, {'calls': rows})
    spans = ((0x633B0, 0x633C8), (0x63510, 0x63528), (0x5A4BC, 0x5A524),
             (0x5A828, 0x5A864), (0x5A8F4, 0x5A8F8), (0x5A684, 0x5A6E8),
             (0x5A5D0, 0x5A620), (0x5A8D4, 0x5A8DC), (0x3FA9C, 0x3FAA0))
    assert all(clean[lo:hi] == arm[lo:hi] for lo, hi in spans)
    assert struct.unpack_from('<I', clean, 0x633BC)[0] == 0xE3A0BF42
    assert struct.unpack_from('<I', clean, 0x5A520)[0] == 281
    assert struct.unpack_from('<I', clean, 0x5A8F4)[0] == 282
    assert struct.unpack_from('<I', clean, 0x5A8D4)[0] == 100000
    assert clean[0x3FA9C:0x3FAA0] == bytes.fromhex('1eff2fe1')
    assert set(bindings) == DATA.keys()
    return bindings, [dict(runtime_address=previous.BASE + lo, exact_hex=clean[lo:hi].hex()) for lo, hi in spans]


def main():
    load, digest = previous.load, previous.digest
    assert not OUTPUT.exists()
    release = load(RELEASE)
    assert digest(CLEAN) == release['clean_input_sha256'] and digest(release['candidate']) == release['candidate_sha256']
    source, target = (NdsImage.open(path) for path in (CLEAN, release['candidate']))
    clean, arm = (rom.read_file(ARM) for rom in (source, target))
    jp = common_message_entries(source.read_file(COMMON), clean)
    common = target.read_file(COMMON)
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    en = owned_entries(common, arm, sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    inventory = load(previous.CALLS)
    assert inventory['source_rom_sha256'] == release['clean_input_sha256']
    bindings, spans = original_bindings(clean, arm, inventory)
    ledger = load(previous.LEDGER)
    assert ledger['current_integrated_candidate']['sha256'] == release['candidate_sha256']
    done = {row['id'] for row in ledger[previous.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}

    def exact(n):
        source_row, previous_row = jp[n], en[n]
        return dict(message_ID=n, file_path=COMMON, id=f'COMMON_MESSAGE_{n}',
            source_reference=reference(source_row), source_hex=source_row.text.hex(), clean_Japanese=source_row.text.decode('cp932'),
            current_reference=reference(previous_row), current_hex=previous_row.text.hex(), current_English=previous_row.text.decode('cp932'),
            native_callers=bindings.get(n, []), new_credit=0)

    records = []
    for n, (english, meaning, context, note) in DATA.items():
        row = exact(n)
        assert row['id'] not in done and row['native_callers']
        macro_count = row['clean_Japanese'].count('%s')
        assert macro_count == english.count('%s') == row['current_English'].count('%s')
        records.append(row | dict(speaker='System', english=english, source_meaning=meaning, context=context,
            localization_note=note, native_substitution_count=macro_count,
            decision='retention' if english == ' '.join(row['current_English'].split()) else 'revision',
            review=dict(source=True, context=True, localization=True, naturalness=True, formatting=False)))
    anchor = exact(267)
    assert anchor['id'] in done
    assert len(records) == 24
    previous.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'],
        records=records, already_credited_context=[anchor],
        pending_consumer=[exact(n) | dict(english=english, source_meaning=meaning, context=context)
                          for n, (english, meaning, context) in HOLD.items()],
        clean_current_supporting_spans=spans, registered_predecessor=release['candidate'],
        registered_predecessor_sha256=release['candidate_sha256'], clean_ROM_sha256=release['clean_input_sha256'],
        source_and_context_ready=True, new_completion_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (RELEASE, previous.CALLS, Path(__file__))}))
    print('Reviewed 24 source-bound shipyard and fleet records; 267 supplies credited context and 284 remains open.')


if __name__ == '__main__':
    main()
