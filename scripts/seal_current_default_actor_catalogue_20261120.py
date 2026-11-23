"""Compare the current default name catalogue with its completed editorial ledger."""

from argparse import ArgumentParser
from functools import lru_cache
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from scripts import check_named_actor_deck_catalogue_20261120 as deck
from scripts import review_named_actor_catalogue_20261120 as review


base = review.base
BOOK = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
EARLIER = BOOK / 'default_character_names_20261115_v1.json'
FINAL = BOOK / 'default_actor_names_current_20261120_v1.json'
NAME_PLANES = review.ROOT / 'native/native_name_planes.json'


def reconcile(draft, previous):
    read_report = lru_cache(maxsize=None)(base.load)
    forms = {}
    for key, ref in draft['earlier_personal_name_decisions'].items():
        ident = int(key)
        assert base.digest(ref['path']) == ref['sha256']
        row, = (r for r in read_report(ref['path'])['records'] if r.get('actor_ID') == ident and r['id'] == ref['record'])
        assert all(row['review'][gate] is True for gate in review.GATES)
        forms[ident] = review.compared_forms(row)
    for key, ref in draft['earlier_role_and_hostess_decisions'].items():
        assert base.digest(ref['precedent']) == ref['precedent_sha256']
        forms[int(key)] = ref['english'], ref['catalogue_english']
    for row in draft['records']:
        forms[row['actor_ID']] = review.compared_forms(row)
    known = {r['actor_ID']: r for r in previous['current_default_names']}
    roles = {int(n): row for n, row in draft['earlier_role_and_hostess_decisions'].items()}
    inventory = base.load(review.names.INVENTORY)['records']
    assert set(known) == set(range(82)) and not set(known) & set(roles)
    assert set(known) | set(roles) == set(forms) == set(range(207))
    assert previous['default_actor_count'] == len(forms)
    records = []
    for ident, form in sorted(forms.items()):
        if ident in known:
            original = known[ident]
            assert review.compared_forms(original) == form
            source_fields = original['source_name_fields']
            decision = original['earlier_review']
        else:
            assert form == (roles[ident]['english'], roles[ident]['catalogue_english'])
            assert inventory[ident]['actor_ID'] == ident
            source_fields = inventory[ident]['clean_actor_table_fields']
            decision = roles[ident]
        exact_fields = draft['clean_and_current_actor_fields'][str(ident)]
        for earlier, current in zip(source_fields, exact_fields, strict=True):
            assert earlier['field'] == current['field'] and earlier['ARM9_pointer_field_offset'] == current['offset']
            ja = earlier['clean']
            if ja:
                assert current['clean'] and (ja['hex'], ja['pointer']) == (current['clean']['hex'], current['clean']['pointer'])
            else:
                assert current['clean'] is None
        records.append(dict(actor_ID=ident, file_path='/__arm9__.bin', exact_fields=exact_fields,
                            progressive_nameplate=form[0], full_catalogue=form[1],
                            completed_default_decision=decision))
    return records


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--viewed-sha', nargs=2, required=True)
    args = parser.parse_args()
    assert not FINAL.exists()
    draft, previous, native, panes = map(base.load, (review.DRAFT, EARLIER, NAME_PLANES, deck.PROOF))
    runtime = draft['runtime']
    assert native['runtime'] == panes['runtime'] == runtime
    assert base.digest(review.head.ROM) == runtime['candidate_sha256']
    assert base.load(base.LEDGER)['current_integrated_candidate']['sha256'] == runtime['candidate_sha256']
    assert panes['draft_sha256'] == base.digest(review.DRAFT)
    sheets = [*native['review_sheets'], panes['sheet']]
    assert [base.digest(s['path']) for s in sheets] == args.viewed_sha == [s['sha256'] for s in sheets]
    actors = reconcile(draft, previous)
    earlier_cases = {r['actor_ID']: r for r in previous['records']}
    native_by_text = {r['text']: r for r in native['planes']}
    deck_by_actor = {r['actor_ID']: r for r in panes['rows']}
    assert len(draft['records']) == len(native_by_text) == len(deck_by_actor) == 9
    for row in draft['records']:
        ident, text = row['actor_ID'], row['english']
        original = earlier_cases[ident]
        assert all(original['review'][g] is True for g in review.GATES)
        assert original['english'] == original['catalogue_english'] == text
        panel = deck_by_actor[ident]
        assert panel['english'] == text and len(panel['offline_supplied_actor_Draw_cases']) == 2
        assert all(c['exact_independent_font_match'] and c['bitmap_header_and_neighbor_guards_exact']
                   for c in panel['offline_supplied_actor_Draw_cases'])
        font = native_by_text[text]
        assert font['complete_first_internal_final_codes_bounds_andindependent_font_pixels_pass']
        assert base.digest(font['native_plane']) == font['native_plane_sha256']
        row['review']['formatting'] = True
        row['previous_editorial_decision'] = original['id']
        row['previous_retention_note'] = original['localization_note']
        row['dialogue_name_plane_sha256'] = font['native_plane_sha256']
        row['Deck_draw_cases'] = panel['offline_supplied_actor_Draw_cases']
    validate_natural_dialogue_batch(draft)
    base.save(FINAL, dict(
        candidate_sha256=runtime['candidate_sha256'], runtime=runtime,
        original_default_names_exact_for_207_actors=True, source_and_current_default_name_fields=actors,
        default_getters_verified=414, focused_retention_reviews=draft['records'],
        complete_source_and_current_exchanges=draft['complete_exchanges'], reviewed_sheets=sheets,
        original_default_editorial_ledger=str(EARLIER), original_default_editorial_ledger_sha256=base.digest(EARLIER),
        scope='Default names and roles. New nameplane checks were offline with supplied actors and original draw calls. '
              'This checkpoint does not cover selection eligibility, conditional aliases or alternate joined-name owners.',
        new_emulator_runs=0, new_editorial_credit=0, rom_changed=False,
        evidence={str(p): base.digest(p) for p in (review.DRAFT, review.BINDINGS, NAME_PLANES, deck.PROOF, Path(__file__))}))
    print('All 207 default decisions still match. Nine progressive and 18 Deck name masks passed.')


if __name__ == '__main__':
    main()
