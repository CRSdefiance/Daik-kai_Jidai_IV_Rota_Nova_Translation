"""Record source/layout progress while leaving production and gameplay gates open."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.review_scheme_followup_v777 import ROOT, CURRENT, MANUSCRIPT
from scripts.verify_village_wrap_v608 import read, save

LEDGER = Path('translations/editorial_review_current_v1.json')
DOC = Path('docs/scheme_followup_v777_research.md')
ARCHIVE = Path('E:/Rota Nova translations/Editorial review/V777 Followup research')


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    assert sha(source.read_bytes()) == sha(target.read_bytes())


def main():
    manuscript = read(MANUSCRIPT)
    context = read(ROOT/'native_context.json')
    layout = read(ROOT/'layouts_v1/verification.json')
    inputs = read(ROOT/'input_contract.json')
    latest = read('out/editorial_review_latest.json')
    digest = sha(CURRENT.read_bytes())
    assert latest['sha256'] == context['candidate_sha256'] == layout['candidate_sha256'] == inputs['source_ROM_sha256'] == digest
    assert layout['manuscript_sha256'] == sha(MANUSCRIPT.read_bytes())
    assert layout['native_supplied_layouts'] == 13699 and not layout['findings_count']
    assert len(layout['complete_font_planes']) == 53 and len(layout['sheets']) == 5
    assert all(sha(Path(p['path']).read_bytes()) == p['sha256'] for p in layout['complete_font_planes'] + layout['sheets'])
    assert len(context['all160_actual_actor_voice_selections']) == 160
    assert len(context['five_original_consumer_fragments']) == 5
    assert len(manuscript['records']) == 25 and sum(r['decision'] == 'revise' for r in manuscript['records']) == 10
    assert all(not r['review']['formatting'] for r in manuscript['records'])
    assert inputs['six_original_paths_include_Bribe_function_02056998']
    protected = read('work/analysis/tavern_schemes_integration_v776/checkpoint.json')['protected_files_unchanged']
    protected[str(CURRENT)] = digest
    for path, pin in protected.items():
        assert sha(Path(path).read_bytes()) == pin, path
    ledger = read(LEDGER)
    assert ledger['records_editorially_completed'] == 311
    assert ledger['records_with_source_and_prose_pass'] in (314, 339)
    if ledger['records_with_source_and_prose_pass'] == 314:
        save(ROOT/'editorial_ledger_before_v777.json', ledger)
    else:
        assert (ROOT/'editorial_ledger_before_v777.json').exists()
    ledger['records_with_source_and_prose_pass'] = 339
    ledger['records_with_source_prose_drafts'] = 339
    ledger['active_source_prose_drafts'] = {
        'native_message_IDs': [750, 751, 752, *range(964, 989)],
        'manuscripts': ['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json', str(MANUSCRIPT)],
        'status': '750-752-context-unmapped;964-988-source-prose-and-prospective-layout-reviewed-production-and-gameplay-pending',
        'note': '25 new drafts remain unfinished despite clean supplied-value layouts and reviewed previews. No completed-record credit or new ROM.'}
    ledger['coverage_units'][0]['next'] = 'Integrate964-988 via owned no-growth production routing;prove scoped layouts/copies,registered patch and representative actual scenes. Then989 onward,750-752 contexts,wider shared/all routes/other prose. Keep graphics audit and older-record follow-up open.'
    ledger['latest_checkpoint'] = 'V777 source/context/prose-reviews25 followup/bribe/crowd/rumor entries(10 revisions/15 retained),with160 voice selections,five native callers,16 condition branches,13699 clean prospective layouts and53 reviewed full fonts. Source closure proves Bribe fixed nonplayer names;one false Thumb scan candidate is an independently executed original ARM thunk.339 source/prose,28 drafts;311 complete(235 revised/76 retained) unchanged. Production integration/patch/gameplay pending;V776 remains latest. Full editorial and graphics goals remain unfinished.'
    checkpoint = {
        'id': 'V777-followup-source-context-prose-and-prospective-layouts',
        'documentation': str(DOC), 'source_prose_records': 25, 'draft_revisions': 10, 'retained_wordings': 15,
        'new_editorially_completed': 0, 'new_ROM': False, 'manuscript': str(MANUSCRIPT),
        'source_context_proof': str(ROOT/'native_context.json'),
        'source_input_contract': str(ROOT/'input_contract.json'),
        'prospective_layouts': str(ROOT/'layouts_v1/verification.json'),
        'remaining_gates': ['Owned no-growth production routing', 'Full scoped production layouts and copy preservation',
                            'Registered combined ROM and exact clean patch', 'Representative actual gameplay and New Game regression'],
        'full_goal_complete': False}
    if not any(r['id'] == checkpoint['id'] for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(checkpoint)
    save(LEDGER, ledger)
    latest['latest_research_checkpoint'] = str(DOC)
    save('out/editorial_review_latest.json', latest)
    DOC.write_text('''# V777: follow-up,bribery,crowded refusal and separate rumor review

25 entries964–988 have clean-Japanese source/context/prose review:10 proposed
revisions and15 justified retained wordings. These remain drafts.311 editorial
entries are complete(235 revised/76 retained),unchanged.339 have source/prose
passes;28 active drafts include these25 and context-unmapped750–752. V776 remains
the latest registered combined ROM. No new ROM,patch or canonical promotion.

## Source and natural English

Four unchanged original voice tables select24 records across40 real officer
objects:160 native selections and four null fallbacks pass. The separate972 uses
a town barmaid/NPC caller. Five executed original caller fragments prove the role,
table/ID and argument order. Sixteen original condition-branch cases establish
that972 follows condition codes5–11;it is not a scheme result. Full original
control spans show the arrangement reply before the1000-gold deduction and the
crowded refusal returning before scheme selection or payment. Adjacent message
storage never establishes a sequential conversation.

The10 revisions address stiff town-selection/confirmation wording,a regular-run
ship rumor,and more natural seat/privacy refusals. TOWN precedes FACTION in each
bribe confirmation;no argument is lost or reversed. Preserve Admiral only where
spoken,seat availability where explicit,and tomorrow only in988. Arrangement
replies keep each voice's anticipation or uncertainty without claiming the scheme
has succeeded.972 retains this month's expected regular run,storm/sinking and
hearsay;it invents no ship name,cargo,piracy or certainty. Existing natural replies
are retained,with full-width Latin I normalized by the established literal path.
All paragraphs use natural-dialogue-v2/en-US and have no authored alignment/LF.

## Native supplied-value layouts and previews

13699 prospective original printf/literal-formatter cases cover all25 entries,
including114 town names ×20 fixed faction names for each of six confirmations.
Every complete word,substitution,guard/callee-saved contract,four-row width bound,
final row and weak-ending check passes without findings.53 complete native font
planes independently match the game font;all five preview sheets were visually
reviewed for complete letters,margins,line breaks and readability. These are CPU
layout/font previews,not gameplay activations or production-dispatcher approval.

The extended current-ROM source proof closes six original scheme paths,including
the Bribe function02056998 with its original sole caller0205703C. Original first
target selection excludes the edited player company. All20 immutable information
rows/native initializers and save/load boundaries prove fixed nonplayer names.
The earlier legal edited-name stress warnings are not waived globally;those names
cannot reach this specific original consumer. The original prospective report's
then-pending input note is resolved by neighboring input_contract.json.

A bytewise scan initially decoded original ARM branch0208961C as a Thumb BLX into
the Bribe function. Source/current complete thunk bytes are exact,all pointer
references are even,and native ARM execution reaches020C7558 with the original
minus80 this adjustment and Thumb mode clear. Only that exact unchanged ARM
instruction is classified;there is no generic Thumb-reference waiver. An early
test's guessed object indices were corrected using actual native catalog getters:
town0 is London,Clifford is faction4. No rejected probe receives coverage credit.

## Required next gates and preservation

Formatting approval remains false on every draft. Establish exact production
parent/table routing in already owned storage,with no section/cache/payload growth;
repeat scoped production layouts and complete native copy preservation;register
the combined release and exact clean-input patch;verify representative actual
bribe/follow-up/condition/refusal scenes,normal transitions and ordinary New Game.
No successful scheme,earned qualifications or ordinary-event activation is claimed.

Canonical base,clean ROM,original donors,V773 and V776 remain hash-exact. The
user's676/677 formatting repair and watchlist remain intact.989 onward,other shared
text,all routes and remaining player-facing prose still need review. The separate
graphics audit,18 original plaques and older-record follow-up stay unfinished.
Research,source pins,native reports,preview sheets and manuscript are archived at
E:/Rota Nova translations/Editorial review/V777 Followup research. No guide-scene
or physical hardware verification is claimed.
''', encoding='utf-8')
    heading = '## V777: follow-up and bribe editorial research'
    section = f'\n\n{heading}\n\n25 source/context/prose drafts(10 revised/15 retained),160 original voice selections,five caller fragments,16 condition branches,13699 clean supplied-value layouts and53 visually reviewed independent font planes. Six source calling paths and fixed-name providers are closed;one false Thumb scan hit is proven an original ARM thunk.339 source/prose,28 active drafts;311 completed remains unchanged. Production routing/integration/copies,exact patch and actual scenes remain required. V776 stays latest;broader shared/routes/prose and separate graphics audit remain open. See [V777 research](scheme_followup_v777_research.md).\n'
    for name in ('translation_progress.md', 'todo.md', 'known_issues.md'):
        path = Path('docs')/name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip()+section, encoding='utf-8')
    save(ROOT/'checkpoint.json', {'candidate_unchanged': latest, 'new_source_prose_IDs': list(range(964, 989)),
                                  'new_completed_records': 0, 'source_prose_total': 339, 'active_drafts': 28,
                                  'protected_files_unchanged': protected, 'goal_status': 'active',
                                  'all_five_preview_sheets_visually_reviewed': True,
                                  'full_goal_complete': False, 'producer_sha256': sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE/'evidence'/path.relative_to(ROOT))
    for path in [DOC, LEDGER, MANUSCRIPT, Path('out/editorial_review_latest.json'),
                 *sorted(Path('scripts').glob('*v777.py'))]:
        copy(path, ARCHIVE/path)
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json', {'candidate_unchanged': latest, 'files': files, 'full_goal_complete': False})
    assert all(sha((ARCHIVE/p).read_bytes()) == h for p, h in files.items())
    print('V777 research recorded:339 source/prose,28 drafts;311 complete and V776 ROM unchanged. Goal active.', flush=True)


if __name__ == '__main__':
    main()
