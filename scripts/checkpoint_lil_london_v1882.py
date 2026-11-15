"""Record111 fresh contextual reviews without native/actual/release credit."""
from copy import deepcopy
import os
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_London_checkpoint_v1882')
SOURCE=Path('work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json')
DOC=Path('translations/lil_london_editorial_manuscript_v2.json')
PROBE=Path('work/analysis/lil_London_body_probe_v1881d/body_only_prose_layout_research.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,source,probe=map(read,(DOC,SOURCE,PROBE))
    assert len(doc['records'])==len(source['records'])==len(probe['rows'])==111
    assert probe['manuscript_sha256']==sha(DOC.read_bytes())
    assert not any('error' in r for r in probe['rows'])
    assert all(all(r['review'][k] for k in ('source','context','localization','naturalness'))
        and r['review']['formatting'] is False for r in doc['records'])
    assert all(all(r['source_Japanese'].count(k)==r['english'].count('{MACRO:'+k+'}') for k in ('FI','FA','FO')) for r in doc['records'])
    assert (sum(r['editorial_decision']=='revise' for r in doc['records']),
        sum(r['editorial_decision']=='retain-wording' for r in doc['records']))==(81,30)
    raw=LEDGER.read_bytes()
    ledger=read(LEDGER)
    before=deepcopy(ledger)
    assert (ledger['records_editorially_completed'],ledger['records_with_source_and_prose_pass'])==(1580,1696)
    assert not any(ledger['reviewed_but_incomplete_route_record_IDs'].values())
    ids=[r['id'] for r in doc['records']]
    assert len(set(ids))==111
    ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(raw)
    (ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']+=111
    ledger['records_with_source_prose_drafts']+=111
    ledger['source_prose_reviewed_counts_by_file']['/data/SC2.DK4']+=111
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC2.DK4']=ids
    drafts=ledger['active_source_prose_drafts']
    drafts['manuscripts'].append(str(DOC))
    drafts['route_record_subsets_pending'][str(DOC)]=ids
    drafts.update(status='116-reviewed-COMMON-and111-London-fresh-source-prose-drafts-open',
        note='Stockholm51 integratedV1875. London111 source/context/prose reviewed,81 proposed revisions30 retentions;body-only layouts pass. Newscene controls/FE/nativefonts/relocation/representative actual/release pending.')
    ledger['coverage_units'].append(dict(id='Lil-London-Clifford111-source-prose',file_path='/data/SC2.DK4',blocks=[26],
        record_IDs=ids,status='source-context-prose-reviewed;native-controls-fonts-map-actual-release-pending',
        manuscript=str(DOC),source_context=str(SOURCE),proposed_revisions=81,proposed_retentions=30,
        completed_entries_added=0,source_prose_reviews_added=111,full_goal_complete=False))
    for unit in ledger['coverage_units']:
        if unit['id']=='all-route-scenes':
            unit.update(reviewed_route_records=289,completed_route_records=178,
                next='MapB26 original97/FE/Clifford1c presentation withrepresentative gameplay;preserve source-boundGerhard10 scope. Verify nativeparagraphs,typed branchmap andregistered cumulative release;fullall-routes/player prose stillopen.')
    pending_prefixes={p:[r['id'] for r in doc['records'] if r['source_presentation_prefix_hex']==p] for p in ('97','fe','1c','10')}
    ledger['formatting_watchlist']['Lil_London_Clifford111']=dict(status='source-prose-reviewed;full-native-display-pending',
        manuscript=str(DOC),source_context=str(SOURCE),body_only_probe=str(PROBE),
        pending_scene_presentation_prefixes_and_record_IDs=pending_prefixes,
        no_control_or_FE_display_approval_from_body_probe=True,
        whole_preambles_runtime_macros_complete_glyphs_bounds_pagination_andtransitions_required=True)
    ledger['next_route_scene_editorial_packet']=dict(file_path='/data/SC2.DK4',block=26,source_context=str(SOURCE),
        manuscripts=[str(DOC)],source_prose_review_complete=True,editorial_review_complete=False,
        actual_activation_pending=True,source_relocation_reference_map_pending=True,
        note='London26 original event/category5/town0 predicate accepted only inprior offline destination copy;no liveLondon visit orcurrenteligibility claim. B25 stillrequires128.')
    fresh=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert fresh['fresh_pass_records_explicitly_reread']==51
    assert not set(ids)&set(fresh['record_IDs'])
    fresh['record_IDs']+=ids
    fresh.update(fresh_pass_records_explicitly_reread=162,fresh_pass_records_integrated=51,
        fresh_pass_records_pending_native_actual_release=111,
        latest_contextual_manuscript=str(DOC),
        coverage_note='Stockholm51 reread andintegrated;London111 completeexchange reread andlocalized,display/release pending. Other prior reviews requireexplicit evidence reconciliation.')
    summary=('V1882 London111 clean-source/full-exchange reviews:81 proposed revisions30 justified retentions. '
        'Recognition,grotesque rumor,Clifford reveal,dinner/clothing backhanded compliment andwary alliance conversation reviewed asoneexchange. '
        'Restore Africa/India/Asia/NewWorld,the dye\'s map-deciphering role,hearsay,provisionaltrust andLil\'s actual betrayal warning. '
        '262 original commands111 completepreambles match clean/current;native actor/catalog/macros arecopied-state source evidence. '
        'Source97crew voice and3FE anonymousClifford objects remainpresentation-unverified;Clifford1c andGerhard10 needexactB26 scene approval. '
        'Initial extractor1879 rejected97 withoutoutput;1879b quarantines97/FE ratherthan inventing speakers. '
        'All111 body-only paragraph probes pass after3 faithful concision revisions;this isnotfullnativeglyph,FEconsumer orspeaker proof. '
        'No newROM orcompletioncredit:1580 historical completions(1196 revised384 retained),1807 source/prose reviewed. '
        'FreshV1871 contextual coverage162 reread,51 integrated,111 pending. RegisteredV1875/479batches/114accepted layers andexactpatch unchanged. '
        '116 incompleteCOMMON,otherstorylines/shared/random/player prose,separate graphics/all18plaques andlater older-recordtechnical re-audit remainopen. Fullgoalactive,V1492promoted.')
    ledger['latest_checkpoint']=summary
    ledger['research_checkpoints'].append(dict(id='V1882-London111-source-context-prose',proof=str(ROOT/'checkpoint_receipt.json'),
        completed_entries_added=0,source_prose_reviews_added=111,full_goal_complete=False))
    for key in ('records_editorially_completed','records_revised_and_integrated','retained_wordings_editorially_completed',
                'completed_editorial_record_counts_by_file','current_integrated_candidate','unresolved_graphics_work',
                'reviewed_but_incomplete_COMMON_IDs','older_record_reaudit_after_full_editorial_goal'):
        assert ledger[key]==before[key],key
    assert ledger['records_with_source_and_prose_pass']==sum(ledger['source_prose_reviewed_counts_by_file'].values())==1807
    assert fresh['fresh_pass_records_explicitly_reread']==len(set(fresh['record_IDs']))==162
    pending=LEDGER.with_name('editorial_review_current_v1882_pending.json')
    assert not pending.exists() and LEDGER.read_bytes()==raw
    save(pending,ledger)
    os.replace(pending,LEDGER)
    Path('docs/lil_london_v1882_source_review.md').write_text('# V1882 London full-exchange source review\n\n'+summary+
        f'\n\nManuscript: {DOC.as_posix()}\n\nSource: {SOURCE.as_posix()}\n\nBody-only probe: {PROBE.as_posix()}\n',encoding='utf-8')
    for name in ('translation_progress.md','known_issues.md','todo.md','editorial_review_goal.md'):
        with (Path('docs')/name).open('a',encoding='utf-8') as f:
            f.write('\n\n## V1882 London111 source/context/prose\n\n'+summary+'\n\nSee [review](lil_london_v1882_source_review.md).\n')
    text=HANDOFF.read_text(encoding='utf-8')
    text=text.replace('# Current editorial handoff - V1878','# Current editorial handoff - V1882',1)
    text=text.replace('1696 source/prose reviewed.**','1807 source/prose reviewed.**',1)
    text=text.replace('Fresh V1871 contextual pass explicitly reread/reconciled: Stockholm51.',
        'Fresh V1871 contextual pass explicitly reread:162(Stockholm51 integrated+London111 pending).')
    text=text.replace('reviewed1518COMMON+178SC2. Noactive reviewed-incomplete route drafts;',
        'reviewed1518COMMON+289SC2. London111 reviewed-incomplete route drafts;')
    start=text.index('### Exact next work')
    end=text.index('## Latest completed scene: Lil trade routes and officers, SC2 B24')
    next_work=f'''## Current working unit: London B26 - V1882

{summary}

- Source packet: {SOURCE.as_posix()};111speeches,262nestedcommands. CurrentV1875 B26/runtime/EV2 exactV1841;source cleanJapanese unchanged.
- Manuscript: {DOC.as_posix()};81revisions30retentions;allsource/context/localization/naturalness gates true,formatting false. Preservev1 andallproducers.
- Three paragraphs refined inv2 afterfive-row body-only overflow:R0087 grotesquerumor,R0461Valdes,R0566destinations. Every sourcefact retained. Current bodyprobe111/111 encodes;not native/fullcontrol approval.
- Pending presentation:97 crew1object,FE anonymousClifford3objects,1cClifford34objects,10Gerhard5objects. ExactIDlists inledgerwatchlist. FE mustkeep itsseparate nativeconsumer;do notapplyprogressive formattingblindly.
- SourceFE stranger isidentified byhisownmonster reply andLil's immediate recognition;thisprose context doesnotestablish portrait/name/layout mapping.97speaker remainsunidentifiedcrew,explicit sourceadmiraladdress retained.
- No London gameplay started. AllStockholm/release/startupjobs terminal. No completedchecks needrepetition.

### Exact next work

1. Establish source-bound B26 presentation/control contracts andrepresentative original gameplay for97/FE anonymousreveal/Clifford1c,plusnewscene transitions. RetainGerhard10 private runtime/source scope;globalprofiles stayunchanged. No needindividually visit111speeches orallconditional crewbranches.
2. Run fullnative/macros/font/layout checks forall111 withcomplete leading/trailing glyphs,bounds,pagination,andnegative controls. Body-only probe doesnotgivefullformatcredit. Review source-prose notes wheretechnical evidence changescontext.
3. Approve complete nestedbranch/reference map fromoriginal262commands,rebuild guardedproductioncompiler fromprose/typedspans,register afterentireV1875 stack,andverify researchidentity/exactcleanpatch/startup beforecompletioncredit.
4. Continuefullfreshcontextual pass throughpreviouslytranslated storylines,sharedtown/shop/randomscenes andremainingplayerprose. Prior1529completedrecords requireevidence reconciliation.116COMMONpendingremain;graphics/all18plaques andlaterolder-recordtechnical re-audit separate/open.

Do notrepeatcompletedStockholmchecks absentconcreterisk. PreserveeveryROM andearliertranslation;V1492promoted,canonicalbaselineunchanged.

'''
    HANDOFF.write_text(text[:start]+next_work+text[end:],encoding='utf-8')
    save(ROOT/'checkpoint_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),body_probe=str(PROBE),
        records_reviewed_added=111,proposed_revisions=81,justified_retentions=30,
        historical_completed_unchanged=1580,source_prose_reviewed_after=1807,
        fresh_contextual_reread=162,fresh_contextual_integrated=51,
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        no_new_ROM_no_native_oractual_orcompletion_claim=True,full_goal_remains_active=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose_reviewed=1807,historical_complete=1580,fresh_contextual_reread=162,
        integrated=51,London_pending=111,full_goal_remains_active=True))
