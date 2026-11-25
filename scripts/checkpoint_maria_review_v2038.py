"""Record the38 complete source/prose decisions while native/release gates finish."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_opening_checkpoint_v2038')
DOC=Path('translations/maria_opening_contextual_editorial_manuscript_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,ledger=map(read,(DOC,LEDGER));rows=doc['records'];assert len(rows)==38
    assert sum(r['editorial_decision']=='revise'for r in rows)==23 and sum(r['editorial_decision']=='retain-wording'for r in rows)==15
    assert all(r['review']['formatting']is False for r in rows)
    assert ledger['records_editorially_completed']==2021 and ledger['records_with_source_and_prose_pass']==2137
    f=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert(f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(618,618,0)
    assert '/data/SC3.DK4'not in ledger['source_prose_reviewed_counts_by_file']
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2175
    ledger['source_prose_reviewed_counts_by_file']['/data/SC3.DK4']=38
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC3.DK4']=[r['id']for r in rows]
    ledger['active_source_prose_drafts']['manuscripts'].append(str(DOC))
    ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-and38-Maria-opening-entries-pending-native-reference-release'
    f['record_keys'] +=[dict(file_path='/data/SC3.DK4',id=r['id'])for r in rows]
    assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==656
    f['record_IDs'] +=[r['id']for r in rows]
    f['fresh_pass_records_explicitly_reread']=656;f['fresh_pass_records_pending_native_actual_release']=38
    f['latest_contextual_manuscript']=str(DOC)
    f['pending_contextual_families']=[dict(id='Maria-Hangzhou-opening38',file_path='/data/SC3.DK4',blocks=[33],records=38,
        manuscript=str(DOC),revisions=23,retentions=15,source_prose_reviewed=True,formatting_reference_actual_release_pending=True)]
    f['coverage_note']='656 file-qualified entries explicitly reread:618 integrated/reconciled plus38 Maria opening drafts. Historical2021 completions unchanged;1403 outside reconciled freshpass.'
    summary=('All38 Maria Hangzhou opening speeches reviewed asone complete clean-source exchange:23 revisions15 justified retentions. '
        'Restore enemyboarding tactics,narrow-bay positioning,Jam\'s voice andblame-for-crime account,Yukihisa\'s stowaway/sword-search/compatriot-duty context,France,Ian byname,explicit3percent payment/foreign-vessel disguise,tax-revenue reasoning andthorough maintenance beforeKurushima retaliation. '
        'Nativecatalog names onisolated copies areMariaHuameiLi,XienYan,JamJackLudwyan,YukihisaGenjoShiraki,IanDukov,RichardTownsend. Macro defaults measuredMaria5/Li2/LiClan7. '
        'All38 native progressive planes and308 guarded macro calls passwithzeroerrors/warnings;allfive preview sheets viewed. Explicitprivate leading0A mapsXien,not atext LF;15mapsIan,4AmapsRichard. '
        'Originalcurrent run2035/session23051 usesexisting isolated system-unlock save,notanearned unlock;no savestate/story/location/RNG/funds/outcome fixture. It finishes B33 andisexploring normalHangzhou facilities;not terminalyet. '
        '85original commands,zero relative sites,zerochoices. Draftv1 hasunregistered provisional profile label;approvedsuccessor mustuse actual registeredMaria baseplusprivate source-bound overrides. '
        'Failed2037 unknownprofile and2037b missing0A mapping preserved;2037c iscomplete nativeproof. No prose orROM modifiedtoobtainpassingplanes. '
        'Source/prose2175;fresh656reread/618integrated/38pending;historical2021=1433revised588retained unchanged. '
        'V2030 remainsregistered488batches114acceptedlayers with exactcleanpatch. 116COMMON,1403historical reconciliations,allremaining routes/shared shops/towns/random/playerprose,separategraphics/all18plaques andlaterolder-record technical re-audit remainopen. AllROMs preserved;fullgoalactive.')
    ledger['latest_checkpoint']='V2038 '+summary
    ledger['maria_opening_contextual_v2038']=dict(manuscript=str(DOC),records=rows,summary=summary,formatting_complete=False,goal_turn_classification='progress',full_goal_complete=False)
    assert ledger['goal_status']=='active'and not ledger['full_goal_complete'];save(LEDGER,ledger)
    h=HANDOFF.read_text(encoding='utf-8');h=h.replace('# Current editorial handoff - V2033','# Current editorial handoff - V2038',1)
    h=h.replace('2021 historical completions =1433revised +588retained;2137source/prose reviewed.','2021 historical completions =1433revised +588retained;2175source/prose reviewed.',1)
    h=h.replace('Fresh V1871pass:618 explicitly reread andintegrated/reconciled;0activefresh route drafts.','Fresh V1871pass:656 explicitly reread;618 integrated/reconciled and38 Maria drafts pending.',1)
    h=h.replace('reviewed:1518COMMON +429SC2 +117SC0 +73SC1.','reviewed:1518COMMON +429SC2 +117SC0 +73SC1 +38SC3.',1)
    marker='## Hodram opening/trade/Lil73 integrated - V2033';assert marker in h
    section='## Maria Hangzhou opening38 source/prose review - V2038\n\n'+summary+'\n\n'
    section+='- Manuscript: '+str(DOC)+';source:work/analysis/maria_opening_source_v2034/all38_clean_current_Hangzhou_opening_source.json;native:work/analysis/maria_opening_fonts_v2037c/all38_progressive_native_macros_and_complete_font_planes.json.\n'
    section+='- Actual job23051 islive atHangzhou;close itorrecordlatestverifiedpause beforeending. Normaltown/portcontext isbroader coverage,notneweditorialcredit. Default oldsystemsave donor preserved. Do notrepeat completedHodram/Rafael/Stockholm gates.\n\n'
    HANDOFF.write_text(h.replace(marker,section+marker,1),encoding='utf-8',newline='\n')
    save(ROOT/'checkpoint_receipt.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),ledger_sha256=sha(LEDGER.read_bytes()),
        handoff_sha256=sha(HANDOFF.read_bytes()),new_source_prose_reviews=38,new_completion_credit=0,registered_candidate_unchanged=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose=2175,fresh_reread=656,integrated=618,pending=38,complete=2021))
