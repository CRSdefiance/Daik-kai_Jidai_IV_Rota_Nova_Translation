"""Plan full B207 paragraphs without shortening or authored breaks;formatting gate stays pending."""
from pathlib import Path
from copy import deepcopy
from dk4tool.dialogue import lil_B207_layout_v1 as planner
from dk4tool.dialogue.lil_B207_profile_v1 import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_layout_v6357')
INPUT=Path('translations/lil_B207_editorial_manuscript_v2.json')
OUTPUT=Path('translations/lil_B207_editorial_manuscript_v3.json')
ROW_NOTES={5:'Emilio\'s eager address and wanting-a-weapon idiom remain one complete natural approach.',8:'Lil\'s brief startled question remains a single spoken beat.',12:'Emilio wants to get stronger too,and therefore wants a weapon;the complete eager causal reply wraps as ordinary English.',15:'The food-versus-weapon tease,explicit Kidding! reassurance and name question remain distinct punctuation-led beats within one paragraph.',19:'The exact existing Minotaur Axe title and enthusiastic definite article/exclamation remain complete.',23:'Lil reacts to the name,infers a large weapon,speculates about Emilio\'s ability and asks its location;all four beats remain.',26:'Emilio\'s uncertainty,hearsay,past-island clue and personal knowledge limit remain complete in casual American English.',30:'Lil\'s personal offer to search stays qualified by if I feel like it;no promise or guaranteed find is added.',33:'His first premature Hooray! remains one exuberant beat.',37:'Lil repeats her precise if-I-feel-like-it qualification,not a vague scheduling Maybe.',41:'Still, hooray! keeps his cheerful persistence after her correction.',45:'Lil adds her separate undecided-gift warning in one complete reply,without a loan or ownership claim.',48:'His short disappointed Aw. closes the joke without extra action or an argument.'}
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[207];reports=[];failures=[];notes=[]
    for row in doc['records']:
        assert row['kind']=='progressive';raw=bytes.fromhex(row['source_hex']);p=profile_for(arm,block)
        try:encoded=planner.encode_relocatable_dialogue(raw,row['english'],p);qa=planner.audit_relocatable_dialogue_record(raw,row['english'],p)
        except (ValueError,AssertionError) as e:failures.append(dict(id=row['id'],error=str(e)));continue
        warnings=[v.code for v in encoded.diagnostics if v.severity=='warning']
        if 'line-break-count' in warnings:
            reason=ROW_NOTES[row['source_record_index']]+' Only source/English row count differs. No complete-glyph,bounds,pagination,control,macro,weak-ending,phrase,orphan or blank-page waiver.';row.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=row['id'],reason=reason))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in row.get('qa_waivers',[]))];unwaived=[w for w in warnings if w not in row.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=row['id'],issues=issues,unwaived=unwaived,english=row['english']))
        row['compiled_hex']=encoded.encoded.hex();reports.append(dict(id=row['id'],encoded_hex=row['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all13_spoken_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,no_ROM_registry_ledger_or_review_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==13
    for key,p in [('scoped_profile_module',Path('dk4tool/dialogue/lil_B207_profile_v1.py')),('native_formatter_module',Path('dk4tool/dialogue/lil_B207_layout_v1.py')),('layout_QA_proof',proof)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',status='13-spoken-paragraphs-layout-planned;native-font-relocation-English-scene-release-pending');save(OUTPUT,doc)
    print(dict(spoken_plans=13,row_count_notes=len(notes),unresolved=0,credit=0));print([(r['id'],r['qa']['visible_lines']) for r in reports])
