"""Review recurring town nameplates against clean roles and complete exchanges."""

from argparse import ArgumentParser
from collections import defaultdict
from hashlib import sha256
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_forces_relationships_20261115 as current
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.scan_completed_contraction_wraps_v7831 import raw_speeches


ROOT = Path('work/town_role_labels_20261115_v1')
REVIEW, BINDINGS = ROOT / 'context.json', ROOT / 'display_bindings.json'
NATIVE = ROOT / 'native/native_name_planes.json'
FINAL = names.CHECKPOINT / 'town_role_nameplates_review_20261115_v1.json'
ARM = '/__arm9__.bin'
FACILITY_TABLE = 0x11948C
FAMILIES = {
    2: (range(109, 113), '造船所の親父', 'Shipwright', 'The person who runs the shipyard, with a familiar form of address.'),
    5: (range(147, 151), 'ギルドの元締め', 'Guildmaster', 'The person who heads or runs the local guild.'),
    8: (range(140, 147), '宿屋のおばさん', 'Innkeeper', 'The woman who runs the inn, with a familiar form of address.'),
    11: (range(120, 125), '衛兵', 'Guard', 'A guard on duty, identified by role.'),
    12: (range(95, 104), '酒場の客', 'Patron', 'A tavern customer. The same role slot can appear in local stories.'),
}
REASONS = {
    95: 'Patron works for the unnamed spectator who cheers and heckles at the bullfight. The scene supplies the venue.',
    96: 'Patron keeps the local speaker anonymous. The confrontation over the drug makes his predicament clear without a diagnostic label.',
    97: 'Patron reads naturally above the local who tells Rafael about the missing explorers and challenges him to go back. He speaks as a customer passing on news.',
    98: 'Patron identifies a customer and fits the same selected tavern role used by the other regional variants.',
    99: 'Patron keeps the customer anonymous and leaves the location to the dialogue and town screen.',
    100: 'Patron describes a customer in the native town selector and leaves the regional index as internal metadata.',
    101: 'Patron lets the dialogue establish that this customer sells information. Maria identifies him as the informant herself.',
    102: 'Patron fits the eager customer who asks to taste Sakura’s wine. In Maria’s story it also keeps the local contact anonymous until the script explains his part.',
    103: 'Patron fits the diner who tastes the cheese dish and predicts others will want it. The barkeep remains a separate speaker.',
    109: 'Shipwright fits the sails teacher and the builder who seeks funds to develop armor. The familiar forms of address stay in the dialogue.',
    110: 'Shipwright fits the builder who recognizes how to armor a ship against cannon fire and announces that the work is complete.',
    111: 'Shipwright matches the shipyard service selected for this variant and names the trade without adding a credential or title.',
    112: 'Shipwright matches the native service role. The Japanese familiarity does not establish kinship.',
    120: 'Guard fits the attendant who recognizes Rafael’s fleet and lets him pass. The brief exchange is clear with a simple duty label.',
    121: 'Guard fits the person authorizing Hodram to enter. The person who gives him the item and explains its history has a separate label.',
    122: 'Guard identifies the protective duty in the Japanese name and in the town selector. The role has no personal name in that field.',
    123: 'Guard fits the role presented at the arrest. The later dialogue gets to reveal which parts of the intervention were staged.',
    124: 'Guard fits the person who rushes to alert the daimyo about the missing ornament and accepts orders to find it.',
    140: 'Innkeeper identifies the host Xien calls over to ask about the hidden book. Her reply makes her relationship to the inn explicit.',
    141: 'Innkeeper carries the speaker’s established place in town as she joins the other residents in describing forced labor.',
    142: 'Innkeeper fits the local host who tells Rafael how the divination dish was used. The familiar term Rafael uses in thanking her implies no kinship.',
    143: 'Innkeeper matches the selected lodging role and avoids imposing a title of address on the speaker.',
    144: 'Innkeeper keeps the woman anonymous. The exchange itself establishes that Mao is her son, and her relationship to him remains in the dialogue.',
    145: 'Innkeeper fits the host Jam asks where he can go for a walk. Her knowledge of the castle needs no added occupation or rank.',
    146: 'Innkeeper matches the lodging provider and keeps the native regional metadata out of the nameplate.',
    147: 'Guildmaster is a natural title for the guild’s head. The same speaker can discuss his ceramics collection or cheer in the crowd.',
    148: 'Guildmaster keeps the regional title consistent when the character quarrels about paintings and in scenes where he deals with guild business.',
    149: 'Guildmaster fits the local official who talks about Romance of the Three Kingdoms before sharing a rumor about Zhao Yun’s spear.',
    150: 'Guildmaster preserves the original civic role while the scene shows his deference to the daimyo. His polite speech does not call for a new rank.',
}
EXCHANGES = {
    (0, 81): 'The party attends a bullfight, the crowd heckles and cheers, and Rafael surprises Claudio by recruiting Emilio.',
    (0, 150): 'The innkeeper recounts the divination dish’s use, Rafael tries the lotus leaf, and Hans explains the two keys needed for each map.',
    (0, 162): 'The guard admits the known fleet, an officiant confers the object, and the crew considers where it came from.',
    (0, 180): 'The shipwright offers a lesson with an optional refusal, explains sail types and mast behavior, and returns to work.',
    (0, 195): 'Three art buyers disagree about painters and place their orders. The shopkeeper explains the fashion once they leave.',
    (0, 200): 'The daimyo admires imported glass, asks what it is, and tells the guildmaster to gather it for his collection.',
    (0, 201): 'A guildmaster and shopkeeper talk about porcelain. Two bystanders see a chance to profit from the demand.',
    (0, 207): 'Two customers follow a smell and order the barkeep’s cheese dish. They enjoy it and expect it to catch on.',
    (0, 216): 'Jam takes the innkeeper’s suggestion to visit the castle. The guard reports the missing ornament and the scene ends with Jam’s letter.',
    (0, 224): 'The guildmaster asks about Romance of the Three Kingdoms, reacts to different favorite generals, and mentions Zhao Yun’s spear.',
    (0, 315): 'A patron relays the rumored curse and the explorers’ disappearance. Rafael and his crew decide to investigate.',
    (0, 323): 'Rafael brings Sakura wine. The barkeep and a patron drink it, then Sakura tells him about Kyoto.',
    (1, 58): 'The townspeople confront Espinosa. The innkeeper reports forced labor, Sera identifies him, and Hodram leaves his fate to the residents.',
    (1, 153): 'A guard lets Hodram pass, and the officiant gives him an object and tells him where to look next.',
    (2, 135): 'A desperate customer cannot meet Espinosa’s price. Lil confronts him and Camille backs her decision to oppose him.',
    (2, 143): 'The shipwright asks Lil to finance armor research, names the cost, and promises to get to work after she agrees.',
    (3, 105): 'Mao asks Maria to play. His mother fears she has offended Maria, prompting Maria to confide in Xien.',
    (3, 172): 'Xien and Ian discover a book behind a portrait. The innkeeper says it is unfamiliar and gives them permission to take it.',
    (3, 272): 'The shipwright, gunnery expert and builders work out the armor design. The shipwright asks the party to tell the guildmaster it is ready.',
    (3, 276): 'A local contact approaches an informant at the tavern. Maria buys reliable timing and location details about the approaching mission.',
    (3, 278): 'An apparent guard joins the arrest. The closing conversation reveals the ruse and the crew takes on the local contact.',
}


def facility_selections(arm, common, raw, plan):
    # RegisteredRuntime binds this established factory to the candidate's own snapshot.
    cpu, get, provider = machine(arm, common, raw, plan)
    town_root, actor_root = get(0xCB178), get(0xCB184)
    models = bytes(cpu.mem_read(town_root, 4 + 90 * 108))
    selected = defaultdict(list)
    for number in range(90):
        town = town_root + 4 + number * 108
        culture = get(0xB51B4, town)
        assert 0 <= culture < 21
        for role, (ids, _, _, _) in FAMILIES.items():
            field = FACILITY_TABLE + culture * 14 + role + 1
            ident = get(0xB2D28, town, role)
            assert ident == arm[field] and ident in ids
            assert get(0xB2CD8, town, role) == actor_root + 4 + ident * 32
            selected[ident].append(dict(town_ID=number, culture=culture, facility_selector=role,
                                        actor_table_offset=field))
    assert set(selected) == set(REASONS)
    assert len(provider.reads) == len(provider.opens) == 0
    assert bytes(cpu.mem_read(town_root, len(models))) == models
    return dict(selected)


def story_context(clean, ctx, exchanges=EXCHANGES, reviewed=REASONS):
    inventory, _, _ = scoped_inventory()
    clean_arm = clean.read_file(ARM)
    contexts, uses = {}, defaultdict(list)
    for route in range(4):
        file = f'/data/SC{route}.DK4'
        original, current_blocks = [IlnkContainer.parse(image.read_file(file)).blocks for image in (clean, ctx.image)]
        for (owner, block), summary in exchanges.items():
            if owner != route:
                continue
            key = f'SC{route} B{block}'
            a, b = original[block], current_blocks[block]
            source, installed = [raw_speeches(arm, blob, inventory)[1] for arm, blob in ((clean_arm, a), (ctx.arm, b))]
            assert [row['complete_preamble_hex'] for row in source] == [row['complete_preamble_hex'] for row in installed]
            speakers = sorted({row['selector'] for row in source} & reviewed.keys())
            assert speakers
            for ident in speakers:
                uses[ident].append(key)
            contexts[key] = dict(file=file, block=block, summary=summary,
                                 clean_block_sha256=sha256(a).hexdigest(), current_block_sha256=sha256(b).hexdigest(),
                                 reviewed_actors=speakers,
                                 speeches=[dict(source=old, current=new,
                                                Japanese=bytes.fromhex(old['raw_hex'])[1:].decode('cp932'),
                                                English=bytes.fromhex(new['raw_hex'])[1:].decode('cp932'))
                                           for old, new in zip(source, installed, strict=True)])
    return contexts, uses


def prepare():
    base = current.base
    release = base.load(current.RELEASE)
    assert base.digest(current.stage.CLEAN) == release['clean_input_sha256']
    assert base.digest(current.MANIFEST) == release['manifest_sha256']
    assert base.digest(release['own_registered_startup']) == release['own_registered_startup_sha256']
    clean = base.NdsImage.open(current.stage.CLEAN)
    clean_arm = clean.read_file(ARM)
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    runtime = ctx.receipt()
    for lo, hi in ((0xB2CD8, 0xB2D58), (0xB51B4, 0xB51CC), (FACILITY_TABLE, FACILITY_TABLE + 21 * 14)):
        assert clean_arm[lo:hi] == ctx.arm[lo:hi]
    selections = ctx.execute(facility_selections)
    assert sum(map(len, selections.values())) == 450
    contexts, occurrences = story_context(clean, ctx)
    before = base.load(names.INVENTORY)
    assert before['clean_ARM9_sha256'] == sha256(clean_arm).hexdigest()
    original_roles = dict(names.native_clean_roles(clean_arm))
    getters = names.current_getters(ctx)
    records = []
    for role, (ids, japanese, english, meaning) in FAMILIES.items():
        family_scenes = sorted({key for ident in ids for key in occurrences.get(ident, [])})
        for ident in ids:
            source = original_roles[ident]
            current_names = getters['rows'][ident * 2:ident * 2 + 2]
            known = before['records'][ident]
            assert source == known['clean_ordinary_role_consumers']
            assert [row['text'] for row in source] == [japanese] * 2
            assert all(row['actor_ID'] == ident and row['text'] == english for row in current_names)
            assert [row['text_hex'] for row in known['current_consumers']] == [row['text_hex'] for row in current_names]
            direct = occurrences.get(ident, [])
            context = ' '.join(contexts[key]['summary'] for key in direct) if direct else (
                f'The original town selector returns this actor as a regional {english.lower()} in the recorded town cases. '
                'The listed complete scenes establish the role across its regional variants.')
            records.append(dict(id=f'ACTOR_{ident:03d}_TOWN_LABEL', actor_ID=ident, speaker=english,
                                english=english, decision='retention', source_Japanese=japanese, source_meaning=meaning,
                                localization_note=REASONS[ident], context=context, review=names.GATES.copy(),
                                source_reference=source, source_actor_fields=known['clean_actor_table_fields'],
                                current_reference=dict(candidate_sha256=runtime['candidate_sha256'], ARM9_sha256=runtime['ARM9_sha256']),
                                current_consumers=current_names, facility_role=role,
                                native_town_selections=selections[ident], exact_actor_exchanges=direct,
                                representative_role_exchanges=family_scenes))
    assert len(records) == len(REASONS) == 29
    ROOT.mkdir(parents=True, exist_ok=True)
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                           review_gates=list(names.GATES), records=records, complete_exchanges=contexts,
                           prior_inventory=str(names.INVENTORY), prior_inventory_sha256=base.digest(names.INVENTORY),
                           current_original_getters_checked=len(getters['rows']), source_facility_selections=450, runtime=runtime,
                           actual_gameplay_reference='docs/inn_editorial_v801_checkpoint.md',
                           new_gameplay=False, new_dialogue_credit=0))
    base.save(BINDINGS, dict(runtime=runtime, records=[dict(actor_ID=row['actor_ID'], current_consumers=row['current_consumers'])
                                                     for row in records]))
    print('Bound 29 labels and', len(contexts), 'complete exchanges. Progressive font and visual review pending.')


def seal(viewed_sha):
    base = current.base
    draft, native = base.load(REVIEW), base.load(NATIVE)
    assert draft['runtime'] == native['runtime'] and len(draft['records']) == native['actors'] == 29
    sheet, = native['review_sheets']
    assert base.digest(sheet['path']) == sheet['sha256'] == viewed_sha
    planes = {row['text']: row for row in native['planes']}
    assert set(planes) == {family[2] for family in FAMILIES.values()}
    assert native['all_name_strings_ASCII_complete_andfit_style11_216px']
    for plane in planes.values():
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert base.digest(plane['native_plane']) == plane['native_plane_sha256']
        assert base.digest(plane['preview']) == plane['preview_sha256']
    for row in draft['records']:
        row['review']['formatting'] = True
        row['progressive_nameplate_plane_sha256'] = planes[row['english']]['native_plane_sha256']
        row['full_catalogue_getter_verified'] = True
    draft.update(viewed_sheet=sheet, native_receipt=str(NATIVE), native_receipt_sha256=base.digest(NATIVE),
                 historical_inn_play_scope='An ordinary earlier Istanbul Inn replay observed actor 142. The new getter and renderer results are offline.',
                 scope='Existing progressive nameplates and both stored getter forms. Catalog screen layout and other role branches remain open.',
                 revision_count=0, role_retentions=29)
    validate_natural_dialogue_batch(draft)
    base.save(FINAL, draft)
    print('Approved 29 retentions across five role labels. Catalog display layout remains open.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', help='Seal after directly viewing the generated nameplate sheet.')
    args = parser.parse_args()
    if args.viewed_sha:
        seal(args.viewed_sha)
    else:
        prepare()
