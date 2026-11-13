"""Correct a sample-name label after inspecting actual historical duel captures."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
OLD=Path('work/analysis/static_duel_history_v2505b/historical_static_duel_current_binding.json');ROOT=Path('work/analysis/static_duel_history_v2505c')
if __name__=='__main__':
 assert not ROOT.exists();doc=deepcopy(read(OLD));key='original_actor_IDs_1_32_and_conditional_Clifford_name_unchanged';assert doc.pop(key)is True;challenge=[r for r in doc['historical_holds']if r['message_id']==1932];assert len(challenge)==2;names={bytes.fromhex(r['original_name_hex']).decode('cp932')for r in challenge};assert names=={'Centurione'};assert all('Centurione'in r['expanded_text']and'Clifford'not in r['expanded_text']for r in challenge);assert all(r['source_actor_IDs']==[1,32]for r in doc['historical_holds'])
 doc.update(original_actor_IDs_1_32_and_source_selected_name_unchanged=True,actual_historical_challenge_name='Centurione',metadata_correction='The native holds and RGB proof always used source-selected Centurione. A descriptive field incorrectly said Clifford,which belongs only to the independent CPU layout samples. Correct the label without altering text,ROM,captures or verified masks.',prior_verification_proof=str(OLD),prior_verification_proof_sha256=sha(OLD.read_bytes()),all_native_pixel_scope_and_transition_evidence_unchanged=True,producer_sha256=sha(Path(__file__).read_bytes()))
 ROOT.mkdir(parents=True);save(ROOT/'historical_static_duel_current_binding.json',doc);print('Historical challenge name metadata corrected to source-selected Centurione;all glyph and transition evidence preserved.')
