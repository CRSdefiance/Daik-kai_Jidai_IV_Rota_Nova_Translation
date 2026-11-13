"""Bind menu requests to the exact saved source-command references before fixture creation."""
from scripts.audit_story_glyph_consistency import load,save
from scripts.approve_hodram_B211_B230_display_v1 import OUT
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT

if __name__=='__main__':
    path=ROOT/'focused_selection_v2.json';assert not path.exists()
    doc=load(ROOT/'focused_selection_v1.json');proof=load(OUT/'menus.json')
    commands={(r['block'],r['source_command_offset']) for r in proof['menus']}
    for fixture in doc['fixtures']:
        for action in fixture['sequence']:
            if 'menu' in action and action['menu']['block']==224:
                assert action['menu']['source_command_offset']==136
                action['menu']['source_command_offset']=138
        assert {(a['menu']['block'],a['menu']['source_command_offset']) for a in fixture['sequence'] if 'menu' in a}==commands
    doc['preparation_correction']='B224 menu source offset is 138, not 136. The v1 fixture preparation stopped before saving a ROM; preserve the failed attempt.'
    save(path,doc)
