"""Bind the pre-existing registered modal alignment call rather than assert it is clean."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

original=Path('scripts/replay_courier_consumer_v2238.py')
source=original.read_text()
for old,new in(("work/analysis/courier_context_v2238'","work/analysis/courier_context_v2238b'"),('(0x546B8,0x5479C)','(0x546B8,0x54798)')):
    assert source.count(old)==1,old
    source=source.replace(old,new)
env={'__name__':'__main__','__file__':__file__}
exec(compile(source,__file__,'exec'),env)
arm=NdsImage.open(env['ROM']).read_file('/__arm9__.bin')
prior=NdsImage.open('out/all_routes_combined_v792_candidate.nds').read_file('/__arm9__.bin')
clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
assert arm[0x54798:0x5479C]==prior[0x54798:0x5479C]==bytes.fromhex('22a0feeb')
assert clean[0x54798:0x5479C]==bytes.fromhex('5dfcffeb')
save(env['ROOT']/'registered_modal_call_scope_correction.json',dict(original_verifier=str(original),original_verifier_sha256=sha(original.read_bytes()),effective_source_sha256=sha(source.encode()),source_clean_call_at0x02054798=clean[0x54798:0x5479C].hex(),registered_current_call_at0x02054798=arm[0x54798:0x5479C].hex(),registered_current_target=0x01FFC828,exact_to_historical_registered_V792=True,current_all3_complete_original_modal_consumers_pass=True,earlier_failed_overbroad_clean_span_assumption_preserved=True,no_ROM_consumer_or_alignment_repair=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
