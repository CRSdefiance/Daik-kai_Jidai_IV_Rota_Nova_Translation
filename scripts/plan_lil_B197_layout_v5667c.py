"""Plan21 paragraphs without authored breaks andrecord unresolved native-QA findings honestly."""
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue import lil_B197_layout_v1 as planner
from dk4tool.dialogue.lil_B197_profile import profile_for
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_layout_v5667c')
INPUT=Path('translations/lil_B197_editorial_manuscript_v1.json')
OUTPUT=Path('translations/lil_B197_editorial_manuscript_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not OUTPUT.exists();doc=deepcopy(read(INPUT));image=NdsImage.open(doc['current_ROM']);arm=image.read_file('/__arm9__.bin');blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;reports=[];failures=[];notes=[]
    for r in doc['records']:
        raw=bytes.fromhex(r['source_hex']);profile=profile_for(arm,blocks[r['block']],'FE-paper' if r['kind']=='system-FE' else 'progressive')
        try:encoded=planner.encode_relocatable_dialogue(raw,r['english'],profile);qa=planner.audit_relocatable_dialogue_record(raw,r['english'],profile)
        except (ValueError,AssertionError) as e:failures.append(dict(id=r['id'],error=str(e)));continue
        warnings=[x.code for x in encoded.diagnostics if x.severity=='warning']
        if 'line-break-count' in warnings:
            reason='Japanese source row breaks are not English dramatic pauses. One complete logical paragraph preserves meaning;the native formatter owns wrapping. Only row-count difference is accepted;no glyph,bounds,pagination,weak-ending,orphan,macro,control orblank-page exemption.';r.update(qa_waivers=['line-break-count'],qa_waiver_reason=reason);notes.append(dict(id=r['id'],reason=reason))
        if r['id']=='DK4_MES_B197_R0074':
            assert raw.hex()=='15948382c182c482a082b082bd82a282aa0a8e8482c982cd82bb82f182c891e58be082cd82c882a282f182be' and r['english']=="{SPEAKER:15}I'd like to buy it, but I don't have that kind of money."
            assert qa['visible_lines']==["I'd like to buy it, but I don't", 'have that kind of money.']
            assert [i['code'] for i in qa['issues']]==['weak-line-ending']
            r.update(qa_waivers=['weak-line-ending'],qa_waiver_reason="Exact B197 R74 only:the complete56-character personal explanation wraps into two readable rows,31 and24 visible characters,at the ordinary don't/have word boundary. A soft wrap is not a spoken pause. The full negative verb remains adjacent across the row transition;both rows start/end with complete glyphs and keep all words. Breaking earlier after I or but merely moves the dependency;after the comma leaves a much shorter first row. Do not narrow the viewport,shorten the sentence or add a dramatic break to satisfy a weak-word preference. This waives only this warning at these exact two rows;all native glyph,phase,bounds,pagination,source-control and consumer checks remain required.",
                exact_reviewed_soft_wrap_rows=["I'd like to buy it, but I don't", 'have that kind of money.'],exact_reviewed_soft_wrap_source_hex='15948382c182c482a082b082bd82a282aa0a8e8482c982cd82bb82f182c891e58be082cd82c882a282f182be')
            notes.append(dict(id=r['id'],reason="Exact B197 R74 only:the complete56-character personal explanation wraps into two readable rows,31 and24 visible characters,at the ordinary don't/have word boundary. A soft wrap is not a spoken pause. The full negative verb remains adjacent across the row transition;both rows start/end with complete glyphs and keep all words. Breaking earlier after I or but merely moves the dependency;after the comma leaves a much shorter first row. Do not narrow the viewport,shorten the sentence or add a dramatic break to satisfy a weak-word preference. This waives only this warning at these exact two rows;all native glyph,phase,bounds,pagination,source-control and consumer checks remain required.",exact_rows=["I'd like to buy it, but I don't", 'have that kind of money.']))
        issues=[i for i in qa['issues'] if i['severity'] in ['warning','error'] and not(i['severity']=='warning' and i['code'] in r.get('qa_waivers',[]))];unwaived=[i for i in warnings if i not in r.get('qa_waivers',[])]
        if issues or unwaived:failures.append(dict(id=r['id'],issues=issues,unwaived=unwaived,english=r['english']))
        r['compiled_hex']=encoded.encoded.hex();reports.append(dict(id=r['id'],kind=r['kind'],encoded_hex=r['compiled_hex'],formatted_markup=encoded.formatted_markup,qa=qa,encoder_warning_codes=warnings))
    ROOT.mkdir(parents=True);proof=ROOT/'all21_paragraph_layout_QA.json';save(proof,dict(manuscript=str(INPUT),manuscript_sha256=sha(INPUT.read_bytes()),records=reports,failures=failures,row_count_notes=notes,no_ROM_registry_ledger_orcredit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    if failures:print(failures);raise SystemExit(1)
    assert len(reports)==21
    for key,p in [('scoped_profile_module',Path('dk4tool/dialogue/lil_B197_profile.py')),('native_formatter_module',Path('dk4tool/dialogue/lil_B197_layout_v1.py')),('layout_QA_proof',proof)]:doc[key]=str(p);doc[key+'_sha256']=sha(p.read_bytes())
    doc.update(previous_manuscript=str(INPUT),previous_manuscript_sha256=sha(INPUT.read_bytes()),dialogue_profile='lil-opening-editorial-native-v1',status='source-prose-layout-planned;native-font-reference-release-pending');save(OUTPUT,doc);print(dict(plans=21,row_count_notes=len(notes),unresolved=0,credit=0))
