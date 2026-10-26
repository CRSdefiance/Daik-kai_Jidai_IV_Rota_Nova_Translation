"""Record13 source/prose reviews;preserve separate native/release/actual gates."""
from copy import deepcopy
from pathlib import Path
import os
from dk4tool.dialogue.encoder import encode_fixed_dialogue,encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B24_checkpoint_v1824')
OLD=Path('translations/lil_trade_routes_officers_editorial_manuscript_v1.json')
NEW=Path('translations/lil_trade_routes_officers_editorial_manuscript_v2.json')
SOURCE=Path('work/analysis/lil_B24_source_v1822/B24_clean_current_native_source_and_town_predicates.json')
INVENTORY=Path('work/analysis/lil_followup_inventory_v1821b/source_event_state_and_dependency_inventory.json')
MACROS=Path('work/analysis/lil_B24_prose_v1823/native_macros_and_allocation_probe_NOT_display_approval.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()and not NEW.exists();ROOT.mkdir(parents=True)
    doc=deepcopy(read(OLD));packet=read(SOURCE);macros=read(MACROS)
    assert len(doc['records'])==len(packet['records'])==len(macros['macro_cases'])==13
    profile=get_dialogue_profile('lil-opening-editorial-native-v1');allocation=[]
    for row in doc['records']:
        row.pop('not_yet_a_source_prose_or_formatting_review',None)
        if row['record_index']==9:
            row['english']="{SPEAKER:09}Let's keep signing contracts with more towns. Even a one percent share in each lets us establish our own trade routes.{PAD}"
            row['localization_note']+=' Combine keep this up/sign more contracts as keep signing,anduse each to refer to the immediately named towns. All facts remain explicit;this removes redundant wording without restoring the earlier omitted quantity orshortening to fit the old allocation.'
        assert all(row['review'][k]for k in('source','context','localization','naturalness'))and not row['review']['formatting']
        fixed={'id':row['id']}
        try:
            result=encode_fixed_dialogue(bytes.fromhex(row['source_hex']),row['english'],profile)
            fixed.update(fixed_encodes=True,padding_bytes=result.padding_bytes)
        except ValueError as error:fixed.update(fixed_encodes=False,fixed_error=str(error))
        try:
            result=encode_relocatable_dialogue(bytes.fromhex(row['source_hex']),row['english'].removesuffix('{PAD}'),profile)
            fixed.update(research_size_independent_format_encodes=True,formatted_markup=result.formatted_markup,
                diagnostics=[{'severity':d.severity,'code':d.code,'message':d.message}for d in result.diagnostics])
        except ValueError as error:fixed.update(research_size_independent_format_encodes=False,research_format_error=str(error))
        allocation.append(fixed)
    doc.update(predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),
        status='13-source-context-prose-reviewed;11-fixed-capacity-failures;native-format-map-integration-andactual-pending',
        row_source_prose_review_metadata_now_explicit=True)
    try:validate_natural_dialogue_batch(doc)
    except ValueError as error:assert 'formatting'in str(error).lower()
    else:raise AssertionError('Unreviewed formatting passed release validation')
    save(NEW,doc)
    save(ROOT/'updated_research_allocation_probe_NOT_native_display_approval.json',{'cases':allocation,
        'fixed_encodes':sum(r['fixed_encodes']for r in allocation),'fixed_failures':sum(not r['fixed_encodes']for r in allocation),
        'size_independent_research_format_passes':sum(r['research_size_independent_format_encodes']for r in allocation),
        'source_complete_one_percent_per_town_fact_and_original_city_names_preserved':True,
        'no_approved_relocation_batch_or_map_created_by_this_probe':True,'all_native_full_fonts_glyphs_pages_andactual_scene_gates_pending':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    raw=LEDGER.read_bytes();ledger=read(LEDGER);before=deepcopy(ledger)
    assert(ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1516,1632)
    assert ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']==114
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']==[]
    ids=[r['id']for r in doc['records']];assert len(set(ids))==13
    assert not any(r.get('block')==24 for f in ledger['completed_editorial_families']if f.get('file_path')=='/data/SC2.DK4'for r in f.get('records',[]))
    assert sum(r['editorial_decision']=='revise'for r in doc['records'])==12
    assert sum(r['editorial_decision']=='retain-wording'for r in doc['records'])==1
    (ROOT/'ledger_before.json').write_bytes(raw);(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']+=13;ledger['records_with_source_prose_drafts']+=13
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']+=13
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    drafts=ledger['active_source_prose_drafts'];drafts['manuscripts'].append(str(NEW));drafts['route_record_subsets_pending'][str(NEW)]=ids
    drafts.update(status='116-reviewed-COMMON-and13-Lil-B24-source-prose-drafts-open',
        note='Seven covering-fire entries completed. B24 has13 new source/prose-reviewed butincomplete speeches;12 proposed revisions1 retention. Native formatting,reference mapping,registered integration andactual activation/return remain open.')
    ledger['coverage_units'].append({'id':'Lil-B24-trade-routes-officers13-source-prose','file_path':'/data/SC2.DK4','blocks':[24],
        'record_IDs':ids,'status':'source-context-prose-reviewed;format-map-integration-actual-pending','manuscript':str(NEW),
        'source_context':str(SOURCE),'proposed_revisions':12,'proposed_retentions':1,'completed_entries_added':0,
        'source_prose_reviews_added':13,'full_goal_complete':False})
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':unit.update(reviewed_route_records=127,completed_route_records=114,
            next='Finish native formatting/reference map andfull original B24 trigger/current scene;retain all other routes/player prose in scope.')
    ledger['lil_B24_editorial_v1824']={'source_context':str(SOURCE),'event_inventory':str(INVENTORY),'manuscript':str(NEW),
        'current_macro_proof':str(MACROS),'new_source_prose_reviews':13,'proposed_revisions':12,'retentions':1,
        'original_source_event24_category5_action25_targets_B24':True,
        'not_Bruges_andCamille_present_conditions_mapped_extra_context_prefix_unmapped':True,
        'native_display_reference_map_registered_patch_andactual_pending':True,'completed_entries_added':0,'full_goal_complete':False}
    ledger['formatting_watchlist']['Lil_B24_trade_routes_officers13']={'status':'source-prose-only-native-format-pending',
        'source_context':str(SOURCE),'manuscript':str(NEW),'no_shortening_to_old_slots':True,
        'complete_leading_trailing_letters_source_headers_FI_macro_bounds_pages_andtransitions_must_pass':True}
    ledger['next_route_scene_editorial_packet']={'file_path':'/data/SC2.DK4','block':24,'source_context':str(SOURCE),
        'source_prose_review_complete':True,'editorial_review_complete':False,'manuscripts':[str(NEW)],
        'actual_activation_pending':True,'note':'Dependency-backed candidate,not inferred sequential order. Need full remaining context predicate andoriginal arrival activation outside Bruges.'}
    summary=('V1824 adds13 clean-source/context/prose reviews for Lil SC2B24:12 proposed revisions1 justified retained response. '
        'The complete original native walk inventories17 commands and13 speech objects,with matching clean/current offsets,extents,headers andspeaker prefixes. '
        'All336 original EV2 event getters andcompletion statuses areread-only verified against the shipped table in the verified terminalBruges snapshot. '
        'Only22,23,120 arecomplete;220 uncompleted events pass dependency gates only,not full eligibility. Event24/category5/action25->SC2B24 is the sole uncompleted dependency-ready event directly requiring23/120 (it requires120). '
        'Original condition16 requires not being inBruges3 andcurrently fails;condition14 confirms Camille present. Extra source00FFFFFF context prefix andfull actual activation remain unverified. '
        'One original event161 usesFFFF sentinel dependencies;original23840 returnsfalse forFFFF. Failed1821 assumed every dependency was a real eventID;1821b maps the source sentinel without changing it. '
        'Thirteen current native macro/catalog probes preserve the entire4MiB,input/output guards andABI;FI correctly expands toLil. '
        'Draft prose restores one percent per town,Istanbul,the fleet-staffing meaning,officers commanding sailors,hearsay,andCamilles praise;no added seasoned-sailor fact. '
        'Complete source facts are retained in one paragraph per record withspeaker/FI controls;two fixed allocations encode and11 reject capacity. Research size-independent formatting isnot an approved relocation ordisplay. '
        'No ROM,registry,patch,global profile orcompleted-entry count changes. Current V1807 stays experimental,V1492 promoted. '
        '1516 complete(1146 revised370 retained),1645 source/prose reviewed,116 reviewed-incomplete COMMON plus13 B24 route drafts andbroader shared/routes/player prose remain. '
        'Full editorial goal active;graphics/all18 plaques andlater older-record re-audit stay separate/open.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append({'id':'V1824-Lil-B24-source-prose13','proof':str(ROOT/'checkpoint_receipt.json'),
        'completed_entries_added':0,'source_prose_reviews_added':13,'full_goal_complete':False})
    for key in('current_integrated_candidate','unresolved_graphics_work','completed_editorial_record_counts_by_file','reviewed_but_incomplete_COMMON_IDs',
        'records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_with_source_and_prose_pass']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==1645
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    pending=LEDGER.with_name('editorial_review_current_v1824_pending.json');assert not pending.exists()and LEDGER.read_bytes()==raw
    save(pending,ledger);os.replace(pending,LEDGER)
    document=Path('docs/lil_B24_v1824_source_review.md');document.write_text('# V1824 Lil B24 source/prose review\n\n'+summary+
        '\n\nNext manuscript: '+str(NEW)+'\n\nNative source context: '+str(SOURCE)+'\n\nThis is a prose draft. Keep all native-format andactual-scene gates open.\n',encoding='utf-8')
    for name in('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as f:f.write('\n\n## V1824 Lil B24 source/prose13\n\n'+summary+'\n\nSee [source review](lil_B24_v1824_source_review.md).\n')
    handoff=HANDOFF.read_text();assert handoff.startswith('# Current editorial handoff - V1820')
    handoff=handoff.replace('# Current editorial handoff - V1820','# Current editorial handoff - V1824',1)
    handoff=handoff.replace('1632 source/prose reviewed. Completed per file:','1645 source/prose reviewed. Completed per file:',1)
    handoff=handoff.replace('No active reviewed-incomplete route drafts remain.','Thirteen B24 route speech drafts are source/prose reviewed butincomplete;12 proposed revisions1 retention.',1)
    anchor='## Latest completed family - V1820';assert handoff.count(anchor)==1
    section='## Latest source/prose review - V1824\n\n'+summary+'\n\n'+f'Manuscript: {NEW.as_posix()}. Source context: {SOURCE.as_posix()}. Event/state/dependency inventory: {INVENTORY.as_posix()}. Macro andfixed-slot proof: {MACROS.as_posix()}.\n\n'+'Next: map B24s17 command/reference contracts (61FF,A000,13 speeches,C200,terminal0) andthe remaining original event context prefix;verify new full native fonts,rows/pages andreal activation/return before registering any B24 bytes. Keep the B22 profile as an allocation probe until B24 binding isapproved. Do not shorten complete prose to the old slots orcount13 drafts complete. The source-controlled Lookout successful-shot test remains an alternative open task;do not repeat closed families.\n\n'
    handoff=handoff.replace(anchor,section+anchor,1)
    handoff=handoff.replace('Continue the earlier123 COMMON entries','Continue the earlier116 COMMON entries')
    handoff=handoff.replace('Vicinity/Armed Latina actual UI also remains pending.','Armed Latina actual name UI remains pending;vicinity614 was verified in V1794.')
    HANDOFF.write_text(handoff,encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',{'manuscript':str(NEW),'manuscript_sha256':sha(NEW.read_bytes()),
        'source_prose_before_after':[1632,1645],'completed_entries_unchanged':1516,'reviewed_incomplete_COMMON':116,
        'reviewed_incomplete_SC2_B24':13,'proposed_revisions':12,'retentions':1,
        'source_proofs':{str(p):sha(p.read_bytes())for p in(SOURCE,INVENTORY,MACROS)},
        'ledger_sha256':sha(LEDGER.read_bytes()),'handoff_sha256':sha(HANDOFF.read_bytes()),
        'no_ROM_registry_patch_profile_or_completed_credit_change':True,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'source_prose_reviewed':1645,'completed':1516,'B24_drafts':13,
        'research_size_independent_formats':sum(r['research_size_independent_format_encodes']for r in allocation),
        'registered_native_andactual_gates_still_open':True},flush=True)
