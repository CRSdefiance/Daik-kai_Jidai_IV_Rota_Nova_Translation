"""Correct draft batch gate metadata before standard five-gate validation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/approve_lil_shrines_fonts_v3189.py')
NEW=Path('scripts/approve_lil_shrines_fonts_v3190b.py')
ROOT=Path('work/analysis/lil_Shrines_Temples_approval_tools_v3190')
if __name__=='__main__':
    assert not NEW.exists() and not ROOT.exists()
    text=OLD.read_text(encoding='utf-8')
    old="""OUTPUTS=[Path('translations/lil_shrines_temples_editorial_manuscript_v6.json'),
         Path('translations/lil_shrines_temples_actor_style_manuscript_v4.json'),
         Path('translations/lil_shrines_temples_choice_manuscript_v3.json')]"""
    new=old.replace('editorial_manuscript_v6','editorial_manuscript_v7').replace('actor_style_manuscript_v4','actor_style_manuscript_v5').replace('choice_manuscript_v3','choice_manuscript_v4')
    assert text.count(old)==1
    text=text.replace(old,new).replace('lil_Shrines_Temples_font_approval_v3189','lil_Shrines_Temples_font_approval_v3190b')
    anchor="            encoder='dialogue-relocatable-v1',prose_companions="
    assert text.count(anchor)==1
    text=text.replace(anchor,"            review_gates=['source','context','localization','naturalness','formatting'],\n"+anchor)
    NEW.write_text(text,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'approval_metadata_successor.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        reason='Initial source-prose drafts declared only four batch gates. Every235per-record formatting gate is now proven; declare the full required five batch gates before unchanged standard validation.',
        no_gate_check_removed_or_waived=True,no_predecessor_modified=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
