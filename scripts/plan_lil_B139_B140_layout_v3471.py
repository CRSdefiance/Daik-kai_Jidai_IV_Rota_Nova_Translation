"""Create a source-bound successor planner and plan67 progressive speeches."""
from copy import deepcopy
from pathlib import Path
import importlib
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B139_B140_layout_v3471')
SOURCE=Path('work\\analysis\\lil_remaining_B139_B140_source_v3456\\next67_B139_B140_clean_current_context.json')
PROFILE=Path('dk4tool\\dialogue\\lil_B139_B140_profile.py')
FORMATTER=Path('dk4tool\\dialogue\\lil_B139_B140_layout_v1.py')
OLD=Path('dk4tool\\dialogue\\lil_B122_B127_layout_v2.py')
INPUTS=[Path('translations/lil_B139_B140_editorial_manuscript_v3.json')]
OUTPUTS=[Path('translations/lil_B139_B140_editorial_manuscript_v4.json')]

if __name__=='__main__':
    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    source=read(SOURCE)
    profile_for=importlib.import_module('dk4tool.dialogue.lil_B139_B140_profile').profile_for
    planner=importlib.import_module('dk4tool.dialogue.lil_B139_B140_layout_v1')
    image=NdsImage.open(source['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    docs=[deepcopy(read(p)) for p in INPUTS];reports=[];failures=[];notes=[]
    for doc in docs:
        for row in doc['records']:
            if row['kind']=='typed-choice-label':
                value=row['english'].encode('ascii');assert value and value.strip()==value and len(value)<=36 and all(32<=c<127 for c in value)
                row['compiled_hex']=value.hex();reports.append(dict(id=row['id'],kind=row['kind'],label_hex=value.hex(),selection_geometry_native_gates_pending=True));continue
            raw=bytes.fromhex(row['source_hex']);profile=profile_for(arm,blocks[row['block']],'FE-paper' if row['kind']=='system-FE' else 'progressive')
            try:
                result=planner.encode_relocatable_dialogue(raw,row['english'],profile)
                qa=planner.audit_relocatable_dialogue_record(raw,row['english'],profile)
            except (ValueError,AssertionError) as error:
                failures.append(dict(id=row['id'],error=str(error),english=row['english']));continue
            warnings=[d.code for d in result.diagnostics if d.severity=='warning']
            if 'line-break-count' in warnings:
                reason='Source Japanese wrapping and source staging are not English dramatic breaks. Complete meaning and punctuation remain in one logical paragraph;the calibrated formatter owns balanced pair-safe wrapping. Only row-count differences are accepted. No orphan,weak-ending,glyph,bounds,pagination,control,macro,choice orblank-page exemption is granted.'
                row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);row['localization_note']+=' '+reason;notes.append(dict(id=row['id'],reason=reason))
            issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))]
            unwaived=[v for v in warnings if v not in row.get('qa_waivers',[])]
            if issues or unwaived:failures.append(dict(id=row['id'],issues=issues,unwaived=unwaived,english=row['english']))
            row['compiled_hex']=result.encoded.hex()
            reports.append(dict(id=row['id'],kind=row['kind'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all67_paragraph_layout_QA.json'
    save(proof,dict(manuscripts={str(p):sha(p.read_bytes()) for p in INPUTS},scoped_profile=str(PROFILE),scoped_profile_sha256=sha(PROFILE.read_bytes()),formatter=str(FORMATTER),formatter_sha256=sha(FORMATTER.read_bytes()),previous_formatter=str(OLD),previous_formatter_sha256=sha(OLD.read_bytes()),records=reports,failures=failures,row_count_notes=notes,formatting_approval_not_granted=True,no_ROM_registry_ledger_or_editorial_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:
        print(dict(plans=len(reports),notes=len(notes),unresolved=failures),flush=True);raise SystemExit(1)
    assert len(reports)==67
    for doc,old,new in zip(docs,INPUTS,OUTPUTS,strict=True):
        doc.update(previous_manuscript=str(old),previous_manuscript_sha256=sha(old.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module=str(PROFILE),scoped_profile_module_sha256=sha(PROFILE.read_bytes()),native_formatter_module=str(FORMATTER),native_formatter_module_sha256=sha(FORMATTER.read_bytes()),layout_QA_proof=str(proof),layout_QA_proof_sha256=sha(proof.read_bytes()),status='source-prose-layout-planned;native-font-choice-reference-release-pending')
        save(new,doc)
    print(dict(plans=67,row_count_notes=len(notes),unresolved=0,credit=0),flush=True)
