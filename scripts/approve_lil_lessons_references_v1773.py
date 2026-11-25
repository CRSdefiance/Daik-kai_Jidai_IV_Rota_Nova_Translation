"""Approve exact shipped B120/B23 entries and all nested relocation operands."""
import struct
from pathlib import Path
from ndspy.code import MainCodeFile, loadOverlayTable
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_lessons_v1717 import inventory
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/lil_lessons_reference_approval_v1773')
OUT=Path('translations/lil_lessons_editorial_relocation_map_v1.json')
RESEARCH=Path('work/analysis/lil_lessons_relocation_v1760/nested_source_relocation_research.json')
SOURCE=Path('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
LOADER=Path('work/analysis/lil_lessons_loader_v1762/whole_SC2_and_lesson_initial_entry_proof.json')
FONT=Path('work/analysis/lil_Deck_label_approval_v1758/all60_current_native_font_reconciliation.json')
ACTUAL=[
 Path('work/analysis/lil_revised_wind_v1744/actual_revised_wind_branch_proof.json'),
 Path('work/analysis/lil_crew_scene_v1763_final/complete_B23_scene_and_fixture_audit.json'),
 Path('work/analysis/lil_crew_decline_v1767_decline/complete_B23_scene_and_fixture_audit.json'),
 Path('work/analysis/lil_sailing_choice0_audit_v1772/complete_B120_choice0_scene_audit.json')]

def census(image):
    arm=image.read_file('/__arm9__.bin')
    units=[('section'+str(n),s.ramAddress,bytes(s.data)) for n,s in enumerate(MainCodeFile(arm,0x02000000).sections)]
    units += [('overlay'+str(n),s.ramAddress,bytes(s.data)) for n,s in loadOverlayTable(image.rom.arm9OverlayTable,lambda _,f:image.rom.files[f]).items()]
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
    return {'branches':branches,'literal_aliases':pointers,'units':[{'name':n,'base':b,'bytes':len(d),'sha256':sha(d)}for n,b,d in units]}

if __name__=='__main__':
    assert not ROOT.exists() and not OUT.exists()
    research,packet,loader=map(read,(RESEARCH,SOURCE,LOADER))
    assert research['all60_texts_four_choice_labels_and36_relative_operands_preserved']
    assert research['all180_relocated_native_skip_cases_match_original_target_mapping']
    assert loader['all336_whole_blocks_and672_modes_each_pass']
    assert loader['original_EV2_actions_select_by_block_index_without_interior_byte_offset']
    assert loader['original_parent_both_modes_start_at_loaded_payload_plus8']
    assert all(v['whole_SC2_loads_and_cache_hits']==336 and v['original_parent_modes']==672 for v in loader['versions'])
    for v in loader['versions']:
        for k in ('load','parent'):assert sha(Path(v[k+'_proof']).read_bytes())==v[k+'_sha256']
    clean,current=NdsImage.open('work/clean.nds'),NdsImage.open(research['candidate'])
    assert sha(Path(research['candidate']).read_bytes())==research['candidate_sha256']==packet['current_ROM_sha256']
    assert sha(Path('work/clean.nds').read_bytes())==packet['source_ROM_sha256']
    arm=current.read_file('/__arm9__.bin');assert sha(arm)==packet['ARM9_sha256']
    current_blocks=IlnkContainer.parse(current.read_file('/data/SC2.DK4')).blocks
    clean_blocks=IlnkContainer.parse(clean.read_file('/data/SC2.DK4')).blocks
    entry_census={label:census(im) for label,im in [('clean',clean),('current',current)]}
    fonts={r['id']:r for r in read(FONT)['cases']}
    actual=read(ACTUAL[0]);assert actual['all6_revised_FE_panels_actual_full_ink_matches_prior_composition_contract']
    observed={r['id'] for r in actual['all22_executed_speeches44_holds_complete_native_independent_actual_pixels']}
    actual_rows={p.as_posix():read(p) for p in ACTUAL}
    for p in ACTUAL[1:]:
        d=read(p)
        assert d['all_readonly_callbacks_zero_errors_mismatches_host_restored']
        observed.update(r['id'] for r in d['speeches'])
    assert len(observed)==55
    equivalent={
        'DK4_MES_B120_R0062':'DK4_MES_B120_R0186',
        'DK4_MES_B120_R0080':'DK4_MES_B120_R0186',
        'DK4_MES_B120_R0109':'DK4_MES_B120_R0186',
        'DK4_MES_B23_R0091':'DK4_MES_B120_R0155',
        'DK4_MES_B23_R0095':'DK4_MES_B120_R0163'}
    assert set(fonts)-observed==set(equivalent)
    equivalences=[]
    for ident,activated in equivalent.items():
        a,b=fonts[ident],fonts[activated]
        assert activated in observed and a['encoded_hex']==b['encoded_hex'] and a['consumer']==b['consumer']
        assert a['whole_native_and_independent_font_plane_exact'] and a['complete_printable_glyph_order_unique_cells_and_bounds_verified']
        equivalences.append({'id':ident,'actual_identical_text_sample':activated,'encoded_hex':a['encoded_hex'],
            'same_complete_encoded_text_speaker_and_native_consumer':True,'individually_activated':False})
    blocks=[]
    for proposed in research['blocks']:
        number=proposed['block'];source=current_blocks[number];japanese=clean_blocks[number]
        target=Path(proposed['research_block']).read_bytes()
        assert sha(source)==proposed['source_block_sha256'] and sha(target)==proposed['research_block_sha256']
        spec=next(b for b in packet['blocks'] if b['block']==number)
        assert sha(japanese)==spec['source_block_sha256']
        fresh_source,_=inventory(clean.read_file('/__arm9__.bin'),japanese)
        current_commands,_=inventory(arm,source);target_commands,_=inventory(arm,target)
        assert fresh_source==spec['all_nested_native_commands']
        assert len(fresh_source)==len(current_commands)==len(target_commands)==(69 if number==120 else 55)
        patches=sorted([{'start':r['old_offset'],'end':r['old_offset']+r['old_length'],'delta':r['new_length']-r['old_length']}
            for r in proposed['text_records']+proposed['choice_commands']],key=lambda p:p['start'])
        def mapped(at):
            delta=0
            for p in patches:
                if at<p['start']:break
                assert not p['start']<at<p['end']
                if at==p['start']:return at+delta
                delta+=p['delta']
            return at+delta
        by_offset={r['offset']:r for r in target_commands};mapped_commands=[]
        for old in current_commands:
            new=by_offset[mapped(old['offset'])]
            assert old['word']==new['word'] and new['ancestor_0100_offsets']==[mapped(a)for a in old['ancestor_0100_offsets']]
            if old['word'] not in (0x100,0x200,0x300,0x2100,0x4000):
                assert old['whole_command_hex']==new['whole_command_hex']
            mapped_commands.append({'old_offset':old['offset'],'new_offset':new['offset'],'word':old['word'],
                'old_native_extent':old['native_extent'],'new_native_extent':new['native_extent'],
                'original_0100_ancestors':old['ancestor_0100_offsets'],'relocated_0100_ancestors':new['ancestor_0100_offsets']})
        assert proposed['inverse_restoration_recovers_every_original_logical_byte']
        assert len(proposed['target_native_skip_cases'])==5*len(proposed['relative_skip_fixups'])
        blocks.append({k:v for k,v in proposed.items() if k!='external_entry_and_actual_revised_paths_approval_pending'}|{
            'target_block_sha256':proposed['research_block_sha256'],'entry_point_offset':8,
            'external_references_complete':True,'original_nested_commands':fresh_source,'mapped_native_commands':mapped_commands,
            'complete_nested_native_inventory_reexecuted_on_clean_current_and_target':True})
    assert sum(len(b['mapped_native_commands'])for b in blocks)==124
    ROOT.mkdir(parents=True)
    visual={'new_default_choice0_all14_panels_both_sheets_menu_and_terminal_actually_viewed':True,
        'all_native_texts_complete_readable_and_left_aligned_with_preserved_speaker_nameplates':True,
        'prior_wind_and_both_crew_actual_review_retained_from_V1768':True,
        'individual_actual_speech_count':55,'unvisited_conditional_records':equivalences,
        'failed_V1772_and_V1772b_only_mistaken_FE_count_expectations_no_game_defect_or_partial_output':True,
        'corrected_successor':'scripts/verify_lil_sailing_choice0_v1772c.py',
        'evidence':{str(p):sha(p.read_bytes())for p in ACTUAL},'full_goal_complete':False}
    save(ROOT/'visual_and_coverage_review.json',visual)
    mapping={'format':'dk4-lil-lessons-source-relocation-map-v1','file_path':'/data/SC2.DK4',
        'source_SC2_sha256':sha(current.read_file('/data/SC2.DK4')),'required_runtime_ARM9_sha256':sha(arm),
        'blocks':blocks,'external_references_complete':True,'entry_point_offset':8,'preserve_record_parity':True,
        'parity_mismatch_policy':'append-single-space','native_interpreter_entry_census':entry_census,
        'all124_nested_command_boundaries_and36_relative_sites_verified':True,
        'all180_relocated_relative_skip_cases_preserve_original_targets':True,
        'individual_actual_speech_count':55,'unvisited_conditional_records':equivalences,
        'source_entry_contract':[
            'All336 shipped EV2 kind2 actions supply only the block index;both original parent modes initialize PC at complete loaded payload+8.',
            'Clean and current code sections/overlays each contain only the original24070 direct interpreter call and no2A510 pointer literal alias.',
            'The original240EC-240FC parent advances PC only by the native decoded extent;type2 updates the prior result,type3 preserves it,type0 exits.',
            'All124 nested commands are independently re-inventoried through the original parser on clean/current/target;opaque effects are bridged in this structural test,not claimed as gameplay.',
            'All36 relative span operands are typed0100/0200/0300 fields atcommand+2,targetingcommand+4+span;180 target native cases cover prior0,1,2,3,FFFFFFFF.',
            'Both2100 label objects retain originalopcode/count/two u16relativeoffset semantics and native choice coverage;only reviewed strings/offsets change.',
            'All opaque conditions/effects/portrait commands remain exact. Speech headers,speaker bytes,original macros and record parity are preserved.',
            'Actual coldboot covers both B120 responses andboth B23 responses,55 individual speech IDs andnormal type0returns. Crew tests disclose one16-byte coordinate-only fixture.',
            'Five unvisited conditional IDs have individually approved native planes andexact encoded/speaker/consumer equivalents among activated IDs;they receive no individual actual-visit claim.'],
        'evidence':{str(p):sha(p.read_bytes())for p in [RESEARCH,SOURCE,LOADER,FONT,*ACTUAL,ROOT/'visual_and_coverage_review.json']},
        'scope':'Exact shipped-source SC2B120/B23 and exact bound runtime. Structural native walks bridge opaque effects;not arbitrary streams,whole-route gameplay,hardware verification,registered integration or full editorial completion.',
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(OUT,mapping)
    save(ROOT/'reference_approval_receipt.json',{'reference_map':str(OUT),'sha256':sha(OUT.read_bytes()),
        'all124_nested_commands36_relative_sites_four_choice_labels_and_entry_contract_verified':True,
        '55_individual_actual_speeches_five_explicit_native_equivalences':True,'registered_release_pending':True,'full_goal_complete':False})
    print({'reference_map':str(OUT),'native_commands':124,'relative_operands':36,'individual_actual_speeches':55,'unvisited_native_equivalents':5},flush=True)
