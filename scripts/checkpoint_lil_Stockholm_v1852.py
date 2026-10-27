"""Record51 source/prose reviews;retain native/control/actual release gates."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Stockholm_checkpoint_v1852')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DOC=Path('translations/lil_Stockholm_encounter_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/lil_Stockholm_source_v1848b/all51_clean_current_native_source_context.json')
PROBE=Path('work/analysis/lil_Stockholm_prose_v1849/all51_source_prose_and_allocation_probe.json')
CONTEXT=Path('work/analysis/lil_destination_contexts_v1847/source_destinations_and_original_random_query_classification.json')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,probe,source=map(read,(DOC,PROBE,SOURCE));assert len(doc['records'])==51
    assert(probe['revisions_proposed'],probe['wordings_retained_after_source_review'])==(38,13)
    assert all(all(r['review'][k]for k in('source','context','localization','naturalness'))and not r['review']['formatting']for r in doc['records'])
    failed=[r['id']for r in probe['cases']if not r['size_independent_research']['encodes']]
    assert len(failed)==9 and all('unknown-control'in r['size_independent_research'].get('error','')for r in probe['cases']if r['id']in failed)
    assert sum(r['fixed']['encodes']for r in probe['cases'])==19
    raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1529,1645)
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    ids=[r['id']for r in doc['records']];assert len(set(ids))==51
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']+=51;ledger['records_with_source_prose_drafts']+=51
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']+=51
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].append(str(DOC));drafts['route_record_subsets_pending'][str(DOC)]=ids
    drafts.update(status='116-reviewed-COMMON-and51-Stockholm-source-prose-drafts-open',
        note='B24 complete inV1841. B27 has51 source/prose-reviewed speeches,38 proposed revisions13 retentions. Nine Gerhard0x10 controls blocked bythe current profile;native formatting,reference map,actual paths andregistered integration pending.')
    ledger['coverage_units'].append({'id':'Lil-Stockholm-Hodram51-source-prose','file_path':'/data/SC2.DK4','blocks':[27],
        'record_IDs':ids,'status':'source-context-prose-reviewed;native-control-format-map-actual-release-pending',
        'manuscript':str(DOC),'source_context':str(SOURCE),'proposed_revisions':38,'proposed_retentions':13,
        'completed_entries_added':0,'source_prose_reviews_added':51,'full_goal_complete':False})
    prior_route_metadata=[]
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':
            prior_route_metadata.append(deepcopy(unit))
            unit.update(reviewed_route_records=178,completed_route_records=127,
                next='Map original Gerhard0x10 control inStockholm,verify all51 native layouts/branch references andtargeted scene paths,thenregister the complete scene. Broader all-routes/player-prose scope remains.')
    save(ROOT/'prior_aggregate_route_unit_metadata.json',prior_route_metadata)
    ledger['lil_Stockholm_editorial_v1852']={'source_context':str(SOURCE),'manuscript':str(DOC),
        'source_event27_category5_town7_native_predicate_accepts_offline_context':True,
        'source_prose_reviews_added':51,'proposed_revisions':38,'retained_wordings':13,
        'native_macro_context51_and_complete102_command_inventory':True,
        'unmapped_Gerhard_source_prefix_hex':'10','nine_affected_IDs':failed,
        'no_global_formatter_guard_relaxation_or_ROM_change':True,
        'actual_control_probe_run':'work/analysis/lil_Stockholm_context_run_v1851',
        'actual_probe_session_id':30500,'completed_entries_added':0,'full_goal_complete':False}
    ledger['formatting_watchlist']['Lil_Stockholm_Hodram51']={'status':'source-prose-reviewed;unmapped0x10-andnative-display-pending',
        'manuscript':str(DOC),'source_context':str(SOURCE),'format_probe':str(PROBE),
        'unmapped_control_hex':'10','affected_IDs':failed,'formatting_warnings_waived':False,
        'whole_preambles_leading_trailing_letters_macro_expansion_bounds_pages_andreturns_required':True}
    ledger['next_route_scene_editorial_packet']={'file_path':'/data/SC2.DK4','block':27,'source_context':str(SOURCE),
        'manuscripts':[str(DOC)],'source_prose_review_complete':True,'editorial_review_complete':False,
        'actual_activation_pending':True,'source_context_proof':str(CONTEXT),
        'note':'Independent original event27 explicitly selectsStockholm7 andpasses original full predicate only in anoffline destination copy. LondonB26 remains anunreviewed eligible lead. B25 depends on128,not24.'}
    summary=('V1852 adds51 clean-source/context/prose reviews for Lil Stockholm B27:38 proposed revisions13 justified retentions. '
        '1529 entries remain complete(1158 revised371 retained);1696 source/prose reviewed. '
        'Full original inventory covers102 commands51 speeches andfive speaker IDs. Native macros preserveall4MiB andinput/output guards;'
        'the original name getter uses a separate offline copy becauseit writes the common-name cache. '
        'Remove invented Lord titles,restore one ofthe worlds strongest navies,avoid upgrading a bad experience into physical abuse, '
        'localize rude-address exchanges naturally,andmatch Gerhard Ardelknatts to the established native catalog. '
        '19 fixed probes and42 size-independent probes encode;nine Gerhard speeches fail the unmapped0x10 speaker guard. '
        'No warning waived,no global profile relaxed,no new ROM orcompletion credit. '
        'Unchanged registeredV1841 context test1851 is coldbooting toward originalStockholm discovery/docking to map the control. '
        '116 reviewed-incomplete COMMON plus51 route drafts andbroader shared/routes/player prose remain. '
        'V1492 remains promoted;graphics/all18 plaques andlater older-record re-audit remain separate/open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1852-Lil-Stockholm51-source-prose',
        'proof':str(ROOT/'checkpoint_receipt.json'),'completed_entries_added':0,'source_prose_reviews_added':51,'full_goal_complete':False})
    for key in('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
        'completed_editorial_record_counts_by_file','current_integrated_candidate','unresolved_graphics_work',
        'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_with_source_and_prose_pass']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==1696
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1852_pending.json');assert not pending.exists()and LEDGER.read_bytes()==raw
    save(pending,ledger);os.replace(pending,LEDGER)
    Path('docs/lil_Stockholm_v1852_source_review.md').write_text('# V1852 Stockholm source and prose review\n\n'+summary+
        f'\n\nManuscript: {DOC.as_posix()}\n\nSource context: {SOURCE.as_posix()}\n\n'
        'The current ROM still contains the older English. These51 drafts are not shipped orcountedcomplete. '
        'First map Gerhard\'s original0x10 speaker control through the actual scene;then use anexact-runtime scoped profile,full native fonts,complete reference map andregistered workflow. '
        'Do not permit arbitrary source controls orshorten faithful prose to old allocations.\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:
            f.write('\n\n## V1852 Stockholm source/prose51\n\n'+summary+'\n\nSee [source review](lil_Stockholm_v1852_source_review.md).\n')
    text=HANDOFF.read_text().replace('# Current editorial handoff - V1844','# Current editorial handoff - V1852',1)
    text=text.replace('1645 source/prose reviewed.','1696 source/prose reviewed.',1)
    text=text.replace('reviewed1518 COMMON+127 SC2. No active reviewed-incomplete route drafts;',
        'reviewed1518 COMMON+178 SC2.51 active reviewed-incomplete Stockholm route drafts;')
    marker='## Latest completed scene: Lil trade routes and officers, SC2 B24';assert text.count(marker)==1
    section=f'''## Current working unit: Stockholm B27, source/prose51

{summary}

- Source packet: {SOURCE.as_posix()};prose manuscript: {DOC.as_posix()};allocation probe: {PROBE.as_posix()}.
- Original destination/eligibility proof: {CONTEXT.as_posix()}. CurrentAmsterdam hasno eligible newtown scene;offline London26 andStockholm27 contexts pass. Originalevent80 query advancesonly its original LCG word02168EB8 in a disposable Unicorn copy;neveruseit as a pure query orset live RNG. B25 requires128,not24.
- Frozen1848 failed because the original name getter writes the shared common-name cache.1848b isolates name lookup inanother copied machine;all51 originalmacro calls preserve the original4MiB/input/output/ABI.
- Nine original Gerhard prefix0x10 records are blocked bythe current profile. Keep this guard. Source dispatch2434C resolvesactor16/nameGerhard Ardelknatts,butactual portrait/name effect still requires mapping before scoped formatter support.
- **One live emulator: exec session30500**,scripts/run_lil_Stockholm_context_v1851.py. ROOTwork/analysis/lil_Stockholm_context_run_v1851;CAP E:/Rota Nova translations/Generated/work/emulation_v193/lil_Stockholm_context_run_v1851_RESEARCH_ONLY. RegisteredV1841,no newprose inROM,no save/savestate. Poll originalhandle;neverrestart onobservationtimeout.
-1851 replays exact1834 append-only journal through47650,then normalAmsterdam resupply/departure/sail/log clearing at47770/47930/48180/48430/48630/48750,twoB sailsclosed48780/48810,then16-byteStockholm location-only fixture48840. NativeStockholm knownflag stays0:originaldiscovery/message,docking andeventactivation mustrun. At48840 inspectcapture,clear originaldiscovery log asneeded,anchor(Down+B),approach(Down+A),thenaccept ordinary dockingprompt. Do not assumeactivation beforeobserverconfirmsSC2B27.
- Fixture scripts/native_lil_Stockholm_location_v1850.py dispatches existingBruges1754 andAmsterdam1833c plusStockholm. Stockholm originaltop-left22032,3376,center22056,3400,radius40;source-water target22072,3416. Only16 coherent coordinatebytes owned. Originalknown-town flag0,town115,events/RNG/health/actors unchanged. Noearnedtravelclaim.
- Next:actualoriginal0x10 name/portrait contract,allreachedB27 branches/controlreturn;thenprivate runtime-bound profileextension,nativefullfonts/pages/first-lastletters andcomplete102-command relative-reference map. Compile throughregisteredcumulativeworkflow onlyafterapproval. Keep51 drafts incompleteuntilrequiredgatespass. London111-speechB26 remainsinbroader scope.

'''
    text=text.replace(marker,section+marker,1)
    text=text.replace('All current jobs are **terminal**.','The earlier B24 jobs are **terminal**;newStockholm1851 above islive.')
    text=text.replace('All recorded jobs are terminal;refresh authoritative state before another thread starts testing.',
        'Stockholm1851 is live;poll originalsession30500 or inspectauthoritativeprocess before another thread starts testing.')
    HANDOFF.write_text(text,encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',{'completed_entries_unchanged':1529,'source_prose_before_after':[1645,1696],
        'source_prose_added':51,'proposed_revisions':38,'retained_wordings':13,'formatting_native_reference_andactual_pending':True,
        'prior_route_aggregate_metadata_reconciled_without_extra_completion_credit':True,
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'dependencies':{str(p):sha(p.read_bytes())for p in(DOC,SOURCE,PROBE,CONTEXT)},
        'registered_ROM_andpatch_unchanged':True,'goal_remains_active':True,'full_goal_complete':False,
        'producer_sha256':sha(Path(__file__).read_bytes())})
    print({'complete':1529,'source_prose_reviewed':1696,'new_reviewed_incomplete_B27_lines':51,
        'unmapped_control_records':9,'current_ROM':'V1841 unchanged'},flush=True)
