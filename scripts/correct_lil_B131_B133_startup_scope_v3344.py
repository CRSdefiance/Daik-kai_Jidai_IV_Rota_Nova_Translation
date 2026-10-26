"""Correct inherited scope metadata without rerunning completed gameplay."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    oldproof=Path('work/analysis/lil_B131_B133_startup_v3341/cold_boot_Lil_startup_town_verification.json')
    proof=oldproof.with_name('current_B131_B133_scoped_startup_verification.json');assert not proof.exists()
    d=deepcopy(read(oldproof));assert d['actual_selected_B122_B127_IDs']==[] and d['paired_frame_count']==31 and d['all_current_requested_and_final_framebuffers_equal_V3300']
    d.update(actual_selected_B131_B133_IDs=[],previous_proof=str(oldproof),previous_proof_sha256=sha(oldproof.read_bytes()),scope_metadata_correction='The inherited B122_B127 empty selection field also remains true;the current batch is B131/B133,and no selected scene from either batch is claimed.',scope_correction_producer_sha256=sha(Path(__file__).read_bytes()))
    save(proof,d)
    pairs=[('scripts/complete_lil_B131_B133_v3342b.py','scripts/complete_lil_B131_B133_v3344b.py'),('scripts/verify_editorial_handoff_v3343b.py','scripts/verify_editorial_handoff_v3344c.py')]
    produced=[]
    for a,b in pairs:
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8');needle='lil_B131_B133_startup_v3341/cold_boot_Lil_startup_town_verification.json';assert needle in t
        t=t.replace(needle,'lil_B131_B133_startup_v3341/current_B131_B133_scoped_startup_verification.json')
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');produced.append(dict(previous=str(old),previous_sha256=sha(old.read_bytes()),successor=str(new),successor_sha256=sha(new.read_bytes())))
    root=Path('work/analysis/lil_B131_B133_scope_successors_v3344');root.mkdir(parents=True);save(root/'provenance.json',dict(proof=str(proof),proof_sha256=sha(proof.read_bytes()),previous_proof=str(oldproof),previous_proof_sha256=sha(oldproof.read_bytes()),producers=produced,no_gameplay_orROM_changes=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
