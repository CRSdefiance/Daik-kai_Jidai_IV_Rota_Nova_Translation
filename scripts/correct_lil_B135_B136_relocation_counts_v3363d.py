"""Correct a generator count collision;preserve failed producer andpartial blocks."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    pairs=[]
    def successor(a,b,changes):
        old,new=Path(a),Path(b);assert not new.exists();t=old.read_text(encoding='utf-8')
        for x,y in changes:
            assert x in t,x;t=t.replace(x,y)
        compile(t,str(new),'exec');new.write_text(t,encoding='utf-8');pairs.append((old,new))
    successor('scripts/research_lil_B135_B136_relocation_v3363b.py','scripts/research_lil_B135_B136_relocation_v3363c.py',[
      ('lil_B135_B136_relocation_v3363b','lil_B135_B136_relocation_v3363c'),("sum(len(r['command_map']) for r in results)==35","sum(len(r['command_map']) for r in results)==61")])
    successor('scripts/prepare_lil_B135_B136_research_v3364.py','scripts/prepare_lil_B135_B136_research_v3364b.py',[
      ('lil_B135_B136_relocation_v3363b','lil_B135_B136_relocation_v3363c'),('lil_B135_B136_research_v3364','lil_B135_B136_research_v3364b')])
    for kind,oldver,newver in [('loader','3365','3365b'),('references','3366','3366b')]:
        old=f'scripts/verify_lil_B135_B136_{kind}_v{oldver}.py';new=f'scripts/verify_lil_B135_B136_{kind}_v{newver}.py'
        changes=[('prepare_lil_B135_B136_research_v3364','prepare_lil_B135_B136_research_v3364b')]
        if kind=='loader':changes.append(('lil_B135_B136_loader_v3365','lil_B135_B136_loader_v3365b'))
        else:changes.extend([('lil_B135_B136_loader_v3365','lil_B135_B136_loader_v3365b'),('lil_B135_B136_reference_census_v3366','lil_B135_B136_reference_census_v3366b')])
        successor(old,new,changes)
    successor('scripts/prove_lil_B135_B136_relocated_controls_v3367.py','scripts/prove_lil_B135_B136_relocated_controls_v3367b.py',[
      ('prepare_lil_B135_B136_research_v3364','prepare_lil_B135_B136_research_v3364b'),('lil_B135_B136_reference_census_v3366','lil_B135_B136_reference_census_v3366b'),('lil_B135_B136_relocated_controls_v3367','lil_B135_B136_relocated_controls_v3367b')])
    root=Path('work/analysis/lil_B135_B136_count_successors_v3363d');root.mkdir(parents=True);save(root/'provenance.json',dict(finding='Overlapping generator substitutions incorrectly changed61commands to35;native inventory is61commands/35speech. No native target check is relaxed.',producers=[dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes())) for a,b in pairs],all_failed_partial_artifacts_preserved=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
