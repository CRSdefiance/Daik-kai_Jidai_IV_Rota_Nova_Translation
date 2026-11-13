"""Additional independent exact-byte and count gates for the B180 checkpoint."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read

def audit_relocation(entry):
    from scripts.prepare_lil_B180_checkpoint_v4806 import EVIDENCE
    for p in EVIDENCE:assert entry['evidence'][str(Path(p))]==sha(Path(p).read_bytes())
    plan,stored,_,_,receipt,loader,refs,ends,controls=map(read,EVIDENCE)
    parent,research=map(NdsImage.open,[receipt['parent'],receipt['research_ROM']])
    assert sha(Path(receipt['parent']).read_bytes())==receipt['parent_sha256']==plan['candidate_sha256']
    assert sha(Path(receipt['research_ROM']).read_bytes())==receipt['research_ROM_sha256']
    assert [p for _,p,v in parent.iter_files() if research.read_file(p)!=v]==['/data/SC2.DK4']
    assert all(research.read_file(p)==v for p,v in parent.iter_components())
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,research]]
    assert len(old)==len(new)==336 and [i for i,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[180]
    spec=plan['blocks'][0]
    assert sha(old[180])==spec['source_block_sha256'] and sha(new[180])==spec['research_block_sha256']
    assert len(old[180])==576 and len(new[180])==548 and int.from_bytes(new[180][4:6],'little')+8==546
    assert spec['inverse_restoration_recovers_every_original_logical_byte'] and len(spec['command_map'])==28
    assert len(spec['relative_skip_fixups'])==10 and len(spec['target_native_skip_cases'])==50
    assert stored['current_final_stored_macro_alignment_cases']==44 and stored['all11_final_targets_complete_native_planes_equal_reviewed_planes']
    assert loader['fresh_current_whole_SC2_loads']==loader['fresh_research_whole_SC2_loads']==336
    assert loader['fresh_parent_modes']==1344 and loader['exact_parent_reused_modes']==0
    assert ends['all2_declared_end_decodes_return_type0_extent4_without_post_payload_read']
    assert len(controls['relocated_dispatch_cases'])==11 and len(controls['all7_exact_nonrelative_leaves'])==7
    assert len(controls['predicate_pairs'])==2 and len(controls['C200_pairs'])==1 and len(controls['A000_structural_pairs'])==3
    assert len(controls['all25_source_and_relocated_structural_paths_identical'])==25
    assert controls['new_emulator_runs']==controls['new_review_credit']==0
    pins=read('translations/rom_retention_pins.json')
    assert sum(Path(p['path']).resolve()==Path(receipt['research_ROM']).resolve() for p in pins)==1
    assert entry['approved_uncredited_objects']==11 and entry['new_ROMs']==1 and entry['new_emulator_runs']==0
    assert not entry['full_goal_complete']
