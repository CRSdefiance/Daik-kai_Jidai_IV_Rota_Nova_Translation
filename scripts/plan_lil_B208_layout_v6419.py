"""Plan24 complete paragraphs with four individually justified row-count differences."""
from pathlib import Path
from copy import deepcopy
from dk4tool.dialogue import lil_B208_layout_v5 as planner
from dk4tool.dialogue.lil_B208_profile_v1 import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_layout_v6419');INPUT=Path('translations/lil_B208_editorial_manuscript_v2.json');OUTPUT=Path('translations/lil_B208_editorial_manuscript_v5.json')
ROW_NOTES={
28:"The source face correction,similar-air explanation and tentative strength explanation occupy three Japanese rows. The full English keeps both short complete correction/explanation sentences and wraps the final conjecture over the remaining two native rows. All uncertainty,apparent strength and too remain. Four English rows are within the original capacity;no initial blank row,added pause or dramatic authored break is introduced.",
48:"The interested reaction and location question fit naturally together on one complete English row. The Japanese puts the reaction and question on separate rows;its newline is ordinary physical wrapping,not a dramatic pause. All words and both conversational beats remain without an early English break.",
76:"Cristina's acknowledgment and limited promise to keep the lead in mind fit together on one native row. The source separates acknowledgment from the remembering clause. The full source meaning and restrained commitment remain in one paragraph;no artificial second line or stronger promise is introduced.",
79:"The man's subjective certainty about Cristina's ability and Good luck! both fit on one native row. The two Japanese physical rows do not require English staging. Both encouragement beats and his personal confidence remain complete without an early break or a narrator guarantee."}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');block=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[208];reports=[];failures=[];notes=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,block,'FE-paper' if r['kind']=='system-FE' else 'progressive')
        try:encoded=planner.encode_relocatable_dialogue(raw,r['english'],p);qa=planner.audit_relocatable_dialogue_record(raw,r['english'],p)
        except (ValueError,AssertionError) as e:failures.append(dict(id=r['id'],error=str(e)));continue
        warnings=[x.code for x in encoded.diagnostics if x.severity=='warning']
        if 'line-break-count' in warnings:
            reason=ROW_NOTES[r['source_record_index']]+' Only this exact source/target row-count difference is approved. Complete glyphs,bounds,pagination,controls,weak endings,phrase grouping,orphan and blank-page checks are not waived.'
            r.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=r['id'],source_Japanese=r['source_Japanese'],target_English=r['english'],formatted_markup=encoded.formatted_markup,reason=reason))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]) and r.get('qa_waiver_reason'))];unwaived=[x for x in warnings if x not in r.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=r['id'],issues=issues,unwaived=unwaived))
        r['compiled_hex']=encoded.encoded.hex();r['reviewed_ordinary_boundaries']=qa.get('reviewed_ordinary_boundaries',[]);reports.append(dict(id=r['id'],kind=r['kind'],encoded_hex=r['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all24_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==24 and {r['id'] for r in notes}=={f'DK4_MES_B208_R{n:04d}' for n in ROW_NOTES}
    for key,p in [('scoped_profile_module',Path('dk4tool/dialogue/lil_B208_profile_v1.py')),('native_formatter_module',Path('dk4tool/dialogue/lil_B208_layout_v5.py')),('layout_QA_proof',proof)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',status='24-paragraphs-layout-planned;complete-native-plane-review-references-English-scene-release-pending');save(OUTPUT,doc);print(dict(plans=24,row_count_notes=len(notes),unresolved=0,credit=0));print([(r['id'],r['qa']['visible_lines']) for r in reports])
