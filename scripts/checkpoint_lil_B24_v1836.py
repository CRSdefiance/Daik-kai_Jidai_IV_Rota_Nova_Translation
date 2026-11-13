"""Persist B24 native/reference progress without premature editorial completion."""
import json
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_checkpoint_v1836')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DOC=Path('translations/lil_trade_routes_officers_editorial_manuscript_v3.json')
PROOFS=[Path(p)for p in [
 'work/analysis/lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json',
 'work/analysis/lil_B24_font_approval_v1827/visual_review.json',
 'work/analysis/lil_B24_relocation_v1828/parity_and17_native_command_research.json',
 'work/analysis/lil_B24_research_v1829/research_image_receipt.json',
 'work/analysis/lil_B24_loader_v1830/whole_SC2_and_B24_initial_entry_proof.json',
 'work/analysis/lil_B24_event_context_v1832b/original_full_event24_and_packed_set_prefix.json',
 'work/analysis/lil_Amsterdam_location_v1833c/coordinate_only_preflight.json',
 'work/analysis/lil_B24_reference_census_v1835/complete_shipped_entry_and17_mapped_command_census.json']]

if __name__=='__main__':
    assert not ROOT.exists()
    before=read(LEDGER);ledger=deepcopy(before)
    assert before['records_editorially_completed']==1516 and before['records_with_source_and_prose_pass']==1645
    assert len(read(DOC)['records'])==13
    assert read(PROOFS[-1])['all17_native_commands_reexecuted_clean_current_and_research']
    assert read(PROOFS[-3])['source_flag27_requires_empty_intersection_with_original_owner_set']
    assert read('work/analysis/lil_B24_research_run_v1831/terminal.json')['frame']==43800
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes())
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    note=('B24:13 complete native/independent font planes,104 native macro/catalog cases andboth sheets viewed. '
          'All17 native commands preserve sourcepreambles/parity;research resize856->992bytes(+136),inverse exact. '
          'Both current/research336 whole loads and672 parent modes each pass. Clean/current/research code/overlay censuses '
          'find only original24070 interpreter entry,no literal alias. Source flag27 packed word0x00FFFFFF(bytesFFFFFF00) '
          'excludes owner-set bit0;native set decode/intersection andfour full predicate cases pass oncopied RAM. '
          'Original condition16 blocks Bruges3,condition14 requires Camille. Prior navigation test1831 ended43800 normally. '
          'Successor1834 coldboots withtwo separately declared16-byte location fixtures;actual B24 activation/display/return pending. '
          'No registered ROM,patch,source-prose counts orcompleted-entry counts changed. V1807 experimental,V1492 promoted. '
          'Full editorial goal active;broader shared/routes/player prose andseparate graphics/all18 plaques remain unfinished.')
    ledger['latest_checkpoint']='V1836 '+note
    ledger['formatting_watchlist']['Lil_B24_trade_routes_officers13']={
        'status':'complete-native-font-and-source-entry-proofs;actual-scene-and-registered-integration-pending',
        'manuscript':str(DOC),'proofs':{str(p):sha(p.read_bytes())for p in PROOFS},
        'all13_complete_leading_and_trailing_glyphs_bounds_and_zero_row_origins':True,
        'actual_all13_holds_scene_transition_and_registered_exact_patch_still_required':True}
    active=ledger['active_source_prose_drafts']['manuscripts']
    if str(DOC)not in active:active.append(str(DOC))
    ledger['next_route_scene_editorial_packet'].update(manuscripts=[str(DOC)],
        native_font_and_entry_proofs_complete=True,full_original_event_prefix_mapped=True,
        actual_activation_pending=True,editorial_review_complete=False)
    ledger['research_checkpoints'].append({'id':'V1836-Lil-B24-native-and-entry-contracts',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,
        'source_prose_reviews_added':0,'full_goal_complete':False})
    for key in ('records_editorially_completed','records_with_source_and_prose_pass',
        'records_revised_and_integrated','retained_wordings_editorially_completed',
        'current_integrated_candidate','unresolved_graphics_work','completed_editorial_record_counts_by_file',
        'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1836_pending.json');assert not pending.exists()
    save(pending,ledger);os.replace(pending,LEDGER)
    Path('docs/lil_B24_v1836_native_checkpoint.md').write_text('# V1836 Lil B24 native/reference checkpoint\n\n'+note+
        '\n\n'+ '\n'.join('- '+p.as_posix()for p in PROOFS)+
        '\n\nFailed1832 expected inclusion instead of original exclusion;1832b corrects polarity. '
        'Failed1833 assumed Bruges small-town geometry;1833b maps Amsterdam24-offset/40-radius,butits six water guesses allcollide. '
        '1833c source-scans81 in-radius points anduses nearest water20680,4136. All failures wereoffline assertions beforeanylive fixture. '
        'Frozen producers retained;no production defect orfallback hidden.\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:
            f.write('\n\n## V1836 Lil B24 native/reference progress\n\n'+note+
                    '\n\nSee [checkpoint](lil_B24_v1836_native_checkpoint.md).\n')
    handoff='''# Current editorial handoff - V1836

## Active objective and preservation rules

Complete the full scene-by-scene editorial review against clean Japanese: shared shops/towns, every route and all remaining player-facing prose. Use faithful natural en-US and approved Rafael, Joakim, Maria and Camille. Follow natural-dialogue-v2, exact source/current coverage, native formatting, targeted actual gameplay, registered integrated releases and exact clean-input patches. Goal remains active; no subagents authorized. sources/ is read-only. Preserve ALL generated ROMs (user override of retention rules). Executed producers/manuscripts/proofs stay frozen; correct via explicit successors.

Separate graphics audit and all18 plaques remain unfinished. Texture and borders accepted only. Four low-resolution Online bodies excluded; preserve two brown marks. Older-record re-audit follows the full editorial goal.

## Current coverage and registered release

- Ledger: translations/editorial_review_current_v1.json. 1516 complete =1146 revised +370 retained;1645 source/prose reviewed.
- Completed per file1402 COMMON+114 SC2;reviewed1518 COMMON+127 SC2.13 B24 drafts reviewed butincomplete (12 revisions1 retention).116 reviewed-incomplete COMMON andbroader untouched shared/routes/player prose remain.
- Current registered experimental: out/all_routes_combined_v1807_candidate.nds;profile all-routes-unified-v1807;477 manifest batches/114 accepted layers.
- ROM SHA2564851f3c54fba3d4b745a8990002687b943b842e836044ab54285a13ec7648fdc.
- Exact clean patch out/all_routes_combined_v1807_candidate.xdelta SHA2566b3d23db6a718ac73e5b8374441372481bf8492d3a8e3353e130678bd81aedd2.
- Canonical out/raphael_natural_v2_accepted_base.nds SHA2563cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe.
- Clean work/clean.nds SHA256f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d.
- V1492 remains promoted(tag promoted-v1492),SHA25696d0eda08db4f6da69a936a44db1f41abcc1cd6ce202370a9edc5517eb5400fd. No new promotion/push performed.
- Last pushed53c0b58c4be456731024a1e594c3121360395296;branch codex/combined-routes-v89;origin https://github.com/CRSdefiance/Daik-kai_Jidai_IV_Rota_Nova_Translation.git.
- ARM9 SHA256500b7d6cea559d7252ae4e67f94540e67739428823a17cf26842b6827712a41e;staged payload123040bytes unchanged. COMMON SHA256dc26a3260c611fe4686f64deb3d81c4aa50724aa304a7ba399c9ca859b7605ad;SC2 SHA256deda78aaac643baca320abecf7ef2d7002865e7975f29ecd8e1c9bb216156330.

## Immediate work: Lil trade-route/officer scene SC2 B24

Manuscript translations/lil_trade_routes_officers_editorial_manuscript_v3.json.13 source/prose/native-font reviewed lines,12 revisions1 retention. Restored one percent per town,Istanbul,staffing distinction,officers commanding sailors,hearsay andCamilles praise. Preserve actor9 Camille/2 Lil six-byte4000 preambles andone FI runtime Lil expansion. No authored line breaks/alignment. Three narrowly justified line-break-count waivers only. Fixed encoder/profile remains an allocation probe until map approved;11 old allocations too small,complete prose retained.

Proofs (all under work/analysis):

- lil_B24_source_v1822/B24_clean_current_native_source_and_town_predicates.json:clean/current17 commands13 speeches,exact source IDs.
- lil_B24_fonts_v1826/all13_native_macros_and_complete_font_planes.json:104 original native macro/catalog calls;13 full native/independent216x64 planes. Cursor/alignment positions independently source-derived,allvisible origins0,full first/last glyphs.
- lil_B24_font_approval_v1827/visual_review.json:both review sheets13 panels actually viewed;V3 formatting approved.
- lil_B24_relocation_v1828/parity_and17_native_command_research.json:856->992bytes(+136);all13 preambles/parity preserved,four nonspeech commands61FF,A000,C200,terminal0 exact at mapped positions;inverse restores every original logical byte. No relative skip/choice operands.
- lil_B24_research_v1829/research_image_receipt.json:V1807-derived unregistered ROM lil_B24_V1807_derived_RESEARCH_ONLY.nds SHA25684be5d1e7382fcec09ba0846292dec418cff44533f81f843f10dd541c2cd6a28. Only SC2B24 differs;335 other blocks andevery other file/component exact. Not a release/parent.
- lil_B24_loader_v1830/whole_SC2_and_B24_initial_entry_proof.json:current/research336 whole-block loads/cache hits and672 original parent modes each,entry payload+8,SDK IO bridges only.
- lil_B24_event_context_v1832b/original_full_event24_and_packed_set_prefix.json:full original220D8 predicate,source flag27 packed word0x00FFFFFF (bytesFFFFFF00) excludes bit0 oforiginal owner-set. Independent native decode/intersection andfour copied-RAM whole-predicate cases. Original condition16 requires outside Bruges3;14 Camille present. No live town/event mutation. Failed1832 polarity assumption retained.
- lil_B24_reference_census_v1835/complete_shipped_entry_and17_mapped_command_census.json:fresh clean/current/research code sections+overlays only original24070 interpreter call,no pointer alias;all17 complete native walks. Structural opaque effects bridged,not claimed gameplay.

### Specific live test: do not duplicate or restart due timeout

Original1831 test ended normally at43800;terminal.json confirms host slots restored. Ordinary sailing went far north instead ofAmsterdam. It has one16-byte Bruges fixture andno B24 activation.

New explicit successor scripts/run_lil_B24_research_v1834.py,exec session67076,currently coldbooting (verify original handle/process before relying on state). ROOT work/analysis/lil_B24_research_run_v1834;CAP E:/Rota Nova translations/Generated/work/emulation_v193/lil_B24_research_run_v1834_RESEARCH_ONLY. No battery save or savestate. Original script observer733/host ABI installed andrestored by normal terminal. Append-only navigation.jsonl,initial pause29930,replays verified opening/lessons andnormalBruges departure through42520. Then B42550/B42580 closesails,16-byte Amsterdam coordinate fixture42610,Down+B42640anchors,Down+A42760requestsapproach. At42760 inspect actual prompt andnormal A docking. Do not assume B24 activation;read observer/source.

Fixture scripts/native_lil_Amsterdam_location_v1833c.py dispatches original1754 Bruges andnewAmsterdam requests. Each owns only16 coherent position bytes. Native large-town top-left20624,4112+24=center20648,4136,radius40. Original-water81-point scan chooses20680,4136;native78C60 returns2 beforeanytown/event edits. Offline preflight lil_Amsterdam_location_v1833c/coordinate_only_preflight.json. Failed1833 small-town assumption and1833b no-water sixpoint guess preserved;both offline,no live modification. Original town115/events/health/RNG/actor state preserved. Never claim earned travel.

Next:observe original B24 eligibility/entry,all13 speech holds(two complete holds per line),17 complete command pairs,normal terminal return. Audit all inputs,fixture footprints,4MiB snapshots,PNG hashes,observer preservation andhost restoration. View all actual panels/nameplates/portraits/return. Then approve exact source reference map,create successor relocatable manuscript/custom registered post-layer compiler withsource/runtime/QA guards,build cumulative candidate,verify whole research identity/exact clean patch/eight startup controls,andupdate counts only afterallgates. Current registry/ROM/patch andcompleted counts unchanged. Do notcopy research binary into production.

## Completed work to avoid repeating

- Lil opening49:final translations/lil_opening_final_review_v1.json,V1715. All49 actual98 holds90 commands,normalAmsterdam return. No fixture/save.
- Lil lessons64:translations/lil_lessons_final_review_v1.json,V1779 (45 revised19 retained). B120/B23 both choices,70 speech visits140 full holds126 pairs,55 individual IDs+five explicit exact text/speaker/consumer equivalents. RegisteredV1775 whole-ROM exactV1761 research. Four actual proofs1744/1763b-final/1767/1772c;reference map translations/lil_lessons_editorial_relocation_map_v1.json,producer1773. FE original228x48/6x12 logical->16display documented365 papercontract;no glyphstretch. ArchivesV1780/V1795 preserved.
- Fleet sighting15:translations/sighting_editorial_final_review_v1.json,V1794.2700 native wrap/independent planes+15 fresh native samples. Actual614 vicinity/Charles18/Centurione twoholds5413/5443,normalA5503. Original loading normalmode0 admits160..319distance;initialmode1inner<160. Letunseen enemy load medium twice beforeclose;do notset seen/groups. Armed Latina actualname UI remains separateopen.
- Faction reinforcement6:translations/reinforcement_faction_final_review_v1.json,V1814. OnlyV1807 COMMON1911-1916 exactslots revised ships from%s.54 nativecold/warmcopies12caches120layouts7negative controls,eightstartup/exactpatch pass. Actual1911/Charles18/Valdes twoholds5410/5510,A5610entersbattle;19byte own-coordinate/native-diplomatic fixture. GuideE/V1807 Reinforcement announcement verified;archiveV1815.
- Coveringfire7:translations/covering_fire_final_review_v1.json,V1820 (4revised3retained).567 nativewrap/fullindependent planes22freshnative samples. Actual1917/Charles18/Manuel23 regionalfleet57,holds6010/6110,A6310normalduel. Two16/32bytecoordinate fixtures;all4MiB/input/source-disposable saves/observer verified. GuideE/V1807 Covering fire verified;archiveV1825(121files216638896bytes).

## Remaining shared dialogue and Lookout shot

116 reviewed-incomplete COMMON IDs:750-752;1924-1930;1994-2010;2022-2037;2058-2081;2090-2105;2147-2178;2192.750-752 consumer unmapped;productionSC matches areCS lengths,alternate testdataSC3B164 CS0101word750 unclassified. Do notclaim unused. Allbroader untouched routes/player-facing prose remain in scope.

Successful Lookout shot1924-1930 still requiresactualsuccess/dismissal/outcome. Original737C8..74010:ownrole0/index0,enmeyrole2/index0,positive crew,Lookout role7 Aim>150,original519D4(2000) roll<=Aim/10. Nevermodify RNG/message/branch/resultbyte. Originalshot table02117300:(1924,-1,1925,1926,1927,1928,1929,1930). Read-only observer1797 PCs73A44/73B38/73B5C/73B84/73BA0/73BAC.

Last1799pilot session61920terminal6471,206fixtures audited1806,12 qualifying rolls allfailed;originalearnedLookout37->38/Aim166->168 explains strictfixture stop. New scripts/native_lookout_contact_v1798c.py preservesnaturallevel1..100/currentAim>150;offlinepreflight1810passes5503/6195/6471. Notlive yet. Initialown roleActor16room1slot3,emptyprior,slot21actor16;native7E750Luck64->100Aim166withlevel37;nativeAAF38positivecrewto124;maintenance onlystill-live hull/crew. NoRNG/cursor/enemy-result ownership. SourceV1775 bind exactruntime/targettemplates before V1807 reuse. Protected donor regional_fleet_v615/formed_Manuel_regional_copy.dsv SHA2562bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1.

## Execution and evidence

BeforeROM edits readAGENTS.md,docs/build_continuity_protocol.md,translations/release_stack.json,relevantdocs/known_issues.md. Beforeprose readnatural_dialogue_workflow.md/dialogue_delegation_protocol.md. New prose en-US v2,no authoredalignment/LB;preservecompletecontrols/macros;allpalettes/fonts/graphics/nativecodesafe. No automaticpromotion.

C:/Python314/python.exe;PYTHONUTF8=1;PYTHONPATH=.;.deps. Defaultlauncher fails P-drivecredentials;scoped require_escalated works. out/work/analysis areE-drivejunctions;archive lexical absolute().relative_to(cwd.absolute()),neverresolve(). Keepall184 outputROMs plusresearch/reconstructions. Updates<=60seconds,blockingwaits<=60seconds. Neverrestart a live test afterobservationtimeout;poll originalhandle/checkauthoritativeprocess. Boundedsnapshotsarenotproof ofabsenceoftemporarywrite-restore. Targetedheadlesstestsarenotcompleteplaythroughs/hardware. Do notdumpfullledger/registry/help/batchlists.

Prior full V1824 handoff preserved at work/analysis/lil_B24_checkpoint_v1836/handoff_before.md;V1836 receipt recordsallproof hashes. Refresh livehandle/frame beforehandoff toanotherthread. User askedwhethernewthread advisable;recommendedfreshthread,notauthorizedcreationyet.
'''
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',{'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'proofs':{str(p):sha(p.read_bytes())for p in PROOFS},'completed_entries_unchanged':1516,
        'source_prose_reviewed_unchanged':1645,'new_registered_candidate':False,'active_test_session':67076,
        'source_1831_terminal43800':True,'goal_remains_active':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'checkpoint':'V1836','complete':1516,'source_prose':1645,'registered_V1807_unchanged':True},flush=True)
