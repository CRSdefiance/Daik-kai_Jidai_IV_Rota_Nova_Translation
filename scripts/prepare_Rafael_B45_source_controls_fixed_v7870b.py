"""Use the existing five-argument seeded-end adapter;preserve the failed four-argument call."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    root=Path('work/analysis/Rafael_B45_source_controls_repair_v7870b');assert not root.exists()
    old="    ends=[end_case(arm,block,758,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]"
    new="""    end_proof=Path('work/analysis/lil_B218_controls_v6878/two_A000_structural_cases50_normal_seeded_ends_no_relative_or_predicate.json')
    end_adapter=read(end_proof)['source_owned_seeded_end_adapter'];endenv=dict(end_case.__globals__)
    exec(compile(end_adapter,__file__+'::original-five-argument-seeded-end','exec'),endenv)
    ends=[endenv['end_case'](arm,block,758,previous,seed) for previous in [0,1,2,3,0xFFFFFFFF] for seed in [0,1,2,3,0xFFFFFFFF]]"""
    result=derive('scripts/prove_Rafael_B45_source_controls_v7870.py','scripts/prove_Rafael_B45_source_controls_v7870b.py',{
        'work/analysis/Rafael_B45_source_controls_v7870':'work/analysis/Rafael_B45_source_controls_v7870b',
        old:new,
        'source_owned_predicate_probe=inspect.getsource(probe),':'source_owned_predicate_probe=inspect.getsource(probe),source_owned_seeded_end_adapter=end_adapter,seeded_end_precedent=str(end_proof),seeded_end_precedent_sha256=sha(end_proof.read_bytes()),',
    })
    root.mkdir(parents=True);save(root/'provenance.json',dict(derivation=result,
        correction='The imported original end_case accepts four arguments;the existing source-owned seeded adapter accepts previous andseed separately.',
        failed_original_andpartial_context_preserved=True,all_native_high_constants_andguards_unchanged=True,
        no_ROM_gameplay_ornegative_rejection_claim_from_the_TypeError=True,full_goal_complete=False))
