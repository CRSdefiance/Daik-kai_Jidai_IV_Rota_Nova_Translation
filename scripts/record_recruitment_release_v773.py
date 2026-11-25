"""Record completed recruiting family and explicitly unfinished rumor gameplay."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_recruitment_release_v773 import ROOT,RESEARCH,MANUSCRIPT,CONFIG
from scripts.verify_village_wrap_v608 import read,save

ROM=Path('out/all_routes_combined_v773_candidate.nds')
LEDGER=Path('translations/editorial_review_current_v1.json')
DOC=Path('docs/recruitment_v773_checkpoint.md')
ARCHIVE=Path('E:/Rota Nova translations/Editorial review/V773 Recruitment')
SHOTS=Path('E:/Rota Nova translations/Screenshots/Guide candidates/V773 Recruitment')


def copy(source,target):
    target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    assert sha(source.read_bytes())==sha(target.read_bytes())


def main():
    registered=read(ROOT/'registered_verification.json');patch=read(ROOT/'patch_proof.json')
    game=read(ROOT/'recruitment_gameplay_verification.json');doc=read(MANUSCRIPT);config=read(CONFIG)
    manifest=read(ROM.with_suffix('.manifest.json'));digest=sha(ROM.read_bytes())
    assert registered['candidate_sha256']==patch['candidate_sha256']==game['candidate_sha256']==digest
    assert patch['byte_exact_reconstruction'] and game['source_cost']==1573
    assert {r['message_id'] for r in game['actual_cost_invitation_crowd_count_holds']}=={890,897,904,907}
    protected=read(RESEARCH/'research_checkpoint.json')['protected_files_unchanged']
    for path,h in protected.items():assert sha(Path(path).read_bytes())==h
    latest={'path':str(ROM),'sha256':digest,'profile':manifest['profile'],'MESFILE_sha256':config['target_common_sha256'],
        'ARM9_sha256':config['target_arm9_sha256'],'patch_sha256':patch['patch_sha256'],'status':'experimental',
        'manifest':str(ROM.with_suffix('.manifest.json')),'details':str(DOC),
        'initial_source_pins_retained_as_V743_reference_not_overwritten':True,
        'remaining_in_this_registered_batch':'905/906 condition-rumor actual scenes;other broader editorial/graphics work remains',
        'full_goal_complete':False}
    ledger=read(LEDGER);assert ledger['records_editorially_completed']==230
    save(ROOT/'editorial_ledger_before_v773.json',ledger)
    complete=list(range(883,905))+[907];records=[]
    for row in doc['records']:
        n=row['message_id']
        if n not in complete:continue
        records.append({'message_id':n,'decision':'revised-and-integrated' if row['decision']=='revise' else 'retain-wording',
            'manuscript':str(MANUSCRIPT),'source_native_context_and_complete_font_verified':True,
            'ordinary_actual_display_verified':n in(890,897,904,907),
            'actual_display_scope':'Ordinary cost/invitation/crowd/count sample covers all four original recruiting consumer shapes;other19 voices have source/native/full-font coverage',
            'runtime_argument_contract':row['source_native_arguments'],'English_argument_source_indices':row['English_argument_source_indices']})
    assert len(records)==23 and sum(r['decision']=='revised-and-integrated' for r in records)==14
    family='Tavern-recruitment-voices-volunteer-count-and-crowd883-904-907'
    assert not any(r['id']==family for r in ledger['completed_editorial_families'])
    ledger['completed_editorial_families'].append({'id':family,'native_message_IDs':complete,'records':records})
    ledger['records_editorially_completed']=253;ledger['records_revised_and_integrated']=189;ledger['retained_wordings_editorially_completed']=64
    ledger['current_integrated_candidate']={k:v for k,v in latest.items() if k not in('details','full_goal_complete')}
    ledger['active_source_prose_drafts']={'native_message_IDs':[750,751,752,905,906],
        'manuscripts':['work/analysis/market_contract_v758/unmapped_750_752_prose_DRAFT.json',str(MANUSCRIPT)],
        'status':'750-752-context-unmapped;905-906-integrated-native-reviewed-actual-condition-scenes-pending',
        'note':'The goal still includes905/906 and all broader shared/routes/prose;this checkpoint does not remove those requirements.'}
    ledger['coverage_units'][0]['completed_families'].append(family)
    ledger['coverage_units'][0]['next']='Verify actual905/906 town-condition rumors,then908 onward;map750-752 and continue broader shared/Lil/all route and player-facing prose. Preserve separate graphics audit and older-record follow-up.'
    ledger['latest_checkpoint']='V773 integrates25 drafts;23 recruiting entries complete via all native gates and actual four-consumer family sample.253 complete(189 revised/64 retained),258 source/prose.905/906 native-reviewed and integrated but actual rumors remain pending;750-752 context remains open.1573-gold charge,34 volunteers,crew confirmation/return and7 New Game frames pass.470/114 inherited layers and exact clean patch verified. Full editorial and graphics goals remain unfinished.'
    ledger['formatting_watchlist']['reference_case']+=' V773 retains repaired676/677 bytes and research native wrapping exactly;actual recruiting four-consumer glyphs,blank paper,bounds,crew follow-up and return are verified. No new actual activation of676/677 is claimed.'
    save(LEDGER,ledger);save('out/editorial_review_latest.json',latest)
    DOC.write_text(f'''# V773: recruitment integrated; condition-rumor gameplay remains open

23 recruiting entries883–904 and907 complete editorial review:14 revised,nine
retained. Overall253 complete(189 revised/64 retained),258 source/prose passes.
Five remain active drafts:750–752 caller contexts and905/906 actual rumor scenes.
The full shared/all-route/player-facing editorial goal and separate graphics audit
remain unfinished. The new registered build includes all25 reviewed paragraphs,
but this checkpoint grants no completion credit to905/906.

## Verified meaning and presentation

Clean Japanese,neighboring selections and original callers establish every voice
and substitution. Cost is a recruitment plan,not a promised headcount.904 reports
willing volunteers before assignment.907 is the crowd's nautical affirmation
“Aye!” Existing natural voices are retained. No new rank,kinship or gender is
invented. Approved Rafael,Joakim,Maria and Camille choices remain unchanged;the
donor's existing player-entered captain name is preserved.

The no-growth runtime and complete selection map from V772 reproduce exactly.
128644 paired scope/register cases,84 quantity cases,140 whole8MiB typed-field
contracts,3423 substituted layouts,91 independent full fonts and7336 whole cold/
warm message copies pass. Fourteen private allocations/four source tails preserve
all section,autoload,BSS,cache and123040-byte staged-payload sizes.114 fixed town
culture/NPC mappings and627 isolated original-wrapper pointer-construction cases
resolve this batch to the portrait core;the separate null system core is unchanged.

Eight actual holds across890,897,907,904 have complete independently decoded
font planes and blank-paper checks. All pixels outside the dialogue body,
including portraits and controls,match V770. The actual1573-gold charge matches
{game['cash_before']}→{game['cash_after']};34 volunteers lead into the original Recruit More,
Assign Sailors and unassigned-crew confirmation sequence,then normal town return.
{len(game['whole_screen_controls'])} other full frames and{len(game['paired_native_state_model_frames'])} native state/model/object pairs match.
Seven fixture-free New Game/title/captain/opening frames are byte-identical.
Recruiting runs use ordinary inputs and copied isolated donor saves,no RAM
fixture or savestate. These are targeted automated emulator tests,not a full
route playthrough or physical hardware verification.

905/906 preserve hearsay,recency,severity and complete grammatical condition
phrases such as “a serious shortage of luxury goods.” All native/font/copy checks
pass,but their actual gameplay scenes remain required. The existing donor has
genuine North Sea booms in London,Amsterdam,Nantes and Oslo;the current Istanbul
scene has no eligible same-region condition. A bounded location fixture or another
genuine save can test the original rumor caller585D4 without fabricating those
conditions. No such new fixture is claimed as executed by this checkpoint.

## Experimental release

- ROM:`{ROM}`;SHA-256:`{digest}`.
- Canonical base:`out/raphael_natural_v2_accepted_base.nds`;
  SHA-256:`3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe`.
- Profile:`{manifest['profile']}`;all470 batches/114 accepted layers and the
  complete inherited experimental stack remain. Canonical promotion is not made.
- Only`/COMMON/MESFILE.DK4` and`/__arm9__.bin` differ from V770;all other files,
  overlays,ARM7 and previous graphics remain byte-identical.
- COMMON:`{config['target_common_sha256']}`;ARM9:`{config['target_arm9_sha256']}`.
- Patch:`{ROM.with_suffix('.xdelta')}`;SHA-256:`{patch['patch_sha256']}`.
- Exact clean input:`work/clean.nds`;
  SHA-256:`f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d`.
  The patch reconstructs the entire candidate byte for byte.
- One proven directory digest is added; six explicit configurations replay their
  frozen earlier outputs.3643 other visible strings,19 other blocks,opaque whole
  payloads1854/1865 and the user's repaired676/677 remain exact. Ten negative
  source/current/policy/format/argument gates reject malformed work.
- Verifiers:`verify_recruitment_consumers_v773.py`,V772 ownership/native/copy
  scripts,`verify_recruitment_release_v773.py`,`verify_recruitment_gameplay_v773.py`.
- User cold-boot acceptance remains pending. Recommended areas:title/New Game,
  Tavern recruiting cost/decline/accept,full invitation/count/crew return and the
  remaining condition-rumor scenes. Further work proceeds without preview approval.

ROM,manifest,patch,evidence and six raw guide-candidate captures are saved on E.
All18 original plaques and remaining graphics requirements retain their separate
open audit status;unchanged materials in these screenshots grant no new art credit.
''',encoding='utf-8')
    section='''\n\n## V773: recruitment integrated; condition rumors remain open\n\n23 recruiting entries complete(14 revised/9 retained):253 total(189 revised/64 retained),258 source/prose.25 paragraphs are integrated,but905/906 still need actual rumor scenes;750-752 contexts remain open.128644 scope cases,84 quantity cases,140 whole8MiB contracts,3423 layouts/91 fonts and7336 whole native copies pass. Eight actual holds across four consumer shapes,1573-gold payment,34 volunteers,crew confirmation/return and7 New Game frames pass.470/114 inherited layers and exact clean patch retained. Only COMMON/ARM9 differ from V770. Experimental;all broader prose and graphics work remain open. See [V773 checkpoint](recruitment_v773_checkpoint.md).\n'''
    for name in('translation_progress.md','known_issues.md','todo.md'):
        p=Path('docs')/name;text=p.read_text(encoding='utf-8');assert '## V773: recruitment integrated;' not in text
        p.write_text(text.rstrip()+section,encoding='utf-8')
    selected=[(next(r['capture'] for r in game['actual_cost_invitation_crowd_count_holds'] if r['message_id']==n),name)
        for n,name in((890,'Recruiting_cost'),(897,'Recruiting_invitation'),(907,'Crowd_response'),(904,'Volunteer_count'))]
    capture=read('E:/Rota Nova translations/Generated/work/emulation_v193/recruitment_v773_return_v773/capture_report.json')
    selected += [(next(r for r in capture['frames_captured'] if r['frame']==f),name) for f,name in((7400,'Assign_Sailors'),(8800,'Town_return'))]
    provenance=[]
    for row,name in selected:
        source=Path(row['path']);assert sha(source.read_bytes())==row['PNG_sha256']
        target=SHOTS/f'{name}_V773.png';copy(source,target)
        provenance.append({'path':str(target),'sha256':row['PNG_sha256'],'source_capture':row,'ROM_sha256':digest,
            'unedited_native_capture':True,'experimental_guide_candidate':True,'graphics_audit_still_open':True})
    save(SHOTS/'provenance.json',provenance)
    save(ROOT/'proof.json',{'candidate':latest,'completed_records':253,'new_completed_IDs':complete,
        'revised_total':189,'retained_total':64,'pending_in_this_batch':[905,906],'active_drafts':[750,751,752,905,906],
        'protected_files_unchanged':protected,'goal_status':'active','full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    for path in ROOT.rglob('*'):
        if path.is_file():copy(path,ARCHIVE/'evidence'/path.relative_to(ROOT))
    paths=[ROM,ROM.with_suffix('.manifest.json'),ROM.with_suffix('.xdelta'),DOC,LEDGER,MANUSCRIPT,CONFIG,Path('translations/release_stack.json')]
    paths += [Path('dk4tool/patch')/n for n in('recruitment_editorial.py','recruitment_editorial_runtime.py','recruitment_quantity_runtime.py')]
    paths += sorted(Path('scripts').glob('*v773.py'))+[Path('scripts/build_integrated_release.py'),Path('dk4tool/script/common_message_table.py')]
    for path in paths:copy(path,ARCHIVE/path)
    for path in SHOTS.iterdir():
        if path.is_file():copy(path,ARCHIVE/'guide_candidates'/path.name)
    files={str(p.relative_to(ARCHIVE)):sha(p.read_bytes()) for p in ARCHIVE.rglob('*') if p.is_file() and p.name!='archive_manifest.json'}
    save(ARCHIVE/'archive_manifest.json',{'candidate':latest,'files':files,'source_research_archive':'E:/Rota Nova translations/Editorial review/V772 Owned recruitment runtime research'})
    assert all(sha((ARCHIVE/p).read_bytes())==h for p,h in files.items())
    print('V773 recorded:253 completed,905/906 actual scenes pending. ROM/patch,evidence and six guide candidates saved on E;goal active.',flush=True)


if __name__=='__main__':main()
