"""Preserve allprose;resolve concrete phrase splits on five viewed sheets."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B135_B136_visual_refinement_v3358');assert not root.exists();fontpath=Path('work/analysis/lil_B135_B136_fonts_v3357b/current_macro_QA_and_progressive_font_proof.json');font=read(fontpath)
    for s in font['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    old=Path('dk4tool/dialogue/lil_B135_B136_layout_v1.py');new=Path('dk4tool/dialogue/lil_B135_B136_layout_v2.py');assert not new.exists();t=old.read_text(encoding='utf-8');anchor='PROTECTED_BOUNDARIES=frozenset({';assert anchor in t;t=t.replace(anchor,anchor+"('young','lady'),('come','on'),('want','it'),('stop','you'),('upper','and'),('and','lower'),");compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    oldplan=Path('scripts/plan_lil_B135_B136_layout_v3356b.py');plan=Path('scripts/plan_lil_B135_B136_layout_v3358b.py');assert not plan.exists();t=oldplan.read_text(encoding='utf-8')
    t=t.replace("INPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v1.json')]","INPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v2.json')]").replace("OUTPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v2.json')]","OUTPUTS=[Path('translations/lil_B135_B136_editorial_manuscript_v3.json')]")
    t=t.replace('lil_B135_B136_layout_v3356b','lil_B135_B136_layout_v3358b').replace('lil_B135_B136_layout_v1','lil_B135_B136_layout_v2');compile(t,str(plan),'exec');plan.write_text(t,encoding='utf-8')
    oldfont=Path('scripts/verify_lil_B135_B136_fonts_v3357b.py');newfont=Path('scripts/verify_lil_B135_B136_fonts_v3359.py');assert not newfont.exists();t=oldfont.read_text(encoding='utf-8').replace('lil_B135_B136_fonts_v3357b','lil_B135_B136_fonts_v3359').replace('lil_B135_B136_layout_v1','lil_B135_B136_layout_v2').replace('lil_B135_B136_editorial_manuscript_v2','lil_B135_B136_editorial_manuscript_v3')
    a='    cases=[];qa_reports=[];pictures=[];macro_calls=0';assert a in t;t=t.replace(a,a+f"\n    reused_path=Path({str(fontpath)!r});reused=read(reused_path);oldcases={{c['id']:c for c in reused['cases']}};fresh_ids=[];reused_ids=[]")
    a="        logical=row['english'].split('}',1)[1]";i=t.index(a)
    t=t[:i]+"""        prior=oldcases[row['id']]
        if prior['encoded_hex']==result.encoded.hex():
            assert sha(Path(prior['preview']).read_bytes())==prior['preview_sha256']
            cases.append(prior);pictures.append((row['id'],'selector'+row['source_presentation_prefix_hex'],Image.open(prior['preview']).convert('RGB')));macro_calls+=8;reused_ids.append(row['id']);continue
        fresh_ids.append(row['id'])
"""+t[i:]
    a='current_original_macro_alignment_calls=280,';assert a in t;t=t.replace(a,a+"reused_proof=str(reused_path),reused_proof_sha256=sha(reused_path.read_bytes()),newly_executed_font_cases=len(fresh_ids),reused_unchanged_font_cases=len(reused_ids),changed_IDs=fresh_ids,")
    compile(t,str(newfont),'exec');newfont.write_text(t,encoding='utf-8');root.mkdir(parents=True)
    save(root/'all5_viewed_native_sheets_and_phrase_findings.json',dict(all5_progressive_sheets_viewed=True,sheets=font['review_sheets'],findings=[dict(id=i,protect_phrase=p) for i,p in [('DK4_MES_B135_R0053','young lady'),('DK4_MES_B135_R0073','want it'),('DK4_MES_B135_R0110','stop you'),('DK4_MES_B136_R0009','Upper and Lower'),('DK4_MES_B136_R0029','Come on')]],prose_words_unchanged=True,previous_formatter=str(old),previous_formatter_sha256=sha(old.read_bytes()),formatter=str(new),formatter_sha256=sha(new.read_bytes()),successor_planner=str(plan),successor_font_producer=str(newfont),producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
