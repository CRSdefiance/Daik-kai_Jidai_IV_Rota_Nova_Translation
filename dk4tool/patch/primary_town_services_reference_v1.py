"""Exact registered V2097 COMMON reference view; no arbitrary-directory bypass."""
from pathlib import Path
from dk4tool.patch.duel_editorial import owned_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read
CONFIG='translations/primary_town_services_editorial_release_v1.json'

def current_entries(common,arm):
 conf=read(CONFIG);assert sha(common)==conf['target_COMMON_sha256']and sha(arm)==conf['target_ARM9_sha256']
 path=conf['payload_plan'];assert sha(Path(path).read_bytes())==conf['dependencies'][path]
 return owned_entries(common,arm,read(path)['directory_sha256'])
