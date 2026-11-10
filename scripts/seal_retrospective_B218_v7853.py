"""Seal exact source/current/native/actual references for a zero-credit formatting revisit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.retrospective_SC2_reconstruction_v2 import reconstruct
from scripts.retrospective_B218_final_paths_v7853 import *
from scripts.verify_village_wrap_v608 import read,save
if __name__=='__main__':
    assert not MAP.exists() and not SEALED.exists() and not SEAL.parent.exists()
    p=proofs();data={k:read(v) for k,v in p.items()};doc=read(APPROVED)
    assert data['approval']['manuscript_sha256']==sha(APPROVED.read_bytes()) and data['approval']['all13_individual_five_gates_approved']
    assert len(doc['records'])==13 and all(all(r['review'].values()) for r in doc['records'])
    assert data['policy']['positive_count']==13 and data['policy']['negative_count']==221
    assert data['loader']['all336_native_loads_cache_hits_and672_modes_pass']
    assert data['caller']['only_original24070_interpreter_call_andno_literal_alias']
    assert data['actual_view']['all_eight_sheets_directly_viewed']
    original=data['source_context'];assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==original['candidate_sha256']
    parent,reference,clean=[NdsImage.open(x) for x in [PARENT,ROM,'work/clean.nds']]
    old,new,jp=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [parent,reference,clean]]
    group=deepcopy(original['groups'][0])
    assert reconstruct(old[218],jp[218],group,original['current_packet'],doc['records'],[])==new[218]
    assert [i for i,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[218]
    inverse=list(new);inverse[218]=old[218];assert IlnkContainer(inverse).to_bytes()==parent.read_file('/data/SC2.DK4')
    assert [f for _,f,v in parent.iter_files() if reference.read_file(f)!=v]==['/data/SC2.DK4']
    assert all(reference.read_file(f)==v for f,v in parent.iter_components())
    group.update(route=2,route_identity='Lil',external_references_complete=True,original_entry_payload_offset=8,
        approved_manuscript=str(APPROVED),approved_manuscript_sha256=sha(APPROVED.read_bytes()),
        source_header_hex=old[218][:8].hex())
    evidence={str(x):sha(Path(x).read_bytes()) for x in [APPROVED,*p.values(),
        'dk4tool/patch/retrospective_SC2_reconstruction_v2.py',__file__]}
    save(MAP,dict(format='dk4-B218-retrospective-source-relocation-map-v1',source_ROM=str(PARENT),source_ROM_sha256=sha(PARENT.read_bytes()),
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),file_path='/data/SC2.DK4',
        source_archive_sha256=sha(parent.read_file('/data/SC2.DK4')),target_archive_sha256=sha(reference.read_file('/data/SC2.DK4')),
        groups=[group],current_packet=deepcopy(original['current_packet']),proofs=p,
        observed_comparison_contract=measured_summary(data['actual']),**{k:True for k in FLAGS},
        evidence=evidence,new_credit=0,full_goal_complete=False))
    doc.update(native_approved_manuscript=str(APPROVED),native_approved_manuscript_sha256=sha(APPROVED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),reference_approval=str(SEAL),
        reference_research_ROM=str(ROM),reference_research_ROM_sha256=sha(ROM.read_bytes()),
        source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),
        current_ARM9_sha256=sha(parent.read_file('/__arm9__.bin')),current_COMMON_sha256=sha(parent.read_file('/COMMON/MESFILE.DK4')),
        proof_paths=p,proof_hashes={k:sha(Path(v).read_bytes()) for k,v in p.items()},
        status='13 retained wordings/one automatic wrap;exact references sealed;atomic registered integration pending')
    save(SEALED,doc);SEAL.parent.mkdir(parents=True)
    save(SEAL,dict(manuscript=str(SEALED),manuscript_sha256=sha(SEALED.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),all13_individual_gates_andexact_references_sealed=True,
        one_automatic_wrap_only_all13_words_retained=True,all15_commands_andboth_inverses_preserved=True,
        measured_comparison_contract=measured_summary(data['actual']),evidence=evidence,new_credit=0,full_goal_complete=False))
    print('B218 retrospective exact13 records/one wrap sealed;all335 other blocks/files/components exact.Atomic registered production pending;zero credit.')
