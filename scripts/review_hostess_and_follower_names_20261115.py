"""Reconcile secondary actor nameplate decisions on the current cumulative ROM."""

from argparse import ArgumentParser
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_square_trend_dialogue_20261115 as current
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_barmaid_town_labels_20261115 import CALLERS, draw_input, read_static, read_text
from scripts.review_town_role_labels_20261115 import story_context


base, stage = current.base, current.stage
ROOT = Path('work/hostess_and_follower_names_20261115_v1')
DRAFT, BINDINGS = ROOT / 'draft.json', ROOT / 'bindings.json'
NATIVE = ROOT / 'native/native_name_planes.json'
FINAL = names.CHECKPOINT / 'hostess_and_follower_names_20261115_v1.json'
HISTORICAL = (
    (names.CHECKPOINT / 'shared_occupational_nameplates_reviewed_v1.json', 'records'),
    (names.CHECKPOINT / 'town_role_nameplates_review_20261115_v1.json', 'records'),
    (names.CHECKPOINT / 'ruler_and_ritual_nameplates_review_20261115_v1.json', 'records'),
    (names.CHECKPOINT / 'special_town_and_story_nameplates_reviewed_20261114.json', 'records'),
    (Path('releases/all_routes_editorial_20261115_special_target_labels_candidate/verification/registered_review.json'), 'records'),
    (Path('releases/all_routes_editorial_20261115_aziza_mutiny_dialogue_candidate/verification/registered_review.json'), 'nameplates'),
)
TOWN_REVIEW = Path('releases/all_routes_editorial_20261115_barmaid_town_labels_candidate/verification/registered_review.json')
FOLLOWER = {
    (0, 115): 'The follower answers each declaration by the Sect Leader with cheers.',
    (0, 293): 'The follower repeats the leader’s chant at the stone circle and cheers the group’s plan.',
    (1, 115): 'The follower cheers the leader, then cries out as the group is captured.',
    (1, 259): 'A follower interrupts the guildmaster to ask for a map, which connects the sect to the ruined site.',
    (2, 106): 'The follower echoes the Sect Leader as the ritual escalates and the villagers intervene.',
    (3, 88): 'The follower cheers the Sect Leader and flees from what they mistake for the army.',
}
# The story context identifies the speaker. Uncertain Latin spellings remain
# project spellings where the Japanese supplies no Latin form or alternate name.
HOSTESSES = {
    186: ('Francisca', (0, 253), 'Thanks Rafael for returning the Frozen Rose and tells him about a church. Francisca represents フランシスカ and fits her existing greeting and portrait.'),
    187: ('Marie', (0, 297), 'Welcomes Rafael and shares her customers’ theories about the ruins. Marie preserves マリー without changing the host’s identity to Maria.'),
    188: ('Margrete', (0, 109), 'Offers a contact at a nearby church after hearing about the treasure hunt. Keep the existing Margrete spelling for マルグレーテ.'),
    189: ('Wanda', (0, 264), 'Greets the player and says she knows of no famous ruins in town. Wanda retains ワンダ and the direct personal name.'),
    190: ('Julia', (0, 263), 'Greets the player and considers the question before answering about the local ruins. Julia is the established form of ジュリア.'),
    191: ('Donna', (0, 111), 'Recommends visiting Santiago Cathedral while the party is in Seville. Donna retains ドナ as her name without adding a social title.'),
    192: ('Matilda', (0, 311), 'Alerts the party to the Colosseum and reminds them to buy a map. Matilda is the established form of マチルダ.'),
    193: ('Myrine', (0, 257), 'Points out the ruins on a hill above town. Keep the established spelling of ミュリネー without tying her to a historical or mythological namesake.'),
    194: ('Faticia', (1, 295), 'Teases Hodram and passes on a rumor about a hidden Christian village. Keep the existing rendering of ファティシア, also used in the registered tavern exchange.'),
    195: ('Nelly', (0, 258), 'Insists Rafael see the pyramid and offers directions. Nelly retains ネリー and the separate Alexandria name-panel label.'),
    196: ('Hatra', (0, 259), 'Uses the good weather to suggest a visit to rumored ruins. Keep the established Hatra for ハトラ without treating the name as a geographic claim.'),
    197: ('Safia', (0, 314), 'Thanks Rafael for helping her dance and offers a lead on a mosque. Safia retains サフィア and keeps the greeting personal.'),
    198: ('Benazir', (0, 124), 'Repays the player’s gift with a tip about a site requiring a map. Benazir retains ベナジール without adding a title or surname.'),
    199: ('Lucia', (0, 302), 'Warns the party about the forest and offers directions if they bring a map. Lucia retains ルシア as the personal name used in this exchange.'),
    200: ('Titis', (0, 262), 'Makes an exception for the travelers when she tells them about nearby ruins. Keep the project spelling of ティティス and its separate Jakarta catalogue label.'),
    201: ('Mihwa', (0, 326), 'Quietly shares directions to the city gate despite restrictions on visitors. The clean field gives 美華 without a reading. Keep the existing project reading without inferring nationality from it.'),
    202: ('Reika', (0, 185), 'Tells Rafael and Claudio what she heard about the crown and the earlier visitor. The clean field gives 麗姫 without a reading. Keep the project reading and leave the visitor’s identity tentative.'),
    203: ('Sakura', (0, 321), 'Listens to Rafael’s travel story and asks about chintz. Sakura preserves the source さくら as her given name.'),
    204: ('Verisa', (0, 331), 'Uses her improved fortune-telling to thank Rafael and point him toward ruins. Keep the project spelling of ヴェリーサ and its separate Sao Jorge label.'),
    205: ('Silvia', (0, 328), 'Shares a report of an illustrated map but cannot say where it is. Silvia retains シルビア with no extra surname.'),
    206: ('Isabel', (0, 335), 'Asks the crew to inquire about a missing monk. Isabel retains イサベル and the Japanese distinction between her Bahamas label and the Havana port name.'),
}


def prior_decisions(inventory, current_names):
    cases = {}
    for row in inventory['historical_label_reviews_reconciled']:
        path = Path(row['historical_review'])
        proof = next(r for r in base.load(path)['records'] if r['id'] == row['historical_record'])
        assert base.digest(path) == row['historical_review_sha256']
        cases[row['actor_ID']] = (path, proof)
    for path, key in HISTORICAL:
        for row in base.load(path)[key]:
            if 'actor_ID' not in row:
                continue
            n = row['actor_ID']
            assert n not in cases
            cases[n] = (path, row)
    result = {}
    for n, (path, row) in sorted(cases.items()):
        assert all(row['review'][gate] for gate in names.GATES), (path, row['id'])
        a, b = current_names[n * 2:n * 2 + 2]
        assert a['text'] == row['english'] and b['text'] == row.get('catalogue_english', row['english']), (n, a, b)
        result[n] = dict(english=a['text'], catalogue_english=b['text'], precedent=str(path),
                         precedent_sha256=base.digest(path), record=row['id'])
    assert len(result) == 103
    return result


def prepare():
    assert not any(path.exists() for path in (DRAFT, BINDINGS, FINAL))
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    runtime = ctx.receipt()
    clean = base.NdsImage.open(stage.CLEAN)
    clean_arm = clean.read_file(stage.ARM)
    archive = base.load(names.INVENTORY)
    assert stage.digest(clean_arm) == archive['clean_ARM9_sha256']
    clean_roles = dict(names.native_clean_roles(clean_arm))
    getter_rows = names.current_getters(ctx)['rows']
    precedent = prior_decisions(archive, getter_rows)
    assert set(range(82, 207)) - precedent.keys() == {178, *HOSTESSES}
    reviewed = {178: 'Follower', **{n: data[0] for n, data in HOSTESSES.items()}}
    scenes = FOLLOWER | {data[1]: data[2].split('. ')[0] for data in HOSTESSES.values()}
    context, occurrences = story_context(clean, ctx, scenes, reviewed)
    assert len(context) == len(scenes) == 27 and set(occurrences) == set(reviewed)
    town_rows = {r['actor']: r for r in base.load(TOWN_REVIEW)['records']}
    assert town_rows.keys() == HOSTESSES.keys()
    cpu, get, provider = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    actor_count = 4 + 207 * 32
    actors = bytes(cpu.mem_read(ctx.actor_root, actor_count))
    records = []
    for n, english in reviewed.items():
        source = clean_roles[n]
        consumers = getter_rows[2 * n:2 * n + 2]
        field = names.TABLE + 32 * n
        clean_field = read_static(clean_arm, field)
        assert all(r['text'] == clean_field['text'] for r in source)
        assert all(r['text'] == english and r['actor_ID'] == n for r in consumers)
        note = ('Follower preserves 信徒 and the group’s allegiance to the Sect Leader. It fits both the collective '
                'chants and the individual map request without assigning a personal name.') if n == 178 else HOSTESSES[n][2]
        meaning = 'A follower or adherent of the sect.' if n == 178 else f'The personal name {clean_field["text"]}.'
        row = dict(id=f'ACTOR_{n:03d}_DEFAULT_NAME', actor_ID=n, speaker=english, english=english,
                   source_meaning=meaning, source_Japanese=clean_field['text'], source_ARM9_field=clean_field,
                   source_reference=source, current_consumers=consumers, current_reference=runtime,
                   localization_note=note, decision='retention', review=names.GATES.copy(),
                   context=' '.join(context[k]['summary'] for k in occurrences[n]), complete_exchanges=occurrences[n])
        if n in HOSTESSES:
            town = town_rows[n]
            match = get(0x79D8, town['town_ID'])
            assert match and bytes(cpu.mem_read(match, 3)) == clean_arm[match - names.BASE:match - names.BASE + 3]
            assert cpu.mem_read(match, 1)[0] == n
            actor = ctx.actor_root + 4 + 32 * n
            primary = read_text(cpu, get(0x7EB0C, actor))
            town_name = read_text(cpu, get(0x7EAF4, actor))
            joined = read_text(cpu, get(0x7EA8C, actor))
            assert primary == english and town_name == town['english'] and joined == f'{english} {town_name}'
            panel_cases = [draw_input(cpu, actor, *caller) for caller in CALLERS]
            assert all(case['visible_input'] == joined for case in panel_cases)
            row.update(town_table_reference=dict(source_address=match, town_ID=town['town_ID'], town_label=town_name),
                       full_name_panel_draw_inputs=panel_cases)
        records.append(row)
    assert not provider.reads and bytes(cpu.mem_read(ctx.actor_root, actor_count)) == actors
    ROOT.mkdir(parents=True, exist_ok=True)
    base.save(DRAFT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(names.GATES), runtime=runtime, records=records, complete_exchanges=context,
        earlier_decisions=precedent, town_review=str(TOWN_REVIEW), town_review_sha256=base.digest(TOWN_REVIEW),
        original_name_getter_count=len(getter_rows), full_panel_draw_inputs=42, rom_changed=False,
        new_gameplay=False, new_dialogue_credit=0))
    base.save(BINDINGS, dict(runtime=runtime, records=[dict(actor_ID=r['actor_ID'], current_consumers=r['current_consumers'])
                                                        for r in records]))
    print('22 contextual retentions, 27 complete dialogue sequences and 103 prior decisions bound. Visual check pending.')


def seal(viewed):
    draft, proof = map(base.load, (DRAFT, NATIVE))
    assert not FINAL.exists()
    assert draft['runtime'] == proof['runtime'] and len(draft['records']) == proof['actors'] == 22
    assert base.digest(current.ROM) == draft['runtime']['candidate_sha256']
    assert tuple(base.digest(s['path']) for s in proof['review_sheets']) == viewed == tuple(
        s['sha256'] for s in proof['review_sheets'])
    planes = {row['text']: row for row in proof['planes']}
    assert len(planes) == 22 and proof['all_name_strings_ASCII_complete_andfit_style11_216px']
    for row in draft['records']:
        plane = planes[row['english']]
        assert plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert base.digest(plane['native_plane']) == plane['native_plane_sha256']
        row['review']['formatting'] = True
        row['progressive_nameplate_plane_sha256'] = plane['native_plane_sha256']
    coverage = set(map(int, draft['earlier_decisions'])) | {row['actor_ID'] for row in draft['records']}
    assert coverage == set(range(82, 207))
    draft.update(reviewed_default_actor_range=[82, 206], reviewed_default_actor_count=len(coverage),
                 visual_review=proof['review_sheets'], native_proof=str(NATIVE), native_proof_sha256=base.digest(NATIVE),
                 review_scope='Default name and role decisions. Actual full list and conditional name consumers have separate display coverage.')
    validate_natural_dialogue_batch(draft)
    base.save(FINAL, draft)
    print('Sealed 22 retentions and reconciled all 125 default name decisions for actors 82–206.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2)
    args = parser.parse_args()
    if args.viewed_sha:
        seal(tuple(args.viewed_sha))
    else:
        prepare()
