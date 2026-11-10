"""Reconstruct all330 reviewed objects with source-owned FE pagination;grant no actual/release credit."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.script.reviewed_scene_rebuild_v3 import rebuild_block
from dk4tool.script.reviewed_FE_pagination_v1 import insert_FE_continuations
from dk4tool.dialogue.reviewed_choice_object_v2 import compile_choices
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory

ROOT=Path('work/analysis/Rafael_B81_B84_rebuilt_20261105')
PARENT=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Rafael_B81_B84_current_20261105/current_effective.json')
FORMAT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
CHILD=Path('work/analysis/Rafael_B84_FE_pagination_20261105')
CHOICES=Path('work/analysis/Rafael_B84_choices_20261105')

def main():
    assert not ROOT.exists()
    doc=deepcopy(load(PARENT));packet=load(CURRENT);native=load(FORMAT/'combined_native_v5.json')
    layout=load(FORMAT/'automatic_subset_v5/automatic_plans.json')
    childdoc,childplans,childnative=[load(CHILD/p) for p in ['child_page_manuscript_v1.json','automatic_v1/automatic_plans.json','native_v1/compiled_native_pages.json']]
    two,three=[load(CHOICES/p/'menu_provider_and_planes.json') for p in ['two_choice_native_v1','three_choice_native_v1']]
    assert native['runtime']==packet['runtime']==childnative['runtime']==two['runtime']==three['runtime']
    assert native['all323_subset_body_layouts_approved'] and native['pages']==332 and not native['direct_visual_review_pending']
    assert childnative['pages']==4 and childnative['fresh_compiled_alignments']==16
    assert childnative['all_first_internal_final_glyph_codes_pixels_input_canaries_andbounds_pass'] and childnative['complete_consumption_andpagination_exact']
    assert two['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'] and three['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']
    assert two['native_provider_alignments']==three['native_provider_alignments']==6
    assert len(two['compiler_negatives_rejected'])==7 and len(three['compiler_negatives_rejected'][0]['rejected'])==8
    assert len(childnative['review_sheets'])==1 and len(three['review_sheets'])==1
    for sheet in [*childnative['review_sheets'],two['review_sheet'],*three['review_sheets']]:
        assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    plan={r['id']:deepcopy(r) for r in layout['records']};owners={o['source_ID']:o for o in childdoc['pagination_owners']}
    bychild={r['id']:r for r in childplans['records']}
    for ident,owner in owners.items():
        p=deepcopy(bychild[owner['child_IDs'][0]])
        p.update(id=ident,logical_English=owner['unchanged_logical_English'],expected_native_pages=2,
            native_FE_child_pages=[bychild[k] for k in owner['child_IDs']],
            encoded_hex_is_first_native_panel_only=True,complete_paragraph_owned_by_two_native_FE_commands=True)
        plan[ident]=p
    choices=[]
    for filename in ['B84_C3114_manuscript.json','B84_C5298_manuscript.json']:
        choices.extend(load(CHOICES/filename)['records'])
    assert len(plan)==325 and len(choices)==5
    bychoice={r['id']:r for r in choices}
    for i,r in enumerate(doc['records']):
        if r['kind']=='typed-choice-label':doc['records'][i]=deepcopy(bychoice[r['id']]);continue
        r['source_record_index']=r['source_reference']['record_index'];r['current_record_index']=r['current_reference']['record_index']
        if r['id'] in owners:r['formatter_owned_FE_pagination']=owners[r['id']]
    doc.update(all330_prose_unchanged=True,all_fifth_gates_false_until_stored_actual_andrelease=True,
        physical_native_speech_commands_after_pagination=327,source_editorial_speeches=325,
        original_speech_command_controls_preserved_plus_two_exact_FE_repeats=True,
        parent_manuscript=str(PARENT),parent_manuscript_sha256=sha(PARENT.read_bytes()))
    image=NdsImage.open(doc['current_ROM']);assert sha(Path(doc['current_ROM']).read_bytes())==doc['current_ROM_sha256']
    archive=image.read_file(doc['file_path']);assert sha(archive)==doc['current_archive_sha256']==packet['current_archive_sha256']
    arm=image.read_file('/__arm9__.bin');assert sha(arm)==native['runtime']['ARM9_sha256']
    container=IlnkContainer.parse(archive);blocks=list(container.blocks);inventory,_,_=scoped_inventory()
    ROOT.mkdir();save(ROOT/'formatting_bound_manuscript_v2.json',doc)
    save(ROOT/'complete_two_source_FE_page_plan.json',dict(records=list(plan.values()),
        source_editorial_speeches=325,target_native_speech_commands=327,complete_display_pages=336,
        two_FE_encoded_hex_fields_represent_first_panel_only_children_preserved_separately=True,
        no_source_prose_orcredit_added=True,new_credit=0))
    groups=[];negatives=[]
    for group in packet['groups']:
        block=group['block'];current=blocks[block];clean=bytes.fromhex(group['clean_block_hex'])
        assert current.hex()==group['current_block_hex'] and sha(clean)==group['clean_block_sha256']
        assert inventory(arm,current)[0]==group['all_current_commands'] and inventory(arm,clean)[0]==group['all_source_commands']
        rows=[r for r in doc['records'] if r['block']==block and r['kind']!='typed-choice-label'];compound=[]
        if block==84:
            for offset,proof in [(3114,two),(5298,three)]:
                items=[r for r in choices if r['source_command_offset']==offset]
                source,prior=map(bytes.fromhex,[items[0]['source_choice_object_hex'],items[0]['current_choice_object_hex']])
                value=compile_choices(source,prior,items,require_formatting=False)
                proved=proof['native_choice_object_hex'] if offset==3114 else proof['menus'][0]['target_object_hex']
                assert value.hex()==proved
                compound.append(dict(id=f'B84_C{offset}_menu',word=0x2100 if offset==3114 else 0x2200,
                    offset=items[0]['current_reference']['command_offset'],source_hex=source.hex(),current_hex=prior.hex(),compiled_hex=value.hex(),records=items))
        intermediate,firstproof=rebuild_block(arm,clean,current,rows,plan,inventory,compound)
        final=intermediate;pageproof=None
        if block==84:
            pagination=[]
            for ident,owner in owners.items():
                first=next(r for r in firstproof['text_records'] if r['id']==ident)
                pages=[dict(native_child_page=i+1,logical_English=bychild[k]['logical_English'],encoded_hex=bychild[k]['encoded_hex']) for i,k in enumerate(owner['child_IDs'])]
                pagination.append(dict(source_ID=ident,first_command_offset=first['new_offset']-5,
                    first_stored_hex=first['stored_hex'],complete_source_preamble_hex=owner['complete_source_preamble_hex'],
                    continuation_encoded_hex=pages[1]['encoded_hex'],pages=pages,unchanged_logical_English=owner['unchanged_logical_English']))
            final,pageproof=insert_FE_continuations(arm,intermediate,pagination,inventory)
            (ROOT/'B84_first_FE_pages_INTERMEDIATE_NOT_PLAYABLE.bin').write_bytes(intermediate)
            for kind in ['wrong-speaker','wrong-first-offset','changed-first-page','changed-child-prose','omitted-closing-sentence','wrong-child-index','changed-child-control']:
                attempt=deepcopy(pagination)
                if kind=='wrong-speaker':attempt[0]['complete_source_preamble_hex']='0040ffff0000'
                elif kind=='wrong-first-offset':attempt[0]['first_command_offset']+=2
                elif kind=='changed-first-page':attempt[0]['first_stored_hex']='fe41'
                elif kind=='changed-child-prose':attempt[0]['pages'][1]['logical_English']+=' changed'
                elif kind=='omitted-closing-sentence':attempt[0]['unchanged_logical_English']=attempt[0]['pages'][0]['logical_English']
                elif kind=='wrong-child-index':attempt[0]['pages'][1]['native_child_page']=3
                else:attempt[0]['continuation_encoded_hex']='00'+attempt[0]['continuation_encoded_hex'][2:]
                try:insert_FE_continuations(arm,intermediate,attempt,inventory)
                except (AssertionError,ValueError):negatives.append(kind)
                else:raise AssertionError('Pagination accepted '+kind)
            assert len(negatives)==7
        blocks[block]=final;path=ROOT/f'B{block}_RESEARCH_ONLY.bin';path.write_bytes(final)
        groups.append(dict(block=block,target_block=str(path),target_sha256=sha(final),current_sha256=sha(current),clean_sha256=sha(clean),
            first_page_reconstruction=firstproof,FE_pagination=pageproof,
            all_target_commands=inventory(arm,final)[0],final_speech_commands=len(inventory(arm,final)[1]),
            current_bytes=len(current),target_bytes=len(final),new_logical_end=8+int.from_bytes(final[4:6],'little')))
    resource=IlnkContainer(blocks).to_bytes();assert [i for i,(a,b) in enumerate(zip(container.blocks,blocks,strict=True)) if a!=b]==doc['blocks']
    inverse=list(blocks)
    for b in doc['blocks']:inverse[b]=container.blocks[b]
    assert IlnkContainer(inverse).to_bytes()==archive
    research=deepcopy(image);research.replace_file(doc['file_path'],resource)
    assert [p for _,p,v in image.iter_files() if research.read_file(p)!=v]==[doc['file_path']]
    assert all(research.read_file(p)==v for p,v in image.iter_components())
    rom=ROOT/'reviewed_FE_paginated_RESEARCH_ONLY.nds';research.save(rom)
    reopened=NdsImage.open(rom);assert reopened.read_file(doc['file_path'])==resource
    reopened.replace_file(doc['file_path'],archive);assert bytes(reopened.rom.save())==Path(doc['current_ROM']).read_bytes()
    path=ROOT/'reviewed_RESEARCH_ONLY.DK4';path.write_bytes(resource)
    save(ROOT/'reconstruction.json',dict(parent=doc['current_ROM'],parent_sha256=doc['current_ROM_sha256'],
        manuscript=str(ROOT/'formatting_bound_manuscript_v2.json'),manuscript_sha256=sha((ROOT/'formatting_bound_manuscript_v2.json').read_bytes()),
        source_manuscript=str(PARENT),source_manuscript_sha256=sha(PARENT.read_bytes()),
        source_archive_sha256=sha(archive),target_archive=str(path),target_archive_sha256=sha(resource),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        groups=groups,changed_blocks=doc['blocks'],source_editorial_objects=330,source_speeches=325,native_speech_commands=327,
        complete_native_display_pages=336,typed_choice_labels=5,typed_choice_objects=2,
        all_original_scene_controls_scopes_complete_FE_preambles_andclean_current_inverses_bound=True,
        seven_FE_pagination_invalid_cases_rejected=negatives,only_SC0_changed_all_other_files_components_fonts_graphics_andruntime_exact=True,
        reviewed_prose_unchanged_no_new_editorial_credit=True,stored_native_actual_controller_andregistered_release_pending=True,
        not_registered_candidate_or_natural_activation=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [PARENT,CURRENT,FORMAT/'combined_native_v5.json',
            CHILD/'native_v1/compiled_native_pages.json',CHOICES/'two_choice_native_v1/menu_provider_and_planes.json',
            CHOICES/'three_choice_native_v1/menu_provider_and_planes.json',Path('dk4tool/script/reviewed_FE_pagination_v1.py'),Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve complete Rafael330 research reconstruction with source-owned FE pagination. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before);pending=pins.with_name('rom_retention_pins.Rafael330_research.pending.json');assert not pending.exists();save(pending,values)
    assert pins.read_bytes()==before;os.replace(pending,pins)
    print('Reconstructed330 source objects/327 native speeches/336 pages plusfive native captions;allfour whole blocks andseven FE rejects pass. Stored/actual/release pending.')

if __name__=='__main__':main()
