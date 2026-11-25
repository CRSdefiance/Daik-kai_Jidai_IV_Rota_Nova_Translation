"""Compare independent sparse-source reconstruction with the tested complete research image; no ROM write."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.hodram_outcome_references_v1 import reconstruct_and_bind,serializable_groups
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_outcome_independent_rebuild_v8344')
DOC=Path('translations/hodram_B47_B48_editorial_manuscript_v4.json')
PACKET=Path('work/analysis/Hodram_outcome_current_binding_v8343/six_exact_source_current_final_refs_registered_parent_anddisplay_binding.json')
RELOC=Path('work/analysis/Hodram_outcome_relocation_v8326/two_blocks6_speeches15_commands_full_source_parent_inverses.json')
REFERENCE=Path('work/analysis/Hodram_outcome_reference_v8329/research_image_receipt.json')
if __name__=='__main__':
    assert not ROOT.exists();doc,packet,reloc,reference=map(read,[DOC,PACKET,RELOC,REFERENCE]);assert packet['manuscript_sha256']==sha(DOC.read_bytes())
    parent=NdsImage.open(doc['current_ROM']);clean=NdsImage.open('work/clean.nds');referencebytes=Path(reference['research_ROM']).read_bytes()
    assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']==reference['parent_sha256'] and sha(referencebytes)==reference['research_ROM_sha256']
    result=reconstruct_and_bind(parent,clean,doc,reloc,packet);planned=deepcopy(parent);planned.replace_file(doc['file_path'],result['target_archive']);assert bytes(planned.rom.save())==referencebytes
    inverse=deepcopy(planned);inverse.replace_file(doc['file_path'],parent.read_file(doc['file_path']));assert bytes(inverse.rom.save())==Path(doc['current_ROM']).read_bytes()
    assert sum(len(g['all_target_commands']) for g in result['groups'])==15 and sum(len(g['text_records']) for g in result['groups'])==6
    ROOT.mkdir(parents=True);save(ROOT/'six_records15_commands_two_clean_source_inverses_entire_tested_ROM_equal.json',dict(candidate=doc['current_ROM'],candidate_sha256=doc['current_ROM_sha256'],reference_ROM=reference['research_ROM'],reference_ROM_sha256=reference['research_ROM_sha256'],
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),packet=str(PACKET),packet_sha256=sha(PACKET.read_bytes()),groups=serializable_groups(result),
        independent_sparse_source_reconstruction_matches_commandwise_research_archive_andentire_tested_ROM=True,all_full_clean_source_blocks_predecessor_archive_andwhole_ROM_inverses_exact=True,
        only_SC1_blocks47_48_change_all323_others_every_other_file_andcomponent_exact=True,frozen_policy_andindependent_actual_atomic_registered_integration_pending=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,PACKET,RELOC,REFERENCE,Path('dk4tool/patch/hodram_outcome_rebuild_v1.py'),Path('dk4tool/patch/hodram_outcome_references_v1.py'),Path(__file__)]}))
    print('Independent sparse rebuild:6refs/15commands/2clean inverses/323unownedblocks/allparentbytes;entire ROM equals tested reference.No ROMwrite orcredit.')
