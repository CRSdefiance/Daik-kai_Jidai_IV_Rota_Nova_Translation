"""Record verified rumor family and separately unfinished scheme drafts."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_tavern_schemes_v774 import MANUSCRIPT
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/condition_rumor_v774')
SCHEMES=Path('work/analysis/tavern_schemes_editorial_v774')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/editorial_v774_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V774 Rumors and scheme drafts')


def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)
    assert sha(source.read_bytes())==sha(target.read_bytes())


def main():
    game=read(ROOT/'gameplay_verification.json')
    context=read(SCHEMES/'native_context.json')
    drafts=read(MANUSCRIPT)
    previews=read(SCHEMES/'prospective_example_verification.json')
    latest=read('out/editorial_review_latest.json')
    assert latest['sha256']==game['candidate_sha256']==context['candidate_sha256']==previews['candidate_sha256']
    assert sha(Path(latest['path']).read_bytes())==latest['sha256']
    assert previews['manuscript_sha256']==sha(MANUSCRIPT.read_bytes())
    assert len(game['actual_condition_rumor_holds'])==2 and game['normal_dismissal_and_town_return_frame']==32800
    assert len(drafts['records'])==56 and all(not r['review']['formatting'] for r in drafts['records'])
    assert sum(r['decision']=='revise' for r in drafts['records'])==44
    prior=read('work/analysis/recruitment_owned_v772/research_checkpoint.json')['protected_files_unchanged']
    for path,h in prior.items():assert sha(Path(path).read_bytes())==h
    ledger=read(LEDGER)
    assert ledger['records_editorially_completed'] in (253,255)
    if ledger['records_editorially_completed']==253:
        assert ledger['records_with_source_and_prose_pass']==258
        save(ROOT/'editorial_ledger_before_v774.json',ledger)
    else:
        assert ledger['records_with_source_and_prose_pass']==314
        assert (ROOT/'editorial_ledger_before_v774.json').exists()
    manuscript='translations/recruitment_editorial_manuscript_v3.json'
    family='Tavern-condition-rumors905-906'
    records=[{'message_id':n,'decision':'revised-and-integrated','manuscript':manuscript,
        'source_native_context_and_complete_font_verified':True,
        'ordinary_actual_display_verified':False,
        'actual_display_with_disclosed_condition_fixture':n==906,
        'actual_display_scope':'Two real906 holds through original paid-round logic;905 represented by same-consumer family sample and prior114-town x12-status x2-voice native matrix. No earned condition event claim.',
        'runtime_argument_contract':['town','original_UI_status'],
        'English_argument_source_indices':[0,1]} for n in (905,906)]
    if not any(f['id']==family for f in ledger['completed_editorial_families']):
        ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':[905,906],
            'records':records,'gameplay_evidence':str(ROOT/'gameplay_verification.json')})
    if family not in ledger['coverage_units'][0]['completed_families']:
        ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['records_editorially_completed']=255
    ledger['records_revised_and_integrated']=191
    assert ledger['retained_wordings_editorially_completed']==64
    ledger['records_with_source_and_prose_pass']=314
    ledger['records_with_source_prose_drafts']=314
    ledger['active_source_prose_drafts']={
        'native_message_IDs':[750,751,752,*range(908,964)],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'750-752-context-unmapped;908-963-source-context-prose-reviewed-formatting-integration-gameplay-pending',
        'note':'All56 scheme drafts remain unfinished. One representative native preview each does not establish full argument coverage or production selector behavior.'}
    ledger['coverage_units'][0]['next']='Finish all56 scheme drafts908-963: full runtime-name layouts,owned no-growth selector/integration,exact patch and representative gameplay. Continue964 onward and750-752 context mapping,then wider shared/all routes/player-facing prose. Preserve graphics audit and older-record follow-up.'
    ledger['latest_checkpoint']='V774 verifies905/906 family in unchanged V773:two actual906 condition-rumor holds,32 whole-screen controls,31 paired state/model/object frames,normal Tavern dismissal and town return.255 complete(191 revised/64 retained).56 scheme drafts908-963(44 revised/12 retained) have source/context/prose and56 prospective font examples;formatting/integration/gameplay unfinished.314 source/prose,59 active drafts including750-752. Full editorial and graphics goals remain unfinished.'
    checkpoint={'id':'V774-condition-rumor-gameplay-and-scheme-source-review',
        'documentation':str(DOC),'source_prose_records':56,'draft_revisions':44,'retained_wordings':12,
        'new_editorially_completed':2,'new_ROM':False,'manuscript':str(MANUSCRIPT),
        'evidence':str(ROOT/'gameplay_verification.json'),'context_proof':str(SCHEMES/'native_context.json'),
        'prospective_examples':str(SCHEMES/'prospective_example_verification.json'),
        'remaining_gates':['All substituted-name layouts and font classes','Owned no-growth production selector and integration','Registered exact patch and representative scheme gameplay']}
    if not any(r['id']==checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    latest['remaining_in_this_registered_batch']='All25 recruitment/condition entries reviewed;broader shared/all-route/player-facing editorial and graphics audit remain open.'
    latest['supplemental_verification']=str(DOC)
    save(LEDGER,ledger)
    save('out/editorial_review_latest.json',latest)
    # A standalone diagnostic did not predict the live fleet-report priorities.
    # Keep that failed approximation visible and outside all verification claims.
    diagnosis=read(ROOT/'live_priority_diagnosis.json')
    diagnosis.update({'usable_as_verification':False,
        'disposition':'Standalone eligibility replay incorrectly predicted no fleet reports while actual game selected three. It is not used for selection,coverage or gameplay claims. Actual frozen input replay is authoritative.'})
    save(ROOT/'live_priority_diagnosis.json',diagnosis)
    DOC.write_text('''# V774: condition-rumor verification and scheme editorial drafts

The V773 ROM and exact clean-input patch are unchanged. The two condition-rumor
entries905/906 now complete the original25-entry recruitment/rumor batch through
native coverage plus a representative actual906 scene. Overall255 entries are
editorially complete:191 revised and64 retained. The wider editorial goal and
separate graphics audit remain active and unfinished.

## Actual scene and test scope

Two terminal32800-frame cold boots compare V770 with V773. Each uses a protected
copy of the London save and the same declared two-byte Amsterdam fixture: Boom3,
duration30. All other4MiB bytes are unchanged at insertion. The fixture receipt
is independently reproduced against each pre-insertion snapshot. The original
save remains unchanged. This tests display; it does not claim an earned boom.

Original paid-round logic chooses three fleet reports before the fourth round's
condition rumor. At28000 and28400, the actual906 text is:

> Word is, Amsterdam's been going
> through a major economic
> boom lately.

Both complete independent font planes,blank-paper cells,left margins,full words,
leading/trailing letters and bounds pass. Portraits and all other screen pixels
match the baseline;advance-indicator frames match original animation.32 complete
screen controls and31 paired state/model/actor/town/item/goods frames pass.
The normal Tavern menu appears at28800;ordinary town return is visible at32400
and held to32800. Original global status labels stay unchanged.905 has prior
source/native/full-font coverage and the same consumer-family sample;it was not
individually activated in this gameplay run. No hardware/full-route claim is made.

A first verifier expected a third rumor hold at28800,but visual inspection showed
the original Tavern menu had already returned while stale template RAM remained.
That frame is now an exact whole-screen dismissal control. An earlier standalone
fleet-eligibility approximation failed to predict live priorities and is explicitly
excluded from verification claims. No rejected observation receives coverage credit.

## Next56 scheme drafts908-963

Clean Japanese,original caller fragments and actual argument providers establish
eight distinct voice tables,320 officer selections,eight original null fallbacks
and eleven caller fragments. The first faction and second faction are distinct
steps;Bad Rumors confirms TOWN then FACTION,whereas Lure Fleet supplies FACTION
then TOWN. Original action labels and faction names are preserved.

44 revised wordings and12 retained wordings are drafted under natural-dialogue-v2.
Corrections include target selection,missing bad-rumor meaning,incomplete questions
and962's unwarranted assumption that the target is an individual person.56
prospective examples use original printf/existing literal wrapping;their complete
independently decoded native font planes pass and all four sheets were visually
reviewed. These are supplied examples,not production-selector or gameplay tests.

All56 drafts remain unfinished:full runtime-name matrices,owned no-growth selector
integration,registered reconstruction patch and representative scheme gameplay
remain required. Formatting approval is false on every draft. Total source/prose
coverage is314;59 active drafts include these56 plus unmapped750-752.964 onward,
other shared text,all routes and other player-facing prose still require review.
The user's676/677 shop-formatting correction remains verified in V773 and stays
on the audit watchlist. No new playable ROM or canonical promotion was made.

Evidence:work/analysis/condition_rumor_v774/gameplay_verification.json and
work/analysis/tavern_schemes_editorial_v774/native_context.json. Captures and
archives remain on E:/Rota Nova translations. The ROM is the registered
all-routes-unified-v773 candidate,SHA256
4b799e769123620bd4574b2dd6fc10ea38ce87d3d28ebc797a78349b1897415b.
''',encoding='utf-8')
    section='''
## V774: condition rumors verified;56 scheme drafts remain open

Unchanged V773 now has representative actual906 rumor verification:two complete
holds,32 whole-screen controls,31 paired native states/models/objects and normal
Tavern dismissal/town return. A declared two-byte Amsterdam Boom fixture tests
display;no earned event or individual905 activation is claimed.255 entries complete
(191 revised/64 retained).56 new scheme drafts(44 revised/12 retained) have source,
context,prose and56 prospective native-font examples;all remain open for full
name layouts,production integration,exact patch and gameplay.314 source/prose;
59 active drafts including750-752. Wider shared/routes/prose and graphics remain
unfinished. See [V774 checkpoint](editorial_v774_checkpoint.md).
'''
    for path in ('docs/todo.md','docs/translation_progress.md','docs/known_issues.md'):
        p=Path(path)
        text=p.read_text(encoding='utf-8')
        if '## V774: condition rumors verified;' not in text:
            p.write_text(text+section,encoding='utf-8')
    files=[LEDGER,DOC,MANUSCRIPT,ROOT/'gameplay_verification.json',SCHEMES/'native_context.json',
        SCHEMES/'source_and_neighbors.json',SCHEMES/'prospective_example_verification.json',
        Path('scripts/verify_condition_rumor_gameplay_v774.py'),Path('scripts/context_tavern_schemes_v774.py'),
        Path('scripts/review_tavern_schemes_v774.py'),Path('scripts/preview_tavern_schemes_v774.py'),
        Path(__file__),Path('out/editorial_review_latest.json')]
    for f in files:
        relative=f.relative_to(Path.cwd()) if f.is_absolute() else f
        copy(f,ARCHIVE/relative)
    shots=Path('E:/Rota Nova translations/Screenshots/Test fixtures/V774 Condition rumors')
    for frame in (28000,28400,28800,32800):
        source=Path(game['capture_reports'][1]).parent/f'frame_{frame:06d}_navigation.png'
        copy(source,shots/source.name)
    for row in previews['sheets']:copy(Path(row['path']),ARCHIVE/'Draft previews'/Path(row['path']).name)
    save(ROOT/'checkpoint.json',{'completed':255,'revised':191,'retained':64,'source_prose':314,
        'active_drafts':59,'same_registered_V773_ROM':latest['sha256'],
        'archive':str(ARCHIVE),'fixture_screenshots':str(shots),
        'protected_files_unchanged':prior,'producer_sha256':sha(Path(__file__).read_bytes()),
        'full_goal_complete':False})
    print('255 complete;56 new scheme drafts remain open. V773 ROM/patch,canonical and donors unchanged;E-drive evidence saved.',flush=True)


if __name__=='__main__':main()
