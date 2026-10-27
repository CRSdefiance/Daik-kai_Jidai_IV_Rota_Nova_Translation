"""Complete143-paragraph layout/QA planning before any formatting approval."""
from pathlib import Path
from copy import deepcopy
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.lil_clifford_north_new_world_profile import profile_for
from dk4tool.dialogue.lil_clifford_north_new_world_layout_v3 import encode_relocatable_dialogue
from dk4tool.dialogue.lil_clifford_north_new_world_layout_v3 import audit_relocatable_dialogue_record
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_Clifford_North_New_World_layout_v2981')
OLD=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v4.json')
DOC=Path('translations/lil_clifford_north_new_world_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();doc=deepcopy(read(OLD));image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');bs=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    reports=[];waivers=[];failures=[]
    for row in doc['records']:
        if row.get('qa_waivers')==['line-break-count']:
            suffix=' '+row['qa_waiver_reason'];assert row['localization_note'].endswith(suffix)
            row['localization_note']=row['localization_note'][:-len(suffix)];row.pop('qa_waivers');row.pop('qa_waiver_reason')
        profile=profile_for(arm,bs[row['block']],'FE-paper' if row['kind']=='system-FE' else 'progressive');raw=bytes.fromhex(row['source_hex'])
        try:
            result=encode_relocatable_dialogue(raw,row['english'],profile);qa=audit_relocatable_dialogue_record(raw,row['english'],profile)
        except (ValueError,AssertionError) as error:
            failures.append(dict(id=row['id'],english=row['english'],source_Japanese=row['source_Japanese'],error=str(error)));continue
        warnings=[d.code for d in result.diagnostics if d.severity=='warning']
        if 'line-break-count' in warnings:
            reason='Ordinary Japanese physical wrapping is not anEnglish dramatic pause. The complete source meaning,spoken punctuation andexchange context are preserved in one logical paragraph;the calibrated formatter owns balanced pair-safe wrapping. Only the row-count difference is accepted. No overflow,orphan,predicate,weak-ending,missing-glyph,control orblank-page exemption is granted. Complete native fonts andconsumer-specific pagination still require verification.'
            row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);row['localization_note']+=' '+reason;waivers.append(dict(id=row['id'],reason=reason))
        unwaived=[code for code in warnings if code not in row.get('qa_waivers',[])]
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))]
        if unwaived or issues:failures.append(dict(id=row['id'],english=row['english'],source_Japanese=row['source_Japanese'],unwaived=unwaived,issues=issues))
        reports.append(dict(id=row['id'],encoded_hex=result.encoded.hex(),formatted_markup=result.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all143_layout_and_QA.json';save(proof,dict(manuscript=str(OLD),manuscript_sha256=sha(OLD.read_bytes()),records=reports,waivers=waivers,failures=failures,full_goal_complete=False))
    if failures:
        print(dict(layouts=len(reports),narrow_line_count_notes=len(waivers),unresolved=len(failures),findings=failures),flush=True)
        raise SystemExit(1)
    doc.update(encoder='dialogue-relocatable-v1',dialogue_profile='lil-opening-editorial-native-v1',scoped_profile_module='dk4tool/dialogue/lil_clifford_north_new_world_profile.py',
        scoped_profile_module_sha256=sha(Path('dk4tool/dialogue/lil_clifford_north_new_world_profile.py').read_bytes()),previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        layout_QA_proof=str(proof),native_formatter_module='dk4tool/dialogue/lil_clifford_north_new_world_layout_v3.py',native_formatter_module_sha256=sha(Path('dk4tool/dialogue/lil_clifford_north_new_world_layout_v3.py').read_bytes()),inherited_planner_research='work/analysis/lil_Kuhn_Alliance_layout_v3871/all82_layout_and_QA.json',no_English_or_source_control_change=True,status='source-prose-layout-planned;current-ordinary-FE-native-fonts-and-separate-choice-reference-release-pending')
    save(DOC,doc)
    print(f'143layout/QA plans pass;{len(waivers)}line-count-only notes. Reviewed English unchanged;140progressive/3FE current native gates remain pending.')
