"""Derive only the generic native loader/caller validator for the two outcome blocks."""
import inspect
from pathlib import Path
from dk4tool.patch import hodram_three_blocks_controls_v1 as old
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_outcome_loader_tools_v8352');target=Path('dk4tool/patch/hodram_outcomes_loaders_v1.py');assert not root.exists() and not target.exists()
    source=inspect.getsource(old.check_loaders_and_census)
    body=checked_text(source,{"data['native_loader'],data['native_caller']":"data['loaders'],data['callers']","len(caller['groups'])==3":"len(caller['groups'])==2"})
    prefix='''"""Independent original SC1 loaders, cache, parent modes and caller census for B47/B48."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.approve_lil_lessons_references_v1773 import census
PATH='/data/SC1.DK4'
'''
    target.write_text(prefix+body,encoding='utf8');compile(target.read_text('utf8'),str(target),'exec')
    root.mkdir(parents=True);save(root/'two_outcome_loader_validator_source_derivation.json',dict(source=str(Path(old.__file__)),source_sha256=sha(Path(old.__file__).read_bytes()),original_function_sha256=sha(source.encode()),target=str(target),target_sha256=sha(target.read_bytes()),only_proof_keys_andtwo_group_count_changed=True,all_native_high_constants_preserved=True,new_credit=0,full_goal_complete=False))
