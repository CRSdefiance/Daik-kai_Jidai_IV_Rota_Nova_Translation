"""Preserve failed3273; correct the proof wrapper/rows distinction."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/prepare_lil_B122_B127_layout_v3273.py')
NEW=Path('scripts/prepare_lil_B122_B127_layout_v3273b.py')
PROFILE=Path('dk4tool/dialogue/lil_B122_B127_profile.py')
NEXT=Path('dk4tool/dialogue/lil_B122_B127_profile_v2.py')
if __name__=='__main__':
    assert not NEW.exists() and not NEXT.exists()
    text=PROFILE.read_text(encoding='utf-8');old="len(voice['fresh_eight_actor_names'])!=8";assert text.count(old)==1
    text=text.replace(old,"len(voice['fresh_eight_actor_names']['rows'])!=8")
    compile(text,str(NEXT),'exec');NEXT.write_text(text,encoding='utf-8')
    text=OLD.read_text(encoding='utf-8')
    start=text.index("    assert not any(p.exists()")
    end=text.index("    image=NdsImage.open",start)
    text=text[:start]+'''    assert not ROOT.exists() and not any(p.exists() for p in OUTPUTS)
    source=read(SOURCE)
    profile_for=importlib.import_module('dk4tool.dialogue.lil_B122_B127_profile_v2').profile_for
    planner=importlib.import_module('dk4tool.dialogue.lil_B122_B127_layout_v1')
'''+text[end:]
    text=text.replace("lil_B122_B127_layout_v3273'","lil_B122_B127_layout_v3273b'").replace("lil_B122_B127_profile.py'","lil_B122_B127_profile_v2.py'")
    compile(text,str(NEW),'exec');NEW.write_text(text,encoding='utf-8')
    save('work/analysis/lil_B122_B127_layout_repair_v3273b/successor_provenance.json',dict(previous={str(p):sha(p.read_bytes()) for p in [OLD,PROFILE]},successors={str(p):sha(p.read_bytes()) for p in [NEW,NEXT]},reason='fresh_eight_actor_names is a five-field proof wrapper with eight rows; require its rows length. No actor,source,prose,ROM or earlier producer modified.',producer_sha256=sha(Path(__file__).read_bytes())))
