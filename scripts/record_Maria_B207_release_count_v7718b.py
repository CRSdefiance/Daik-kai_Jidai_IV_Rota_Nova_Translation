"""Correct only the console's inherited628 shorthand; preserve the completed629-byte verification."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_release_count_v7718b')
PROOF=Path('work/analysis/maria_B207_release_v7718/registered_release_verification.json')
if __name__=='__main__':
    assert not ROOT.exists();proof=read(PROOF);mp=Path(proof['manifest']);manifest=read(mp)
    assert proof['manifest_batches']==len(manifest['batches'])==629 and proof['all629_manifest_batches_and114_accepted_layers_present']
    assert proof['whole_clean_input_ROM_reconstruction_byte_exact'] and proof['whole_ROM_equals_pinned_approved_reference']
    assert sha(Path(proof['candidate']).read_bytes())==proof['candidate_sha256']==manifest['candidate_sha256']
    ROOT.mkdir(parents=True);save(ROOT/'authoritative629_manifest_count_console628_superseded.json',dict(release_proof=str(PROOF),release_proof_sha256=sha(PROOF.read_bytes()),manifest=str(mp),manifest_sha256=sha(mp.read_bytes()),actual_manifest_batches=629,actual_accepted_layers=114,actual_release_checks=18,actual_regressions=110,historical_verifier_console_batched628_typo_preserved=True,verifier_andall_ROM_patch_proof_bytes_unchanged_no_replay=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print(dict(candidate_sha256=proof['candidate_sha256'],patch_sha256=proof['patch_sha256'],batches=629,accepted=114,checks=18,regressions=110,console628_typo_superseded_without_replay=True))
