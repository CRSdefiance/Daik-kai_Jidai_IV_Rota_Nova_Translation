"""Record73 fresh whole-exchange prose decisions without completion inflation."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/hodram_opening_checkpoint_v2020')
DOC=Path('translations/hodram_opening_contextual_editorial_manuscript_v1.json')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,ledger=map(read,(DOC,LEDGER));records=doc['records'];assert len(records)==73
    assert sum(r['editorial_decision']=='revise'for r in records)==38
    assert sum(r['editorial_decision']=='retain-wording'for r in records)==35
    assert all(r['review']['formatting']is False for r in records)
    assert (ledger['records_editorially_completed'],ledger['records_revised_and_integrated'],ledger['retained_wordings_editorially_completed'])==(1948,1395,553)
    assert ledger['records_with_source_and_prose_pass']==ledger['records_with_source_prose_drafts']==2064
    f=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert (f['fresh_pass_records_explicitly_reread'],f['fresh_pass_records_integrated'],f['fresh_pass_records_pending_native_actual_release'])==(545,545,0)
    assert '/data/SC1.DK4'not in ledger['source_prose_reviewed_counts_by_file']
    ROOT.mkdir(parents=True);(ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger['records_with_source_and_prose_pass']=ledger['records_with_source_prose_drafts']=2137
    ledger['source_prose_reviewed_counts_by_file']['/data/SC1.DK4']=73
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC1.DK4']=[r['id']for r in records]
    ledger['active_source_prose_drafts']['manuscripts'].append(str(DOC))
    ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-and73-Hodram-opening-entries-pending-native-reference-release'
    f['record_keys'] += [dict(file_path='/data/SC1.DK4',id=r['id'])for r in records]
    assert len(f['record_keys'])==len({(r['file_path'],r['id'])for r in f['record_keys']})==618
    f['record_IDs'] += [r['id']for r in records]
    f['legacy_bare_record_IDs_are_sequence_only_not_unique_across_files']=True
    f['fresh_pass_records_explicitly_reread']=618;f['fresh_pass_records_pending_native_actual_release']=73
    f['latest_contextual_manuscript']=str(DOC)
    f['pending_contextual_families']=[dict(id='Hodram-opening-trade-and-Lil73',file_path='/data/SC1.DK4',blocks=[42,43,44],
        records=73,manuscript=str(DOC),revisions=38,retentions=35,source_prose_reviewed=True,formatting_reference_actual_release_pending=True)]
    f['coverage_note']='618 file-qualified entries explicitly reread:545 integrated/reconciled plus73 Hodram opening/trade/Lil encounter drafts. Bare IDs overlap between routes;use record_keys. Historical1948 completions unchanged,1403 stilloutside reconciled freshpass.'
    summary=("V2020 reviews all73 clean-source Hodram opening/trade/Lil speeches ascomplete exchanges:38 proposed revisions35individual justified retentions. "
        "Restore pirate-like patrol fleet rather thanpiratehunters,the namedVestaros,public policy support forProtestants,the first battle-thrill recollection,world-leading trade-network ambition,wartime rival-contract conditions,andLil/Camille/Gerhard exchange details. "
        "Current native names measured onisolated catalog copies areHodramJoakimBergstrom,CharlesJeanRochefort,ManuelAlmeida,GerhardArdelknatts,LilArgot andCamilleMarinusOverijssel. "
        "Separate untouched macro machine expandsHodram6/Bergstrom9/BergstromFleet15. Actualsource Charles12 andManuel17 portraits/nameplates viewed;Gerhard10/Hodram01 exactpriorSC1/runtime controls inherited. "
        "V2013 remainsregistered487batches114acceptedlayers;noROM/patch/registry change. Newformat/native planes,complete typed references,representative revised transitions andregistered integration remainpending. "
        "Live ordinary no-fixture context2018/session99041 hasfinished B42 andis exploring normaldeparture;not a terminal gameplay proof yet. "
        "Fresh618reread/545integrated/73pending;source/prose2137=1518COMMON429SC2117SC073SC1;historical1948complete=1395revised553retained unchanged. "
        "116COMMON,1403historical completions outsidefreshpass,allremaining routes/shared/town/random/playerprose,separategraphics/all18plaques andlater older-record technical re-audit remainopen;fullgoalactive.")
    ledger['latest_checkpoint']=summary
    ledger['hodram_opening_contextual_v2020']=dict(summary=summary,manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),
        records=records,goal_turn_classification='progress',formatting_complete=False,full_goal_complete=False)
    save(LEDGER,ledger)
    text=re.sub(r'\n{3,}','\n\n',HANDOFF.read_text(encoding='utf-8'))
    text=text.replace('# Current editorial handoff - V2017b','# Current editorial handoff - V2020',1)
    old='**1948 historical completions =1395revised +553retained;2064source/prose reviewed.**';assert old in text
    text=text.replace(old,old.replace('2064','2137'),1)
    old='Fresh V1871pass:545 explicitly reread andintegrated/reconciled;0activefresh route drafts.';assert old in text
    text=text.replace(old,'Fresh V1871pass:618 explicitly reread;545 integrated/reconciled and73 Hodram drafts pending.',1)
    text=text.replace('reviewed:1518COMMON +429SC2 +117SC0.','reviewed:1518COMMON +429SC2 +117SC0 +73SC1.',1)
    section='## Hodram73 source/prose review - V2020\n\n'+summary+'\n\n'
    section+='- Manuscript:'+str(DOC)+';73complete source/current references,glosses anddecisions. Allformatting gatesfalse. Counterkey isfile_path plusID,because SC0/SC1 B44IDs overlap.\n'
    section+='- Nativepresentation counts:01=26,10=10,12=9,17=8,02=9,09=5,FE=6;67progressive/six separateFE,zerochoices. All171original commands(93/31/47) and24relative sites belongtothe typed-source packet. No B42R0032 nonprosefragment istranslated.\n'
    section+='- Vestaros spelling isconfirmed inactualcurrent shipdata(frame004000 RAM containsVestaros,notVasteros) andearlier native headings. V2017source-lead spelling wasprovisional;draft usesVestaros.\n'
    section+='- Actualrun:work/analysis/hodram_opening_context_v2018;captures:E:/Rota Nova translations/Generated/work/emulation_v193/hodram_opening_context_v2018_V2013. Handle99041 remainslive. Beforeendingtheturn,close orrecord itslatestverifiedpause/handle;do notrestart froma timeout. Broader B135portdeparture dialogue isobserved unreviewedcontext,noeditorialcredit.\n\n'
    marker='## Next complete family prepared - V2017';assert marker in text
    text=text.replace(marker,section+marker,1)
    HANDOFF.write_text(text,encoding='utf-8',newline='\n')
    for name in('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
        with(Path('docs')/name).open('a',encoding='utf-8',newline='\n')as out:out.write('\n\n## V2020 Hodram73 contextual source/prose review\n\n'+summary+'\n')
    save(ROOT/'checkpoint_receipt.json',dict(summary=summary,ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        manuscript_sha256=sha(DOC.read_bytes()),no_new_completed_records_or_ROM_registry_patch_changes=True,
        source_prose=2137,fresh_reread=618,integrated=545,pending=73,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(source_prose=2137,fresh_reread=618,integrated=545,pending=73,completed_unchanged=1948))
