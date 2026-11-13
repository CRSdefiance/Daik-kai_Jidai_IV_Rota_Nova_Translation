"""Record76 prose drafts/native prototypes,without granting completion credit."""

import shutil
from collections import Counter
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_item_diplomacy_v784 import ROOT, CURRENT
from scripts.review_item_diplomacy_v784 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/item_diplomacy_v784_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V784 Item and diplomacy research')


def main():
    manuscript, context = read(MANUSCRIPT), read(ROOT/'native_context.json')
    layout = read(ROOT/'layout_prototypes/verification.json')
    matrix = read(ROOT/'layout_prototypes/native_layout_matrix.json')
    assert context['candidate_sha256'] == layout['candidate_sha256'] == sha(CURRENT.read_bytes())
    assert sha(MANUSCRIPT.read_bytes()) == layout['manuscript_sha256']
    assert len(manuscript['records']) == 76 and Counter(r['decision'] for r in manuscript['records']) == {'revise': 63, 'retain': 13}
    assert all(not r['review']['formatting'] for r in manuscript['records'])
    assert matrix['count'] == layout['complete_native_layouts'] == 2774 and not matrix['findings']
    assert len(context['all2080_actor_voice_selections']) == 2080
    assert layout['all76_IDs'] == list(range(1070, 1146))
    assert len(layout['complete_font_planes']) == 76 and len(layout['preview_sheets']) == 7
    for row in layout['complete_font_planes']+layout['preview_sheets']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
    visual = {'all76_native_font_planes_reviewed_in_seven_complete_sheets': True,
        'reviewed_sheets': layout['preview_sheets'], 'complete_leading_trailing_letters': True,
        'visible_margins_bounds_line_breaks_and_complete_substitutions_reviewed': True,
        'all2774_layout_cases_pass_but_only76_complete_font_planes_are_rendered': True,
        'proposed_type_phrase_inputs_are_not_actual_getter_or_gameplay_results': True,
        'no_formatting_production_or_full_game_approval': True}
    save(ROOT/'layout_prototypes/visual_review.json', visual)
    repaired_ids = [r['message_id'] for r in manuscript['records']
                   if r['message_id'] >= 1117 and ' '.join(r['current_English'].split()).startswith('Which faction should we oppose?')]
    assert repaired_ids == [1117, 1119, 1120, 1121, 1122, 1125, 1126, 1127, 1133, 1138, 1139, 1141, 1142, 1143, 1144, 1145]
    source_pins = {p['path']: p['ROM_sha256'] for p in manuscript['source_pins']}
    protected = dict(read('work/analysis/shared_metadata_v783/verification.json')['protected_files_unchanged'])
    protected.update(source_pins)
    protected[str(CURRENT.with_suffix('.xdelta'))] = '9a23ef0e69dea7a460e48c35e9278936344778d20b93cb1161441f2c56014b7f'
    for p, h in protected.items():
        assert sha(Path(p).read_bytes()) == h, p
    cfg = read('translations/shared_dialogue_editorial_release_v2.json')
    for p, h in cfg['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(Path(cfg['manuscript']).read_bytes()) == cfg['manuscript_sha256']
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 417
    assert ledger['records_revised_and_integrated'] == 293 and ledger['retained_wordings_editorially_completed'] == 124
    if ledger['records_with_source_and_prose_pass'] == 420:
        save(ROOT/'editorial_ledger_before_research_v784.json', ledger)
    else:
        assert ledger['records_with_source_and_prose_pass'] == 496 and (ROOT/'editorial_ledger_before_research_v784.json').exists()
    ledger.update({'records_with_source_and_prose_pass': 496, 'records_with_source_prose_drafts': 496})
    ledger['active_source_prose_drafts'] = {'native_message_IDs': [750, 751, 752, *range(1070, 1146)],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '750-752-context-unmapped;1070-1145-source-prose-and-prototype-reviewed;production-argument-formatting-and-gameplay-pending',
        'note': '76 drafts(63 revisions/13 retained) have zero production-formatting approval and no completion credit. Six nominal English letter-type phrases require verified owned runtime storage/routing;actual93D5C type0-5 values remain Japanese.79 drafts total.'}
    ledger['coverage_units'][0]['next'] = 'Complete Guild constructor/core and branch/argument closure,English nominal letter-type implementation preserving type6-9,exact no-growth native routing/storage/copies,registered integration/exact patch and actual item/diplomatic samples for1070-1145. Continue1146 onward,resolve750-752,and review all routes/remaining prose;preserve graphics audit and older-record follow-up.'
    summary = ('V784 reviews76 item-shop/diplomatic entries1070-1145:63 proposed revisions/13 retained wordings,with2080 native voice selections and2774 prototype layouts/76 independent fonts/seven visually reviewed sheets. '
               'Sixteen unrelated faction-choice translations are replaced in drafts with letter-drafting,absence or submission-warning meaning. '
               '1072 loses an invented buy question;1097 is a1000-coin service fee;Purser/First Mate roles and IC pronouns are source-bound. '
               'Six still-Japanese type values need scoped nominal English;the shared getter also supplies earlier English type6-9,which must remain exact. '
               '496 source/prose,79 drafts,417 complete unchanged. V783 ROM/patch remains current;production and actual scenes remain next. Full editorial/graphics goals stay open.')
    ledger['latest_checkpoint'] = summary
    finding_id = 'COMMON1070-1145-Guild-drafting-selection-and-warning-meaning'
    if not any(f['id'] == finding_id for f in ledger['findings']):
        ledger['findings'].append({'id': finding_id, 'native_message_IDs': repaired_ids,
            'status': 'source-reviewed-revisions-drafted-not-integrated',
            'detail': 'Sixteen entries incorrectly repeat Which faction should we oppose where Japanese offers to draft a letter,reports missing recipients/opponents,or warns against a submission demand. See exact source/current pairs and manuscript.'})
    checkpoint = {'id': 'V784-item-diplomacy-source-and-prospective-layout-research', 'documentation': str(DOC),
        'manuscript': str(MANUSCRIPT), 'source_prose_IDs': list(range(1070, 1146)), 'proposed_revisions': 63,
        'retained_wordings': 13, 'new_editorially_completed': 0, 'native_voice_selections': 2080,
        'prospective_layouts': 2774, 'complete_font_planes': 76, 'visually_reviewed_sheets': 7,
        'new_ROM': False, 'full_goal_complete': False}
    if not any(c['id'] == checkpoint['id'] for c in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest = read('out/editorial_review_latest.json')
    assert latest['path'] == ledger['current_integrated_candidate']['path'] and latest['sha256'] == sha(CURRENT.read_bytes())
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V784: item-shop and diplomatic-letter editorial research

COMMON1070-1145 receive76 clean-source/context/prose reviews:63 proposed revisions
and13 retained wordings. They are drafts,with all production-formatting gates false.
496 entries have source/prose review,79 are drafts and417 remain completed
(293 revised/124 retained). V783 remains the current integrated candidate;no ROM,
patch,registry,canonical input,original save or frozen production dependency changes.
The full editorial goal and separate unfinished graphics audit remain active.

## Meaning and fluent English

The group contains item buying/selling and bargain voices,letter delivery,recipient
and joint-enemy selection,pact confirmations,letter drafting,no-recipient/no-enemy
responses,and warnings that a target is unlikely to submit. Sixteen current entries
repeat the unrelated question "Which faction should we oppose?" in those other
contexts. The drafts restore each actual meaning instead of polishing the wrong
question. Full source/current bytes and native offsets are pinned in the manuscript.

1072 is an insufficient-funds taunt,not another purchase confirmation. The invented
"Buy it?" is removed there. Actual source1073 still asks whether to buy. Numeric
prices come from originalABF50 as full-width digits without units;coins is supplied
once by the prose. Source1097 charges1000 gold coins for courier service;it is not
a job reward. The original dispatch subtracts1000 at5BB00. Source1130 preserves
the five-or-six-day courier wait rather than inventing an exact guaranteed date.

The original bargain calls select role3 Purser,not the captain. Diplomatic speech
selects role1 First Mate,with the game's own fallback. Ten voice tables cover2080
original actor selections plus null fallbacks. SourceIC in1118/1140 is a first-
person pronoun;English uses I/our without inventing an actor name. Unlike the old
V115 snapshot,current53914 has two registered F/I literal guards. Those exact two
branch slots and the complete resident guard bytes are verified;restoring only
those slots reproduces the entire clean parser span. IC behavior is retained.

## Six diplomatic type arguments

Original93D5C still returns Japanese for types0-5:goodwill,pact formation,pact
termination,truce,war declaration and intimidation. New drafts propose contextual
nominal English phrases:goodwill letter,pact proposal,notice of pact termination,
truce proposal,declaration of war,and demand for submission. This lets recipient
questions and confirmations read naturally without mistaking the type for a
letter's owner or leaving Japanese inside English sentences. All source argument
positions remain intact:recipient first,type second;partner before opponent in
the separate pact confirmation. Established menu action names are not renamed.

The proposed phrases are explicit research inputs,not current getter results.
Their owned storage,routing and complete consumer preservation are still required.
Three original direct-call leads reach this getter. The third,56F34,belongs to the
earlier Strategist table915-920 and supplies action indices6-9. Those four labels
are already English and must remain exact. No global getter rewrite is performed.
Indirect references and full caller closure remain an implementation gate.

## Prospective formatting and visual checks

2774 original printf/existing literal-formatter prototype cases pass complete-word,
four-row/35-byte bounds,guard and weak-ending checks. They cover the original20
named faction values,all supplied partner/opponent combinations,six proposed type
phrases and explicit numeric-width stress values. Not every supplied combination
or numeric bound is claimed eligible or earned. Slot20 is an empty sentinel,
excluded according to the original diplomatic loops'0-19 bound. An initial21-slot
assumption failed on that empty slot and was corrected without changing game data.

76 complete native font planes independently match the original game font. All
seven sheets are visually reviewed for natural reading,full leading/trailing
letters,consistent visible margins,complete substitutions and bounds. There are
no remaining prototype findings. These directly invoke an existing formatter;
they do not prove the future private dispatcher,provider implementation,all
portrait/confirmation consumers or actual player-visible scenes. No formatting
approval or completed-entry credit is granted from these previews.

## Next work and preservation

Finish the Guild NPC constructor/core binding and full branches/argument/filter
contracts. Implement the six contextual type phrases in verified owned storage,
preserving earlier6-9 behavior. Extend exact native routing without growing a
section,BSS,cache,arena or the123040-byte staged payload. Then integrate all prose
through the registered stack,verify native copies and exact clean-input patch,
and exercise actual buy/sell/bargain and diplomatic scenes plus ordinary startup.
750-752 remain queued for original context mapping;1146 onward,all routes and other
prose remain in scope. The18 plaques,Online-body exclusion,preserved brown marks
and older-record follow-up remain unchanged. No commit or GitHub push is made.

Research and preview sheets are archived under E:/Rota Nova translations/Editorial
review/V784 Item and diplomacy research. They are CPU previews,not gameplay or
finished guide screenshots. The previous goal turn completed50 entries;this turn
makes progress on the next76 through source review and prototype verification.
''', encoding='utf-8')
    for file in ('docs/todo.md', 'docs/known_issues.md', 'docs/translation_progress.md'):
        path = Path(file)
        text = path.read_text(encoding='utf-8')
        heading = '## V784: item-shop and diplomatic-letter editorial research'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+summary+' See [V784 research](item_diplomacy_v784_research.md).\n', encoding='utf-8')
    save(ROOT/'checkpoint.json', {**checkpoint, 'protected_files_unchanged': protected,
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'goal_status': 'active',
        'producer_sha256': sha(Path(__file__).read_bytes())})
    sources = [p for p in ROOT.rglob('*') if p.is_file()]
    sources += [MANUSCRIPT, DOC, LEDGER, Path('out/editorial_review_latest.json')]
    sources += [Path('scripts')/name for name in ('context_item_diplomacy_v784.py', 'review_item_diplomacy_v784.py',
                'probe_item_diplomacy_layout_v784.py', 'record_item_diplomacy_research_v784.py')]
    for source in sources:
        relative = source.relative_to(ROOT) if source.is_relative_to(ROOT) else source
        target = ARCHIVE/relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
    save(ROOT/'archive_receipt.json', {'archive': str(ARCHIVE), 'every_copy_SHA256_verified': True,
        'prose_drafts': 76, 'new_completion_credit': 0, 'full_goal_complete': False})
    print('V784 research recorded and archived:76 drafts,2774 prototypes,76 reviewed fonts;496 source/prose,79 drafts,417 complete unchanged. Full goal active.', flush=True)


if __name__ == '__main__':
    main()
