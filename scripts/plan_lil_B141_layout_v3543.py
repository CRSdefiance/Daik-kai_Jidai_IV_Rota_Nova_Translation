"""Plan14 complete paragraphs with no authored line breaks or display exemptions."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue import lil_B141_layout_v1 as planner
from dk4tool.dialogue.lil_B141_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B141_layout_v3543')
INPUT=Path('translations/lil_B141_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B141_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));source=read(doc['source_context']);image=NdsImage.open(doc['current_ROM']);profile=profile_for(image.read_file('/__arm9__.bin'),IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[141]);reports=[];failures=[];notes=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex'])
        try:
            encoded=planner.encode_relocatable_dialogue(raw,r['english'],profile);qa=planner.audit_relocatable_dialogue_record(raw,r['english'],profile)
        except (ValueError,AssertionError) as e:failures.append(dict(id=r['id'],error=str(e)));continue
        warnings=[x.code for x in encoded.diagnostics if x.severity=='warning']
        if 'line-break-count' in warnings:
            reason='Japanese source row breaks are not English dramatic pauses. Complete meaning and punctuation stay in one logical paragraph;the native formatter owns wrapping. Only the source/target row-count difference is accepted. No glyph,bounds,pagination,orphan,weak-ending,macro,control or blank-page exemption is granted.';r.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);r['localization_note']+=' '+reason;notes.append(dict(id=r['id'],reason=reason))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]))];unwaived=[i for i in warnings if i not in r.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=r['id'],issues=issues,unwaived=unwaived,english=r['english']))
        r['compiled_hex']=encoded.encoded.hex();reports.append(dict(id=r['id'],kind=r['kind'],encoded_hex=r['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all14_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,source_macro_count_preserved=True,no_ROM_registry_ledger_review_orcompletion_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==14
    profilepath=Path('dk4tool/dialogue/lil_B141_profile.py');formatterpath=Path('dk4tool/dialogue/lil_B141_layout_v1.py');doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module=str(profilepath),scoped_profile_module_sha256=sha(profilepath.read_bytes()),native_formatter_module=str(formatterpath),native_formatter_module_sha256=sha(formatterpath.read_bytes()),layout_QA_proof=str(proof),layout_QA_proof_sha256=sha(proof.read_bytes()),status='source-prose-layout-planned;native-font-reference-release-pending');save(OUTPUT,doc)
    print(dict(plans=14,row_count_notes=len(notes),unresolved=0,credit=0))
