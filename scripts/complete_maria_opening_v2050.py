"""Integrate the38-entry family only after registered release,patch and startup."""
from copy import deepcopy
from pathlib import Path
from shutil import copy2
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_completion_v2050')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
ROM=Path('out/all_routes_combined_v2047_candidate.nds')
DOC=Path('translations/maria_opening_contextual_editorial_manuscript_v2.json')
MAP=Path('translations/maria_opening_editorial_relocation_map_v1.json')
FINAL=Path('translations/maria_opening_contextual_final_review_v1.json')
RELEASE_ROOT=Path('work/analysis/maria_opening_release_v2046')
RELEASE=RELEASE_ROOT/'registered_release_verification.json'
STARTUP=RELEASE_ROOT/'ordinary_startup_verification.json'
ACTUAL=Path('work/analysis/maria_opening_actual_v2044/ordinary_current_revised_opening_and_full_actual_planes.json')
GUIDE=Path('E:/Rota Nova translations/Guide screenshots/V2047 Maria Hangzhou opening verified')

if __name__=='__main__':
    assert not ROOT.exists()and not FINAL.exists()and not GUIDE.exists()
    ledger,doc,mapping,release,startup,actual=map(read,(LEDGER,DOC,MAP,RELEASE,STARTUP,ACTUAL))
    digest=sha(ROM.read_bytes());assert digest==release['candidate_sha256']==startup['candidate_sha256']==mapping['research_ROM_sha256']
    assert digest=='096945ba367a10edbe3e116e49072734a7b6373fdda2b07083c828f72292e227'
    assert release['complete_reconstruction_byte_exact']and release['all489_batches114_accepted_layers_and_prior_profiles_preserved']
    assert startup['all8_complete_startup_title_NewGame_frames_exact']and startup['no_battery_save_savestate_or_fixtures']
    assert actual['complete_matching_speech_panels']==actual['complete_matching_speech_holds']==38
    assert actual['all38_speeches85_commands_and_normal_Hangzhou_return']
    assert actual['existing_isolated_system_unlock_save_not_earned_and_no_savestate_story_location_RNG_funds_outcome_fixture']
    assert len(read(RELEASE_ROOT/'registration_provenance.json')['negative_cases'])==27
    manifest=read(ROM.with_suffix('.manifest.json'));registry=read('translations/release_stack.json')
    assert len(manifest['batches'])==489 and len(registry['accepted_layers'])==114
    assert registry['latest_promoted_build']['profile']=='all-routes-unified-v1492'and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    block=IlnkContainer.parse(NdsImage.open(ROM).read_file('/data/SC3.DK4')).blocks[33]
    assert block[:4]==b'CS\1\1';texts={r['id']:r for r in mapping['blocks'][0]['text_records']};records=[]
    for old in doc['records']:
        row=deepcopy(old);ref=texts[row['id']];start=ref['new_command_offset'];at=start+5;end=block.index(b'\0',at+1);raw=block[at:end];index=block[:at].count(b'\0')
        assert block[start:start+6].hex()==row['source_complete_preamble_hex']and index==ref['new_record_index']
        assert block[start:start+len(bytes.fromhex(ref['target_hex']))].hex()==ref['target_hex']
        row['before_integration_current_reference']=row['current_reference'];row['before_integration_current_text_hex']=row['current_text_hex'];row['before_integration_record_index']=row['record_index']
        row['current_reference']=dict(header_offset=start,offset=at,bytes=len(raw),segment_index=index,terminator_offset=end,
            consume_leading_actor_byte_before_text_NUL=True,complete_preamble_hex=row['source_complete_preamble_hex'])
        row['current_text_hex']=raw.hex();row['current_stored_English']=raw[1:].decode('cp932');row['record_index']=index;row['current_ROM']=str(ROM);row['current_ROM_sha256']=digest
        row.pop('native_display_proof',None);row['native_display_evidence']=dict(approved_manuscript=str(DOC),approved_manuscript_sha256=sha(DOC.read_bytes()),reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()))
        row['integrated_editorial_status']='complete-source-context-prose-native-formatting-registered-release';records.append(row)
    assert len(records)==len({(r['file_path'],r['id'])for r in records})==38
    assert sum(r['editorial_decision']=='revise'for r in records)==23 and sum(r['editorial_decision']=='retain-wording'for r in records)==15
    assert all(r.get('fresh_retained_wording_justification')for r in records if r['editorial_decision']=='retain-wording')and all(all(r['review'].values())for r in records)
    assert(ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(2021,1433,588)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2175
    f=ledger['contextual_story_natural_dialogue_pass_v1871'];assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(656,618,38)
    assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==656
    assert ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC3.DK4']==[r['id']for r in records]
    assert not any(family.get('file_path')=='/data/SC3.DK4'for family in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    evidence={str(p):sha(p.read_bytes())for p in(DOC,MAP,RELEASE,STARTUP,ACTUAL,Path('work/analysis/maria_opening_approval_v2045/approval_receipt.json'),
        Path('dk4tool/dialogue/maria_opening_profile.py'),Path('dk4tool/patch/maria_opening_editorial.py'),Path('scripts/register_maria_opening_v2046.py'),Path(__file__))}
    summary=("Maria's complete Hangzhou opening38 is integrated:23 revisions and15 individually justified retentions. The clean-source review restores the wako ships' boarding tactics,the narrow bay,Jam's conversational voice andcrime-blame account,Yukihisa's stowaway journey/sword search/compatriot duty,France,Ian byname,three-percent payments andforeign-vessel disguise,tax revenue,andthorough maintenance beforeKurushima retaliation. "
        "All38 native216x64 planes,308 guarded macro calls,andfinal parity planes pass withzero errors,warnings orwaivers. Exact default substitutions areMaria5/Li2/LiClan7. Xien0A isexplicitly scoped asanactor byte inits six-byte preamble;global profiles stay unchanged. "
        "All85 commands,the nativeCS0101 header and47 non-speech commands arepreserved;there areno relative sites orchoices. Exactinverse restoration,303loads606parent modes perROM andunchanged executable-entry census pass. "
        "Current38500-frame andrevised31000-frame coldboots execute all85 opening commands and38speeches. Every revised speech hasone complete matching native/actual panel;all38 panels,six portraits/fullnameplates andnormal Hangzhou return wereviewed. These runs use theexisting isolated system-unlock save,notanearned unlock,andno savestate/story/location/RNG/funds/outcome fixture. "
        "Current follow-on coverage samples theport,resupply/ratio prompts,palace/trader/tavern menus,andMiwa's drink interaction through theTen coins bill. Those areunreviewed context samples,no neweditorial credit orcomplete random-event coverage. "
        "RegisteredV2047 equals thewhole tested researchROM. OnlySC3B33 grows72bytes;all302otherblocks,everyotherfile/component,COMMON,SC0,SC1,SC2,ARM9,fonts,graphics and123040staged bytes remainexact. All489batches114acceptedlayers,27negative release gates,exactclean-input patch reconstruction andeight ordinary startup/title controls pass;viewed. "
        "Coverage is2059 historical completions=1456revised603retained;2175source/prose reviewed. All656 fresh entries areintegrated/reconciled. Other1403historical completions stillneedfresh reconciliation;116COMMON remainincomplete. Everyremaining storyline/shared shop/town/random/playerprose,separategraphics/all18plaques,SC3B109 classification andthelater older-record technical re-audit remainopen. AllROMs andearlier translations arepreserved;V1492 remainspromoted andthecanonicalbaseline staysunchanged. Fullgoal active.")
    save(FINAL,dict(format='dk4-editorial-family-final-review-v1',family='Maria-Hangzhou-opening38',file_path='/data/SC3.DK4',blocks=[33],
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),candidate=str(ROM),candidate_sha256=digest,
        revised_count=23,retained_count=15,records=records,summary=summary,evidence=evidence,
        actual_scope=dict(opening_commands=85,activated_speeches=38,complete_native_actual_panels=38,complete_holds=38,
            existing_system_unlock_not_earned=True,no_savestate_or_story_location_RNG_funds_outcome_fixture=True,
            following_town_and_drink_context_unreviewed=True,not_complete_random_event_or_full_route_hardware_proof=True),full_goal_complete=False))
    family=dict(id='Maria-Hangzhou-opening38',file_path='/data/SC3.DK4',blocks=[33],record_IDs=[r['id']for r in records],final_review=str(FINAL),revised_count=23,retained_count=15,actual_verification_scope=summary,records=records)
    ledger['completed_editorial_families'].append(family);ledger['records_editorially_completed']=2059;ledger['records_revised_and_integrated']=1456;ledger['retained_wordings_editorially_completed']=603
    ledger['completed_editorial_record_counts_by_file']['/data/SC3.DK4']=38;ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC3.DK4']=[]
    ledger['active_source_prose_drafts']['manuscripts'].append(str(DOC));ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-incomplete;0fresh-route-drafts;historical-manuscript-list-preserved'
    ledger['active_source_prose_drafts']['note']='Fresh656 integrated/reconciled throughV2050. Continue116incomplete COMMON,1403historical reconciliations,andallremaining routes/shared town/random/playerprose.'
    ledger['active_source_prose_drafts']['route_record_subsets_pending'][str(Path('translations/maria_opening_contextual_editorial_manuscript_v1.json'))]=[]
    f.update(fresh_pass_records_integrated=656,fresh_pass_records_pending_native_actual_release=0,pending_contextual_families=[],latest_completed_family=family['id'],latest_final_review=str(FINAL),latest_contextual_manuscript=str(DOC))
    f['reconciled_families'].append(dict(id=family['id'],records=38,final_review=str(FINAL),new_revisions=23,justified_retentions=15,historical_reconciliation_only=False,new_completed_records=38,all_source_native_actual_and_registered_checks_complete=True))
    f['coverage_note']='All656 file-qualified explicitly reread records integrated/reconciled,includingMaria38. Other1403historical completions requireexplicit freshreconciliation. Usefile_path plusID;bareIDs overlap acrossroutes.'
    assert f['historical_completed_records_outside_reconciled_fresh_pass']==2059-656==1403
    ledger['integrated_candidate_reference_history'].append(deepcopy(ledger['current_integrated_candidate']))
    candidate=dict(path=str(ROM),sha256=digest,profile=manifest['profile'],MESFILE_sha256=release['COMMON_sha256'],ARM9_sha256=release['ARM9_sha256'],
        SC0_sha256=release['SC0_sha256'],SC1_sha256=release['SC1_sha256'],SC2_sha256=release['SC2_sha256'],SC3_sha256=release['SC3_sha256'],
        patch=release['patch'],patch_sha256=release['patch_sha256'],manifest=str(ROM.with_suffix('.manifest.json')),status='experimental-verified-editorial-checkpoint-not-promoted',details=summary,full_goal_complete=False)
    ledger['current_integrated_candidate']=candidate;ledger['current_native_relocation_reference'].update(candidate=str(ROM),candidate_sha256=digest,SC3_sha256=release['SC3_sha256'],Maria_B33_38_source_native_and_representative_actual_complete=True,Maria_opening_source_bound_map=str(MAP))
    ledger['latest_checkpoint']='V2050 '+summary;ledger['maria_opening_contextual_v2038']['superseded_by_integrated_checkpoint']='V2050'
    ledger['maria_opening_v2050']=dict(final_review=str(FINAL),evidence=evidence,summary=summary,goal_turn_classification='progress',full_goal_complete=False)
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete']
    assert sum(ledger['completed_editorial_record_counts_by_file'].values())==sum(len(g.get('records',[]))for g in ledger['completed_editorial_families'])==2059
    assert sum(ledger['source_prose_reviewed_counts_by_file'].values())==2175
    GUIDE.mkdir(parents=True);copies=[(Path(p),Path(p).name)for p in actual['representative_contact_sheets']]
    controls=Path('work/analysis/maria_opening_controls_v2039/six_actual_portraits_and_full_native_nameplates.png');copies.append((controls,controls.name))
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/maria_opening_context_v2035_V2030')
    copies +=[(cap/f'frame_{n:06d}_navigation.png',label+'.png')for n,label in((31400,'port_resupply_context'),(33300,'palace_context'),(34500,'trader_context'),(36100,'barkeep_context'),(37700,'Miwa_context'),(38500,'drink_bill_context'))]
    guide=[]
    for source,name in copies:
        dest=GUIDE/name;copy2(source,dest);assert sha(dest.read_bytes())==sha(source.read_bytes());guide.append(dict(path=str(dest),source=str(source),sha256=sha(dest.read_bytes())))
    save(ROOT/'guide_copies.json',dict(folder=str(GUIDE),files=guide,all_byte_exact=True));save(LEDGER,ledger)
    old=HANDOFF.read_text(encoding='utf-8');marker='## Maria Hangzhou opening38 source/prose review - V2038';assert marker in old
    top=old.split('## Current coverage and registered release',1)[0].replace('# Current editorial handoff - V2038','# Current editorial handoff - V2050',1)
    top=top.replace('approved Rafael, Joakim, Maria and Camille','approved Rafael, Hodram, Joakim, Maria and Camille')
    history=marker+old.split(marker,1)[1]
    coverage=('## Current coverage and registered release\n\n'
        '- Ledger: `translations/editorial_review_current_v1.json`. **2059 historical completions = 1456 revised + 603 retained; 2175 source/prose reviewed.**\n'
        '- Fresh V1871 pass: **656 explicitly reread and integrated/reconciled; 0 fresh route drafts.** Other 1403 historical completions need explicit fresh reconciliation.\n'
        '- Completed:1402 COMMON +429 SC2 +117 SC0 +73 SC1 +38 SC3. Reviewed:1518 COMMON +429 SC2 +117 SC0 +73 SC1 +38 SC3. 116 COMMON incomplete; all remaining routes/shared shops/towns/random/player prose stay in scope.\n'
        '- Registered experimental: `'+str(ROM)+'`, profile `'+manifest['profile']+'`; 489 manifest batches /114 accepted layers. SHA256 `'+digest+'`.\n'
        '- Exact clean-input patch: `'+release['patch']+'`; SHA256 `'+release['patch_sha256']+'`. Whole-ROM reconstruction exact.\n'
        '- ARM9 `'+release['ARM9_sha256']+'`; COMMON `'+release['COMMON_sha256']+'`; SC3 `'+release['SC3_sha256']+'`. SC0/SC1/SC2 and123040 staged bytes unchanged.\n'
        '- Canonical baseline and clean Japanese input unchanged. Preserve all ROMs and earlier translations. V1492 remains promoted; no new promotion,commit orpush.\n\n')
    section='## Maria Hangzhou opening38 integrated - V2050\n\n'+summary+'\n\n'
    section+='- Final review: `'+str(FINAL)+'`; approved manuscript: `'+str(DOC)+'`; map: `'+str(MAP)+'`. All38 exact clean/current references,source glosses,revision/retention reasons andactual panel bindings arefile-qualified.\n'
    section+='- Private profile: `dk4tool/dialogue/maria_opening_profile.py`; compiler: `dk4tool/patch/maria_opening_editorial.py`; config: `translations/maria_opening_editorial_release_v1.json`. Focused Ruff and27 negative guards pass. Explicit0A/15/4A controls,macro5/2/7;global profiles unchanged. Draft2036 provisional unknownprofile label is superseded;failed2037 and2037b remain preserved,2037c is the complete proof.\n'
    section+='- Actual: `'+str(ACTUAL)+'`. All38 revised speech panels match full native ink;all85 command pairs andnormal Hangzhou return pass. Current38500 frames ends at thebarkeep Ten coins bill after theMiwa drink invitation. Context samples areunreviewed anddo not provecomplete random-event coverage. Existing system-unlock donor unchanged,not earned. Current23051,revised18324 andallbuild/startup/patch jobs terminal.\n'
    section+='- Release: `'+str(RELEASE)+'`; startup: `'+str(STARTUP)+'`. Whole candidate equals actual-tested research;onlyB33 grows72 bytes. All302 otherSC3 blocks,includingunclassifiedB109,allotherfiles/components exact. NativeCS0101/all47 non-speech commands preserved;303 loads/606 parent modes perROM.\n'
    section+='- Guide: `'+str(GUIDE)+'`; '+str(len(guide))+' byte-exact copies. Keep allgeneratedROMs,includingresearch andreconstruction.\n'
    section+='- Next: continue complete exchanges across remaining storylines andshared shop/town/random/player prose. Reuse completed Maria/Hodram/Rafael/Stockholm checks. 116 COMMON,1403 historical reconciliations,SC3B109 classification,separate graphics/all18 plaques andlater older-record technical re-audit remainopen. Full objective active.\n\n'
    HANDOFF.write_text(top+coverage+section+history,encoding='utf-8',newline='\n')
    for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
        with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2050 Maria Hangzhou opening38 integrated\n\n'+summary+'\n')
    Path('docs/maria_opening_v2050_completion.md').write_text('# Maria Hangzhou opening V2050\n\n'+section,encoding='utf-8',newline='\n')
    assert sha(ROM.read_bytes())==digest and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    save(ROOT/'completion_receipt.json',dict(summary=summary,final_review=str(FINAL),final_review_sha256=sha(FINAL.read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),
        handoff_sha256=sha(HANDOFF.read_bytes()),proofs=evidence,completed2059_revised1456_retained603_source_prose2175=True,
        fresh656_integrated656_pending0=True,remaining_historical_reconciliations1403=True,guide=str(GUIDE),guide_files=len(guide),
        all_generated_ROMs_preserved=True,V1492_promoted_canonical_unchanged_full_goal_active=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(completed=2059,revised=1456,retained=603,source_prose=2175,fresh_integrated=656,pending=0,guide_files=len(guide),full_goal_complete=False))
