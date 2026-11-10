"""Independently reconstruct both owned changes and seal source/current/final references without integration credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.gerhard_surname_rebuild_v1 import rebuild
from dk4tool.dialogue.gerhard_surname_profile_v1 import contract,validate_approved_batch,validate_runtime,validate_name_transition,profile_for
from dk4tool.dialogue.gerhard_surname_layout_v1 import encode_relocatable_dialogue
from scripts.Gerhard_surname_release_paths_v8238 import PARENT,ROM,DRAFT,APPROVED,MAP,SEAL,FLAGS,proofs
from scripts.verify_village_wrap_v608 import read,save
ROOT=SEAL.parent
if __name__=='__main__':
    assert not ROOT.exists() and not APPROVED.exists() and not MAP.exists()
    doc=read(DRAFT);c=validate_approved_batch(doc);data={k:read(p) for k,p in proofs().items()}
    parent,target=NdsImage.open(PARENT),NdsImage.open(ROM)
    assert sha(PARENT.read_bytes())==c['parent_ROM_sha256'] and sha(ROM.read_bytes())==c['target_ROM_sha256']
    validate_runtime(parent);validate_runtime(target,'target')
    policy=data['policy_validation'];assert len(policy['positive_body_records'])==5 and policy['negative_count']==260 and policy['all_rejections_match_expected_semantic_guard']
    assert sha(Path(policy['negative_cases']).read_bytes())==policy['negative_cases_sha256']
    expected=read(proofs()['source_relocation']);archive=parent.read_file(doc['file_path']);arm=parent.read_file('/__arm9__.bin')
    result=rebuild(archive,arm,doc['records']);assert result['target_archive']==target.read_file(doc['file_path'])
    rows=deepcopy(doc['records']);groups=[]
    for g in result['groups']:
        old=next(x for x in expected['groups'] if x['block']==g['block'])
        for field in ['source_block_sha256','target_block_sha256','source_bytes','source_logical_end','source_tail_bytes','target_bytes','target_logical_end','target_tail_bytes','command_map','all_target_commands']:
            assert g[field]==old[field],(g['block'],field)
        assert g['target_block']==Path(old['target_block']).read_bytes()
        for x,y in zip(g['relative_fixups'],old['relative_fixups'],strict=True):assert all(x[k]==y[k] for k in x)
        for x in g['text_records']:
            y=next(v for v in old['text_records'] if v['id']==x['id']);assert all(x[k]==y[k] for k in x)
            r=next(r for r in rows if r['id']==x['id']);p=profile_for(arm,parent.read_file('/__arm9__.bin') if False else bytes.fromhex(next(s for s in data['source_context']['groups'] if s['block']==g['block'])['current_block_hex']),r['id'],r['file_path'],'progressive')
            encoded=encode_relocatable_dialogue(bytes.fromhex(r['source_hex']),r['planned_English_markup'],p);assert encoded.encoded.hex()==x['compiled_hex']==r['compiled_hex']
            assert r['final_stored_hex']==x['target_hex'] and r['final_reference']['offset']==x['new_offset']
            r['integrated_reference_pending']=dict(file_path=r['file_path'],block=g['block'],offset=x['new_offset'],bytes=x['new_length'],header_offset=x['new_offset']-5,
                record_index=x['new_record_index'],target_block_sha256=g['target_block_sha256'])
        group={k:deepcopy(v) for k,v in g.items() if k not in ['target_block','all_current_commands']};groups.append(group)
    name=doc['name_records'][0];at=name['offset'];newarm=bytearray(arm);newarm[at:at+name['bytes']]=bytes.fromhex(name['target_hex'])
    assert bytes(newarm)==target.read_file('/__arm9__.bin');name_validation=validate_name_transition(arm,bytes(newarm))
    planned=deepcopy(parent);planned.replace_file('/__arm9__.bin',bytes(newarm));planned.replace_file(doc['file_path'],result['target_archive'])
    assert bytes(planned.rom.save())==ROM.read_bytes()
    restored=deepcopy(planned);restored.replace_file('/__arm9__.bin',arm);restored.replace_file(doc['file_path'],archive);assert bytes(restored.rom.save())==PARENT.read_bytes()
    assert [p for _,p,v in parent.iter_files() if target.read_file(p)!=v]==['/data/SC2.DK4']
    assert [p for p,v in parent.iter_components() if target.read_file(p)!=v]==['/__arm9__.bin']
    proofpaths=proofs();digests={p:sha(Path(p).read_bytes()) for p in proofpaths.values()}
    frozen_actual=dict(complete_body_holds=30,relevant_name_holds=262,initial_runs=6,repeat_runs=2,total_scene_frames=int('176008'),
        selected_wholeB27_speeches=35,wholeB27_unvisited=16,wholeB27_normal_return_frames=[12415,12415],wholeB27_later_final_captains=[0,0],
        selected_wholeB74_speeches=75,wholeB74_unvisited=4,wholeB74_normal_return_frames=[22255,22255],wholeB74_actual_choice_option=0,
        intro_display_speeches=8,intro_outercondition_unexecuted=True,intro_normal_return_frames=[5695,5694],
        scene_portrait_pairs=117,duration_difference_counts=[0,19,2],command_difference_counts=[1,74,8],later_RGB_counts=[328,164,106],later_RGB_difference_counts=[0,0,29],
        all_selected_results_UI_andmemberships_equal=True,first7_focused_RAM_components_equal=True,
        final_phase_changed_bytes=dict(fleet=2,all207_actors_and_current_captain=150,all90_towns=54),
        raw_final_phase_calendars=[dict(ticks=535,original_zero_based_date=[0,11,7]),dict(ticks=534,original_zero_based_date=[0,11,6])],
        all_exact_replay_rows_exceptpaths_selected_framebuffers_andfinalRAM_equal_perversion=True,
        no_normal_Lilcontinuity_claim_from_fullB27_tail=True,no_full_original_B27_effects_claim_from_intro_display=True,
        no_broad_simulation_futureoutcome_hardware_fullroute_orall_conditional_visit_claim=True)
    mapping=dict(format='dk4-Gerhard-sparse-name-anddialogue-reference-map-v1',file_path=doc['file_path'],parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),source_SC2_sha256=sha(archive),target_SC2_sha256=sha(result['target_archive']),
        source_ARM9_sha256=sha(arm),target_ARM9_sha256=sha(bytes(newarm)),blocks=groups,name_record=deepcopy(name),name_validation=name_validation,
        actual_scope=frozen_actual,proofs=proofpaths,proof_sha256=digests,**{flag:True for flag in FLAGS},
        source_full_clean_TEXT_inverse_not_claimed_for_sparse_revisit=True,not_registered_ornew_parent=True,new_credit=0,full_goal_complete=False)
    approved=deepcopy(doc);approved['records']=rows;approved.update(prior_manuscript=str(DRAFT),prior_manuscript_sha256=sha(DRAFT.read_bytes()),
        approved_reference_map=str(MAP),external_references_complete=True,all_sealed_reference_scope_flags=FLAGS,
        independent_atomic_registered_release_andownstartup_pending=True)
    validate_approved_batch(approved)
    ROOT.mkdir(parents=True);save(MAP,mapping);approved['approved_reference_map_sha256']=sha(MAP.read_bytes());save(APPROVED,approved)
    save(SEAL,dict(manuscript=str(APPROVED),manuscript_sha256=sha(APPROVED.read_bytes()),prior_manuscript=str(DRAFT),prior_manuscript_sha256=sha(DRAFT.read_bytes()),
        reference_map=str(MAP),reference_map_sha256=sha(MAP.read_bytes()),parent_ROM=str(PARENT),parent_ROM_sha256=sha(PARENT.read_bytes()),
        reference_ROM=str(ROM),reference_ROM_sha256=sha(ROM.read_bytes()),independent_reconstruction_byte_equal_reference=True,
        every_predecessor_block_archive_andwholeROM_byte_reconstructed_exactly=True,proofs=proofpaths,proof_sha256=digests,
        flags=FLAGS,actual_scope=frozen_actual,source_native_five_gates_andscoped_actual_bound=True,
        name_asset12_andBlades8_owned_separately_pointer_fields_andallother_bytes_preserved=True,
        original_prose_andindividual_justified_retentions_preserved_except_surname=True,
        production_atomic_semantic_challenges_registered_build_cleanpatch_regressions_startup_pending=True,
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DRAFT,MAP,Path(__file__),Path('dk4tool/patch/gerhard_surname_rebuild_v1.py'),Path('scripts/Gerhard_surname_release_paths_v8238.py')]}))
    print('Independent5speech+12byte name rebuild equalsfullreference;allsource/current/final refs andactual limits sealed. Atomic production/registeredrelease pending;zero credit.')
