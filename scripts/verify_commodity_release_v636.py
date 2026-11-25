"""Repeat every actual-screen and release check for source-correct V636."""

from pathlib import Path

from dk4tool.patch.commodity_fidelity import CHANGES_V2
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_commodity_release_v635 as verify
from scripts.verify_village_wrap_v608 import read, save

if __name__ == '__main__':
    verify.ROOT = Path('work/analysis/commodity_fidelity_v636')
    verify.CONFIG = Path('translations/commodity_fidelity_v2.json')
    verify.ROM = Path('out/all_routes_combined_v636_candidate.nds')
    verify.PROFILE = 'all-routes-unified-v636'
    verify.RUN_PREFIX = 'commodity_fidelity_v636'
    verify.CHANGES = CHANGES_V2
    verify.main()
    proof_path = verify.ROOT / 'release_proof.json'
    proof = read(proof_path)
    parent_digest = sha(Path('out/all_routes_combined_v633_candidate.nds').read_bytes())
    _, source, source_shots, source_receipt = verify.report('commodity_fidelity_v636_startup_633', 19700, parent_digest)
    _, current, current_shots, current_receipt = verify.report('commodity_fidelity_v636_startup_636', 19700, proof['candidate_sha256'])
    assert source['scripted_input_schedule'] == current['scripted_input_schedule']
    assert source_shots.keys() == current_shots.keys() and len(current_shots) == 17
    assert 'battery_save_preloaded' not in current
    for frame in source_shots:
        assert verify.Image.open(source_shots[frame]['path']).tobytes() == verify.Image.open(current_shots[frame]['path']).tobytes()
    proof['all17_explicit_title_New_Game_captain_opening_story_frames_exact_V633'] = sorted(current_shots)
    proof['reports'].extend([source_receipt, current_receipt])
    proof['verification_wrapper'] = str(Path(__file__))
    proof['verification_wrapper_sha256'] = sha(Path(__file__).read_bytes())
    proof['source_terminology_decision'] = str(verify.ROOT / 'terminology_decision.json')
    proof['rejected_V635_Palm_Oil_not_reused'] = True
    save(proof_path, proof)
