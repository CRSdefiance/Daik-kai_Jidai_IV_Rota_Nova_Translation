"""Plan59 paragraphs without authored breaks andrecord unresolved native-QA findings honestly."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue import lil_B152_B154_layout_v4 as planner
from dk4tool.dialogue.lil_B152_B154_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_layout_v4633')
INPUT=Path('translations/lil_B152_B154_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B152_B154_editorial_manuscript_v5.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;reports=[];failures=[];notes=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);profile=profile_for(arm,blocks[r['block']])
        try:encoded=planner.encode_relocatable_dialogue(raw,r['english'],profile);qa=planner.audit_relocatable_dialogue_record(raw,r['english'],profile)
        except (ValueError,AssertionError) as e:failures.append(dict(id=r['id'],error=str(e)));continue
        warnings=[x.code for x in encoded.diagnostics if x.severity=='warning']
        if 'line-break-count' in warnings:
            reason='Japanese source row breaks are not English dramatic pauses. One complete logical paragraph preserves meaning;the native formatter owns wrapping. Only row-count difference is accepted;no glyph,bounds,pagination,weak-ending,orphan,macro,control orblank-page exemption.';r.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=r['id'],reason=reason))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]))];unwaived=[i for i in warnings if i not in r.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=r['id'],issues=issues,unwaived=unwaived,english=r['english']))
        if r['id']=='DK4_MES_B154_R0075':assert "A man's either cool or not to you." in qa['visible_lines']
        r['compiled_hex']=encoded.encoded.hex();reports.append(dict(id=r['id'],kind=r['kind'],encoded_hex=r['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all59_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==59
    for key,p in [('scoped_profile_module',Path('dk4tool/dialogue/lil_B152_B154_profile.py')),('native_formatter_module',Path('dk4tool/dialogue/lil_B152_B154_layout_v4.py')),('layout_QA_proof',proof)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',status='source-prose-layout-planned;native-font-reference-release-pending');save(OUTPUT,doc);print(dict(plans=59,row_count_notes=len(notes),unresolved=0,credit=0))
