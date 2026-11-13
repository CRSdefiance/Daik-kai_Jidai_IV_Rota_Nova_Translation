"""Review the ten artifact rumors selected by the original Ancient Map exchange."""

from collections import Counter
from hashlib import sha256
from struct import unpack_from
from unicodedata import normalize

from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_arrival_month_labels_v1 as parent
from scripts import review_treasure_map_documents_v1 as map_review
from scripts.probe_common_display_name_hook import branch_link
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.seal_shared_text_source_v1 import reference


base, BASE, ARM, COMMON, CLEAN = map_review.base, map_review.BASE, map_review.ARM, map_review.COMMON, map_review.CLEAN
OUTPUT = map_review.OUTPUT.with_name('ancient_map_rumors_context_v1.json')
CONTEXT = ('The native informant tells the player that the Ancient Map may lead to legendary treasure, '
           'then describes the rumored artifact. The same artifact index selects the inscription in the '
           'map document. This is a spoken account with its own hearsay, doubts and reactions.')
DECISIONS = {
    3658: ("They say it's a strange jewel the color of a blazing fire.", 'Keep the story attributed and the color comparison vivid.'),
    3659: ("They say it's an ancient dagger with writing on it. I doubt anyone can still read it.", 'Keep the report about the dagger and inscription, and preserve the speaker’s doubt about reading it.'),
    3660: ("I hear priests used this stone mask long ago. It's carved with an eerie serpent pattern.", 'Keep the ancient priests, stone mask and eerie carving in two natural spoken beats.'),
    3661: ("It's a crimson crystal. They say you can see a star-shaped pattern inside if you hold it up to the light.", 'Keep the crystal’s color, the shape of the pattern and the action that reveals it.'),
    3662: ("They say it's a strange crystal with a diamond inside. A jewel that eats jewels, they call it.", 'Keep the reported diamond and the playful jewel-eating image.'),
    3663: ("They say that sword is sharp enough to cut without touching a thing. Who knows if it's true?", 'Keep the impressive sharpness and make clear that cutting without contact is a doubtful story.'),
    3664: ("I hear it's a statue of a Siren, once used as a figurehead. Who'd put a witch that wrecks ships on the bow?", 'Keep the reported figurehead and the informant’s incredulity about its subject.'),
    3665: ("They say it's a twisted horn. Some say it's a dragon's. I hear you can make medicine from it that cures any illness.", 'Keep the shape, possible origin and separate medicinal rumor.'),
    3666: ("They say it was a great king's shield, with a goddess pictured on it. Sailors say there's no better charm.", 'Keep the king, the depiction and the sailors’ reported preference.'),
    3667: (None, 'Keep the reported size and the ability to drive away evil. Trim legacy padding.'),
}


def main():
    assert not OUTPUT.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256'] and base.digest(base.REGISTRY) == release['registry_sha256']
    runtime = RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    source = base.NdsImage.open(CLEAN)
    arm = source.read_file(ARM)
    assert base.digest(CLEAN) == release['clean_input_sha256']
    assert arm[0x5C188:0x5C1D0] == runtime.arm[0x5C188:0x5C1D0]
    assert arm[0x5C450:0x5C460] == runtime.arm[0x5C450:0x5C460]
    assert unpack_from('<III', arm, 0x5C454) == (0x023800CC, 0x02143D20, 3658)
    assert unpack_from('<I', arm, 0x5C1CC)[0] == branch_link(BASE + 0x5C1CC, BASE + 0x53FE4)
    assert unpack_from('<I', arm, 0x5C1BC)[0] == branch_link(BASE + 0x5C1BC, BASE + 0x54020)
    assert unpack_from('<I', arm, 0x5B22C)[0] == branch_link(BASE + 0x5B22C, BASE + 0x5C108)
    assert arm[0x5B208:0x5B230] == runtime.arm[0x5B208:0x5B230]
    jp = common_message_entries(source.read_file(COMMON), arm)
    en = owned_entries(runtime.common, runtime.arm, sha256(runtime.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest())
    historical = {row['message_id']: row for row in base.load(map_review.SOURCE)['records']}
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    cpu, get, _ = runtime.machine(runtime.arm, runtime.common, runtime.raw, runtime.plan)
    catalog = get(0xCB190) + 4

    def word(at):
        return unpack_from('<I', cpu.mem_read(at, 4))[0]

    records = []
    for number, (replacement, note) in DECISIONS.items():
        key = f'COMMON_MESSAGE_{number}'
        assert key not in credited and jp[number].text.hex() == historical[number]['source_hex'].lower()
        current = en[number].text.decode('cp932')
        logical = ' '.join(normalize('NFKC', current).split())
        english = replacement or logical
        assert english.isascii() and (english != logical) == bool(replacement)
        assert '%' not in english and b'%' not in jp[number].text and b'%' not in en[number].text
        artifact = number - 3658 + 188
        actor = catalog + 20 * artifact
        getter = word(word(actor) + 8)
        ptr = get(getter - BASE, actor)
        name = bytes(cpu.mem_read(ptr, 48)).split(b'\0')[0]
        assert name and name.isascii()
        records.append(dict(id=key, message_ID=number, file_path=COMMON, source_reference=reference(jp[number]),
            current_reference=reference(en[number]), source_Japanese=jp[number].text.decode('cp932'),
            source_hex=jp[number].text.hex(), current_English=current, current_hex=en[number].text.hex(),
            english=english, context=CONTEXT, speaker='Ancient Map informant', source_meaning=historical[number]['source_meaning'],
            localization_note=note, decision='revision' if replacement else 'retention',
            artifact_ID=artifact, original_name_getter=getter, current_item_name=name.decode('ascii'),
            companion_inscription=3648 + artifact - 188, original_substitution_count=0,
            review={gate: gate != 'formatting' for gate in map_review.GATES}))
    assert bytes(cpu.mem_read(runtime.actor_root, 0x1A04)) == runtime.actor_bytes
    counts = dict(Counter(row['decision'] for row in records))
    base.save(OUTPUT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=map_review.GATES, records=records, counts=counts, registered_input=runtime.receipt(),
        original_caller=0x0205C1CC, original_consumer=0x02053FE4,
        original_native_selection_code_hex=arm[0x5C188:0x5C1D0].hex(),
        original_menu_dispatch=0x0205B22C, original_runtime_item_table=0x023800CC,
        original_preamble_reference=0x02143D20,
        original_preamble_Japanese=arm[0x143D20:0x143DB0].split(b'\0')[0].decode('cp932'),
        current_preamble_English=runtime.arm[0x143D20:0x143DB0].split(b'\0')[0].decode('cp932'),
        formatting_pending=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} Ancient Map rumor decisions {counts}, with item names and companion inscriptions bound.')


if __name__ == '__main__':
    main()
