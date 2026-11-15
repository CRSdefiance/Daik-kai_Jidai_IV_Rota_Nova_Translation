"""Preserve a failed inherited actor-list assertion and bind the seven B138 actors."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/lil_B138_final_storage_scope_repair_v3442b');assert not root.exists();pairs=[]
    for old,new,changes in [
        ('scripts/prepare_lil_B138_research_v3442.py','scripts/prepare_lil_B138_research_v3442b.py',[('lil_B138_research_v3442','lil_B138_research_v3442b'),('[2,9,14,16,17,20,22,23,38,92,198]','[2,14,20,21,22,23,92]')]),
        ('scripts/verify_lil_B138_loader_v3443.py','scripts/verify_lil_B138_loader_v3443b.py',[('lil_B138_loader_v3443','lil_B138_loader_v3443b'),('lil_B138_research_v3442','lil_B138_research_v3442b')]),
        ('scripts/verify_lil_B138_references_v3444.py','scripts/verify_lil_B138_references_v3444b.py',[('lil_B138_reference_census_v3444','lil_B138_reference_census_v3444b'),('lil_B138_loader_v3443','lil_B138_loader_v3443b'),('lil_B138_research_v3442','lil_B138_research_v3442b')])]:
        a,b=Path(old),Path(new);assert not b.exists();t=a.read_text(encoding='utf-8')
        for x,y in changes:assert x in t,x;t=t.replace(x,y)
        compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');pairs.append((a,b))
    failed=Path('work/analysis/lil_B138_research_v3442');assert failed.exists() and not (failed/'research_image_receipt.json').exists()
    assert not any(failed.glob('*.nds'));root.mkdir(parents=True)
    save(root/'failure_and_successor_receipt.json',dict(failed_producer='scripts/prepare_lil_B138_research_v3442.py',failed_assertion='Inherited B137 list excluded source-proven static Ian21.',failed_partial_directory=str(failed),failed_artifacts_preserved={str(p):sha(p.read_bytes()) for p in failed.rglob('*') if p.is_file()},failed_research_ROM_created=False,source_seven_actor_list=[2,14,20,21,22,23,92],successors=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],no_source_ROM_or_editorial_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
