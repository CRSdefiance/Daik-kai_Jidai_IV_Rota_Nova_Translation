"""Fresh five static selectors including00; reuse exact full actor catalog."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    old=Path('scripts/reconcile_lil_B122_B127_voices_v3264.py');new=Path('scripts/reconcile_lil_B131_B133_voices_v3307b.py');assert not new.exists();t=old.read_text(encoding='utf-8')
    changes={
      'lil_B122_B127_voices_v3264':'lil_B131_B133_voices_v3307b',
      'work/analysis/lil_B122_B127_source_v3260c/complete159_clean_current_native_context.json':'work/analysis/lil_remaining_B131_B140_source_v3306b/next63_B131_B133_clean_current_context.json',
      'chosen==[2,6,9,20,26,92,95,151]':'chosen==[0,2,5,9,20]',
      '::eight_names':'::five_names',
      'current_eight_static_names_voices_and207_catalog_rebind.json':'current_five_static_names_voices_selector00_and207_catalog_rebind.json',
      'fresh_eight_actor_names=fresh':'fresh_five_actor_names=fresh',
      'source_97_is_static_retainer151_not_dynamic_D0_fallback=True':'source00_is_static_actor0_not_empty_text_or_dynamic_role=True',
      "'Eight current static names/voices andselector resolutions pass;207catalog rebound byexact runtime/data. No rolefixtures ornewnameplates.'":"'Five current static names/voices,including source00,pass;207catalog rebound byexact runtime/data. No rolefixtures ornewnameplates.'"}
    for a,b in changes.items():assert a in t,a;t=t.replace(a,b)
    compile(t,str(new),'exec');new.write_text(t,encoding='utf-8')
    root=Path('work/analysis/lil_B131_B133_voice_tools_v3307');root.mkdir(parents=True);save(root/'five_selector_successor_provenance.json',dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes()),source00_body_retained_and_static_identity_not_assumed_from_empty_C_string=True,no_previous_producer_or_ROM_modified=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
