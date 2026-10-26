"""Record viewed native sheets and protect only concrete phrase findings."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    root=Path('work/analysis/lil_B122_B127_visual_refinement_v3280');assert not root.exists()
    old=Path('dk4tool/dialogue/lil_B122_B127_layout_v1.py');new=Path('dk4tool/dialogue/lil_B122_B127_layout_v2.py');assert not new.exists()
    pairs=[('raise','hell'),('pretty','well'),('enemy','fleet'),('fleet','movements'),('one','unit'),('lot','of'),('final','round')]
    text=old.read_text(encoding='utf-8');anchor='PROTECTED_BOUNDARIES=frozenset({';assert text.count(anchor)==1
    text=text.replace(anchor,anchor+','.join(repr(p) for p in pairs)+',');compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    pold=Path('scripts/prepare_lil_B122_B127_layout_v3275.py');pnew=Path('scripts/prepare_lil_B122_B127_layout_v3281.py');assert not pnew.exists()
    text=pold.read_text(encoding='utf-8').replace('lil_B122_B127_layout_v3275','lil_B122_B127_layout_v3281').replace('lil_B122_B127_layout_v1','lil_B122_B127_layout_v2')
    a="OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v3.json'),Path('translations/lil_B122_B127_choice_manuscript_v2.json')]";assert a in text
    text=text.replace(a,"OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v4.json'),Path('translations/lil_B122_B127_choice_manuscript_v3.json')]")
    compile(text,str(pnew),'exec');pnew.write_text(text,encoding='utf-8')
    font=read('work/analysis/lil_B122_B127_fonts_v3277/current_macro_QA_and_progressive_font_proof.json');fe=read('work/analysis/lil_B122_B127_FE_v3278/current_FE_macro_font_and_typed_paper_proof.json');choices=read('work/analysis/lil_B122_B127_choices_v3279/all2_typed_menu_native_proof.json')
    sheets=font['review_sheets']+fe['review_sheets']+[dict(path=r['review_sheet'],sha256=r['review_sheet_sha256']) for r in choices['menus']]
    assert len(sheets)==23 and all(sha(Path(r['path']).read_bytes())==r['sha256'] for r in sheets)
    findings=[dict(id=i,phrase=p,reason=r) for i,p,r in [
        ('DK4_MES_B122_R0094','raise hell','FE row split the afterlife farewell idiom.'),
        ('DK4_MES_B124_R0005','pretty well','Adverb phrase split between third and fourth rows.'),
        ('DK4_MES_B124_R0016','enemy fleet movements','Compound information topic split after fleet.'),
        ('DK4_MES_B126_R0061','one unit','Trading-volume unit split after one.'),
        ('DK4_MES_B127_R0107','a lot of','Indefinite quantity phrase split after lot.'),
        ('DK4_MES_B127_R0089','final round','Game-stage noun phrase split between rows.')]]
    root.mkdir(parents=True);save(root/'all23_viewed_native_sheets_and_phrase_findings.json',dict(all19_progressive_two_FE_and_two_choice_sheets_viewed=True,sheets=sheets,findings=findings,protected_pairs=pairs,successors={str(p):sha(p.read_bytes()) for p in [new,pnew]},previous={str(p):sha(p.read_bytes()) for p in [old,pold]},all_source_words_meaning_names_macros_punctuation_retained=True,no_preceding_producer_or_prose_modified=True,no_ROM_orcredit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
