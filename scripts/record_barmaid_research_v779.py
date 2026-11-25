"""Record31 editorial drafts and verified name layouts;do not grant completion."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.context_barmaid_dialogue_v779 import ROOT, CURRENT
from scripts.review_barmaid_dialogue_v779 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/barmaid_v779_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V779 Barmaid research')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    doc = read(MANUSCRIPT)
    context = read(ROOT/'native_context.json')
    bounds = read(ROOT/'captain_first_name_bound.json')
    layout = read(ROOT/'layouts_v1/verification.json')
    names = read(ROOT/'layouts_v1/name_token_findings.json')
    latest = read('out/editorial_review_latest.json')
    digest = sha(CURRENT.read_bytes())
    assert digest == latest['sha256'] == context['candidate_sha256'] == bounds['candidate_sha256'] == layout['candidate_sha256']
    assert len(doc['records']) == 31 and sum(r['decision'] == 'revise' for r in doc['records']) == 14
    assert [r['message_id'] for r in doc['records'] if not r['review']['context']] == [996]
    assert all(not r['review']['formatting'] for r in doc['records'])
    assert len(context['all84_original_city_and_name_provider_cases']) == 84
    assert len(context['all21_original_barmaids']) == 21
    assert len(bounds['cases']) == 24 and bounds['capacity'] == 16 and bounds['serialized_bytes'] == 17
    assert layout['native_layouts'] == 273 and layout['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    assert len(layout['complete_font_planes']) == 52 and len(layout['sheets']) == 5
    assert len(names['five_naive_article_diagnostics_are_exactly_bound_to_name_bytes']) == 5
    assert not names['unresolved_prose_or_layout_findings'] and names['literal_prose_negative_control_rejected']
    assert all(sha(Path(p['path']).read_bytes()) == p['sha256'] for p in layout['complete_font_planes']+layout['sheets'])
    refs = read(ROOT/'latent996_reference_leads.json')
    assert refs['0x2059358']['absolute'] == [['section0', 0x020E5789, 0x02059400]]
    # A failed source-closure attempt is research,never a verified caller proof.
    save(ROOT/'latent996_open_reference.json', {
        'candidate_sha256': digest, 'normal_reachability_closed': False,
        'unclassified_byte_window': ['section0', 0x020E5789, 0x02059400],
        'classification': 'Unaligned four-byte scan hit spanning source words;not established as an executable pointer or dismissed as harmless.',
        'source_catalog58_has_no_barmaid': True, 'original_speech_branch996_tests_city58': True,
        'source_caller_closure_script_not_verified': 'scripts/close_barmaid_latent_context_v779.py',
        'formatting_and_context_approval_for996_still_false': True,
        'next': 'Classify source byte-window use and finish original caller/guard closure;preserve original dispatch and retained996 wording.'})
    protected = read('work/analysis/scheme_followup_integration_v778/checkpoint.json')['protected_files_unchanged']
    protected[str(CURRENT)] = digest
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 336
    assert ledger['records_with_source_and_prose_pass'] in (339, 370)
    if ledger['records_with_source_and_prose_pass'] == 339:
        save(ROOT/'editorial_ledger_before_v779.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_v779.json').exists()
    ledger['records_with_source_and_prose_pass'] = 370
    ledger['records_with_source_prose_drafts'] = 370
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752, *range(989, 1020)],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '750-752-context-unmapped;989-1019-prose-and-prospective-layout-reviewed;996-caller-reachability-open;all-production-and-gameplay-gates-pending',
        'note': '31 new drafts receive zero completed-record credit. Context996 remains false;all31 formatting approvals remain false until owned production routing and integration.'}
    ledger['coverage_units'][0]['next'] = 'Finish996 original caller/guard classification;integrate31 barmaid drafts via owned no-growth routing,all substituted layouts/copies,registered exact patch and representative actual scenes. Continue1020 onward,750-752 contexts,wider shared/all routes/other prose. Preserve graphics audit and older-record follow-up.'
    ledger['latest_checkpoint'] = 'V779 reviews31 barmaid entries(14 revisions/17 retained).21 native barmaids/114 lookups/84 caller cases establish30 catalog variants;996 is a latent original city58 branch with unresolved unaligned reference lead.24 native first-name editor/setter/getter/save-load cases prove16-byte field/17-byte serialized extent.273 prospective layouts and52 full-font planes pass;five naive article warnings are exactly source-bound player-name initials with a literal-prose negative control.370 source/prose,34 drafts;336 complete remains unchanged. V778 stays latest;production integration/actual scenes and wider prose/graphics remain unfinished.'
    checkpoint = {'id': 'V779-barmaid-source-prose-name-contract-and-layout-research', 'documentation': str(DOC),
                  'new_source_prose_records': 31, 'draft_revisions': 14, 'retained_wordings': 17,
                  'new_editorially_completed': 0, 'new_ROM': False, 'manuscript': str(MANUSCRIPT),
                  'native_context': str(ROOT/'native_context.json'), 'name_bounds': str(ROOT/'captain_first_name_bound.json'),
                  'prospective_layouts': str(ROOT/'layouts_v1/verification.json'),
                  'typed_name_diagnostics': str(ROOT/'layouts_v1/name_token_findings.json'),
                  'remaining_gates': ['996 original reference/guard closure', 'Owned no-growth production routing',
                                      'Scoped layouts and complete native copies', 'Registered combined ROM/exact patch',
                                      'Actual representative scenes and New Game regression'], 'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V779: barmaid conversation and editable-name research

31 entries989–1019 have clean-source/prose review:14 proposed revisions and17
retained wordings.30 have mapped original catalog context;996 still needs caller
reachability closure. All31 remain drafts with formatting approval false.370 have
source/prose passes,including34 active drafts;336 completed(245 revised/91 retained)
is unchanged. V778 remains the latest registered ROM;no ROM,patch or registry edit.
The full editorial goal and separate graphics audit remain unfinished.

## Natural English and factual fidelity

Revisions make introductions,family obligations,gift thanks,garden reflections,
song explanations,ruin descriptions,fashion judgments,fortune-telling and flirtation
more conversational. Days off replaces the misleading holidays;spoil you... just a
little preserves the teasing offer without specifying a sexual act.1015 retains
the criticism of restrictive gender roles and women\'s broader social participation.
991 preserves hope for a nice partner/happiness without inventing marriage. Songs
retain fado and the woman awaiting her seafaring lover,without adding death or
abandonment. Source opinions about fur hunting remain character dialogue. Already
natural lines are retained;approved name spellings and all runtime names remain.

Original city and gift branches select independent paragraphs;adjacent storage is
not scene order.989 introduces BARMAID then CAPTAIN FIRST NAME;990 supplies CAPTAIN
FIRST NAME then BARMAID;999 supplies only the captain\'s first name. No surname,
full name,title or faction is substituted. Native114 city lookups find21 real
barmaids.84 original caller/provider fragments cover all30 catalog-reachable IDs
and preserve existing827/840 defaults. The one-in-three ordinary-chat case begins
after its original random branch;no random event or actual gameplay is claimed.

## Real name bounds and prototype display

The actual first-name editor passes16 bytes to its keyboard.24 current-ROM native
cases cover ASCII lengths1–16 and CP932 lengths2–16. Original dispatch,strlen/copy,
record-to-shadow setter,first-name getter,NUL and adjacent guards pass. Both original
17-byte save/load caller loops execute completely. Keyboard UI and byte-I/O helpers/
physical saves are explicit contracts;the compiler\'s former company-name18-byte
bound is not used for this different field.

273 supplied-name layouts cover four actual defaults(Rafael,Hodram,Lil,Maria),the
six real introduction-name values and35 supplied captain-name variants,including
legal maximum-length,spaced,hyphenated and CP932 names. Every substituted byte,word,
guard,callee-saved contract,row bound and final row passes.52 complete native font
planes independently match the game font;all five preview sheets were visually
reviewed for readability,margins and full leading/trailing letters. They are CPU
previews,not in-game screenshots or production-dispatcher verification.

Five naive weak-ending diagnostics concern a literal player name A or a name
component A. Exact expanded-byte origin maps bind every affected token to the
captain-first-name argument. The same displayed text authored as literal prose
does not receive this classification. No English-article,weak-ending or arbitrary
name warning is waived globally;the original diagnostics and exact cases remain.
No unresolved prose/layout finding remains in these273 supplied examples. This
does not exhaust every possible player-authored string or grant release approval.

## Open996 source mismatch

Original996 is selected by the city58 branch,while the immutable21-barmaid lookup
has no city58 entry;Osaka\'s entry is59. All84 real city/actor cases skip996. A
separate explicitly invalid city58/actor59 CPU pairing reaches its source speech.
That is branch research,not a valid ordinary-game activation or an invented pairing.
The existing wording is retained and context approval remains false.

A caller-closure scan finds the expected original ARM calls,but also an unaligned
four-byte scan hit at020E5789→02059400 spanning source words. This is not confirmed
as an executable pointer and is not dismissed as harmless. The attempted closure
script fails its gate and receives no verification credit. Classify that lead and
finish original guard/caller closure before approving996. No original city dispatch
or catalog is patched to make a test pass.

## Next gates and preserved state

Establish owned no-growth production routing,prove the actual parent/ID path,
complete copies and registered reconstruction patch,then exercise representative
introductions,ordinary chat,gifts and transitions in actual cold-boot gameplay.
No completed-record credit,earned gifts,travel,full-route or hardware verification.
1020 onward,750–752 contexts,wider shared/all routes/other prose remain in scope.
The18 original plaques,remaining graphics audit and older-record follow-up stay
unfinished. User676/677 formatting watch and V778 remain intact. Canonical,clean,
prior candidates and original donor saves remain hash-exact. Research and previews
are archived on E:/Rota Nova translations/Editorial review/V779 Barmaid research;
they are not promoted as guide screenshots. No GitHub commit/push was performed.
''', encoding='utf-8')
    heading = '## V779: barmaid prose and name-layout research'
    section = f'\n\n{heading}\n\n31 source/prose drafts(14 revised/17 retained);30 catalog contexts mapped,996 caller/guard closure open.21 barmaids,114 lookups,84 native caller cases and24 native first-name editor/setter/getter/save-load cases pass.273 prospective layouts and52 independent fonts/five reviewed sheets pass;five apparent article endings are source-bound name initials with a negative control.370 source/prose,34 drafts;336 complete/V778 unchanged. Production integration/copies/patch/gameplay and broader prose/graphics remain open. See [V779 research](barmaid_v779_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs')/name
        prior = path.read_text(encoding='utf-8')
        if heading not in prior:
            path.write_text(prior.rstrip()+section, encoding='utf-8')
    save(ROOT/'checkpoint.json', {'latest_ROM_unchanged': latest, 'new_source_prose_IDs': list(range(989, 1020)),
                                  'new_completed_records': 0, 'source_prose_total': 370, 'active_drafts': 34,
                                  'protected_files_unchanged': protected, 'goal_status': 'active',
                                  'all_five_preview_sheets_visually_reviewed': True,
                                  'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE/'evidence'/path.relative_to(ROOT))
    for path in [DOC, LEDGER, MANUSCRIPT, Path('out/editorial_review_latest.json'), *sorted(Path('scripts').glob('*v779.py'))]:
        copy(path, ARCHIVE/path)
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json', {'latest_ROM_unchanged': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE/p).read_bytes()) == h for p, h in files.items())
    print('V779 research recorded:370 source/prose,34 drafts;336 completed and V778 ROM unchanged. Goal active.', flush=True)


if __name__ == '__main__':
    main()
