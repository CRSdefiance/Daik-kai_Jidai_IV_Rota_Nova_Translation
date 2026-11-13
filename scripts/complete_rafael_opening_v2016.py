"""Integrate117 reviewed opening records after all registered release checks.

The full all-routes/shared/random/player-prose goal remains active.
"""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_opening_completion_v2016')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v2013_candidate.nds')
DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v3.json')
CHOICES=Path('translations/rafael_opening_contextual_choices_editorial_draft_v2.json')
FINAL=Path('translations/rafael_opening_contextual_final_review_v1.json')
MAP=Path('translations/rafael_opening_editorial_relocation_map_v1.json')
RELEASE=Path('work/analysis/rafael_opening_release_v2012/registered_release_verification.json')
STARTUP=Path('work/analysis/rafael_opening_release_v2012/ordinary_startup_verification.json')
ACTUAL1=Path('work/analysis/rafael_independent_actual_v2007e/independent_preparation_and_normal_Lisbon_return.json')
ACTUAL0=Path('work/analysis/rafael_guided_actual_v2009/guided_preparation_repaired_outer_skip_and_Lisbon_return.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2013 Rafael Lisbon opening verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    ledger,doc,menu,mapping,release,startup,actual1,actual0=map(read,(LEDGER,DOC,CHOICES,MAP,RELEASE,STARTUP,ACTUAL1,ACTUAL0))
    digest=sha(ROM.read_bytes());assert digest==release['candidate_sha256']==startup['candidate_sha256']==mapping['research_ROM_sha256']
    assert digest=='29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55'
    assert release['complete_reconstruction_byte_exact']and release['all487_batches114_accepted_layers_and_prior_profiles_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact']and startup['no_battery_save_savestate_or_fixtures']
    assert actual0['both_actual_branches_union115_source_speeches']and actual0['union_complete_matching_panel_samples']==107
    assert actual0['union_complete_matching_panel_holds']==111 and actual0['normal_Lisbon_town_ID']==11
    assert len(read('work/analysis/rafael_opening_release_v2012/registration_provenance.json')['negative_cases'])==25
    manifest=read(ROM.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==487 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    image=NdsImage.open(ROM);block=IlnkContainer.parse(image.read_file('/data/SC0.DK4')).blocks[44]
    texts={r['id']:r for r in mapping['text_records']};records=[]
    for old in doc['records']:
        row=deepcopy(old);ref=texts[row['id']];start=ref['new_command_offset'];at=start+5
        end=block.index(b'\0',at+1);raw=block[at:end]
        assert block[start:start+6].hex()==row['source_complete_preamble_hex']
        index=block[:at].count(b'\0')+int(raw[:1]==b'\0');assert index==ref['new_record_index']
        row['before_integration_current_reference']=row['current_reference'];row['before_integration_current_text_hex']=row['current_text_hex']
        row['before_integration_record_index']=row['record_index']
        row['current_reference']=dict(header_offset=start,offset=at,bytes=len(raw),segment_index=index,
            terminator_offset=end,consume_leading_actor_byte_before_text_NUL=True)
        row['current_text_hex']=raw.hex();row['current_stored_English']=raw[1:].decode('cp932');row['record_index']=index
        row['current_ROM']=str(ROM);row['current_ROM_sha256']=digest
        row.pop('native_display_proof',None)
        row['native_display_evidence']=dict(approved_manuscript=str(DOC),approved_manuscript_sha256=sha(DOC.read_bytes()),
            source_bound_reference_map=str(MAP),source_bound_reference_map_sha256=sha(MAP.read_bytes()))
        row['integrated_editorial_status']='complete-source-context-prose-native-formatting-registered-release'
        records.append(row)
    old_choice=mapping['typed_target_choices'][0]
    for i,old in enumerate(menu['records']):
        row=deepcopy(old);label=old_choice['labels'][i];at=label['offset'];raw=bytes.fromhex(label['hex'])
        assert block[at:at+len(raw)]==raw and block[at+len(raw)]==0
        index=block[:at].count(b'\0')
        row['before_integration_current_reference']=row['current_reference'];row['before_integration_record_index']=row['record_index']
        row['current_reference']=dict(offset=at,bytes=len(raw),segment_index=index,choice_command_offset=old_choice['command_offset'],option_index=i)
        row['current_text_hex']=raw.hex();row['record_index']=index;row['current_ROM']=str(ROM);row['current_ROM_sha256']=digest
        row['integrated_editorial_status']='complete-source-context-prose-typed-native-choice-registered-release'
        records.append(row)
    assert len(records)==len({r['id']for r in records})==117
    assert sum(r['editorial_decision']=='revise'for r in records)==33 and sum(r['editorial_decision']=='retain-wording'for r in records)==84
    assert all(r.get('fresh_retained_wording_justification')for r in records if r['editorial_decision']=='retain-wording')
    assert all(all(r['review'].values())for r in records)
    assert ledger['records_editorially_completed']==1831 and ledger['records_revised_and_integrated']==1362 and ledger['retained_wordings_editorially_completed']==469
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2064
    f=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(545,428,117)
    assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==545
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC0.DK4']==[r['id']for r in records]
    assert not any(family.get('file_path')=='/data/SC0.DK4'for family in ledger['completed_editorial_families'])
    assert sum(len(family.get('records',[]))for family in ledger['completed_editorial_families'])==1831
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    evidence={str(p):sha(p.read_bytes())for p in(DOC,CHOICES,MAP,RELEASE,STARTUP,ACTUAL0,ACTUAL1,
        Path('work/analysis/rafael_opening_approval_v2010b/approval_receipt.json'),Path('dk4tool/dialogue/rafael_opening_profile.py'),
        Path('dk4tool/patch/rafael_opening_editorial.py'),Path('scripts/register_rafael_opening_v2012.py'),Path(__file__))}
    summary=("Fresh Rafael Lisbon opening117 integrated:all115 source speeches/system panels andboth choice labels reread asone complete exchange,33 revisions84individual justified retentions. "
        "Restore the father's why-question,personal trust behind Julio's loan,explicit captain/admiral/company-leader roles,Claudio's compliment defense andother voice/meaning details. "
        "All114progressive targets pass complete216x64 native/independent planes,916guarded logical/wrapped macro calls andfinal parity pixels;measured default FI isRafael6,FA Castor6,FO CastorCo.10. "
        "Speaker00 remainsowned bythe whole six-byte native preamble;FE money notice usesits separate228x48 mode1 consumer;two unchanged8/14-byte choice labels passfour native style planes andthree VM selection/cancel cases. "
        "All182commands,four relative sites,60current/normalized/target native cases,exactinverse restoration,343loads/686parentmodes perROM andunchanged executable-entry census pass. "
        "Two inherited tutorial skips areexplicitly repaired fromclean command correspondence:old0300 at6446 needs158rather than148;old0100 at6604 needs76rather than64 before final relocation. "
        "Both ordinary controller choices execute inactual coldboots withno save/savestate/location/RNG/funds/event/outcome fixtures,including actual repaired jumps andnormal Lisbon returns. "
        "Both paths activateall115speeches;107complete native/actual panel samples111holds areverified,with nofresh per-panel pixelclaim forthe other8early speeches. "
        "One source-bound R0327 weak-line-ending heuristic isexplicitly justified bythe complete four-row native/actual paragraph;no control,bounds,capacity orparity gate waived. "
        "RegisteredV2013 equals theentire tested researchROM.OnlySC0B44 grows60bytes;342otherblocks,everyotherfile/component,COMMON,SC2,ARM9,fonts,graphics and123040staged bytes remainexact. "
        "All487batches114acceptedlayers,25negative release gates,exactclean-input patch reconstruction andeight fresh ordinary startup/title controls pass;viewed. "
        "Ledger1948historical completions=1395revised553retained;2064source/prose reviewed=1518COMMON429SC2117SC0. Fresh545allintegrated/reconciled;0fresh routedrafts. "
        "1403historical completions stillneedfresh reconciliation;116COMMON incomplete,everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques andlater older-record technical re-audit remainopen. "
        "SC3B109's initial command-structure difference remainsunclassified. AllROMs andearlier translations preserved;V1492 promoted,canonicalbaseline unchanged,fullgoalactive.")
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family='Rafael-Lisbon-opening117',file_path='/data/SC0.DK4',blocks=[44],
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),candidate=str(ROM),candidate_sha256=digest,
        revised_count=33,retained_count=84,records=records,summary=summary,evidence=evidence,
        actual_scope=dict(both_ordinary_choices=True,activated_speeches=115,complete_native_actual_panels=107,complete_holds=111,
            other8_only_execution_and_offline_native_plane=True,no_fixtures_or_hardware_full_route_claim=True),full_goal_complete=False))
    family=dict(id='Rafael-Lisbon-opening117',file_path='/data/SC0.DK4',blocks=[44],record_IDs=[r['id']for r in records],
        final_review=str(FINAL),revised_count=33,retained_count=84,actual_verification_scope=summary,records=records)
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=1948;ledger['records_revised_and_integrated']=1395;ledger['retained_wordings_editorially_completed']=553
    ledger['completed_editorial_record_counts_by_file']['/data/SC0.DK4']=117
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC0.DK4']=[]
    ledger['active_source_prose_drafts']['manuscripts'] += [str(DOC),str(CHOICES)]
    ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-incomplete;0fresh-route-drafts;historical-manuscript-list-preserved'
    f['fresh_pass_records_integrated']=545;f['fresh_pass_records_pending_native_actual_release']=0;f['pending_contextual_families']=[]
    f['latest_completed_family']=family['id'];f['latest_final_review']=str(FINAL);f['latest_contextual_manuscript']=str(DOC);f['latest_contextual_choice_draft']=str(CHOICES)
    f['reconciled_families'].append(dict(id=family['id'],records=117,final_review=str(FINAL),new_revisions=33,justified_retentions=84,
        historical_reconciliation_only=False,new_completed_records=117,all_source_native_actual_and_registered_checks_complete=True))
    f['coverage_note']='All545 explicitly reread records integrated/reconciled:Stockholm51,London111,Speyer59,Hamburg81,trade/officer13,Lil opening49,sailing/crew64,Rafael opening117. Other1403historical completions stillneed explicit fresh reconciliation.'
    assert f['historical_completed_records_outside_reconciled_fresh_pass']==1948-545==1403
    ledger['integrated_candidate_reference_history'].append(deepcopy(ledger['current_integrated_candidate']))
    candidate=dict(path=str(ROM),sha256=digest,profile=manifest['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        SC0_sha256=release['SC0_sha256'],SC2_sha256=release['SC2_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=str(ROM.with_suffix('.manifest.json')),
        status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    ledger['current_integrated_candidate']=candidate
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,SC0_sha256=release['SC0_sha256'],
        Rafael_B44_117_source_native_and_both_actual_choices_complete=True,Rafael_B44_source_bound_map=str(MAP))
    ledger['latest_checkpoint']='V2016 '+summary
    ledger['rafael_opening_contextual_v2000']['superseded_by_integrated_checkpoint']='V2016'
    ledger['rafael_opening_v2016']=dict(final_review=str(FINAL),evidence=evidence,summary=summary,goal_turn_classification='progress',full_goal_complete=False)
    assert ledger['goal_status']=='active'and ledger['full_goal_complete']is False
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==1948
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2064
    assert sum(len(family.get('records',[]))for family in ledger['completed_editorial_families'])==1948
    GUIDE.mkdir(parents=True);guide=[]
    source_cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/rafael_opening_trace_v2003_RESEARCH_ONLY')
    for sheet in actual1['representative_contact_sheets']:
        dest=GUIDE/Path(sheet).name;copy2(sheet,dest);assert sha(dest.read_bytes())==sha(Path(sheet).read_bytes());guide.append(dict(path=str(dest),source=sheet,sha256=sha(dest.read_bytes())))
    for frame,label in((26160,'money_notice'),(44880,'preparation_choice'),(45330,'independent_encouragement'),(45690,'normal_Lisbon_return')):
        source=source_cap/f'frame_{frame:06d}_navigation.png';dest=GUIDE/f'{label}_{frame:06d}.png';copy2(source,dest)
        assert sha(dest.read_bytes())==sha(source.read_bytes());guide.append(dict(path=str(dest),source=str(source),sha256=sha(dest.read_bytes())))
    guided_cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/rafael_opening_guided_v2008_RESEARCH_ONLY')
    for frame,label in((45240,'guided_first_instruction'),(45630,'guided_town_advice'),(46020,'guided_Lisbon_return')):
        source=guided_cap/f'frame_{frame:06d}_navigation.png';dest=GUIDE/f'{label}_{frame:06d}.png';copy2(source,dest)
        assert sha(dest.read_bytes())==sha(source.read_bytes());guide.append(dict(path=str(dest),source=str(source),sha256=sha(dest.read_bytes())))
    save(ROOT/'guide_copies.json',dict(folder=str(GUIDE),files=guide,all_byte_exact=True))
    save(LEDGER,ledger)
    handoff=HANDOFF.read_text(encoding='utf-8');marker='## Rafael opening117 source/native checkpoint - V2000'
    prefix,history=handoff.split(marker,1)
    changes={
        '# Current editorial handoff - V2000':'# Current editorial handoff - V2016',
        '**1831 historical completions =1362revised +469retained;2064source/prose reviewed.**':'**1948 historical completions =1395revised +553retained;2064source/prose reviewed.**',
        'Fresh V1871pass:545 explicitly reread;428 integrated/reconciled and117 Rafael-opening entries pending.':'Fresh V1871pass:545 explicitly reread andintegrated/reconciled;0activefresh route drafts.',
        'opening49,sailing/crew64.':'opening49,sailing/crew64,Rafael opening117.',
        'Completed:1402COMMON +429SC2;':'Completed:1402COMMON +429SC2 +117SC0;',
        'all_routes_combined_v1986_candidate':'all_routes_combined_v2013_candidate',
        'all-routes-unified-v1986;485manifest':'all-routes-unified-v2013;487manifest',
        'f2dcb4cc4d688e1cd40a22367180841d27d06e540edbd16927f784b2cfcb50ca':digest,
        '3bb9efa435dd2a4e3e1b33ba109c55e7d83149edaf6a553b7b3f65a9eccd7998':release['patch_sha256'],
    }
    for old,new in changes.items():assert old in prefix,old;prefix=prefix.replace(old,new,1)
    section='## Rafael Lisbon opening117 integrated - V2016\n\n'+summary+'\n\n'
    section+='- Finalreview:'+str(FINAL)+';approvedmanuscript:'+str(DOC)+';choices:'+str(CHOICES)+';map:'+str(MAP)+'. All117 exactclean/current refs andindividual reasons recorded;actor00 preservedas nativepreamble,notordinary NULtext.\n'
    section+='- Privateprofile:dk4tool/dialogue/rafael_opening_profile.py;compiler:dk4tool/patch/rafael_opening_editorial.py;config:translations/rafael_opening_editorial_release_v1.json. FocusedRuff passes;25meaningful invalid-release cases rejectwithoutpartialwrites. Allotherprofiles/globalformatters unchanged.\n'
    section+='- Actualchoice1:'+str(ACTUAL1)+';177original commandpairs,113speeches executed,105matchingpanel samples107holds. Choice0:'+str(ACTUAL0)+';178pairs,114speeches executed,twonewpanels/fourholds. Union115activatedspeeches,107fullpixelpanels111holds;8earlyobjects execution/offlineproof only. Bothnormalreturns arecategory5,town11=Lisbon. No imported save,savestate,location/funds/event/RNG/outcome fixture.\n'
    section+='- Source/runtime repairs:0300old6446 stored148,butclean correspondence requires158 toold6608;0100old6604 stored64,butrequires76 toold6684. Finaltargets move to6490/span180 and6670/span68. Bothactual paths exercise those repairs. Failed2001 typed-boundary gate preserved;2001b derivesboth sitesfromclean182-command correspondence. Thisdoesnotclose thelater general older-record technical re-audit.\n'
    section+='- Audit2007/b/c/d predecessors preserved:inputjournal isexplicitlynotanexecutionreceipt;EV0pair iscategory5,town11,not[0,0]/[11,0]. Correct2007e binds terminalcapture/177returns andmeasured[5,11]. No ROM orinput waschanged tofix auditexpectations. Syntaxfailed2010 preserved;2010b approvedoutputs arecurrent.\n'
    section+='- Release:'+str(RELEASE)+';startup:'+str(STARTUP)+'. Wholecandidate exactlyactual-testedresearch;cleanpatch reconstructsexactly.All487batches/114acceptedlayers,342otherSC0blocks/allotherfiles/components exact. SC0SHA256:'+release['SC0_sha256']+'.\n'
    section+='- Guide:'+str(GUIDE)+';'+str(len(guide))+'byteexactcopies. Alljobs terminal:builder45797,independent28214,guided74462,newgame76780,title andpatch jobs. KeepallgeneratedROMs,includingresearchandreconstruction.\n'
    section+='- Nextreview:continuewholeexchanges ontheother routes andshared/town/random/playerprose;the1307-block raw/native census remainsa sourceinventory,noteditorialcredit. SC3B109 initialcommanddifference remainsunclassified. 116COMMON,1403historical records outsidefreshpass,separategraphics/all18plaques andlaterolder-record re-audit remainopen;fullgoalactive.\n\n'
    HANDOFF.write_text(prefix+section+marker+history,encoding='utf-8')
    for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
        with(Path('docs')/name).open('a',encoding='utf-8')as out:out.write('\n\n## V2016 Rafael Lisbon opening117 integrated\n\n'+summary+'\n')
    Path('docs/rafael_opening_v2016_completion.md').write_text('# Rafael Lisbon opening V2016\n\n'+summary+'\n\n'+section,encoding='utf-8')
    assert sha(ROM.read_bytes())==digest and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    save(ROOT/'completion_receipt.json',dict(summary=summary,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),proofs=evidence,
        source_prose2064_completed1948_revised1395_retained553=True,fresh545_integrated545_pending0=True,
        remaining_historical_reconciliations1403=True,guide=str(GUIDE),guide_files=len(guide),all_generated_ROMs_preserved=True,
        V1492_promoted_canonical_unchanged_full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(completed=1948,revised=1395,retained=553,source_prose=2064,fresh_integrated=545,pending=0,guide_files=len(guide),full_goal_complete=False))
