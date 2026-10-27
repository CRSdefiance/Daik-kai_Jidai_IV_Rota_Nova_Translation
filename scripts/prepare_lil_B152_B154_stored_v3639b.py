"""Correct only the pre-write replacement ordering in the preserved derivation."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
SOURCE=Path('scripts/prepare_lil_B152_B154_stored_v3639.py')
if __name__=='__main__':
    text=SOURCE.read_text(encoding='utf-8');old="('all38_final_stored_targets152','all59_final_stored_targets236')";new="('all59_final_stored_targets152','all59_final_stored_targets236')";assert old in text
    namespace={'__name__':'__main__','__file__':__file__};exec(compile(text.replace(old,new),str(SOURCE)+'[ordering-correction]', 'exec'),namespace)
    p=Path('work/analysis/lil_B152_B154_stored_derivation_v3639/ordering_correction.txt');p.write_text('The first producer stopped at its pre-write replacement guard: all38 had already become all59. Successor3639b corrects only that filename replacement; original producer and font probe remain preserved.\nSuccessor SHA256 '+sha(Path(__file__).read_bytes())+'\n',encoding='utf-8')
