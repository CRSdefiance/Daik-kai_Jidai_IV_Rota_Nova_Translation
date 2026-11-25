"""Bind the current registered six-paragraph successor to original actual1911."""
import inspect
from pathlib import Path
from dk4tool.patch import reinforcement_faction_prose as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_reinforcement_gameplay_v1052b as previous
from scripts.native_reinforcement_pact_v1811 import apply_fixture
from scripts.verify_village_wrap_v608 import read

def current_entries(common,arm):
    config=read(owned.CONFIG)
    assert sha(common)==config['target_COMMON_sha256']and sha(arm)==config['required_ARM9_sha256']
    return owned.entries(common,arm,config['directory_sha256'])

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    changes=[('work/analysis/reinforcement_sniping_v1049/terminal_preservation.json','work/analysis/reinforcement_faction_actual_v1812/terminal_preservation.json'),('translations/reinforcement_sniping_editorial_manuscript_v2.json','translations/reinforcement_sniping_editorial_manuscript_v4.json'),("font=read(doc['native_font_proof'])","font={'cases':read(doc['successor_native_format_proof'])['all120_cases']}")]
    for old,new in changes:
        assert source.count(old)==1,(old,source.count(old));source=source.replace(old,new)
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/reinforcement_faction_actual_v1813'),'ROM':Path('out/all_routes_combined_v1807_candidate.nds'),'FOLDER':Path('E:/Rota Nova translations/Generated/work/emulation_v193/reinforcement_faction_actual_v1812_1807'),'apply_fixture':apply_fixture,'current_entries':current_entries}
    exec(compile(source,__file__,'exec'),env);env['main']()
