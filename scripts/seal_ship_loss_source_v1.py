"""Read the complete native crew-loss and abandon-confirmation variants from clean Japanese."""

import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.audit_story_glyph_consistency import save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.seal_shared_text_source_v1 import reference


ROOT = Path('translations/editorial_checkpoints/ShipLoss_20261110_v1')
SOURCE = ROOT/'clean_first_drafts.json'
CLEAN = Path('work/clean.nds')
DRAFTS = {
    338: ("%s has sunk!", "A neutral announcement that the named ship sank."),
    339: ("%s has no sailors left!", "A neutral announcement that there is no sailor left on the named ship."),
    2663: ("%s has sunk!", "A polite but urgent report of the ship sinking."),
    2664: ("%s went down!", "A compressed, emphatic report. Keep the punch of the original fragments."),
    2665: ("%s went down!", "Casual alarm at the ship having gone down."),
    2666: ("%s has gone down!", "A forceful report using the original emphatic ending."),
    2667: ("%s has gone down!", "The clean line exactly matches the neighboring voice slot. Keep the two slots distinct."),
    2668: ("Oh no, %s went down!", "The informal elongated ending expresses dismay."),
    2669: ("%s has sunk!", "A formal emphatic announcement of the ship sinking."),
    2670: ("%s has no sailors left!", "A polite urgent report that every sailor is gone."),
    2671: ("There are no sailors aboard %s!", "A polite report of absence, without claiming how it happened."),
    2672: ("%s doesn't have a single sailor left!", "A casual emphatic warning about the empty crew."),
    2673: ("%s hasn't got a sailor left!", "A rougher emphatic report, without adding a rank or relationship."),
    2674: ("There's not a sailor left aboard %s!", "A gruff report that there are no sailors remaining."),
    2675: ("Oh no, %s has no sailors left!", "The drawn-out casual ending conveys dismay."),
    2676: ("%s has no sailors aboard!", "A polite emphatic report. Preserve the observed absence."),
    2677: ("You're sure? We'll abandon %s.", "The polite speaker checks the decision before saying the ship will be discarded."),
    2678: ("It can't be helped. We'll abandon %s, then.", "The speaker reluctantly accepts the choice and states the action."),
    2679: ("Are we really abandoning %s?", "The casual question asks whether the player truly wants to discard the ship."),
    2680: ("So we're abandoning %s, right?", "An informal check that the decision to discard the ship is correct."),
    2681: ("It can't be helped. We'll abandon %s, then.", "The gruff speaker is resigned to discarding the ship. The source does not assign a rank."),
    2682: ("We'll abandon %s, then. You're sure?", "A casual speaker states the intended action and checks that the player agrees."),
}
TABLES = [(0x2C640,0x02116EE0,'sunk-personality'),
          (0x2C648,0x02116F60,'empty-crew-personality'),
          (0x2C658,0x02117000,'abandon-confirmation-personality')]


def main():
    assert not ROOT.exists()
    assert digest(CLEAN) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image = NdsImage.open(CLEAN)
    arm = image.read_file('/__arm9__.bin')
    entries = common_message_entries(image.read_file('/COMMON/MESFILE.DK4'), arm)
    groups = {}
    tables = []
    for field, pointer, name in TABLES:
        assert struct.unpack_from('<I', arm, field)[0] == pointer
        raw = arm[pointer-0x02000000:pointer-0x02000000+32]
        slots = struct.unpack('<8i', raw)
        tables.append(dict(name=name, field=field, pointer=pointer, table_hex=raw.hex(), slots=slots))
        for slot, n in enumerate(slots):
            if n != -1:
                assert n not in groups
                groups[n] = dict(group=name, native_personality_slot=slot)
    for n, field, name in [(338,0x2C63C,'sunk-system'), (339,0x2C644,'empty-crew-system')]:
        assert struct.unpack_from('<I', arm, field)[0] == n
        groups[n] = dict(group=name, literal_field=field)
    assert set(groups) == set(DRAFTS) and len(groups) == 22
    rows = []
    for number, (english, meaning) in sorted(DRAFTS.items()):
        row = entries[number]
        assert row.text.count(b'%s') == english.count('%s') == 1
        rows.append(dict(id=f'COMMON_MESSAGE_{number}', message_ID=number, file_path='/COMMON/MESFILE.DK4',
            **groups[number], source_reference=reference(row), source_hex=row.text.hex(),
            clean_Japanese=row.text.decode('cp932'), clean_source_meaning=meaning, independent_English=english,
            new_credit=0, current_template_comparison_pending=True))
    ROOT.mkdir(parents=True)
    save(SOURCE, dict(clean_ROM=str(CLEAN), clean_ROM_sha256=digest(CLEAN), native_personality_tables=tables,
        records=rows, records_count=22, context='The original fleet scan can report a sunk ship or an empty crew. '
        'The latter leads to Assign Sailors while other crew remain. Back can open the named abandonment confirmation. No returns to the menu.',
        incidental_existing_English_observed_in_two_live_messages_before_clean_draft=True,
        current_stored_templates_not_extracted_before_drafts=True,
        all_native_fallback_slots_preserved=True, broader_editorial_scope_active=True,
        current_comparison_andformatting_pending=True, new_credit=0, full_goal_complete=False))
    print('Saved 22 source-first crew-loss and abandonment drafts, with complete native voice tables.')


if __name__ == '__main__':
    main()
