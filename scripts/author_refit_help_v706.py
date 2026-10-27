"""Source-reviewed Refit paragraphs; layout belongs to the compiler."""

from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.trace_refit_text_v706 import IDS, ROOT
from scripts.verify_village_wrap_v608 import save

PROSE = {
    1248: 'A carpenter can repair damaged ships.',
    1249: "A ship's doctor can treat illnesses affecting officers and sailors.",
    1250: 'A chief cook saves water and food and helps sailors tire less quickly.',
    1251: 'Officers in this room recover their morale and help sailors tire less quickly.',
    1252: 'An animal keeper helps your food supplies last longer.',
    1253: "A missionary eases sailors' discontent and lets you distribute trade goods in the square.",
    1254: 'A strategist lets you plan schemes at the tavern.',
    1255: 'A purser lets you bargain and corner markets.',
    1268: 'A split sail improves square sail performance, increasing speed with the wind.',
    1269: 'A jigger spanker improves fore-and-aft performance, increasing speed against the wind.',
    1270: 'Extra armor increases durability but slightly reduces speed.',
    1271: 'Extra Armor 2 further increases durability but slightly reduces speed.',
    1272: 'A bow gun can fire ahead of the ship, but its shots have low power.',
    1273: 'A stern gun can fire behind the ship, but its shots have low accuracy.',
    1274: 'A ram lets you attack by ramming the side of an enemy ship.',
    1275: 'A marine captain increases boarding attack power. You can install up to four quarters.',
    1276: 'A gunner increases firing speed. You can install up to four quarters.',
    1277: 'This room stores water and food.',
    1278: 'Cargo holds carry trade goods. You can install up to five holds.',
    1279: 'You can add a cargo hold here, but it slightly reduces speed.',
    1280: 'You can add a ram or bow gun here. Medium and larger ships can also add a split sail.',
    1281: 'You can fit extra armor here.',
    1282: 'You can add a stern gun here. Large ships can also add a jigger spanker.',
    1283: 'You can mount a figurehead you own here.',
    1284: "You can change the ship's cannon type here.",
    1285: 'Lateen sails work well against the wind. You cannot put a square sail behind one.',
    1286: 'A topsail improves square sail performance, increasing speed with the wind.',
    1287: 'Square sails work well with the wind. You cannot put a lateen sail ahead of one.',
    1288: 'A staysail improves fore-and-aft performance, increasing speed against the wind.',
    1289: 'This sail improves both fore-and-aft and square sail performance.',
}

GLOSSES = {
    1248: 'A ship carpenter allows repair when a ship is damaged.',
    1249: 'A ship doctor can cure abnormal health conditions of navigators and sailors.',
    1250: 'A chief cook conserves water and food and makes sailors tire less easily.',
    1251: 'Navigators here refresh their mood and also make sailors tire less easily.',
    1252: 'An animal keeper slows food consumption.',
    1253: 'A missionary relieves sailor dissatisfaction and permits trade-good distribution in the square.',
    1254: 'A strategist allows schemes to be devised in taverns.',
    1255: 'A purser enables bargaining and buying out a market.',
    1268: 'A split sail raises square-sail performance and speed in a following wind.',
    1269: 'A jigger spanker raises fore-and-aft performance and speed against the wind.',
    1270: 'Additional armor raises durability but slightly reduces speed.',
    1271: 'Additional armor 2 raises durability further but slightly reduces speed.',
    1272: 'A bow gun allows forward cannon fire with low power.',
    1273: 'A stern gun allows rearward cannon fire with low accuracy.',
    1274: 'A ram permits a collision attack against an enemy ship side.',
    1275: 'A marine captain increases hand-to-hand attack power; at most four rooms may be installed.',
    1276: 'A gunner speeds up cannon fire; at most four rooms may be installed.',
    1277: 'This room carries water and food.',
    1278: 'This room carries trade goods; at most five rooms may be installed.',
    1279: 'A cargo hold can be added here with a slight speed loss.',
    1280: 'A ram or bow gun can be added here; medium and larger ships can add a split sail.',
    1281: 'Additional armor can be equipped here.',
    1282: 'A stern gun can be added here; a large ship can instead add a jigger spanker.',
    1283: 'A figurehead already owned can be installed here.',
    1284: 'The kind of cannon installed on the ship can be changed here.',
    1285: 'Lateen sails suit adverse wind; a square sail cannot be fitted behind a lateen sail.',
    1286: 'A topsail raises square-sail performance and speed in a following wind.',
    1287: 'Square sails suit a following wind; a lateen sail cannot be fitted ahead of a square sail.',
    1288: 'A staysail raises fore-and-aft performance and speed against the wind.',
    1289: 'This sail improves both fore-and-aft and square-sail performance relative to a square sail.',
}


def main():
    clean = NdsImage.open('work/clean.nds')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    path = '/COMMON/MESFILE.DK4'
    original = common_message_entries(clean.read_file(path), clean.read_file('/__arm9__.bin'))
    baseline = common_message_entries(canonical.read_file(path), canonical.read_file('/__arm9__.bin'), clean=False)
    assert tuple(PROSE) == IDS and set(GLOSSES) == set(IDS)
    rows = []
    for message_id in IDS:
        source, accepted = original[message_id], baseline[message_id]
        rows.append({'id': f'REFIT_HELP_{message_id}', 'message_id': message_id,
            'clean_source_hex': source.text.hex(), 'clean_source_Japanese': source.text.decode('cp932'),
            'canonical_source_hex': accepted.text.hex(),
            'english': PROSE[message_id], 'speaker': 'Ship component or crew-room help',
            'context': 'Original stable COMMON message ID used by the Refit component/help family; separate from spoken shipyard IDs1256..1267.',
            'source_meaning': GLOSSES[message_id],
            'localization_note': 'Preserve the stated effect, limitation, count and equipment category in natural US English. Generate all line breaks in the consumer-specific formatter; author no indentation or line breaks.',
            'review': dict.fromkeys(('source', 'context', 'localization', 'naturalness', 'formatting'), True)})
    manuscript = {'format': 'dk4-refit-help-manuscript-v1', 'translation_policy': 'natural-dialogue-v2',
        'target_locale': 'en-US', 'encoder': 'dialogue-relocatable-v1',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'],
        'source_clean_COMMON_sha256': sha(clean.read_file(path)),
        'source_canonical_COMMON_sha256': sha(canonical.read_file(path)),
        'layout_authoring': 'One natural paragraph; original consumer native verification remains a separate gate.',
        'records': rows}
    validate_natural_dialogue_batch(manuscript)
    save('translations/refit_help_manuscript_v1.json', manuscript)
    save(ROOT / 'editorial_review.json', {'source': 'clean Japanese COMMON native IDs, not current reblocked record ordinals',
        'all30_source_meanings_reviewed': True, 'original_room_limits_and_sail_placement_restrictions_preserved': True,
        'no_authored_breaks_indentation_or_placeholder_prose': True,
        'actual_renderer_all30_and_integrated_build_verification_pending': True,
        'author_sha256': sha(Path(__file__).read_bytes())})
    print('V706 all30 source-reviewed natural paragraphs authored; native layout and release gates remain pending.', flush=True)


if __name__ == '__main__':
    main()
