"""Record31 source/context/prose drafts; preserve167 completed and latest V762."""

import ast
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_tavern_conversations_v763 import CURRENT, ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.review_tavern_conversations_v763 import IDS, MANUSCRIPT, RETAINED
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/tavern_conversations_v763_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V763 Tavern conversation research')


def main():
    assert not ARCHIVE.exists()
    context, manuscript = read(ROOT / 'native_context.json'), read(MANUSCRIPT)
    assert context['current_ROM_sha256'] == sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    assert tuple(r['message_id'] for r in manuscript['records']) == IDS
    assert len(context['392_hint_provider_cases_and6_person_trend_fragments']) == 398
    assert len(context['eight_original_four_captain_gift_voice_selections']) == 8
    assert len(context['actual218_item_names']) == 218 and len(context['actual124_named_commodity_objects']) == 124
    assert len(context['actual90_town_names']) == 90 and len(context['actual_coordinate_formatter_arguments_for842']) == 94
    assert context['untranslated_Japanese_distance_fragments_confirmed']
    assert context['COMMON842_argument_contains_provider_LF_and_spacing_to_normalize']
    assert all(all(r['review'][g] for g in ('source', 'context', 'localization', 'naturalness'))
        and not r['review']['formatting'] for r in manuscript['records'])
    assert sum(r['decision'] == 'retain-wording' for r in manuscript['records']) == len(RETAINED) == 8
    scripts = [Path('scripts') / p for p in ('context_tavern_conversations_v763.py', 'review_tavern_conversations_v763.py', 'record_tavern_conversations_v763.py')]
    for p in scripts: ast.parse(p.read_text(encoding='utf-8'), filename=str(p))
    ledger = read(LEDGER)
    assert (ledger['records_editorially_completed'], ledger['records_revised_and_integrated'], ledger['retained_wordings_editorially_completed']) == (167, 124, 43)
    assert ledger['records_with_source_and_prose_pass'] == 170 and ledger['active_source_prose_drafts']['native_message_IDs'] == [750, 751, 752]
    save(ROOT / 'editorial_ledger_before_v763.json', ledger)
    latest = Path('out/editorial_review_latest.json').read_bytes(); registry = Path('translations/release_stack.json').read_bytes()
    ledger['records_with_source_and_prose_pass'] = ledger['records_with_source_prose_drafts'] = 201
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752, *IDS],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '34-source-prose-drafts-not-completed',
        'groups': [{'IDs': [750, 751, 752], 'remaining': 'Actual caller/packed-script context mapping'},
            {'IDs': list(IDS), 'remaining': 'Private English distance/cardinal and profession providers; correct direct/YesNo/player/table caller scopes; native layouts/fonts with all source substitutions; owned integration/copies/exact patch and actual scenes.'}],
        'note': 'Source/prose approval does not waive runtime/provider/formatting gates. The data-only English provider is disposable CPU research. None of these34 drafts is counted as completed.'}
    ledger['latest_checkpoint'] = 'V763 source research reviews31 Tavern entries820-850:23 revised drafts/8 retained.398 original argument fragments,eight captain-table selections,218 item names,124 named goods,90 towns and94 original coordinate strings are mapped. Japanese distance morphemes and coordinate-provider LF/spacing require high-level scoped fixes.201 source/prose entries include34 drafts;167 completed unchanged. V762 remains latest; full goal active.'
    ledger['coverage_units'][0]['next'] = 'Complete all31 Tavern820-850 provider/localization/formatting gates and registered actual verification. Map750-752 context; continue851 onward,wider shared prose,Lil/all routes and other player-facing text.'
    ledger['research_checkpoints'].append({'id': 'V763-Tavern-rumor-gift-directions-source-and-provider-review', 'documentation': str(DOC),
        'manuscript': str(MANUSCRIPT), 'source_prose_records': 31, 'new_editorially_completed': 0, 'new_ROM': False,
        'evidence': str(ROOT / 'native_context.json')})
    ledger['findings'].append({'id': 'COMMON-843-845-untranslated-qualitative-distance-provider', 'native_message_ids': [843, 844, 845],
        'status': 'confirmed-original-provider-source-reviewed-private-English-data-prototype-not-integrated',
        'detail': 'Original arrays contain Japaneseちょっ/ずっ/ずーっ and abbreviated shared cardinals.843 passes item,NS qualifier,NS direction,EW qualifier,EW direction;844/845 pass item plus one qualifier/direction pair. The old and/then prose misrepresents these as separate legs. Patch function-local provider references to private English copies,retaining shared UI arrays/labels. The old V508 north/52/east/5 tests explicitly did not prove the real provider.'})
    ledger['findings'].append({'id': 'COMMON-842-coordinate-argument-leading-LF-and-spacing', 'native_message_ids': [842],
        'status': '94-actual-coordinate-provider-strings-mapped-formatting-integration-pending',
        'detail': '51580 supplies latitude/longitude text with a leading LF and alignment spaces,not a place/region name. Normalize only through the declared consumer and prove complete N/S/E/W letters and numbers; do not globally strip native coordinate formatting.'})
    ledger['findings'].append({'id': 'COMMON-826-drinking-context-and840-gift-promise', 'native_message_ids': [826, 840],
        'status': 'source-context-prose-restored-drafts-not-integrated',
        'detail': '826 follows declining another cup,so its weakness is a teasing drinking remark.840 explicitly promises to cherish the gift; the old A treasure fragment omits that promise.'})
    ledger['findings'].append({'id': 'COMMON-848-850-commodity-grammar-and-reported-popularity', 'native_message_ids': [848, 849, 850],
        'status': 'source-context-prose-reviewed-provider-formatting-pending',
        'detail': 'Use grammatical templates for both mass and plural commodity labels,retain current/prospective and reported distinctions,and restore850 popularity. Original remote argument order is town then commodity.'})
    save(LEDGER, ledger)
    DOC.write_text('''# V763 research: Tavern rumors, gifts and directions

Thirty-one entries820-850 have clean-source/context/prose reviews:23 revised drafts and8 retained wordings (822,824,825,827,834,839,846,847). Completed remains167 (124 revised,43 retained). Source/prose coverage is201,including34 unfinished drafts:these31 and750-752. V762 remains the latest combined ROM. This checkpoint emits no ROM,release profile or patch and awards no completion credit.

## Natural English and source meaning

The drafts restore complete questions,reported information and the gift recipient's promise to cherish the item. The original another-cup prompt59 precedes826,so the teasing weakness remark concerns drinking tolerance rather than combat. Drink remains neutral about a regional beverage. Four independent captain identification slots and four request slots remain intact; natural English does not need invented gender or rank markers to imitate Japanese sentence particles.

Person rumors preserve name,town and profession. Their source Town getter does not supply a country/faction name. Commodity reports retain current versus prospective trends,reported information and the omitted popularity sentence. Sales of and a craze for keep grammar natural with mass and plural commodity labels. Remote rumor arguments remain town first,commodity second.

## Important provider defect

The real843-845 providers still return Japanese distance fragments:ちょっ,ずっ andずーっ. The template contributes the Japanese connective needed to form their adverbial phrases. These mean a little,far andvery far in directional travel context. They are not numeric coordinates,miles,days or two sequential journeys.

Original843 argument order is:

1. Item name.
2. North/south distance qualifier.
3. North/south direction.
4. East/west distance qualifier.
5. East/west direction.

844/845 each receive the item plus a single qualifier/direction pair. Internal distance thresholds150/500/2000 select near/single-axis/two-axis text and qualitative classes; they are not proposed English measurement units. Tests execute392 original hint fragments:196 source/current-provider cases and196 with private English copies in disposable CPU memory. Actual initialized item-name getters remain in use. The English test patches only three function-local literal references; shared N/S/E/W UI labels and arrays stay unchanged. Production ownership of the new resources and executable scope are still unproven.

This supersedes the argument-role assumption in V508's supplied north/52/east/5 layout examples. That old report explicitly said it did not verify the native provider. A new complete-source review must use the actual qualifier/direction contracts.

## Coordinate and caller distinctions

842 uses a different provider. Original51580 formats actual latitude/longitude with a leading LF and spacing;94 valid original item positions return such strings. It does not return a city or region name. Its whitespace must be normalized in the declared dialogue consumer while keeping every N/S/E/W letter and digit. The global coordinate formatter must remain intact for its other uses.

820/821 original fragments confirm person full name,town name and force profession.847/848 native fragments distinguish prospective/current local reports;849/850 preserve actual town/commodity getter order under both threshold cases. All six fragments stop at the original UI boundary,not after a complete scene or earned rumor event.

The two four-captain gift tables select830-833 and835-838 through original53C6C. Eight actual table/route-selector executions prove the slots. Their parent53C14 and table at formatter SP+270 differ from the previously handled role-voice queues.825 instead uses player-only53C24/53C5C with an integer message ID.839 is a separate Yes/No question. Those consumers must be scoped correctly before a release.

The current initialized argument inventory contains218 real item-name getters (maximum23 bytes),124 named commodity objects and90 town-name getters. Commodity slot124 is a base-class placeholder with a null name member; it is recorded separately and is not treated as a normal named product. These inventories establish observed argument data,not item acquisition,gift eligibility or all possible legal edited names. The reserved slot and all unselected data remain unchanged.

## Remaining work

Build private English cardinal/distance resources and lowercase profession labels for their prose consumers. Preserve every original argument and protect macro-like bytes in supplied names across direct and table-selected speech. Run full native wrapping/font/buffer/bounds checks,including real coordinate LF/spacing and five-argument hints,then prove immutable resource ownership,registered integration,all COMMON copies,exact patch reconstruction and targeted actual gift/rumor scenes with normal transitions. No font-preview pass or actual new scene is claimed by this source checkpoint.

Keep750-752 actual context mapping,851 onward,wider shared prose,Lil/all routes,help/other player-facing text and the separate graphics audit open. The original18 plaques,Online-body exclusion,preserved brown marks,approved names and older-record follow-up remain unchanged. All evidence and drafts are hash-archived on E.
''', encoding='utf-8')
    summary = '\n\n## V763 research: Tavern rumor, gift and location providers\n\n31 source/context/prose drafts820-850 (23 revised/8 retained) bring source/prose coverage to201,including34 active drafts. Completed167 (124 revised/43 retained) is unchanged.398 original provider fragments,eight captain-table selections,218 item names,124 named goods,90 towns and94 coordinate strings are mapped. Confirmed Japanese distance morphemes require private English providers;842 supplies LF-prefixed coordinates,not a region. Provider/scoped native formatting,fonts,ownership,registered copies/patch and actual scenes remain pending. V762 remains latest;750-752,851 onward,wider shared/Lil/all routes/other prose and graphics remain open. See [V763 research](tavern_conversations_v763_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        p = Path('docs') / name; text = p.read_text(encoding='utf-8')
        assert '## V763 research: Tavern rumor, gift and location providers' not in text
        p.write_text(text.rstrip() + summary, encoding='utf-8')
    assert Path('out/editorial_review_latest.json').read_bytes() == latest
    assert Path('translations/release_stack.json').read_bytes() == registry
    save(ROOT / 'proof.json', {'research_only': True, 'source_prose_IDs': list(IDS), 'new_completed_records': 0,
        'completed': 167, 'source_prose_total': 201, 'active_drafts': 34,
        'previous_goal_turn_classification': 'progress: V762 integrated18 entries with native/actual/patch verification and hash archive',
        'source_current_ROM_sha256': sha(CURRENT.read_bytes()), 'unchanged_registry_sha256': sha(registry),
        'reports': {str(p): sha(p.read_bytes()) for p in (ROOT / 'source_and_neighbors.json', ROOT / 'caller_leads.json',
            ROOT / 'native_context.json', MANUSCRIPT, DOC, LEDGER)},
        'syntax_checked_scripts': {str(p): sha(p.read_bytes()) for p in scripts}, 'full_goal_complete': False})
    for p in ROOT.rglob('*'):
        if p.is_file(): copy(p, ARCHIVE / 'evidence' / p.relative_to(ROOT))
    for p in (MANUSCRIPT, LEDGER, DOC, *scripts): copy(p, ARCHIVE / 'repository' / p.as_posix())
    save(ARCHIVE / 'provenance.json', {'files': {p.relative_to(ARCHIVE).as_posix(): sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file()},
        'no_new_ROM_or_completion_credit': True})
    for p, h in read(ARCHIVE / 'provenance.json')['files'].items(): assert sha((ARCHIVE / p).read_bytes()) == h
    print('V763 hash-archived on E:31 new reviewed drafts;201 source/prose;167 completed unchanged;full goal active.', flush=True)


if __name__ == '__main__': main()
