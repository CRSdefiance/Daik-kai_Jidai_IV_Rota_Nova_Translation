"""Record current manuscript and both actual crew branches; no release completion."""
from copy import deepcopy
from pathlib import Path
import os
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_crew_checkpoint_v1768')
DOC=Path('translations/lil_lessons_editorial_manuscript_v5.json')
MENU=Path('translations/lil_lesson_choices_editorial_draft_v2.json')
FULL=Path('work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json')
EARLY=Path('work/analysis/lil_crew_decline_v1767_decline/complete_B23_scene_and_fixture_audit.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()
    full,early=map(read,(FULL,EARLY))
    assert full['all30_speeches60_holds_full_native_independent_actual_ink_match']
    assert early['all4_speeches8_holds_full_native_independent_actual_ink_match']
    assert len(full['all_original_B23_command_pairs_and_mapped_branches_verified'])==46
    assert len(early['all_original_B23_command_pairs_and_mapped_branches_verified'])==9
    initial=read('work/analysis/lil_crew_scene_v1763_initial/complete_B23_scene_and_fixture_audit.json')
    for a,b in zip(initial['speeches'][:-1],full['speeches'][:-1],strict=True):
        assert a['id']==b['id']
        for x,y in zip(a['two_complete_actual_holds'],b['two_complete_actual_holds'],strict=True):
            assert Image.open(x['capture']).convert('RGB').tobytes()==Image.open(y['capture']).convert('RGB').tobytes()
    doc=read(DOC);font=read(doc['native_font_proof'])
    assert sha(DOC.read_bytes())==font['manuscript_sha256']
    assert all(all(r['review'].values()) for r in doc['records'])
    assert full['research_ROM_sha256']==early['research_ROM_sha256']=='6bc6b6bb01f9ea0e763ee1d6c4c3f2bcb1c7c8cca3be3dd54bd43903045cb55a'
    assert read('work/analysis/lil_crew_final_text_v1764/terminal.json')['terminal']
    assert read('work/analysis/lil_crew_decline_v1766/terminal.json')['terminal']
    assert read('work/analysis/lil_crew_lesson_v1756/terminal.json')['terminal']
    assert read('work/analysis/lil_crew_lesson_v1753/terminal.json')['terminal']
    raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1424,1632)
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    visual=ROOT/'actual_crew_visual_review.json'
    save(visual,{'initial_all3_crew_sheets30_panels_actually_viewed':True,
        'final_current_sheet03_with_Deck_View_instruction_actually_viewed':True,
        'all58_full_RGB_frames_for_other29_paragraphs_exact_to_reviewed_initial_run':True,
        'decline_all4_panels_sheet_actual_choice1_and_terminal_Bruges_actually_viewed':True,
        'original_Dock_at_Bruges_prompt_choice0_menu_and_normal_town_return_actually_viewed':True,
        'complete_first_last_letters_uniform_left_alignment_portraits_nameplates_and_pages_acceptable':True,
        'two_conditional_B23_FE_panels_not_activated_after_already_completed_wind_lesson':True,
        'no_full_route_hardware_or_earned_travel_claim':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in (FULL,EARLY)},'full_goal_complete':False})
    drafts=ledger['active_source_prose_drafts'];pending=drafts['route_record_subsets_pending']
    old=next(k for k in pending if k.replace('\\','/')=='translations/lil_lessons_editorial_manuscript_v3.json')
    assert len(pending[old])==60
    pending[old]=[];pending[str(DOC)]=[r['id'] for r in doc['records']]
    drafts['manuscripts'].append(str(DOC))
    crew_ids={r['id'] for r in full['speeches']}|{r['id'] for r in early['speeches']}
    wind_ids={r['id'] for r in read('work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json')['all22_executed_speeches44_holds_complete_native_independent_actual_pixels']}
    assert len(crew_ids)==31 and len(crew_ids|wind_ids)==53
    unvisited=sorted({r['id'] for r in doc['records']}-(crew_ids|wind_ids));assert len(unvisited)==7
    unit=next(u for u in ledger['coverage_units'] if u['id']=='Lil-sailing-lessons64-source-prose')
    unit.update(manuscripts=[str(DOC),str(MENU)],
        status='all64-native-layout-approved;wind22-and-both-crew-choices31-actual-verified;B120-choice0-map-release-pending',
        source_trigger_proof='work/analysis/lil_crew_trigger_v1751/source_bound_B23_trigger_and_original_predicates.json',
        current_native_font_proof=doc['native_font_proof'],current_actual_crew_proofs=[str(FULL),str(EARLY)],
        current_loader_proof='work/analysis/lil_lessons_loader_v1762/whole_SC2_and_lesson_initial_entry_proof.json',
        individually_actual_speech_IDs=sorted(crew_ids|wind_ids),not_individually_actual_speech_IDs=unvisited)
    ledger['lil_lessons_editorial_v1720'].update(speech_manuscript=str(DOC),
        all64_native_formatting_approved=True,B23_both_choices_and_normal_Bruges_returns_verified=True,
        current_actual_crew_proofs=[str(FULL),str(EARLY)],current_native_font_proof=doc['native_font_proof'],
        current_research_ROM='work/analysis/lil_lessons_research_v1761/lil_lessons_V1711_derived_RESEARCH_ONLY.nds',
        current_research_ROM_sha256=full['research_ROM_sha256'],
        B120_choice0_complete_reference_approval_and_registered_release_pending=True)
    ledger['formatting_watchlist']['Lil_sailing_lessons64'].update(
        manuscripts=[str(DOC),str(MENU)],status='all64-open;current-native-layout-approved;wind22-and-crew31-actual-passed;map-release-pending',
        current_Deck_View_instruction_matches_actual_menu_and_full_actual_ink=True,
        source_town_docking_center_distinct_from_spawn_point_verified=True,
        both_crew_choices_portraits_pages_full_letters_and_normal_returns_verified=True)
    next_note=('Next run B120 choice0 using normal A instead of the wind-option Down/A;its R134/R137 are not yet individually visited. '
        'Use current V1761 research ROM andmanuscriptv5;all B23 branches are now actual verified. Then approve complete scoped '
        'reference map from original EV/cache/parent,124 nested commands36 relative sites/native cases andactual paths. '
        'Register source/runtime-bound post-layer after Lil opening,build cumulative ROM/exact clean patch,verify startup/shops '
        'andwhole research/release identity,then close64. Do not repeat completed B23 oropening without a concrete risk.')
    ledger['next_route_scene_editorial_packet'].update(manuscripts=[str(DOC),str(MENU)],note=next_note)
    summary=('V1768 verifies both original Lil crew-lesson choices after source-mapped Bruges entry. Current V1761 research '
        'ROM6bc6b6bb01f9ea0e763ee1d6c4c3f2bcb1c7c8cca3be3dd54bd43903045cb55a contains current manuscriptv5:only B23R166 '
        'changes fromv3 to match actual Deck View menu label;59 other paragraphs/planes exact. All60 native cases and9 FE '
        'planes reconciled. B120 stays2316;B23 now2592(+284 fromV1711). All336 original loads/cache hits and672 parent modes '
        'pass perROM. Final crew full path46 commands30 speeches60 complete actual holds ends41420;other response9 commands '
        '4 speeches8 complete actual holds ends32940. Both original branches return normally to Bruges. 31 unique crew entries '
        'plus22 prior wind entries give53 individually actual speeches;7 remain without individual visits. All source/native '
        'text gates still cover60 speeches and4 labels. Each successful crew coldboot has one16-owned-byte coordinate-only '
        'fixture;original docking,choice andevent state evolve normally. Earlier out-of-range spawn-based approach was '
        'audited with4 coordinate fixtures andno arrival credit. Original known-town scan uses model top-left plus16,not '
        'spawnpoint;corrected native scan returnsBruges3 without any state edit. Source EV2 event23/category5/action24 '
        'requires completed120,not inAmsterdam2,andCamille presence. No event/RNG/outcome fields forced. All runs terminal. '
        'Next B120 choice0,complete reference approval,registered integration/exact patch/startup gates;all64 entries still '
        'incomplete. Counts1424 complete(1076 revised348 retained),1632 source/prose. Registered V1711 andpromoted V1492 '
        'unchanged;full editorial goal active,graphics/all18 plaques andlater older-record re-audit separate/open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1768-current-Lil-crew-both-choices-and-native-label-refinement',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ['records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'records_with_source_and_prose_pass','completed_editorial_record_counts_by_file','source_prose_reviewed_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','unresolved_graphics_work','current_integrated_candidate']:
        assert ledger[key]==before[key],key
    assert sum(map(len,pending.values()))==64 and ledger['goal_status']=='active' and not ledger['full_goal_complete']
    temp=LEDGER.with_name('editorial_review_current_v1768_pending.json');assert not temp.exists()
    save(temp,ledger);assert read(temp)==ledger and LEDGER.read_bytes()==raw;os.replace(temp,LEDGER)
    text=HANDOFF.read_text(encoding='utf-8');assert text.startswith('# Current editorial handoff - V1749')
    text=text.replace('# Current editorial handoff - V1749','# Current editorial handoff - V1768',1)
    start=text.index('## Current lesson work:');end=text.index('## Earlier COMMON and process safeguards',start)
    current='''## Current lesson work - V1768 authoritative state

All64 entries remain incomplete. Current manuscripts: translations/lil_lessons_editorial_manuscript_v5.json (60 speech/system) and translations/lil_lesson_choices_editorial_draft_v2.json (4 labels).45 proposed revisions19 retentions. Earlier versions frozen. Native/visual review covers all64;actual53 unique speeches verified (wind22 +crew31),7 lack individual visits. Current native font proof work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json;current9 FE proof samefolder/all9_current_FE_reconciliation.json. V5 refines onlyB23R166 to exact Deck View menu label;screen title remains Deck.59 other texts/compiled planes unchanged;four new macro alignments,both native/parity planes,three-line actual FE panel pass. Other25 per-record line-count decisions retained. Do not use staleV3R166/researchV1739 as current target.

Current RESEARCH ONLY ROM:work/analysis/lil_lessons_research_v1761/lil_lessons_V1711_derived_RESEARCH_ONLY.nds,SHA2566bc6b6bb01f9ea0e763ee1d6c4c3f2bcb1c7c8cca3be3dd54bd43903045cb55a. It is not registered,parent,promoted or user handoff. Only SC2B1202076->2316 andB232308->2592 differ fromV1711;334 other blocks andevery other file/component/code/font/art exact. Scoped reference research work/analysis/lil_lessons_relocation_v1760/nested_source_relocation_research.json:60 speeches4 labels36 relative operands,180 relocated native skip cases,inverse source restoration. This is NOT an approved release map;external_references_complete remainsfalse. Current whole-loader proof work/analysis/lil_lessons_loader_v1762/whole_SC2_and_lesson_initial_entry_proof.json:336 original EV-selected block loads/cache hits and672 original parent modes perROM,entry+8 andoriginal0x2400 cache. It does not alone prove later references.

Source/native foundations remain:complete recursive source124 commands (B12069,B2355),work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json;36 original relative sites360 cases,work/analysis/lil_lesson_branches_v1722/original_relative_skip_operand_proof.json.0100 always skips,0200 on prior0,0300 on prior1;target=command+4+u16span. Native choice count/getters,bothlabels/twostyles/selected0,1,cancel12cases:work/analysis/lil_lesson_choice_ui_v1735/original_choice_VM_geometry_and_native_pixels.json. Menu auto-sizing shrinks after removing unused oldpadding;no geometry/font/palette code change. FE geometry resolved in V1737 through independently documented V365 paper contract:logical12px source rows compose to16px displayed origins,without stretching glyphs;exact captured mode1 context228x48,font6x12. All6 current actual planes andall9 reviewed native cases pass. Not an independent whole-GPU trace. Global profiles unchanged;FE only in local runtime-bound profile.

## Source trigger and fixture evidence - do not rediscover

Proof work/analysis/lil_crew_trigger_v1751/source_bound_B23_trigger_and_original_predicates.json executes all336 original event getters against independent table walk. Shipped EV2 event23/category5/action24 selectsSC2B23. It requires completed event120,condition15==0 (fleet2 NOT currently inAmsterdam2) andcondition14==1 (actor9 Camille presence). Both predicates pass actual sea state without any edits. Original090E14-090E4C constructs category5 from active fleet town andcalls21D0C. No special Deck View trigger orspecificBruges requirement inthis record.

Correct location-only fixture scripts/native_lil_Bruges_location_v1754.py,preflight work/analysis/lil_Bruges_location_v1754/source_docking_center_and_location_preflight.json. Town3 original virtualpositionB566C returns top-left20224,4320;type0 adds16 gives actual center20240,4336. Original known-town radius32. Earlier spawn-point north16 target20248,4296 is distance-squared1664,OUTSIDE1024 radius. Correct water target20240,4312 is24 away;original78C60(1) returnsBruges3 andleaves all4MiB exact. The fixture owns only16 bytes:one mobilefixedpoint8 plusfleetcache8;all town/event/RNG/health/inventory/outcomes unchanged. Original town115 remainssea untilnormal docking.

Successful normal controls:after original wind terminal29930,A to30230 clears departure log;B to30260 andB to30290 close sails. Apply validated coordinate fixture thenwait to30320. Down+B to30620 keeps anchor;Down+A to30920 opens sails toward port andproduces native Dock atBruges question. Normal AYes to31220 activates B23 firstspeech at30938. Do not repeat failed guessing of AasDock orFunctions submenu;Functions isSave/Load/Quit/Options. Docking requires original sailing approach/control path. All successful tests coldboot without preloaded save/savestate,using one disclosed location fixture. No earned travel/discovery/full-route/hardware credit.

## Actual crew results - current target verified

- Final full lesson:runner scripts/run_lil_crew_final_text_v1764.py,terminal41420. Proof work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json,successful producer scripts/verify_lil_crew_scene_v1763b.py --version final.46 original commands/branch targets,30 speeches60 complete full-native/independent actual holds,normal original type0 end andBruges town UI. Current R166 Deck View instruction fully verified. InitialV1756 run uses oldinstruction;its30/60 proof andall3 sheets were viewed. Infinal version all58 fullRGB screenshots forother29 paragraphs arebyte-exact;newfinalsheet03 viewed. Full/choice0 menu,portraits,Lil/Camille/Fernando nameplates andTownreturn viewed.
- Other response:runner scripts/run_lil_crew_decline_v1766.py,terminal32940. Proof work/analysis/lil_crew_decline_v1767_decline/complete_B23_scene_and_fixture_audit.json,producer scripts/verify_lil_crew_decline_v1767.py --version decline. Original Down/A selects1;9 commands,4 speeches8 full actual holds,proper nested R30 andearlytype0 return toBruges. All4-panel sheet,choice1 andTownreturn viewed. Both response paths use currentV1761 research ROM.
- Two conditional FE panelsB23R91/R95 are not visited after earlier wind lesson;their complete compiled texts/native planes match separately actualB120R155/R163. No claim of individualB23 activation.
- Prior wind22 proof remains work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json.41 commands44 holds/all6 actualFE,choice1 andtype0 end. Its B120 bytes/code/font areexact to currentresearch. Do not repeat without concrete risk.

All fixture replays,original snapshot hashes,input schedules,PNG hashes andread-only callbacks/host restoration pass. Callbacks prove boundary preservation,not absence of temporary write-restore. One V1756 run-plan slashpath incorrectly says1752c;actual import andfixture hash are1754. Explicit erratum inV1763 proofs. The1763 first audit rejected JSONtuple/list equality only;1763b normalizesserialization andpasses. Navigator1759 first speech completed butthen read a stale observer JSON betweenimage write andpauseflush;1759b waits forobserver mtime>=capture/RAM andcontinues SAME pausedrun,retainingfirst hold. No game bug orforcedinput bypass. Allfailedexecutedproducers preserved.

## Process state and exact next action

ALL CURRENT JOBS TERMINAL:1753missedapproach/47502 at32021;1756full/97532 at41420;1759navigator/9929 at41420;1764final/22528 at41420;1766otherresponse/85448 at32940. No process may be resumed/restarted fromthese oldhandles. New evidence checkpoint work/analysis/lil_crew_checkpoint_v1768/checkpoint_receipt.json.

NEXT run B120 choice0 with normal A instead of Down/A at26231/26331. Initial cold opening schedule through22930 is known;forinteractive navigation filter future inputs to<=22930 topreventduplicate automatic keys. Use V1761researchandmanuscriptv5. R134/R137 have native proofs butnoindividualactualvisit. RemainingthreeB120R62/R80/R109 guidance alternatives share reviewed wording/nativeplanes withactualR186;do not force event/choiceoutcome flags toactivate them. Complete source-bound interpreter caller/reference census plus124nestedcommands36relative sites andactualpaths;approve scoped release map. Then implement registered cumulative post-layer afterlil_opening_editorial,compileall60ownedparagraphs/four typed choice labels/recompute36 spans,withsource/runtime/configlocks andnegative/repeatguards. Do not simplyjoinNULrows orcopy researchbins:choicesandnested0100 spansrequiretyped reconstruction. Existing V1710 source locks globalprofiles/layout/encoder;use localFEprofileunder exactARM9 binding.

Build cumulative registeredROM/exactcleanpatch,verifyallacceptedlayers/allothercomponents/startup/shops,andwholecurrentresearch/release byteidentity. Onlythenclose64 (wouldmake1488 ifallpriorcountsconfirmed). Full editorialgoal stillbroader;graphics/all18plaques andlaterolder-recordre-audit remainopen. No fresh push/promotion authorization.

'''
    text=text[:start]+current+text[end:]
    text+='\n## Latest checkpoint V1768\n\n'+summary+'\n'
    HANDOFF.write_text(text,encoding='utf-8')
    Path('docs/lil_crew_v1768_checkpoint.md').write_text('# V1768 Lil crew andcurrent lesson checkpoint\n\n'+summary+'\n\nSee current handoff andreceipt for exact sources/nextgates.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as f:f.write('\n\n## V1768 Lil crew both responses andcurrent instruction\n\n'+summary+'\n\nSee [checkpoint](lil_crew_v1768_checkpoint.md).\n')
    save(ROOT/'checkpoint_receipt.json',{'completed':1424,'source_prose_reviewed':1632,'new_completed':0,
        'native_layout_approved64':True,'individually_actual_speech_IDs':sorted(crew_ids|wind_ids),
        'not_individually_actual_speech_IDs':unvisited,'all64_entries_still_incomplete':True,'all_current_jobs_terminal':True,
        'current_research_ROM_sha256':full['research_ROM_sha256'],'registered_candidate_unchanged':True,
        'proofs':{str(p):sha(p.read_bytes()) for p in (FULL,EARLY,DOC,MENU,visual)},
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1768 saved:currentV5 native64,53 individual actual speeches,crew both choices;all64 stillopen,full goalactive,alljobs terminal.')
