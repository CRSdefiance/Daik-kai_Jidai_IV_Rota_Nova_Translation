"""Review official and religious titles with exact current getter and scene bindings."""

from argparse import ArgumentParser
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import replay_ritual_officiant_labels_20261115 as live
from scripts import stage_ritual_officiant_labels_20261115 as stage
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_town_role_labels_20261115 import story_context


base = stage.base
REVIEW = stage.ROOT / 'context.json'
BINDINGS = stage.ROOT / 'display_bindings.json'
NATIVE = stage.ROOT / 'native/native_name_planes.json'
FINAL = names.CHECKPOINT / 'ruler_and_ritual_nameplates_review_20261115_v1.json'
STARTUP = stage.ROOT / 'own_startup_verification.json'
RUNTIME = stage.ROOT / 'verified_staged_runtime.json'
PATCH = stage.ROOT / 'clean_input.xdelta'
REBUILT = stage.ROOT / 'clean_reconstruction_RESEARCH_ONLY.nds'
RITUAL_CONTEXT = 'docs/ceremony_editorial_v806_checkpoint.md'
PALACE_CONTEXT = 'docs/palace_editorial_v799_checkpoint.md'
TITLES = {
    125: ('King', 'A sovereign king.', 'King matches the ruler Rafael addresses as Your Majesty. Their audience establishes his authority over Portugal.'),
    126: ('Local Lord', 'A territorial lord.', 'Local Lord preserves the territorial scope of the original title and distinguishes this palace role from a king.'),
    127: ('King', 'A sovereign king.', 'King matches the clean palace role and the verified Istanbul audience. The English does not assign a personal identity to this general role.'),
    128: ('Local King', 'A king of the region.', 'Local King preserves the distinction between the regional ruler and the other native royal title. It keeps the rank of king.'),
    129: ('Magistrate', 'The official in charge of a county.', 'Magistrate fits the office being impersonated when orders are given to arrest the smugglers. The reveal stays in the dialogue.'),
    130: ('Daimyo', 'A daimyo, a Japanese territorial lord.', 'Daimyo keeps the original title. The glass and castle scenes show his authority without making him the sovereign of Japan.'),
    131: ('Governor', 'A governor.', 'Governor matches both the Escante discussion and Macao’s own political setting. The surrounding dialogue supplies the relevant jurisdiction.'),
    132: ('Officiant', 'The person presiding over the rite.', 'Officiant fits the person who performs rites and formally presents the Proof clue. It allows the character to describe his own history of resistance without implying a particular clergy office.'),
    133: ('Shaman', 'A ritual practitioner who leads invocations.', 'Shaman describes the regional ritual practitioner selected for the original ceremony, whose function includes leading ritual acts.'),
    134: ('Senior Monk', 'A monk advanced in standing.', 'Senior Monk conveys the standing in the Japanese title. It leaves the office of the selected religious figure unspecified.'),
    135: ('Officiant', 'A person who presides over ritual observances.', 'Officiant keeps the original role in both the temple encounter and the Guam story. The temple guardian explains a sacred tradition, and the man asking for passage has no stated clergy affiliation.'),
    136: ('Senior Monk', 'A monk advanced in standing.', 'Senior Monk suits the monk who corrects Lil’s manners and requests supplies as offerings. His exact institutional office is unspecified.'),
    137: ('Senior Monk', 'A monk advanced in standing.', 'Senior Monk fits the elder who tests the captains’ intentions and helps them understand the Proof, without inventing an abbot’s office.'),
    138: ('Shaman', 'A ritual practitioner who leads invocations.', 'Shaman names the ceremonial function of this original regional variant and leaves the rite to explain the character’s actions.'),
    139: ('Priest', 'A Christian priest.', 'Priest fits the title 神父. The mission sequence names the Society of Jesus, and the dialogue reveals who is posing as its representatives.'),
}
EXCHANGES = {
    (0, 79): 'The priest acknowledges Rafael’s standing in the Mediterranean and presents the cloth. The crew reasons about what it might show.',
    (0, 116): 'The temple guardian demands knowledge of the Vedas, hears the party’s explanation, and entrusts them with a coin after recognizing their text.',
    (0, 120): 'A senior monk tests Rafael’s intentions and tells him where the clan carrying the map went, with a warning about the danger and the Proof.',
    (0, 162): 'A guard admits the fleet. A ritual speaker confers an object, and the crew reflects on who held it.',
    (0, 164): 'The king thanks Rafael, offers to reward him, and hears him defer the reward while Portugal is rebuilding.',
    (0, 165): 'The king explains what the Proofs could mean for the Portuguese Crown, and tells Rafael to keep them out of Spain’s hands.',
    (0, 195): 'A guildmaster, a shipwright and the ritual figure dispute each other’s taste in paintings. The shopkeeper describes the new fashion.',
    (0, 200): 'The daimyo learns what giyaman is and tells the guildmaster to collect it.',
    (0, 304): 'The temple guardian recognizes the Veda Rafael brings back and offers a coin. Rafael must work out what it means.',
    (1, 120): 'The senior monk recounts the Yuan invasion and asks Hodram to bring back the emperor’s keepsake.',
    (1, 153): 'A speaker who confers the Proof clue describes resistance to Ottoman rule and points Hodram to ruins in Turkey.',
    (2, 309): 'A senior monk corrects Lil’s manners and asks her to bring tea and sugar for the offerings.',
    (3, 111): 'A port worker asks Maria to take a shipwrecked man home. The man thanks her in the words the worker taught him.',
    (3, 118): 'A guard recognizes Maria’s fleet and a ritual speaker formally confers the object.',
    (3, 125): 'The governor describes Escante’s failed coup and relays a rumor about the treasure key.',
    (3, 278): 'People posing as missionaries are exposed by a party led by an apparent magistrate. The governor and crew react differently to the staged intervention.',
    (3, 297): 'Maria brings the man home to Guam. He thanks her and gives her a parting gift.',
}


def prepare():
    parent = base.load(stage.parent.RELEASE)
    staged, boot = map(base.load, (stage.STORED, STARTUP))
    assert base.digest(stage.ROM) == staged['candidate_sha256'] == boot['candidate_sha256']
    assert base.digest(stage.CLEAN) == parent['clean_input_sha256']
    if not PATCH.exists():
        make_xdelta(stage.CLEAN, stage.ROM, PATCH)
    if not REBUILT.exists():
        apply_xdelta(stage.CLEAN, PATCH, REBUILT)
    assert REBUILT.read_bytes() == stage.ROM.read_bytes()
    runtime_receipt = parent | dict(candidate=str(stage.ROM), candidate_sha256=staged['candidate_sha256'],
                                   own_registered_startup=str(STARTUP), own_registered_startup_sha256=base.digest(STARTUP),
                                   target_ARM9_sha256=staged['target_ARM9_sha256'], patch=str(PATCH), patch_sha256=base.digest(PATCH),
                                   research_only=True, clean_input_patch_byte_exact=True)
    base.save(RUNTIME, runtime_receipt)
    ctx = RegisteredRuntime(RUNTIME, STARTUP, captain=3)
    runtime = ctx.receipt()
    clean = base.NdsImage.open(stage.CLEAN)
    contexts, occurrences = story_context(clean, ctx, EXCHANGES, TITLES)
    old_bounds = base.load(names.INVENTORY)['records']
    getters = names.current_getters(ctx)['rows']
    changed = [i for i in range(207) if [r['text_hex'] for r in old_bounds[i]['current_consumers']] !=
               [r['text_hex'] for r in getters[2*i:2*i+2]]]
    assert changed == list(stage.ACTORS)
    records = []
    for ident, (english, meaning, reason) in TITLES.items():
        old = old_bounds[ident]
        known = old['clean_ordinary_role_consumers']
        official = 'palace' if ident <= 131 else 'ritual'
        keys = occurrences.get(ident, [])
        context = ' '.join(contexts[key]['summary'] for key in keys) if keys else (
            f'The original {official} dispatch supplies the regional actor. The clean role label provides the title.')
        current = getters[2*ident:2*ident+2]
        assert [row['text'] for row in current] == [english, english]
        records.append(dict(id=f'ACTOR_{ident:03d}_OFFICIAL_TITLE', actor_ID=ident, speaker=english, english=english,
            source_Japanese=known[0]['text'], source_meaning=meaning, localization_note=reason,
            context=context, exact_actor_exchanges=keys, prior_dispatch_context=PALACE_CONTEXT if official == 'palace' else RITUAL_CONTEXT,
            decision='revision' if ident in changed else 'retention', review=names.GATES.copy(),
            source_reference=known, source_actor_fields=old['clean_actor_table_fields'],
            previous_visible_name=old['current_consumers'][0]['text'], current_consumers=current,
            current_reference=dict(candidate_sha256=runtime['candidate_sha256'], ARM9_sha256=runtime['ARM9_sha256'])))
    base.save(REVIEW, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
                           review_gates=list(names.GATES), runtime=runtime, records=records, complete_exchanges=contexts,
                           shared_CD_source_references=[PALACE_CONTEXT, RITUAL_CONTEXT], exact_all_getters_checked=len(getters),
                           expected_changed_actors=changed, exact_clean_patch=str(PATCH), new_dialogue_credit=0))
    base.save(BINDINGS, dict(runtime=runtime, records=[dict(actor_ID=row['actor_ID'], current_consumers=row['current_consumers'])
                                                     for row in records]))


def seal(sheet_hashes):
    draft, native, game = map(base.load, (REVIEW, NATIVE, live.OUTPUT))
    assert draft['runtime'] == native['runtime'] and native['actors'] == len(draft['records']) == 15
    assert game['candidate_sha256'] == draft['runtime']['candidate_sha256']
    sheet, = native['review_sheets']
    assert base.digest(sheet['path']) == sheet['sha256'] == sheet_hashes[0]
    assert base.digest(live.SHEET) == game['sheet_sha256'] == sheet_hashes[1]
    assert [row['actor_ID'] for row in game['results']] == list(stage.ACTORS)
    assert all(row['matched_complete_nameplates'] and row['all_sampled_image_differences_inside_nameplate'] for row in game['results'])
    planes = {row['text']: row for row in native['planes']}
    assert len(planes) == 10 and native['all_name_strings_ASCII_complete_andfit_style11_216px']
    for plane in planes.values():
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert base.digest(plane['native_plane']) == plane['native_plane_sha256']
        assert base.digest(plane['preview']) == plane['preview_sha256']
    for row in draft['records']:
        row['review']['formatting'] = True
        row['progressive_nameplate_plane_sha256'] = planes[row['english']]['native_plane_sha256']
    validate_natural_dialogue_batch(draft)
    base.save(FINAL, draft | dict(native_sheet=sheet, native_receipt=str(NATIVE), native_receipt_sha256=base.digest(NATIVE),
        gameplay=game, gameplay_receipt=str(live.OUTPUT), gameplay_receipt_sha256=base.digest(live.OUTPUT),
        changed_nameplates=2, justified_nameplate_retentions=13, catalog_screen_layout_unvisited=True))


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2)
    args = parser.parse_args()
    seal(args.viewed_sha) if args.viewed_sha else prepare()
