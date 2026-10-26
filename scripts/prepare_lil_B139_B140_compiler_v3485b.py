"""Correct two inherited representative field names before any compiler import."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('dk4tool/patch/lil_B139_B140_editorial_v1.py');b=Path('dk4tool/patch/lil_B139_B140_editorial_v2.py');assert not b.exists();t=a.read_text(encoding='utf-8');assert t.count('B138')==2;t=t.replace('individual_selected_B138_visits','individual_selected_B139_B140_visits').replace('actual_selected_B138_IDs','actual_selected_B139_B140_IDs');compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B139_B140_compiler_tools_v3485b');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous_unimported_draft=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),two_inherited_representative_field_names_corrected_before_positive_tests=True,producer_sha256=sha(Path(__file__).read_bytes()),all_prior_artifacts_preserved=True,full_goal_complete=False))
