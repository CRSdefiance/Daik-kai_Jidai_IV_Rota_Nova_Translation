"""Exact registered V2143 reference view with normalized dependency path keys."""
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/square_contextual_editorial_release_v1.json'

def current_entries(common,arm):
 conf=read(CONFIG);assert sha(common)==conf['target_COMMON_sha256']and sha(arm)==conf['target_ARM9_sha256']
 path=conf['payload_plan'];normal=lambda s:str(s).replace('\\','/');dependencies={normal(p):v for p,v in conf['dependencies'].items()}
 assert sha(Path(path).read_bytes())==dependencies[normal(path)]
 return owned_entries(common,arm,read(path)['directory_sha256'])
