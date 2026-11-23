"""Reconcile default character names with current game data and earlier scene reviews."""

from argparse import ArgumentParser
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import reconcile_shared_speaker_labels_20261111 as names
from scripts import register_square_trend_dialogue_20261115 as current
from scripts.audit_native_given_name_table import string
from scripts.probe_fleet_name_display_callers import execute as fleet_label
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_hostess_and_follower_names_20261115 import FINAL as SECONDARY
from scripts.review_town_role_labels_20261115 import story_context


base, stage = current.base, current.stage
ROOT = Path('work/default_character_names_20261115_v1')
DRAFT, BINDINGS = ROOT / 'draft.json', ROOT / 'bindings.json'
NATIVE = ROOT / 'native/native_name_planes.json'
FINAL = names.CHECKPOINT / 'default_character_names_20261115_v1.json'
POLICY = Path('translations/character_name_localization_policy_v1.json')
GLOSSARY = Path('docs/glossary.md')
FLEET_ONLY = {32, 45, 46, 50, 77}
RETENTIONS = {
    30: ('Dinis Albuquerque', 'Dinis de Albuquerque',
         'Keep Dinis Albuquerque on the short nameplate and preserve the restored de for the original full-name consumer. The silent beat in the face-off with Valdes identifies the actor without creating a new line.'),
    32: ('Paolo Centurione', 'Paolo Centurione',
         'Paolo preserves パオロ and Centurione agrees with the family name behind the Centurione Co. label. Keep the personal name in the actor field and the company name in the Forces roster.'),
    45: ('Charles Gilban', 'Charles Gilban',
         'Use Charles for チャールズ and retain the established Gilban for ギルバン. The family component distinguishes him from Charles Rochefort in the two default name forms.'),
    46: ('Paulo Morais', 'Paulo Morais',
         'Paulo preserves パウロ, distinct from Paolo for パオロ. Morais preserves the existing reading of モライス.'),
    50: ('Enzo Regioni', 'Enzo Regioni',
         'Keep Enzo for エンツォ and the established Regioni for レジオーニ. The faction and the compact fleet template have their own fields.'),
    51: ('Salid Ajar', 'Salid Ajar',
         'Hayreddin addresses him as サリド while reining in his threats. Salid matches the form used in the exchange, while Ajar preserves the separate family component.'),
    54: ('Ibn Niyadi', 'Ibn Niyadi',
         'Retain Ibn and Niyadi as the two authored components. He shows Rafael the way after Uddin offers an alliance. The formal courtesy does not require a new title.'),
    55: ('David Flahven', 'David Flahven',
         'Keep the established Flahven spelling and its repaired ASCII F. The defensive outburst belongs to this actor while Georg advises Kuhn to withdraw.'),
    56: ('Georg Salzgitter', 'Georg Salzgitter',
         'Keep the localized Salzgitter surname from ザルツギッター. His diplomatic greeting in Lil’s story and warning in Hodram’s story use the same person.'),
    58: ('Jorge Albacete', 'Jorge Albacete',
         'Retain both components of ホルヘ・アルバセテ. His sharp interjection during Escante’s introduction has the same name as the default catalogue entry.'),
    59: ('Garcia Oviedo', 'Garcia de Oviedo',
         'Retain Garcia Oviedo as the short name and the source particle as de in the full name. His reply in the fleet preparation is distinct from Valdes’s order.'),
    77: ('Akaboo Damai', 'Akaboo Damai',
         'Keep the project’s phonetic Akaboo for アカブー and preserve the separate ダーマイー component as Damai. The current name is consistent with the earlier cooking pitch and the short fleet-name getter.'),
    80: ('Charlotte Miller', 'Charlotte Miller',
         'Charlotte matches Rafael’s spoken address when he brings the timber. The default nameplate and catalogue retain ミレール as the established surname Miller.'),
}
EXCHANGES = {
    (0, 10): 'Rafael’s crew prepares for the showdown and Valdes and Garcia ready the opposing fleet.',
    (0, 37): 'Salid reacts to Rafael’s parley, then defers to Hayreddin’s conditional offer.',
    (0, 66): 'Rafael brings timber for the trade house and Charlotte promises to put it to work.',
    (0, 147): 'Uddin offers a pact and Ibn Niyadi shows the party out after Uddin gives Rafael time to decide.',
    (1, 38): 'Camille exposes Kuhn’s disguise. David curses, and Georg tells Kuhn their position is unfavorable.',
    (1, 140): 'Jorge interjects after Escante is introduced. Escante then makes his case for a conditional alliance.',
    (2, 50): 'Georg asks Lil to accept Kuhn’s alliance and acknowledges her decision.',
}
PROVENANCE = {
    32: Path('translations/route_forces_arm9_v1.json'),
    77: Path('docs/editorial_review_goal.md'),
}


def previous_decisions(by_actor):
    root = Path('translations')
    patterns = ('*scoped_names*final*.json', '*speaker_name*review*.json', '*scoped_names*review*.json')
    files = sorted({path for pattern in patterns for path in root.glob(pattern)})
    best = {}
    for path in files:
        document = base.load(path)
        if not isinstance(document, dict):
            continue
        for i, row in enumerate(document.get('records', [])):
            n = row.get('actor_ID')
            if n not in by_actor or not all(row.get('review', {}).get(k) is True for k in names.GATES):
                continue
            forms = row.get('current_consumers') or row.get('consumers') or ()
            if len(forms) != 2 or not all(isinstance(form, dict) for form in forms):
                continue
            pair = tuple(form.get('text') for form in forms)
            if pair != tuple(form['text'] for form in by_actor[n]) or not row.get('localization_note'):
                continue
            # Prefer accepted context records with a direct observed header where
            # available. The choice does not expand the scope of that observation.
            score = (bool(row.get('actual_progressive_header_observed_in_disclosed_fixture')),
                     row.get('decision') == 'retention', bool(row.get('context_record_ids')))
            if n in best and best[n][0] >= score:
                continue
            best[n] = (score, dict(path=str(path), sha256=base.digest(path), record_index=i, record_id=row['id'],
                                  progressive=pair[0], catalogue=pair[1], reason=row['localization_note'],
                                  review=row['review']))
    return {n: binding for n, (_, binding) in best.items()}


def prepare():
    assert not any(p.exists() for p in (DRAFT, BINDINGS, FINAL))
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    assert base.digest(stage.CLEAN) == release['clean_input_sha256']
    ctx = RegisteredRuntime(current.RELEASE, release['own_registered_startup'], captain=3)
    runtime = ctx.receipt()
    clean = base.NdsImage.open(stage.CLEAN)
    clean_arm = clean.read_file(stage.ARM)
    inventory = base.load(names.INVENTORY)
    assert stage.digest(clean_arm) == inventory['clean_ARM9_sha256']
    secondary = base.load(SECONDARY)
    assert secondary['runtime']['candidate_sha256'] == runtime['candidate_sha256']
    assert secondary['reviewed_default_actor_range'] == [82, 206] and secondary['reviewed_default_actor_count'] == 125
    all_results = names.current_getters(ctx)['rows']
    current_names = {n: all_results[2 * n:2 * n + 2] for n in range(82)}
    assert all(all(form['actor_ID'] == n and form['text'].isascii() and form['text'].isprintable()
                   for form in pair) for n, pair in current_names.items())
    expected_captains = ('Rafael Castor', 'Hodram Joakim Bergstrom', 'Lil Argot', 'Maria Huamei Li')
    assert tuple(current_names[n][1]['text'] for n in range(4)) == expected_captains
    assert current_names[9][0]['text'] == 'Camille Overijssel'
    assert current_names[9][1]['text'] == 'Camille Marinus Overijssel'
    earlier = previous_decisions(current_names)
    assert len(earlier) == 69 and set(current_names) - earlier.keys() == RETENTIONS.keys()
    context, uses = story_context(clean, ctx, EXCHANGES, RETENTIONS)
    assert set(uses) == RETENTIONS.keys() - FLEET_ONLY
    records, complete = [], []
    for n, consumers in current_names.items():
        fields = inventory['records'][n]['clean_actor_table_fields']
        assert all(not fld['clean'] or string(clean_arm, fld['clean']['pointer']) == fld['clean'] for fld in fields)
        complete.append(dict(actor_ID=n, source_name_fields=fields, current_consumers=consumers,
                             earlier_review=earlier.get(n)))
        if n in earlier:
            continue
        progressive, full, note = RETENTIONS[n]
        assert tuple(form['text'] for form in consumers) == (progressive, full)
        original = '・'.join(fld['clean']['text'] for fld in (fields[0], fields[2], fields[1]) if fld['clean'])
        direct = uses.get(n, [])
        description = ' '.join(context[key]['summary'] for key in direct) if direct else (
            'The original default identity is bound to the stock character model. The two isolated fleet-name '
            'callers illustrate the given-name consumer using a supplied fleet captain index.')
        row = dict(id=f'ACTOR_{n:03d}_DEFAULT_NAME', actor_ID=n, speaker=progressive, english=progressive,
                   catalogue_english=full, Japanese=original, source_meaning=f'The personal name {original}.',
                   context=description, decision='retention', localization_note=note, review=names.GATES.copy(),
                   source_reference=fields, current_reference=runtime, current_consumers=consumers,
                   complete_exchanges=direct)
        if n in FLEET_ONLY:
            cases = [fleet_label(ctx.arm, kind, '', captain_index=n, current_character=3)
                     for kind in ('fixed', 'centered')]
            assert all(case['native_captain_selector_and_name_dispatch_verified'] and
                       0 <= case['x'] <= 192 - len(case['complete_text']) * 6 for case in cases)
            row['offline_fleet_name_inputs'] = cases
        if n in PROVENANCE:
            path = PROVENANCE[n]
            row['related_review'] = dict(path=str(path), sha256=base.digest(path))
        records.append(row)
    ROOT.mkdir(parents=True, exist_ok=True)
    base.save(DRAFT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US', encoder='dialogue-relocatable-v1',
        review_gates=list(names.GATES), runtime=runtime, records=records, current_default_names=complete,
        complete_exchanges=context, secondary_review=dict(path=str(SECONDARY), sha256=base.digest(SECONDARY)),
        established_naming_policy={str(path): base.digest(path) for path in (POLICY, GLOSSARY)},
        prior_default_decisions_reconciled=len(earlier), original_getters_checked=len(all_results),
        rom_changed=False, new_gameplay=False, new_dialogue_credit=0))
    base.save(BINDINGS, dict(runtime=runtime, records=[dict(actor_ID=r['actor_ID'], current_consumers=r['current_consumers'])
                                                        for r in records]))
    print('Bound 69 earlier default names and recorded 13 individual retentions for visual review.')


def seal(viewed):
    assert not FINAL.exists()
    draft, proof = map(base.load, (DRAFT, NATIVE))
    assert draft['runtime'] == proof['runtime'] and base.digest(current.ROM) == draft['runtime']['candidate_sha256']
    assert proof['actors'] == len(draft['records']) == 13
    assert tuple(base.digest(s['path']) for s in proof['review_sheets']) == viewed == tuple(
        s['sha256'] for s in proof['review_sheets'])
    planes = {r['text']: r for r in proof['planes']}
    assert len(planes) == 15 and proof['all_name_strings_ASCII_complete_andfit_style11_216px']
    for row in draft['records']:
        renders = [planes[row[key]] for key in ('english', 'catalogue_english')]
        assert all(plane['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass'] and
                   base.digest(plane['native_plane']) == plane['native_plane_sha256'] for plane in renders)
        row['review']['formatting'] = True
        row['native_planes'] = [plane['native_plane_sha256'] for plane in renders]
    secondary = base.load(SECONDARY)
    covered = {row['actor_ID'] for row in draft['current_default_names']}
    covered.update(range(secondary['reviewed_default_actor_range'][0], secondary['reviewed_default_actor_range'][1] + 1))
    assert covered == set(range(207))
    draft.update(default_actor_count=len(covered), reviewed_actor_range=[0, 81],
        visual_review=proof['review_sheets'], native_proof=dict(path=str(NATIVE), sha256=base.digest(NATIVE)),
        scope='Default names and role labels. Conditional aliases, custom names, full-catalogue UI, and unused fields have separate coverage.')
    validate_natural_dialogue_batch(draft)
    base.save(FINAL, draft)
    print('All 207 default actor-name decisions reconciled and 13 retentions sealed.')


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=1)
    args = parser.parse_args()
    if args.viewed_sha:
        seal(tuple(args.viewed_sha))
    else:
        prepare()
