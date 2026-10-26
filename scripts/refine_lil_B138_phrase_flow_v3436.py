"""Resolve phrase findings on all six viewed native sheets without changing prose."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_visual_refinement_v3436');assert not root.exists();oldproof=Path('work/analysis/lil_B138_fonts_v3435/current_macro_QA_and_progressive_font_proof.json');proof=read(oldproof)
    for s in proof['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    old=Path('dk4tool/dialogue/lil_B138_layout_v1.py');new=Path('dk4tool/dialogue/lil_B138_layout_v2.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    t=t.replace('STRONG_ENDINGS=frozenset({','STRONG_ENDINGS=frozenset({\n    \'am\',\'both\',',1)
    t=t.replace('PROTECTED_BOUNDARIES=frozenset({',"PROTECTED_BOUNDARIES=frozenset({('nothing','but'),('now','sales'),('make','up'),('get','my'),('my','best'),('best','meal'),('both','do'),('brought','this'),",1)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    a=Path('scripts/plan_lil_B138_layout_v3434b.py');plan=Path('scripts/plan_lil_B138_layout_v3436b.py');assert not plan.exists();t=a.read_text(encoding='utf-8')
    t=t.replace('lil_B138_layout_v3434b','lil_B138_layout_v3436b').replace('lil_B138_layout_v1','lil_B138_layout_v2').replace("INPUTS=[Path('translations/lil_B138_editorial_manuscript_v3.json')]","INPUTS=[Path('translations/lil_B138_editorial_manuscript_v4.json')]").replace("OUTPUTS=[Path('translations/lil_B138_editorial_manuscript_v4.json')]","OUTPUTS=[Path('translations/lil_B138_editorial_manuscript_v5.json')]")
    compile(t,str(plan),'exec');plan.write_text(t,encoding='utf-8')
    oldfont=Path('scripts/verify_lil_B138_fonts_v3435.py');font=Path('scripts/verify_lil_B138_fonts_v3437.py');assert not font.exists();t=oldfont.read_text(encoding='utf-8').replace('lil_B138_fonts_v3435','lil_B138_fonts_v3437').replace('lil_B138_layout_v1','lil_B138_layout_v2').replace('lil_B138_editorial_manuscript_v4','lil_B138_editorial_manuscript_v5')
    anchor='    cases=[];qa_reports=[];pictures=[];macro_calls=0';assert anchor in t
    addition=f"\n    reused_path=Path({str(oldproof)!r});reused=read(reused_path);oldcases={{c['id']:c for c in reused['cases']}};fresh_ids=[];reused_ids=[]\n    assert reused['candidate_sha256']==doc['current_ROM_sha256'] and reused['ARM9_sha256']==sha(ctx.arm) and reused['COMMON_sha256']==sha(ctx.common)\n    olddoc=read(reused['manuscript']);assert sha(Path(reused['manuscript']).read_bytes())==reused['manuscript_sha256']\n    assert {{r['id']:r['english'] for r in olddoc['records']}}=={{r['id']:r['english'] for r in doc['records']}}"
    t=t.replace(anchor,anchor+addition)
    anchor="        logical=row['english'].split('}',1)[1]";at=t.index(anchor)
    t=t[:at]+"""        prior=oldcases[row['id']]
        if prior['encoded_hex']==result.encoded.hex():
            assert sha(Path(prior['preview']).read_bytes())==prior['preview_sha256']
            cases.append(prior);pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(prior['preview']).convert('RGB')));macro_calls+=8;reused_ids.append(row['id']);continue
        fresh_ids.append(row['id'])
"""+t[at:]
    anchor='current_original_macro_alignment_calls=352,';assert anchor in t;t=t.replace(anchor,anchor+'reused_proof=str(reused_path),reused_proof_sha256=sha(reused_path.read_bytes()),newly_executed_font_cases=len(fresh_ids),reused_unchanged_font_cases=len(reused_ids),changed_IDs=fresh_ids,')
    compile(t,str(font),'exec');font.write_text(t,encoding='utf-8');root.mkdir(parents=True)
    save(root/'all6_viewed_native_sheets_and_phrase_findings.json',dict(all6_progressive_sheets_viewed=True,sheets=proof['review_sheets'],findings=[dict(id=i,reason=r) for i,r in [('DK4_MES_B138_R0040','Keep Nothing but together.'),('DK4_MES_B138_R0052','Keep Now sales together so the new clause begins as a unit.'),('DK4_MES_B138_R0075','Do not strand am before I in the question.'),('DK4_MES_B138_R0130','Keep brought this together in the consequences judgment.'),('DK4_MES_B138_R0185','Keep make up and get my best meal together.'),('DK4_MES_B138_R0246','Do not strand both before do our best.')]],prose_words_unchanged=True,previous_formatter=str(old),previous_formatter_sha256=sha(old.read_bytes()),formatter=str(new),formatter_sha256=sha(new.read_bytes()),successor_planner=str(plan),successor_font_producer=str(font),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
