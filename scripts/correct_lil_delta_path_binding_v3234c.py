"""Normalize Windows path identity without changing any content hash guard."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    old=Path('scripts/verify_lil_B111_B119_fonts_v3234b.py');new=Path('scripts/verify_lil_B111_B119_fonts_v3234c.py')
    assert not new.exists()
    text=old.read_text(encoding='utf-8')
    a="prior['scoped_profile']==doc['scoped_profile_module']"
    assert text.count(a)==1
    text=text.replace(a,"Path(prior['scoped_profile'])==Path(doc['scoped_profile_module'])")
    text=text.replace('lil_B111_B119_fonts_v3234b','lil_B111_B119_fonts_v3234c')
    new.write_text(text,encoding='utf-8')
    save(Path('work/analysis/lil_B111_B119_delta_tools_v3234/path_binding_correction.json'),dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),failure='Forward-slash versus backslash spelling of the same exact Windows profile path; content hashes already agree.',all_content_hashes_and_source_runtime_prose_guards_preserved=True,failed_producer_and_log_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
