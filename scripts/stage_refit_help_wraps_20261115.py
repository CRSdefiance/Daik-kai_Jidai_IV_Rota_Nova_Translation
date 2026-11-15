"""Review and stage the shipyard Refit help as a single related set."""

from dataclasses import replace
from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.refit_help import PROFILE, compile_paragraph
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_OFFSET, common_message_entries
from scripts import register_name_or_words_confirmation_20261114 as parent
from scripts.review_sound_bgm_titles_v1 import reference
from scripts.verify_release_baseline import files


base = parent.base
ARM, COMMON, CLEAN, GATES = parent.stage.ARM, parent.stage.COMMON, parent.stage.CLEAN, parent.stage.GATES
ROOT = Path('work/refit_help_wraps_20261115_v1')
ROM = ROOT / 'Refit_Help_Wraps_RESEARCH_ONLY.nds'
STORED = ROOT / 'staged.json'
REVIEW = Path('translations/editorial_checkpoints/SharedText_20261110_v1/refit_help_wraps_context_20261115_v1.json')

REVISIONS = {
    1268: ('Fit a spritsail to improve square sail performance and sail faster downwind.',
           'The bow fitting improves square sail performance and makes the ship faster with the wind.',
           'Keep the approved Spritsail name. Use the direct fitting instruction and let square sail performance read together.'),
    1274: ('With a ram, you can strike the side of an enemy ship.',
           'Installing a ram enables a collision attack against the side of an enemy ship.',
           'The ram supplies the means of attack. The second line keeps the complete target together.'),
    1275: ('A marine captain improves attack power when boarding. Fit up to four rooms.',
           'Having a marine captain raises attack power in boarding combat. The player can install at most four rooms of this kind.',
           'Keep the officer, the combat effect and the four-room maximum on complete phrases.'),
    1276: ('Gunners speed up gunfire. Fit up to four gun decks.',
           'Having a gunner speeds up cannon fire. The player can install at most four rooms of this kind.',
           'Name the gun deck and put its full limit on one line. The first line describes the crew effect in plain language.'),
    1278: ('Keep your trade goods here. Fit up to five cargo holds.',
           'This room stores trade goods. The ship can have at most five.',
           'The destination and the five-hold limit each form one line. The English calls the room a cargo hold.'),
    1286: ('Fit a topsail to improve square sail performance and sail faster downwind.',
           'A topsail improves square sail performance and makes the ship faster with the wind.',
           'Use the same sentence pattern as the spritsail because the source describes the same two effects.'),
}
RETENTIONS = {
    1247: 'The cabin note distinguishes officer health and morale from the effects on sailors in the other rooms.',
    1248: 'The carpenter can repair damage. The wording leaves the kind of damage and number of ships to the game.',
    1249: 'The doctor helps both officers and sailors. The existing wording covers ailments without naming diseases.',
    1250: 'The cook conserves food and water and slows sailors’ fatigue. Both effects are clear.',
    1251: 'Officers recover morale here and help sailors tire less quickly. The current wording keeps those roles distinct.',
    1252: 'The animal keeper makes food last longer. The wording preserves the supply effect and gives no water bonus.',
    1253: 'The missionary addresses sailors’ discontent and enables distribution of trade goods in the Square. Both mechanical effects read clearly.',
    1254: 'The strategist enables planning schemes specifically at the tavern, consistent with the menu action.',
    1255: 'The two short verbs preserve the purser’s separate bargaining and market-cornering actions.',
    1269: 'The jigger spanker improves fore-and-aft performance and speed against the wind. The current break keeps the performance term together.',
    1270: 'The durability benefit and the small speed cost read in the same order as the source.',
    1271: 'The title matches the second armor level and the word “further” states its stronger durability bonus.',
    1272: 'The bow gun can shoot forward. The warning about weak shots stays distinct from the stern gun’s accuracy warning.',
    1273: 'The stern gun can shoot behind the ship and has poor accuracy. The English keeps both facts explicit.',
    1277: 'The room holds both food and water. The short description suits the storage tooltip.',
    1279: 'The position can take another cargo hold with a slight speed penalty. The existing sequence presents the option before its cost.',
    1280: 'The bow instructions distinguish the ram and bow gun from the spritsail’s medium-or-larger ship requirement.',
    1281: 'The direct fitting instruction is clear in the armor slot.',
    1282: 'The slot supports a stern gun, with a jigger spanker also available on a large ship.',
    1283: 'The wording tells the player where to mount a figurehead they already own.',
    1284: 'The wording identifies the editable cannon type in the selected slot.',
    1285: 'The description gives an against-the-wind advantage, then prohibits a square sail behind a lateen sail.',
    1287: 'The description gives the corresponding following-wind advantage and prohibits a lateen sail ahead of a square sail.',
    1288: 'The staysail entry uses the same fore-and-aft term and wind direction as the jigger spanker entry.',
    1289: 'The description identifies a square sail and explicitly names its two performance categories.',
}
CONTEXT = {
    range(1247, 1256): 'The player inspects a crew room in the shipyard Refit view. The help describes the effect of the assignment.',
    range(1268, 1275): 'The player inspects a fitting in the shipyard Refit view. The help states its effect in sailing or combat.',
    range(1275, 1280): 'The player inspects a room or hold in the shipyard Refit view. The help gives its purpose and applicable limits or costs.',
    range(1280, 1285): 'The player inspects a slot in the shipyard Refit view. The help identifies compatible fittings or the action available here.',
    range(1285, 1290): 'The player compares sails in the shipyard Refit view. The help explains wind effects, placement restrictions, or performance.',
}


def main():
    assert not ROOT.exists() and not REVIEW.exists()
    release = base.load(parent.RELEASE)
    assert base.digest(parent.ROM) == release['candidate_sha256']
    assert base.digest(CLEAN) == release['clean_input_sha256']
    clean, current = map(base.NdsImage.open, (CLEAN, parent.ROM))
    before = files(current)
    arm, common = before[ARM], before[COMMON]
    assert sha256(arm).hexdigest() == release['target_ARM9_sha256']
    assert sha256(common).hexdigest() == release['target_COMMON_sha256']
    directory = sha256(arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    previous = owned_entries(common, arm, directory)
    original = common_message_entries(clean.read_file(COMMON), clean.read_file(ARM))
    ledger = base.load(base.LEDGER)
    credited = {row['id'] for row in ledger[base.CONTEXT]['integrated_record_keys'] if row['file_path'] == COMMON}
    assert set(REVISIONS).isdisjoint(RETENTIONS)
    assert set(REVISIONS) | set(RETENTIONS) == {i for family in CONTEXT for i in family}
    old_blocks = IlnkContainer.parse(common).blocks
    blocks = list(old_blocks)
    rows, slots = [], {}
    for n in sorted(REVISIONS.keys() | RETENTIONS.keys()):
        source, current_record = original[n], previous[n]
        id_key = f'COMMON_MESSAGE_{n}'
        assert id_key in credited
        assert all(b'%' not in row.text for row in (source, current_record))
        current_prose = ' '.join(current_record.text.decode('ascii').split())
        assert compile_paragraph(current_prose)[0] == current_record.text + b'\0'
        if n in REVISIONS:
            english, meaning, reason = REVISIONS[n]
        else:
            english, meaning, reason = current_prose, RETENTIONS[n], RETENTIONS[n]
        compiled, lines = compile_paragraph(english)
        if n in REVISIONS:
            block, lo, hi = current_record.block, current_record.block_offset, current_record.copy_end
            raw = blocks[block][lo:hi]
            assert block == 16 and raw == current_record.text + b'\0' and len(compiled) <= len(raw)
            replacement = compiled.ljust(len(raw), b'\0')
            blocks[block] = blocks[block][:lo] + replacement + blocks[block][hi:]
            slots[n] = dict(block=block, start=lo, end=hi, before=raw.hex(), after=replacement.hex(),
                            compiled_body=compiled[:-1], skipped_fields=len(raw) - len(compiled))
        context = next(explanation for family, explanation in CONTEXT.items() if n in family)
        rows.append(dict(id=id_key, message_id=n, file_path=COMMON, speaker='Refit help', english=english,
            decision='revision' if n in REVISIONS else 'retention', source_meaning=meaning,
            localization_note=reason, context=context, review=dict.fromkeys(GATES, True) | {'formatting': False},
            source_reference=reference(source), current_reference=reference(current_record),
            Japanese=source.text.decode('cp932'), previous_English=current_record.text.decode('ascii'),
            exact_clean_hex=source.text.hex(), exact_current_hex=current_record.text.hex(),
            staged_hex=compiled[:-1].hex(), generated_lines=lines, existing_credit=True))
    deployed = IlnkContainer(blocks).to_bytes()
    after = owned_entries(deployed, arm, directory)
    for a, b in zip(previous, after, strict=True):
        adjustment = sum(slot['skipped_fields'] for slot in slots.values()
                         if slot['block'] == a.block and slot['end'] <= a.block_offset)
        new_text = slots[a.message_id]['compiled_body'] if a.message_id in slots else a.text
        assert replace(a, record_index=a.record_index + adjustment, text=new_text, end=a.start + len(new_text)) == b
    for row in rows:
        row['staged_reference'] = reference(after[row['message_id']])
    inverse = list(blocks)
    for slot in slots.values():
        i, lo, hi = slot['block'], slot['start'], slot['end']
        inverse[i] = inverse[i][:lo] + bytes.fromhex(slot['before']) + inverse[i][hi:]
        slot['compiled_body'] = slot['compiled_body'].hex()
    assert IlnkContainer(inverse).to_bytes() == common
    assert [i for i, (a, b) in enumerate(zip(old_blocks, blocks, strict=True)) if a != b] == [16]
    current.replace_file(COMMON, deployed)
    changed = files(current)
    assert before.keys() == changed.keys() and {p for p in before if before[p] != changed[p]} == {COMMON}
    ROOT.mkdir()
    current.save(ROM)
    current.replace_file(COMMON, common)
    assert bytes(current.rom.save()) == parent.ROM.read_bytes()
    manuscript = dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        formatter=PROFILE, current_candidate_sha256=release['candidate_sha256'],
        clean_sha256=release['clean_input_sha256'], records=rows)
    base.save(REVIEW, manuscript)
    base.save(STORED, dict(research_only=True, candidate_sha256=base.digest(ROM),
        previous_sha256=release['candidate_sha256'], target_ARM9_sha256=sha256(arm).hexdigest(),
        target_COMMON_sha256=sha256(deployed).hexdigest(), allocations=slots, whole_parent_inverse=True,
        preserved_entries=len(after) - len(slots), manuscript=str(REVIEW), manuscript_sha256=base.digest(REVIEW)))
    print('Staged six Refit help revisions and 25 retentions. All other message bodies and ARM9 remain byte exact.')


if __name__ == '__main__':
    main()
