"""Keep complete meaning while resolving three concrete weak endings."""
from copy import deepcopy
from pathlib import Path
from collections import Counter
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.lil_B122_B127_profile_v2 import profile_for
from dk4tool.dialogue.lil_B122_B127_layout_v1 import encode_relocatable_dialogue,audit_relocatable_dialogue_record
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B122_B127_wrap_refinement_v3274')
OLD=Path('translations/lil_B122_B127_editorial_manuscript_v1.json')
NEW=Path('translations/lil_B122_B127_editorial_manuscript_v2.json')
FIXES={
 'DK4_MES_B122_R0128':("If not for his ties to the English Crown, this wouldn't have happened... I think he wanted to get along with us...",'Use the equivalent if-not-for counterfactual to preserve Crown constraints, the unrealized outcome and Camille\'s explicit speculation while avoiding a weak line ending.'),
 'DK4_MES_B124_R0053':('So all that flirting at taverns was part of being an adventurer?','Remove only the redundant emphasis just to fit the complete skeptical question at a natural boundary. All that flirting, taverns and the adventurer rationalization remain. The earlier working retention is preserved in v1; this final wording is a documented small revision.'),
 'DK4_MES_B125_R0183':("Worrying is your job, Camille! If I worried too, it'd get so gloomy we'd lose every single crewmember!",'Shorten is supposed to be to is: the source role tease remains a hypothetical joke, with Camille, both worriers, gloomy atmosphere and every crewmember intact. Preserve raw legacy and effective registered wording in predecessor provenance; this final wording is a small revision for natural display.')}
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    doc=deepcopy(read(OLD));im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks
    findings=[]
    for row in doc['records']:
        if row['id'] not in FIXES:continue
        body,note=FIXES[row['id']];before=deepcopy(row);tag=row['english'].split('}',1)[0]+'}'
        row['english']=tag+body;row['localization_note']+=' '+note;row['editorial_decision']='revise';row.pop('fresh_retained_wording_justification',None)
        qa=audit_relocatable_dialogue_record(bytes.fromhex(row['source_hex']),row['english'],profile_for(arm,blocks[row['block']]))
        unresolved=[v for v in qa['issues'] if v['severity'] in ['error','warning'] and v['code']!='line-break-count']
        findings.append(dict(id=row['id'],previous=before,english=row['english'],note=note,qa=qa,unresolved=unresolved))
    ROOT.mkdir(parents=True);proof=ROOT/'three_complete_source_native_wrap_refinements.json'
    save(proof,dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),findings=findings,no_earlier_manuscript_modified=True,no_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert len(findings)==3 and not any(r['unresolved'] for r in findings),[(r['id'],r['unresolved'],r['qa']['visible_lines']) for r in findings]
    doc.update(previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),native_wrap_refinement=str(proof),native_wrap_refinement_sha256=sha(proof.read_bytes()),revised=sum(r['editorial_decision']=='revise' for r in doc['records']),retained=sum(r['editorial_decision']=='retain-wording' for r in doc['records']))
    save(NEW,doc);print(dict(refinements=3,speech_decisions=dict(Counter(r['editorial_decision'] for r in doc['records'])),credit=0))
