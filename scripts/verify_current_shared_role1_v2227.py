"""Current First Mate label/room/speech-fallback proof; no historical file edits."""
import inspect
from pathlib import Path
from scripts import review_shared_speaker_context_v782 as original
from scripts.verify_village_wrap_v608 import save
from dk4tool.patch.grand_race_menu_release import sha

ROOT=Path('work/analysis/shared_role1_v2227')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    program=inspect.getsource(original.main)
    program=program[:program.index('    doc = deepcopy(read(V2))')]
    for old,new in(('out/all_routes_combined_v782_candidate.nds','out/all_routes_combined_v2171_candidate.nds'),('shared_v782_recruit_live/capture_report.json','recruitment_actual_v2202_V2171/capture_report.json'),("'metadata_only_registered_replay_still_required': True","'metadata_only_registered_replay_still_required': False")):
        assert old in program
        program=program.replace(old,new)
    env={**original.__dict__,'ROOT':ROOT,'__file__':__file__}
    exec(compile(program,__file__,'exec'),env);env['main']()
    save(ROOT/'current_role1_replay_provenance.json',dict(original=str(Path(original.__file__)),original_sha256=sha(Path(original.__file__).read_bytes()),effective_source_sha256=sha(program.encode()),current_label_room_strict_assignment_and_native_fallback_verified=True,no_old_manuscript_or_proof_modified=True,no_new_English_or_ROM_changes=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
