"""Bind the explicit143->silent42->144 dependency chain and correct context wording."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_entry_v3576')
PRIOR=Path('work/analysis/lil_B142_B145_entry_v3575/source_EV2_B142_B145_action_dependency_and_native_getter_binding.json')
SOURCE=Path('work/analysis/lil_B142_B145_source_v3571/all38_clean_current_complete_context.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=deepcopy(read(PRIOR));source=read(SOURCE);events=proof['all_original_source_events'];assert events[42]['must_be_completed']==[143] and events[42]['script_block']==42 and events[144]['must_be_completed']==[42] and events[142]['must_be_completed']==[141] and events[141]['must_be_completed']==[140]
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(source['current_ROM']);a,b=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[42] for im in [clean,current]];assert a==b==bytes.fromhex('435300010400000000000000')
    ids={r['event_ID'] for r in proof['selected_source_event_and_dependency_native_getters']['rows']};assert {42,141,142,143,144,145}<=ids and proof['selected_source_event_and_dependency_native_getters']['all4MiB_actor_roster_event_RNG_and_original_ABI_exact']
    old='historical_snapshot_is_Lil_opening_not_current_B142_B145_eligibility';assert proof.pop(old) is True
    proof.update(previous_entry_proof=str(PRIOR),previous_entry_proof_sha256=sha(PRIOR.read_bytes()),historical_snapshot_is_Lil_London_not_current_B142_B145_eligibility=True,historical_snapshot=source['actual_historical_snapshot'],historical_snapshot_sha256=source['actual_historical_snapshot_sha256'],context_label_correction='Inherited opening label corrected to the actual immutable London snapshot;native getters and all6 cases are reused unchanged.',source_armor_dependency_chain=[143,42,144],silent_intermediate_SC2_B42=dict(source_hex=a.hex(),current_hex=b.hex(),source_sha256=sha(a),current_sha256=sha(b),only_original0000_terminator_no_player_prose=True),no_duration_or_complete_eligibility_inferred_from_unexecuted_event_payload=True,no_prose_or_older_technical_reaudit_credit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    ROOT.mkdir(parents=True);save(ROOT/'four_scene_entries_and_original_silent_armor_dependency.json',proof);print('Source armor chain143->silent42->144 bound by six existing native getters;London context label corrected;no time/eligibility claim.')
