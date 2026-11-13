"""Record full source census and117 new contextual reviews; no completions added."""
from pathlib import Path
import re
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/editorial_contextual_checkpoint_v2000')
LEDGER=Path('translations/editorial_review_current_v1.json')
HANDOFF=Path('docs/editorial_handoff_current.md')
DOC=Path('translations/rafael_opening_contextual_editorial_manuscript_v2.json')
CHOICES=Path('translations/rafael_opening_contextual_choices_editorial_draft_v1.json')
RAW=Path('work/analysis/editorial_source_census_v1992/four_routes_raw_and_COMMON_source_census.json')
NATIVE=Path('work/analysis/native_storyline_census_v1995/all_route_source_current_native_census.json')
FONT=Path('work/analysis/rafael_opening_fonts_v1998/all114_progressive_native_macros_and_complete_font_planes.json')
SPAN=Path('work/analysis/rafael_opening_span_v1999/current_B44_final_span_diagnosis.json')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    (ROOT/'ledger_before.json').write_bytes(LEDGER.read_bytes());(ROOT/'handoff_before.md').write_bytes(HANDOFF.read_bytes())
    ledger,doc,choices,raw,native,font,span=map(read,(LEDGER,DOC,CHOICES,RAW,NATIVE,FONT,SPAN))
    rom=Path(ledger['current_integrated_candidate']['path']) if 'path'in ledger['current_integrated_candidate']else Path('out/all_routes_combined_v1986_candidate.nds')
    digest=sha(rom.read_bytes());assert digest=='f2dcb4cc4d688e1cd40a22367180841d27d06e540edbd16927f784b2cfcb50ca'
    assert digest==raw['candidate_sha256']==native['candidate_sha256']==font['candidate_sha256']
    manifest=read(rom.with_suffix('.manifest.json'));assert len(manifest['batches'])==485
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(font['cases'])==114 and not font['failures'] and font['native_macro_calls']==916
    assert len(font['review_sheets'])==15
    for row in font['review_sheets']:
        assert sha(Path(row['path']).read_bytes())==row['sha256']
    assert span['commands']==182 and span['required_current_span']==76 and span['no_ROM_manuscript_map_registry_or_file_bytes_modified']
    source=IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC0.DK4')).blocks[44]
    current=IlnkContainer.parse(NdsImage.open(rom).read_file('/data/SC0.DK4')).blocks[44]
    records=doc['records']+choices['records'];assert len(records)==117
    for row in records:
        for value,refkey,hexkey in ((source,'source_reference','source_hex'),(current,'current_reference','current_text_hex')):
            at=row[refkey]['offset'];body=bytes.fromhex(row[hexkey]);assert value[at:at+len(body)]==body and value[at+len(body)]==0
        assert all(row['review'][gate]is True for gate in ('source','context','localization','naturalness')) and row['review']['formatting']is False
        source_text=row['source_Japanese']
        assert re.findall('FI|FA|FO',source_text)==re.findall(r'\{MACRO:(FI|FA|FO)\}',row['english'])
        assert row['localization_note'] and row['source_meaning']
    assert sum(r['editorial_decision']=='revise'for r in records)==33
    assert sum(r['editorial_decision']=='retain-wording'for r in records)==84
    f=ledger['contextual_story_natural_dialogue_pass_v1871']
    assert f['fresh_pass_records_explicitly_reread']==f['fresh_pass_records_integrated']==428
    assert f['fresh_pass_records_pending_native_actual_release']==0
    keys=[dict(file_path='/data/SC2.DK4',id=ident)for ident in f['record_IDs']]
    keys += [dict(file_path='/data/SC0.DK4',id=r['id'])for r in records]
    assert len(keys)==len({(r['file_path'],r['id'])for r in keys})==545
    f['record_keys']=keys
    f['record_keys_are_authoritative_across_routes_bare_IDs_can_collide']=True
    f['record_IDs'] += [r['id']for r in records]
    f['fresh_pass_records_explicitly_reread']=545;f['fresh_pass_records_pending_native_actual_release']=117
    f['latest_contextual_manuscript']=str(DOC);f['latest_contextual_choice_draft']=str(CHOICES)
    f['pending_contextual_families']=[dict(id='Rafael-Lisbon-opening117',file_path='/data/SC0.DK4',block=44,
        record_IDs=[r['id']for r in records],manuscript=str(DOC),choices=str(CHOICES),revisions=33,retentions=84,
        source_prose_reviewed=True,formatting_reference_gameplay_release_pending=True)]
    f['coverage_note']='545 explicitly reread;428 integrated/reconciled Lil entries and117 pending Rafael Lisbon opening entries. Historical1831 completions remain unchanged;1403 historical completions outside the reconciled fresh pass remain open.'
    assert ledger['records_editorially_completed']==1831 and ledger['records_with_source_and_prose_pass']==1947
    ledger['records_with_source_and_prose_pass']=2064;ledger['records_with_source_prose_drafts']=2064
    assert '/data/SC0.DK4'not in ledger['source_prose_reviewed_counts_by_file']
    ledger['source_prose_reviewed_counts_by_file']['/data/SC0.DK4']=117
    ledger['reviewed_but_incomplete_route_record_IDs']['/data/SC0.DK4']=[r['id']for r in records]
    ledger['active_source_prose_drafts']['manuscripts'] += [str(DOC),str(CHOICES)]
    ledger['active_source_prose_drafts']['status']='116-reviewed-COMMON-and117-Rafael-opening-entries-incomplete;historical-manuscript-list-preserved'
    proofs={str(p):sha(p.read_bytes())for p in (DOC,CHOICES,RAW,NATIVE,FONT,SPAN)}
    summary=("V2000 expands the clean/current corpus to1307 blocks across allfour routes and3668 native COMMON entries. "
        "Raw census1992 consumes speaker00 before text NUL;all20980 clean speech boundaries independently match native1995,with328 typed choice labels. "
        "The native walk explicitly supplies previous-result FFFFFFFF;32 guarded clean/current controls prove0200/0300/0400 fallthrough and0100 span behavior. "
        "OnlycurrentSC0B44 stops:its last0100 span64 ends inside R0479;one-byte in-memory64-to76 normalization gives182 exact source-corresponding commands and115 speech boundaries. "
        "SC3B109 also has a distinct initial command-structure difference;neither risk is silently repaired or counted complete. "
        "Rafael's entire Lisbon opening115 speeches/system panels andboth choices are fresh source/prose reviewed:33 revisions84 individually justified retentions. "
        "Draftv2 preserves FO/FI/FA order in the personal-trust loan. Native research measures Rafael6/Castor6/CastorCo.10,validates114 complete216x64 planes and916 guarded macro/alignment calls;all15 sheets viewed. "
        "One R0327 weak-line-ending warning remains explicitly unwaived;FE money modal,choice displays,typed final relocation/current-span repair,representative original/revised transitions andregistered release remain pending. "
        "Fresh545reread/428integrated/117pending;source/prose2064=1518COMMON+429SC2+117SC0;historical1831complete=1362revised469retained unchanged. "
        "All broader routes/shared/town/random/playerprose,116incomplete COMMON,1403historical completions needing reconciliation,separategraphics/all18plaques andlater older-record technical re-audit stayopen. "
        "No new actual-gameplay credit,ROM,patch,registry,baseline orpromotion change;V1986 remains registered485batches114acceptedlayers with exactclean patch,V1492 promoted;fullgoalactive.")
    ledger['latest_checkpoint']=summary
    ledger['rafael_opening_contextual_v2000']=dict(summary=summary,proofs=proofs,records=records,
        native_font_visual_sheets_viewed=True,formatting_completion_or_release_approval=False,
        warnings=[dict(id='DK4_MES_B44_R0327',code='weak-line-ending',status='unwaived;finaldecisionpending')],
        goal_turn_classification='progress',next_actions=['Separate FE andchoice display proofs','Current-source typed182-command map withfour relative sites andexplicit stale span repair',
            'Representative original/revised opening andboth choice transitions','Source-bound native profile andregistered cumulative release with exactclean patch'],
        full_goal_complete=False)
    save(LEDGER,ledger)
    h=HANDOFF.read_text(encoding='utf-8')
    assert h.startswith('# Current editorial handoff - V1989b')
    h=h.replace('# Current editorial handoff - V1989b','# Current editorial handoff - V2000',1)
    h=h.replace('**1831 historical completions =1362revised +469retained;1947source/prose reviewed.**','**1831 historical completions =1362revised +469retained;2064source/prose reviewed.**',1)
    h=h.replace('Fresh V1871pass:428 explicitly reread andintegrated/reconciled;no activefresh route drafts.','Fresh V1871pass:545 explicitly reread;428 integrated/reconciled and117 Rafael-opening entries pending.',1)
    h=h.replace('reviewed:1518COMMON +429SC2.','reviewed:1518COMMON +429SC2 +117SC0.',1)
    heading='## Rafael opening117 source/native checkpoint - V2000\n\n'+summary+'\n\n'
    heading+='- Manuscripts:'+str(DOC)+' and'+str(CHOICES)+'. All117 rows retain exact clean/current offsets,bytes,full preambles,glosses andindividual decisions. Allformatting gates remainfalse. BareIDs cancollide acrossroutes;freshledger record_keys nowincludes file_path plusID.\n'
    heading+='- Source/raw1992:'+str(RAW)+'. Preserve1990/1991/1993 predecessor reports;their speaker00 andimplicit-previous-result/0400 assumptions are superseded,notROM failures. Rawoutside-signature3372Japanese nullsegments and102current Japanese-bearing speech candidates needcontextual classification;noautomatic incomplete-text claim.\n'
    heading+='- Native1995:'+str(NATIVE)+'. All1307clean bodywalks havezeroerrors;1306current complete. HeaderCS0101 isrecorded forSC3;synthetic-body walks donotprove original loaders,outerdispatch orreachability. Opaqueeffects arebridged forstructure only.\n'
    heading+='- Font1998:'+str(FONT)+'.114completeprogressive planes,916macro calls,all15sheets viewed. Samecurrent native F/I guard supports literals;measured FI6 avoids legacy7-byte parity. Researchlocalprofile only,globalprofiles unchanged. Oneweak-line-ending warningR0327 unwaived.\n'
    heading+='- Span1999:'+str(SPAN)+'. CurrentR0479 header6616,text6622,NUL6679;parent6604 old64 targets6672insideEnglish;correctintent target6684 requires76. Purecopy normalization changesbyte6606only andmatchesall182cleancommand words/nesting. Actualcandidate unchanged;nexttarget mustrecompute finalspan andtestindependent-preparation branch.\n'
    heading+='- Actualnewgame snapshot fornative calls:E:/Rota Nova translations/Generated/work/emulation_v193/lil_Lookout_v1986_newgame/final_arm9_ram.bin;route0,selectors0/4/5/6 map0/4/5/6. Thisis existingstartup runtimecontext,notfreshwhole-opening gameplay. Allnewjobs terminal.\n\n'
    marker='## Fresh sailing/crew64 reconciled - V1989b'
    assert marker in h;h=h.replace(marker,heading+marker,1)
    HANDOFF.write_text(h,encoding='utf-8')
    for name in ('editorial_review_goal.md','translation_progress.md','todo.md','known_issues.md'):
        p=Path('docs')/name
        with p.open('a',encoding='utf-8')as out:out.write('\n\n## V2000 full-corpus census andRafael opening117 checkpoint\n\n'+summary+'\n')
    note=Path('docs/rafael_opening_v2000_contextual_checkpoint.md')
    note.write_text('# Rafael Lisbon opening contextual checkpoint V2000\n\n'+summary+'\n\n'+heading,encoding='utf-8')
    assert sha(rom.read_bytes())==digest and sha(Path('translations/release_stack.json').read_bytes())==manifest['release_stack_sha256']
    save(ROOT/'checkpoint_receipt.json',dict(summary=summary,proofs=proofs,ledger_sha256=sha(LEDGER.read_bytes()),handoff_sha256=sha(HANDOFF.read_bytes()),
        source_prose2064=True,fresh545_integrated428_pending117=True,historical1831_unchanged=True,
        ROM_registry_patch_baseline_and_all_generated_ROMs_preserved=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(reviewed=2064,fresh_read=545,integrated=428,pending=117,historical_complete=1831,ROM_unchanged=True))
