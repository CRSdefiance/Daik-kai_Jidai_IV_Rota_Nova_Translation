"""All13 prior direct speech pipelines through the new191-codec dispatch gate."""
import inspect
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_battle_aftermath_escape_v1262 as previous

if __name__=='__main__':
    source=inspect.getsource(previous.main)
    old='work/analysis/battle_aftermath_payload_v1259/native_payload_plan.json'
    assert source.count(old)==1;source=source.replace(old,'work/analysis/search_reports_payload_v1666/native_payload_plan.json')
    raw=Path('E:/Rota Nova translations/Generated/work/emulation_v193/hot_spring_crew_v1651_1637/frame_026531_arm9_ram.bin')
    old="context = read('work/analysis/battle_aftermath_context_v1248d/source_context_and_consumer_frames.json')"
    assert source.count(old)==1;source=source.replace(old,'context = '+repr({'snapshot':str(raw),'snapshot_sha256':sha(raw.read_bytes())}))
    env={**previous.__dict__,'__file__':__file__,'ROOT':Path('work/analysis/search_reports_escape_v1669')}
    exec(compile(source,__file__,'exec'),env);env['main']()
