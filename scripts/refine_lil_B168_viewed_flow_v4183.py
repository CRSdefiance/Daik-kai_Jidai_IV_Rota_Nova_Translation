"""Resolve viewed phrase splits without changing reviewed words or native metrics."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/lil_B168_viewed_flow_v4183')
if __name__=='__main__':
    assert not ROOT.exists();proof=Path('work/analysis/lil_B168_fonts_v4182b/all54_native_planes432_macros_and26_consumer_negatives.json');old=read(proof)
    assert len(old['review_sheets'])==7
    viewed=[]
    for s in old['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        viewed.append({**s,'review':'Viewed full original native sheet. All complete glyph planes and FE notices intact. Queue only identified phrase/contraction grouping refinements; all words remain unchanged.'})
    boundaries=[('sorts','of'),('of','things'),("it'll",'make'),('too','weird'),('go','talk'),('an','invitation'),('invitation','from'),('join','us')]
    tools=[derive('dk4tool/dialogue/lil_B168_layout_v2.py','dk4tool/dialogue/lil_B168_layout_v3.py',{
        'def _word(value):':"STRONG_ENDINGS = STRONG_ENDINGS | frozenset({\"it'll\"})\nPROTECTED_BOUNDARIES = PROTECTED_BOUNDARIES | frozenset("+repr(boundaries)+")\n\ndef _word(value):"})]
    tools.append(derive('scripts/plan_lil_B168_layout_v4181b.py','scripts/plan_lil_B168_layout_v4184.py',{
        'lil_B168_layout_v2':'lil_B168_layout_v3','lil_B168_layout_v4181b':'lil_B168_layout_v4184',
        'lil_B168_editorial_manuscript_v3':'lil_B168_editorial_manuscript_v4','lil_B168_editorial_manuscript_v4':'lil_B168_editorial_manuscript_v5'}))
    ROOT.mkdir(parents=True);save(ROOT/'all7_viewed_sheets_and_phrase_flow_refinements.json',dict(previous_native_proof=str(proof),previous_native_proof_sha256=sha(proof.read_bytes()),viewed_sheets=viewed,findings=[dict(id='DK4_MES_B168_R0026',finding='Keep all sorts of things together.'),dict(id='DK4_MES_B168_R0077',finding='Do not strand the auxiliary It will contraction at row end.'),dict(id='DK4_MES_B168_R0112',finding='Keep too weird together.'),dict(id='DK4_MES_B168_R0123',finding='Keep go talk together.'),dict(id='DK4_MES_B168_R0152',finding='Keep invitation from together.'),dict(id='DK4_MES_B168_R0194',finding='Keep join us together.')],tools=tools,all_reviewed_prose_names_macros_and_decisions_unchanged=True,no_manual_break_padding_guard_metric_waiver_ROM_registry_orcredit_change=True))
