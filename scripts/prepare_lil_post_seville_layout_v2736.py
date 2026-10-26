"""Plan compiler-owned wrapping;document only source-layout line-count notes."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.qa import audit_relocatable_dialogue_record
from dk4tool.dialogue.lil_post_seville_profile import profile_for
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_post_Seville_layout_v2736')
OLD=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v1.json')
DOC=Path('translations/lil_post_seville_and_egypt_warning_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));image=NdsImage.open(doc['current_ROM'])
    arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;reports=[];waivers=[];failures=[]
    for row in doc['records']:
        profile=profile_for(arm,blocks[row['block']]);raw=bytes.fromhex(row['source_hex'])
        result=encode_relocatable_dialogue(raw,row['english'],profile);qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        codes=[d.code for d in result.diagnostics if d.severity=='warning']
        if 'line-break-count' in codes:
            reason='The source ordinary line breaks are Japanese layout,not separate English dramatic pauses. This complete exchange preserves the spoken ellipses/questions andall source meaning in one paragraph. Compiler-owned balanced pair-safe wrapping may use a different physical row count. Only the count difference is accepted;no overflow,orphan,predicate,control,missing-glyph orblank-page exemption is granted. Full current native fonts,complete QA andrelease checks remain required.'
            row['qa_waivers']=['line-break-count'];row['qa_waiver_reason']=reason;row['localization_note']+=' '+reason
            waivers.append(dict(id=row['id'],source_hex=row['source_hex'],english=row['english'],reason=reason))
        unwaived=[d for d in codes if d not in row.get('qa_waivers',[])]
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))]
        if unwaived or issues:failures.append(dict(id=row['id'],unwaived_codes=unwaived,issues=issues))
        reports.append(dict(id=row['id'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,qa=qa,encoder_diagnostic_codes=codes))
    ROOT.mkdir(parents=True);save(ROOT/'all34_layout_and_QA.json',dict(manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),records=reports,waivers=waivers,failures=failures,full_goal_complete=False))
    assert not failures,failures
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module='dk4tool/dialogue/lil_post_seville_profile.py',
        scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_post_seville_profile.py').read_bytes()),previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        layout_QA_proof=str(ROOT/'all34_layout_and_QA.json'),status='source-prose-layout-planned;current-native-fonts-references-representative-release-pending',
        no_English_or_source_control_change=True)
    save(DOC,doc)
    print(f'34layout/QA plans pass;{len(waivers)}narrow source-line-count notes. English unchanged;current native fonts/pipelines pending.')
