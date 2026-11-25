"""Reconcile the73-entry family after cumulative release,patch and startup gates."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_completion_v2033')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v2030_candidate.nds')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v2.json')
MAP=Path('translations/hodram_opening_editorial_relocation_map_v1.json')
FINAL=Path('translations/hodram_opening_contextual_final_review_v1.json')
RELEASE_ROOT=Path('work/analysis/hodram_opening_release_v2029b')
RELEASE=RELEASE_ROOT/'registered_release_verification.json'
STARTUP=RELEASE_ROOT/'ordinary_startup_verification.json'
ACTUAL=Path('work/analysis/hodram_opening_actual_v2027d/ordinary_current_revised_opening_and_full_actual_planes.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2030 Hodram opening verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    ledger,doc,mapping,release,startup,actual=map(read,(LEDGER,DOC,MAP,RELEASE,STARTUP,ACTUAL))
    digest=sha(ROM.read_bytes());assert digest==release['candidate_sha256']==startup['candidate_sha256']==mapping['research_ROM_sha256']
    assert digest=='4ed991686628ef679ee1d0fc6a00ad98bccafc99c0b83cba9371fa335eb53532'
    assert release['complete_reconstruction_byte_exact']and release['all488_batches114_accepted_layers_and_prior_profiles_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact']and startup['no_battery_save_savestate_or_fixtures']
    assert actual['complete_matching_speech_panels']==actual['complete_matching_speech_holds']==37
    assert actual['all37_opening_speeches93_commands_and_town_return']and actual['source_bound_B43_B44_offline_only_not_actual_visits']
    assert len(read(RELEASE_ROOT/'registration_provenance.json')['negative_cases'])==27
    manifest=read(ROM.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==488 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    blocks=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC1.DK4')).blocks
    texts={r['id']:r for b in mapping['blocks']for r in b['text_records']};records=[]
    for old in doc['records']:
        row=deepcopy(old);ref=texts[row['id']];block=blocks[row['block']];start=ref['new_command_offset'];at=start+5
        end=block.index(b'\0',at+1);raw=block[at:end];index=block[:at].count(b'\0')
        assert block[start:start+6].hex()==row['source_complete_preamble_hex']and index==ref['new_record_index']
        assert block[start:start+len(bytes.fromhex(ref['target_hex']))].hex()==ref['target_hex']
        row['before_integration_current_reference']=row['current_reference'];row['before_integration_current_text_hex']=row['current_text_hex']
        row['before_integration_record_index']=row['record_index']
        row['current_reference']=dict(header_offset=start,offset=at,bytes=len(raw),segment_index=index,terminator_offset=end,
            consume_leading_actor_byte_before_text_NUL=True,complete_preamble_hex=row['source_complete_preamble_hex'])
        row['current_text_hex']=raw.hex();row['current_stored_English']=raw[1:].decode('cp932');row['record_index']=index
        row['current_ROM']=str(ROM);row['current_ROM_sha256']=digest;row.pop('native_display_proof',None)
        row['native_display_evidence']=dict(approved_manuscript=str(DOC),approved_manuscript_sha256=sha(DOC.read_bytes()),
            source_bound_reference_map=str(MAP),source_bound_reference_map_sha256=sha(MAP.read_bytes()))
        row['integrated_editorial_status']='complete-source-context-prose-native-formatting-registered-release'
        records.append(row)
    assert len(records)==len({(r['file_path'],r['id'])for r in records})==73
    assert sum(r['editorial_decision']=='revise'for r in records)==38 and sum(r['editorial_decision']=='retain-wording'for r in records)==35
    assert all(r.get('fresh_retained_wording_justification')for r in records if r['editorial_decision']=='retain-wording')
    assert all(all(r['review'].values())for r in records)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(1948,1395,553)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2137
    f=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(618,545,73)
    assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==618
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC1.DK4']==[r['id']for r in records]
    assert not any(family.get('file_path')=='/data/SC1.DK4'for family in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    evidence={str(p):sha(p.read_bytes())for p in(DOC,MAP,RELEASE,STARTUP,ACTUAL,
        Path('work/analysis/hodram_opening_approval_v2028/approval_receipt.json'),Path('dk4tool/dialogue/hodram_opening_profile.py'),
        Path('dk4tool/patch/hodram_opening_editorial_v2.py'),Path('scripts/register_hodram_opening_v2029b.py'),Path(__file__))}
    summary=("Hodram opening/trade/Lil encounter73 integrated from complete clean Japanese exchanges:38 revisions35 individually justified retentions. "
        "Restored territorial warning,polite crew-address request,pirate-like patrol fleet,Vestaros,religious-policy budget context,first battle-thrill recollection,reported state rewards,unexpected quarry without invented escape,world-leading trade-network ambition,wartime rival-contract condition,andLil/Camille/Gerhard emotional progression. "
        "All67 progressive216x64 planes andsix separate FE228x48 native planes pass,with588 guarded native macro calls andfinal parity pixels. Default native names areHodram6/Bergstrom9/Bergstrom Fleet15;fullsix-byte controls remainexact. "
        "All171 commands,24relative sites,360clean/current/research native cases,exactinverse restoration,325loads650parent modes perROM andunchanged executable-entry census pass. "
        "Ordinary revised coldboot executes all93B42 commands and37speeches,each withone complete matching native/actual panel,andreturns normally toStockholm. Portraits/fullnameplates andall37panels viewed. "
        "B43/B44 receive full source/prose/native/reference checks;noactual scene visit isclaimed. Lil02/Camille09 live control evidence isreused onlyafter exactruntime binding. "
        "Original current no-fixture run also observes B135portdeparture andB127sailing tutorial,then closes normally atsea;these areunreviewed context withnoeditorial completion credit. "
        "OneB43R0068 weak-line-ending preference isexplicitly justified bythe complete native paragraph;nohard gate waived. Privateprofiles only;globalformatters unchanged. "
        "RegisteredV2030 equals thewhole actual-tested researchROM;onlySC1B42/B43/B44 change,all322otherblocks,everyotherfile/component,COMMON,SC0,SC2,ARM9,fonts,graphics and123040staged bytes exact. "
        "All488batches114acceptedlayers,27negative release gates,exactclean-input patch reconstruction andeight fresh ordinary startup/title controls pass;viewed. "
        "Coverage:2021historical completions=1433revised588retained;2137source/prose reviewed;fresh618reread andintegrated/reconciled,0freshroute drafts. Other1403historical completions stillneedfresh reconciliation;116COMMON incomplete. "
        "Every remaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques andlater older-record technical re-audit remainopen. SC3B109 initialcommanddifference remainsunclassified. "
        "AllgeneratedROMs andearlier translations preserved;V1492 promoted,canonicalbaseline unchanged,fullgoalactive.")
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family='Hodram-opening-trade-Lil73',file_path='/data/SC1.DK4',blocks=[42,43,44],
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),candidate=str(ROM),candidate_sha256=digest,
        revised_count=38,retained_count=35,records=records,summary=summary,evidence=evidence,
        actual_scope=dict(ordinary_opening_commands=93,activated_speeches=37,complete_native_actual_panels=37,complete_holds=37,
            B43_B44_offline_complete_no_actual_visit=True,broader_B135_B127_observed_unreviewed=True,no_fixtures_or_hardware_full_route_claim=True),full_goal_complete=False))
    family=dict(id='Hodram-opening-trade-Lil73',file_path='/data/SC1.DK4',blocks=[42,43,44],record_IDs=[r['id']for r in records],
        final_review=str(FINAL),revised_count=38,retained_count=35,actual_verification_scope=summary,records=records)
    ledger['completed_editorial_families'].append(family)
    ledger['records_editorially_completed']=2021;ledger['records_revised_and_integrated']=1433;ledger['retained_wordings_editorially_completed']=588
    ledger['completed_editorial_record_counts_by_file']['/data/SC1.DK4']=73
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC1.DK4']=[]
    ledger['active_source_prose_drafts']['manuscripts'].append(str(DOC))
    ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-incomplete;0fresh-route-drafts;historical-manuscript-list-preserved'
    ledger['active_source_prose_drafts']['note']='Fresh618 integrated/reconciled throughV2033;116COMMON reviewed incomplete. Continue allremaining routes/shared town/random/playerprose and1403historical reconciliations.'
    ledger['active_source_prose_drafts']['route_record_subsets_pending'][str(Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json'))]=[]
    f['fresh_pass_records_integrated']=618;f['fresh_pass_records_pending_native_actual_release']=0;f['pending_contextual_families']=[]
    f['latest_completed_family']=family['id'];f['latest_final_review']=str(FINAL);f['latest_contextual_manuscript']=str(DOC)
    f['reconciled_families'].append(dict(id=family['id'],records=73,final_review=str(FINAL),new_revisions=38,justified_retentions=35,
        historical_reconciliation_only=False,new_completed_records=73,all_source_native_representative_actual_and_registered_checks_complete=True))
    f['coverage_note']='All618 file-qualified explicitly reread records integrated/reconciled,includingnewHodram73. Other1403historical completions stillneed explicitfresh reconciliation. BareIDs overlap acrossroutes;record_keys remainauthoritative.'
    assert f['historical_completed_records_outside_reconciled_fresh_pass']==2021-618==1403
    ledger['integrated_candidate_reference_history'].append(deepcopy(ledger['current_integrated_candidate']))
    candidate=dict(path=str(ROM),sha256=digest,profile=manifest['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        SC0_sha256=release['SC0_sha256'],SC1_sha256=release['SC1_sha256'],SC2_sha256=release['SC2_sha256'],patch=release['patch'],patch_sha256=release['patch_sha256'],
        manifest=str(ROM.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    ledger['current_integrated_candidate']=candidate
    ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,SC1_sha256=release['SC1_sha256'],
        Hodram_B42_B43_B44_73_source_native_and_representative_actual_complete=True,Hodram_opening_source_bound_map=str(MAP))
    ledger['latest_checkpoint']='V2033 '+summary
    ledger['hodram_opening_contextual_v2020']['superseded_by_integrated_checkpoint']='V2033'
    ledger['hodram_opening_v2033']=dict(final_review=str(FINAL),evidence=evidence,summary=summary,goal_turn_classification='progress',full_goal_complete=False)
    assert ledger['goal_status']=='active'and ledger['full_goal_complete']is False
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==2021
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2137
    assert sum(len(family.get('records',[]))for family in ledger['completed_editorial_families'])==2021
    GUIDE.mkdir(parents=True);guide=[]
    copies=[(Path(p),Path(p).name)for p in actual['representative_contact_sheets']]
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hodram_opening_revised_v2025_RESEARCH')
    copies +=[(cap/f'frame_{frame:06d}_navigation.png',label+'.png')for frame,label in((4000,'Hodram'),(4600,'Charles'),(6860,'Gerhard'),(7940,'Manuel'))]
    for source,name in copies:
        dest=GUIDE/name;copy2(source,dest);assert sha(dest.read_bytes())==sha(source.read_bytes());guide.append(dict(path=str(dest),source=str(source),sha256=sha(dest.read_bytes())))
    save(ROOT/'guide_copies.json',dict(folder=str(GUIDE),files=guide,all_byte_exact=True));save(LEDGER,ledger)
    handoff=HANDOFF.read_text(encoding='utf-8');marker='## Hodram73 source/prose review - V2020';prefix,history=handoff.split(marker,1)
    changes={
        '# Current editorial handoff - V2020':'# Current editorial handoff - V2033',
        '**1948 historical completions =1395revised +553retained;2137source/prose reviewed.**':'**2021 historical completions =1433revised +588retained;2137source/prose reviewed.**',
        'Fresh V1871pass:618 explicitly reread;545 integrated/reconciled and73 Hodram drafts pending.':'Fresh V1871pass:618 explicitly reread andintegrated/reconciled;0activefresh route drafts.',
        'sailing/crew64,Rafael opening117.':'sailing/crew64,Rafael opening117,Hodram opening/trade/Lil73.',
        'Completed:1402COMMON +429SC2 +117SC0;':'Completed:1402COMMON +429SC2 +117SC0 +73SC1;',
        'all_routes_combined_v2013_candidate':'all_routes_combined_v2030_candidate',
        'all-routes-unified-v2013;487manifest':'all-routes-unified-v2030;488manifest',
        '29d9de4bdd46231b865cbe39a0592dd65a0c55378dfdbb7d8c10aa6104ca7d55':digest,
        '26fdb688b8d7a7063190e5054a68f821d07c6ea933ec59182d1fe98fb4f5b1fb':release['patch_sha256'],
    }
    for old,new in changes.items():
        assert old in prefix,old
        prefix=prefix.replace(old,new)if old=='all_routes_combined_v2013_candidate'else prefix.replace(old,new,1)
    section='## Hodram opening/trade/Lil73 integrated - V2033\n\n'+summary+'\n\n'
    section+='- Final review: '+str(FINAL)+'; approved manuscript: '+str(DOC)+'; map: '+str(MAP)+'. All73 exact clean/current file-qualified references,full source glosses,andindividual revision/retention reasons recorded.\n'
    section+='- Private profile:dk4tool/dialogue/hodram_opening_profile.py;compiler:dk4tool/patch/hodram_opening_editorial_v2.py;config:translations/hodram_opening_editorial_release_v2.json. FocusedRuff and27negative gates pass. Allother profiles andglobalformatters exact. FailedV1 compiler classified informative automatic line-break counts asblocking;explicitV2 filters byseverity,retainingallerrors andunwaivedwarnings. No prose orhardnativegate changed.\n'
    section+='- Actual: '+str(ACTUAL)+'. Current30140frames finishes B42,B135departure andB127sailing tutorial;revised20420frames executes all93B42 commands,37speech panels with37full-native-matching captures,andnormal Stockholm return. Alljobs terminal;priorhandles99041/62480 closed. B43/B44 remain offline-only scene coverage,withnoactual visitclaim.\n'
    section+='- Native:67progressive planes/540calls,six separateFE planes/48calls;all73final parity planes,171commands/24relative sites/360native cases,325loads650parent modes perROM andunchanged executableunits. Exactinverse restoresallthree currentblocks.\n'
    section+='- Release: '+str(RELEASE)+';startup: '+str(STARTUP)+'. 488batches114acceptedlayers;wholeROM exactresearch,onlySC1B42/B43/B44 change;SC1SHA256 '+release['SC1_sha256']+'. Exactclean-input patch '+release['patch']+' SHA256 '+release['patch_sha256']+'.\n'
    section+='- Audit predecessors2027/b/c preserved afterwrongreceipt-key assumptions;2027d readsactualpreview/native_font_plane_sha256 andpasses37/37. Initialbuild2030 omittedrequired--out andcreatednoROM;2030b successfulregistered buildretainsitslog. Registration2029 failedbeforebuilder/registrymutation;2029b usessuccessorcompiler andpreservesoriginalconfig. AllgeneratedROMs preserved,includingresearchandreconstruction. Guide: '+str(GUIDE)+';'+str(len(guide))+'byteexactcopies.\n'
    section+='- Next:continuecomplete exchanges onallremaining routes/shared shop/town/random/playerprose;fresh618complete isnotfullcorpuscoverage. 116COMMON,1403historical recordsoutsidefreshpass,SC3B109 initialcommandclassification,separategraphics/all18plaques andlaterolder-record technical re-audit remainopen. ReusecompletedHodram/Rafael/Stockholm gates;do notrepeat equivalent tests.\n\n'
    HANDOFF.write_text(prefix+section+marker+history,encoding='utf-8',newline='\n')
    for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
        with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2033 Hodram opening/trade/Lil73 integrated\n\n'+summary+'\n')
    Path('docs/hodram_opening_v2033_completion.md').write_text('# Hodram opening V2033\n\n'+summary+'\n\n'+section,encoding='utf-8',newline='\n')
    assert sha(ROM.read_bytes())==digest and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    save(ROOT/'completion_receipt.json',dict(summary=summary,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),
        ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),proofs=evidence,
        source_prose2137_completed2021_revised1433_retained588=True,fresh618_integrated618_pending0=True,
        remaining_historical_reconciliations1403=True,guide=str(GUIDE),guide_files=len(guide),all_generated_ROMs_preserved=True,
        V1492_promoted_canonical_unchanged_full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(completed=2021,revised=1433,retained=588,source_prose=2137,fresh_integrated=618,pending=0,guide_files=len(guide),full_goal_complete=False))
