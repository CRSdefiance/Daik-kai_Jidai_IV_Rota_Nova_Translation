"""Create complete source-branch and clean-transcript successors for nine blocks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
ROOT=Path('work/analysis/lil_B111_B119_context_tools_v3211a')
if __name__=='__main__':
    outputs=[
        (Path('scripts/prove_lil_shrines_temples_branches_v3160.py'),Path('scripts/prove_lil_B111_B119_branches_v3211.py')),
        (Path('scripts/render_lil_shrines_temples_clean_v3163b.py'),Path('scripts/render_lil_B111_B119_clean_v3212.py'))]
    assert not ROOT.exists() and not any(n.exists() for o,n in outputs)
    old,new=outputs[0]
    text=old.read_text(encoding='utf-8')
    for a,b in [
        ('lil_Shrines_Temples_branches_v3160','lil_B111_B119_branches_v3211'),
        ('work/analysis/lil_Shrines_Temples_source_v3159/complete220_clean_current_native_context.json',
         'work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json')]:
        assert a in text;text=text.replace(a,b)
    new.write_text(text,encoding='utf-8')
    old,new=outputs[1];text=old.read_text(encoding='utf-8')
    for a,b in [
        ('lil_Shrines_Temples_clean_transcripts_v3163b','lil_B111_B119_clean_transcripts_v3212'),
        ('work/analysis/lil_Shrines_Temples_source_v3163/complete235_clean_current_native_context.json',
         'work/analysis/lil_B111_B119_source_v3210b/complete182_clean_current_native_context.json'),
        ('lil_Shrines_Temples_branches_v3160','lil_B111_B119_branches_v3211'),
        ('all164speech_56alternatives_and15choices_rendered','all148speech_34alternatives_and_nochoices_rendered'),
        ('Ten complete clean-only transcripts;all235objects','Nine complete clean-only transcripts;all182objects')]:
        assert a in text;text=text.replace(a,b)
    new.write_text(text,encoding='utf-8')
    for old,new in outputs:compile(new.read_text(encoding='utf-8'),str(new),'exec')
    ROOT.mkdir(parents=True)
    save(ROOT/'source_context_tools_provenance.json',dict(
        previous={str(o):sha(o.read_bytes()) for o,n in outputs},
        successors={str(n):sha(n.read_bytes()) for o,n in outputs},
        all_clean_exchanges_before_older_English_comparison_required=True,no_global_helper_or_ROM_change=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
