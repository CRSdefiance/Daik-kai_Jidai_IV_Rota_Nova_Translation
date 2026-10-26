"""Keep the viewed final care-it-deserves object intact without changing reviewed prose."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B166_viewed_flow_v4078c')
if __name__=='__main__':
    assert not ROOT.exists();font=Path('work/analysis/lil_B166_fonts_v4081/current_macro_QA_and_progressive_font_proof.json');d=read(font);sheet=d['review_sheets'][5];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];tools=[]
    tools.append(derive('dk4tool/dialogue/lil_B166_layout_v3.py','dk4tool/dialogue/lil_B166_layout_v4.py',{'def _word(value):':"PROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset({('sure','to'),('care','it'),('it','deserves')})\n\ndef _word(value):"}))
    tools.append(derive('scripts/plan_lil_B166_layout_v4078b.py','scripts/plan_lil_B166_layout_v4078c.py',{'lil_B166_layout_v3':'lil_B166_layout_v4','lil_B166_layout_v4078b':'lil_B166_layout_v4078c','lil_B166_editorial_manuscript_v2':'lil_B166_editorial_manuscript_v3','lil_B166_editorial_manuscript_v3':'lil_B166_editorial_manuscript_v4'}))
    ROOT.mkdir(parents=True);save(ROOT/'viewed_final_warning_clause_refinement.json',dict(viewed_font_proof=str(font),viewed_font_proof_sha256=sha(font.read_bytes()),viewed_sheet=sheet,record='DK4_MES_B166_R0175',finding='The rests-on refinement is correct;keep the care it deserves together andavoid an it deserves last-row fragment.',tools=tools,all42_English_paragraphs_source_meanings_controls_and_decisions_unchanged=True,no_new_waiver_or_global_guard_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('Final viewed care-it-deserves clause refinement recorded;words unchanged.')
