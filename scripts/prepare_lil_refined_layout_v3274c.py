"""Preserve failed refinements; select a complete natural counterfactual."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/refine_lil_three_native_wraps_v3274.py');new=Path('scripts/refine_lil_three_native_wraps_v3274c.py')
    plannerold=Path('scripts/prepare_lil_B122_B127_layout_v3273b.py');plannernew=Path('scripts/prepare_lil_B122_B127_layout_v3275.py')
    assert not new.exists() and not plannernew.exists()
    text=old.read_text(encoding='utf-8').replace('lil_B122_B127_wrap_refinement_v3274','lil_B122_B127_wrap_refinement_v3274c')
    a="If not for his ties to the English Crown, this wouldn't have happened... I think he wanted to get along with us...";assert text.count(a)==1
    text=text.replace(a,"This wouldn't have happened if he hadn't been tied to the English Crown... I think he wanted to get along with us...")
    text=text.replace('Use the equivalent if-not-for counterfactual','Reorder the equivalent counterfactual within its clause')
    compile(text,str(new),'exec');new.write_text(text,encoding='utf-8')
    text=plannerold.read_text(encoding='utf-8').replace('lil_B122_B127_layout_v3273b','lil_B122_B127_layout_v3275')
    a="INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v1.json'),Path('translations/lil_B122_B127_choice_manuscript_v1.json')]";assert text.count(a)==1
    text=text.replace(a,"INPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v2.json'),Path('translations/lil_B122_B127_choice_manuscript_v1.json')]")
    a="OUTPUTS=[Path(str(p).replace('_v1.json','_v2.json')) for p in INPUTS]";assert text.count(a)==1
    text=text.replace(a,"OUTPUTS=[Path('translations/lil_B122_B127_editorial_manuscript_v3.json'),Path('translations/lil_B122_B127_choice_manuscript_v2.json')]")
    compile(text,str(plannernew),'exec');plannernew.write_text(text,encoding='utf-8')
    root=Path('work/analysis/lil_B122_B127_refined_tools_v3274c');root.mkdir(parents=True)
    save(root/'preserved_failures_successor_provenance.json',dict(previous={str(p):sha(p.read_bytes()) for p in [old,plannerold,Path('scripts/repair_lil_layout_actor_guard_v3273b.py')]},successors={str(p):sha(p.read_bytes()) for p in [new,plannernew,Path('dk4tool/dialogue/lil_B122_B127_profile_v2.py')]},failed_repair_receipt='3273b generated both valid successors before its optional receipt directory was missing. Those files remain exact; no rerun or overwrite.',complete_counterfactual_selected_from='work/analysis/lil_counterfactual_wrap_v3274b/equivalent_counterfactual_layout_comparisons.json',no_earlier_producer_or_prose_modified=True,producer_sha256=sha(Path(__file__).read_bytes())))
