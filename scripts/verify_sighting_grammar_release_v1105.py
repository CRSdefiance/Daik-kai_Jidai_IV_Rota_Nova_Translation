"""Verify complete combined ancestry,unchanged runtime and exact clean-input patch."""
from pathlib import Path
from dk4tool.patch import sighting_editorial as parent
from dk4tool.patch import sighting_grammar_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta,apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.sighting_layout_v1069 import compiled,IDS
from scripts.sighting_labels_v1083b import FIELDS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/sighting_grammar_release_v1104')
OLD=Path('out/all_routes_combined_v1086_candidate.nds')
ROM=Path('out/all_routes_combined_v1105_candidate.nds')


def main():
    final=ROOT/'registered_release_verification.json';assert not final.exists()
    registry=read('translations/release_stack.json');prior=read(ROOT/'registry_before.json')
    manifest=read(ROM.with_suffix('.manifest.json'));old_manifest=read(OLD.with_suffix('.manifest.json'))
    assert manifest['profile']=='all-routes-unified-v1105'
    assert manifest['base_rom']=='out\\raphael_natural_v2_accepted_base.nds'
    assert manifest['base_sha256']=='3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    assert manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['candidate_sha256']==sha(ROM.read_bytes())
    assert manifest['batches']==old_manifest['batches'] and len(manifest['batches'])==471
    assert manifest['required_batches']==[] and all(manifest['checks'].values()) and len(registry['accepted_layers'])==114
    restored={**registry,'profiles':{k:v for k,v in registry['profiles'].items() if k!='all-routes-unified-v1105'}}
    assert restored==prior
    old,new=map(NdsImage.open,(OLD,ROM))
    changed=[path for _,path,raw in old.iter_files() if new.read_file(path)!=raw]
    assert changed==['/COMMON/MESFILE.DK4']
    for field in ('arm7','arm9OverlayTable','arm7OverlayTable'):assert getattr(old.rom,field)==getattr(new.rom,field)
    common,arm=new.read_file('/COMMON/MESFILE.DK4'),new.read_file('/__arm9__.bin')
    assert common==(ROOT/'target_COMMON.bin').read_bytes() and arm==(ROOT/'target_ARM9.bin').read_bytes()
    config=read(owned.CONFIG);assert sha(common)==config['target_common_sha256'] and sha(arm)==config['target_arm9_sha256']
    before=parent.current_entries(old.read_file('/COMMON/MESFILE.DK4'),old.read_file('/__arm9__.bin'))
    after=owned.current_entries(common,arm);assert len(before)==len(after)==3668
    assert [a.message_id for a,b in zip(before,after,strict=True) if a.text!=b.text]==list(IDS)
    doc=read(config['manuscript']);rows={r['message_id']:r for r in doc['records']}
    plan=read(ROOT/'repack_plan.json');assert plan['repacked_block_range']==[7,7]
    mapped=set(plan['repacked_native_IDs']);moved=[]
    for a,b in zip(before,after,strict=True):
        assert a.message_id==b.message_id
        if (a.block,a.record_index)!=(b.block,b.record_index):
            assert a.message_id in mapped and a.block==b.block==7
            moved.append({'message_ID':a.message_id,'old_block_record':[a.block,a.record_index],
                'new_block_record':[b.block,b.record_index],'text_unchanged':a.text==b.text})
        assert b.text==(compiled(rows[b.message_id]) if b.message_id in rows else a.text)
    assert len([r for r in after if r.message_id not in rows])==3653
    assert all(before[n].text==after[n].text for n in (676,677,*range(1911,1931),*range(1931,1957),*range(1973,1980)))
    assert all(b'\n' not in after[n].text for n in IDS)
    for at,old_label,new_label in FIELDS:assert arm[at:at+len(new_label)]==old.read_file('/__arm9__.bin')[at:at+len(new_label)]==new_label
    restored_arm=bytearray(arm);old_arm=old.read_file('/__arm9__.bin')
    for at,size in plan['metadata_fields']:restored_arm[at:at+size]=old_arm[at:at+size]
    assert bytes(restored_arm)==old_arm
    builder=Path('scripts/build_integrated_release.py').read_bytes();block=(ROOT/'builder_added_optional_stage.bin').read_bytes()
    assert builder.replace(block,b'',1)==(ROOT/'builder_before.py').read_bytes()
    copies=read(ROOT/'native_copy_proof.json')
    assert copies['complete_native_copies']==7336 and len(copies['sequenced_cache_cases'])==178
    assert copies['COMMON_sha256']==sha(common) and copies['ARM9_sha256']==sha(arm)
    assert plan['all_sections_BSS_cache_arenas_and_entire123040_staged_payload_unchanged']
    save(ROOT/'physical_record_relocation_verification.json',{'all3668_stable_source_IDs_preserved':True,
        'physical_movements_inside_exact_block7_repack':moved,'all3653_unselected_strings_and_opaque_payloads_exact':True})
    patch,result,clean=ROM.with_suffix('.xdelta'),ROOT/'patch_reconstruction_RESEARCH_ONLY.nds',Path('work/clean.nds')
    assert not patch.exists() and not result.exists()
    clean_sha=sha(clean.read_bytes());assert clean_sha=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    make_xdelta(clean,ROM,patch);apply_xdelta(clean,patch,result)
    assert result.read_bytes()==ROM.read_bytes() and sha(clean.read_bytes())==clean_sha
    save(final,{'candidate':str(ROM),'candidate_sha256':manifest['candidate_sha256'],
        'canonical_base':manifest['base_rom'],'canonical_sha256':manifest['base_sha256'],'profile':manifest['profile'],
        'manifest':str(ROM.with_suffix('.manifest.json')),'manifest_sha256':sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'all471_batches114_accepted_layers_and_final_guards_pass':True,
        'only_COMMON7_and_native_message_metadata_changed_from_V1086':True,
        'all3653_unselected_message_strings_including_user676_677_and_inherited_event_prose_exact':True,
        'all_graphics_routes_fonts_other_ROM_files_ARM7_and_overlays_exact':True,
        'entire_renderer_selector_previous_runtime_and_all_native_name_labels_exact':True,
        'all15_one_paragraphs_source_exact_no_LF_before_macro_expansion':True,
        'COMMON_sha256':sha(common),'ARM9_sha256':sha(arm),'patch':str(patch),'patch_sha256':sha(patch.read_bytes()),
        'clean_input_sha256':clean_sha,'exact_clean_input_patch_reconstruction':str(result),
        'whole_reconstruction_sha256':sha(result.read_bytes()),'complete_reconstruction_byte_exact':True,
        'all7336_native_copies178_cache_sequences_and_owned_footprints_pass':True,
        'prior_builder_restores_by_removing_exact_optional_block':True,
        'new_startup_and_actual_changed_wording_geometry_dismissal_and_returns_pending':True,
        'inherited_close_incoming_name_and_admiral_shot_scenes_still_pending':True,
        'no_new_completed_editorial_credit':True,'canonical_not_promoted':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('V1105 complete combined ancestry and exact patch pass;only15 paragraphs/native metadata changed. Runtime and labels exact;actual checks pending.',flush=True)
    print('ROM SHA256',manifest['candidate_sha256']);print('Patch SHA256',sha(patch.read_bytes()))


if __name__=='__main__':main()
