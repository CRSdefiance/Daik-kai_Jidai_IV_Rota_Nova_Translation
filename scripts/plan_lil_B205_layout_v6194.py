"""Plan17 logical paragraphs;document only actual source/target row-count differences."""
from pathlib import Path
from copy import deepcopy
from dk4tool.dialogue import lil_B205_layout_v2 as planner
from dk4tool.dialogue.lil_B205_profile_v2 import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_layout_v6194');INPUT=Path('translations/lil_B205_editorial_manuscript_v3.json');OUTPUT=Path('translations/lil_B205_editorial_manuscript_v4.json')
ROW_NOTES={17:'The source separates Mamma mia from the human-speech reaction. Both complete English reactions fit naturally in one native row;the following independent FE object supplies the mimicry beat. There is no source-authored dramatic blank line to preserve.',44:'The source amused observation and catching announcement stay together as one logical paragraph. Ordinary native wrapping preserves both complete clauses and prospective intent;the source newline is not an English dramatic pause.',51:'All ordered wing beats,bang,crack,thud and rustling remain in one sound caption. The Japanese groups sounds over three rows;English words use ordinary measured FE wrapping without copying those physical groups or inserting a blank row.',59:'The Japanese places the sigh,taunt and laugh on separate rows. All three are present in the English paragraph,with punctuation marking their beats. The following FE remains a separate object echoing only the complete taunt;no authored early breaks are needed.',67:'Lil\'s suppressed laugh,laughter and captured-bird/save-face joke remain a complete paragraph. The Japanese three-row arrangement and older English early break/indent are not dramatic staging;English wraps the full thought using the unchanged native metrics.'}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));im=NdsImage.open(doc['current_ROM']);arm=im.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks;reports=[];failures=[];notes=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);p=profile_for(arm,blocks[r['block']],'FE-paper' if r['kind']=='system-FE' else 'progressive')
        try:encoded=planner.encode_relocatable_dialogue(raw,r['english'],p);qa=planner.audit_relocatable_dialogue_record(raw,r['english'],p)
        except (ValueError,AssertionError) as e:failures.append(dict(id=r['id'],error=str(e)));continue
        warnings=[x.code for x in encoded.diagnostics if x.severity=='warning']
        if 'line-break-count' in warnings:
            reason=ROW_NOTES[r['source_record_index']]+' Only this source/target row-count difference is accepted. Complete native glyphs,bounds,pagination,controls,weak endings,phrase grouping and blank-page behavior still require their own checks.'
            r.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=r['id'],source_Japanese=r['source_Japanese'],target_English=r['english'],formatted_markup=encoded.formatted_markup,reason=reason))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]))];unwaived=[x for x in warnings if x not in r.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=r['id'],issues=issues,unwaived=unwaived,english=r['english']))
        r['compiled_hex']=encoded.encoded.hex();reports.append(dict(id=r['id'],kind=r['kind'],encoded_hex=r['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all17_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==17
    for key,p in [('scoped_profile_module',Path('dk4tool/dialogue/lil_B205_profile_v2.py')),('native_formatter_module',Path('dk4tool/dialogue/lil_B205_layout_v2.py')),('layout_QA_proof',proof)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',status='source-prose-layout-planned;native-font-reference-release-pending');save(OUTPUT,doc);print(dict(plans=17,row_count_notes=len(notes),unresolved=0,credit=0))
