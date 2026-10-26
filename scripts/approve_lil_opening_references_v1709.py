"""Source-bound B22 entry and complete90-command relocation contract."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile,loadOverlayTable
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_opening_references_v1709')
OUT=Path('translations/lil_opening_editorial_relocation_map_v1.json')


if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    scene_path=Path('work/analysis/lil_opening_scene_v1708/complete_B22_actual_scene_proof.json');scene=read(scene_path)
    loader_path=Path('work/analysis/lil_opening_loader_v1705/loader_and_initial_entry_proof.json');loader=read(loader_path)
    research_path=Path('work/analysis/lil_opening_relocation_v1701/parity_and_native_command_research.json');research=read(research_path)
    assert scene['all90_original_command_entry_return_pairs_and_entire3292_byte_resident_source_verified']
    assert scene['all49_revised_dialogues_individually_activated_with98_complete_pixel_exact_holds']
    assert scene['all89_nonterminal_results_type3_and_final_result_type0']
    assert loader['both_original_modes_start_instruction_pointer_at_loaded_payload_plus8']
    assert loader['all_other_SC2_blocks_load_byte_exact_despite_updated_outer_offsets']
    assert all(v['whole_SC2_loads_and_cache_hits']==336 and v['original_parent_mode_cases']==672 for v in loader['versions'])
    clean=NdsImage.open('work/clean.nds');arm=clean.read_file('/__arm9__.bin')
    units=[('section'+str(n),s.ramAddress,bytes(s.data)) for n,s in enumerate(MainCodeFile(arm,0x02000000).sections)]
    units += [('overlay'+str(n),s.ramAddress,bytes(s.data)) for n,s in loadOverlayTable(clean.rom.arm9OverlayTable,lambda _,f:clean.rom.files[f]).items()]
    branches=[];pointers=[]
    for name,base,data in units:
        for at in range(0,len(data)-3,4):
            word=struct.unpack_from('<I',data,at)[0];relative=word&0xFFFFFF
            if relative&(1<<23):relative-=1<<24
            if word&0x0E000000==0x0A000000 and base+at+8+relative*4==0x0202A510:
                branches.append({'unit':name,'address':base+at,'word':word})
        off=0
        while (off:=data.find(struct.pack('<I',0x0202A510),off))>=0:
            pointers.append({'unit':name,'address':base+off});off+=1
    assert [r['address'] for r in branches]==[0x02024070] and not pointers
    ROOT.mkdir(parents=True)
    visual={'all5_actual_sheets49_panels_actually_viewed':True,
        'source_speakers_native_nameplates_full_letters_left_origins_and_pagination_acceptable':True,
        'all_reviewed_body_texts_remain_exact_to_native_approved_manuscript_v2':True,
        'normal_scene_end_crew_joins_and_Amsterdam_control_observed':True,
        'following_Bruges_scene_and_whole_run_terminal_audit_still_pending':True,
        'source_actual_proof':str(scene_path),'source_actual_proof_sha256':sha(scene_path.read_bytes()),
        'sheets':scene['actual_review_sheets'],'full_goal_complete':False}
    save(ROOT/'actual_visual_review.json',visual)
    mapping={'format':'dk4-lil-opening-source-relocation-map-v1','file_path':'/data/SC2.DK4','block':22,
        'source_block_sha256':research['current_source_block_sha256'],'target_block_sha256':research['research_block_sha256'],
        'source_block_bytes':3000,'target_block_bytes':3292,'entry_point_offset':8,'external_references_complete':True,
        'preserve_record_parity':True,'parity_mismatch_policy':'append-single-space','records':research['mapped_texts'],
        'original_90_commands':research['native_90_command_extents'],'native_interpreter_static_entry_census':branches,
        'unclassified_function_pointer_literals_to_interpreter':pointers,
        'evidence':{str(p):sha(p.read_bytes()) for p in (scene_path,loader_path,research_path)},
        'source_entry_contract':['All shipped EV2 kind2 actions supply only the SC block index;no interior byte-offset argument is supplied.',
            'Original24134 loader returns the complete selected ILNK block;original23F4C parent modes0/1 initialize SEventScript PC to payload+8.',
            'All336 current/research blocks and672 parent modes each execute the original source loader/parent with complete payload,cache and tail guards.',
            'The sole statically referenced original interpreter entry is24070 in the proven parent loop;no direct function-pointer literal alias is present in original sections/overlays.',
            'Every one of this blocks90 commands is exercised in original native playback,with complete source bytes verified at both entry and return.',
            'All89 nonterminal returns are type3;original240EC-240FC advances PC by the returned decoded length. Final type0 exits normally. No branch/mode-change/choice entry occurs in B22.',
            'Every41 non-dialogue command remains byte-identical. All49 message headers,speakers,original macros and byte parity remain exact. Only owned speech bodies and CS length change.',
            'The independently observed actual90-command sequence matches the proposed new offsets/extents exactly and reaches normal town control after all three original crew joins.'],
        'scope':'Exact shipped-source B22 original EV/cache/interpreter entry and complete straight-through opening. Does not claim other blocks can be resized,or exclude arbitrary injected/generated streams.',
        'required_runtime_ARM9_sha256':scene['ARM9_sha256'],'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(OUT,mapping)
    save(ROOT/'reference_approval_receipt.json',{'reference_map':str(OUT),'sha256':sha(OUT.read_bytes()),
        'source_bound_B22_external_entry_and_all90_command_paths_verified':True,
        'native_control_flow_and_actual_pointer_sequence_are_independent_of_host_relocation_writer':True,
        'no_prose_completion_or_registered_release_claim':True,'full_goal_complete':False})
    print('B22 relocation map approved from complete original entry/loader and90 actual command returns;all49 actual panels visually reviewed. Other blocks remain outside this map.')
