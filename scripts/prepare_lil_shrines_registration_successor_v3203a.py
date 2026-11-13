"""Correct the D0 negative test's document owner; preserve the failed harness."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
OLD=Path('scripts/register_lil_shrines_v3203.py')
NEW=Path('scripts/register_lil_shrines_v3203b.py')
ROOT=Path('work/analysis/lil_Shrines_Temples_registration_tools_v3203a')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW.exists()
    text=OLD.read_text(encoding='utf-8')
    old="('D0_role_selector_changed',DOC,'manuscript',lambda d:speech(d,'d0').update(english=speech(d,'d0')['english'].replace('SPEAKER:D0','SPEAKER:97')))"
    new="('D0_role_selector_changed',VOICE,'actor_styles',lambda d:d['records'][0].update(english=d['records'][0]['english'].replace('SPEAKER:D0','SPEAKER:CF')))"
    assert text.count(old)==1
    text=text.replace(old,new).replace('lil_Shrines_Temples_registration_v3203','lil_Shrines_Temples_registration_v3203b')
    NEW.write_text(text,encoding='utf-8');ROOT.mkdir(parents=True)
    save(ROOT/'registration_test_owner_successor.json',dict(previous=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        successor=str(NEW),successor_sha256=sha(NEW.read_bytes()),
        reason='D0 is the virtual actor-style prefix in the voice manuscript; no standalone main speech hasD0. Positive235-object reconstruction already passed. The negative harness now changes the actualD0-owned object toCF andretains all44rejection cases.',
        no_production_compiler_or_reviewed_prose_change=True,no_previous_profile_registry_or_ROM_changed=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
