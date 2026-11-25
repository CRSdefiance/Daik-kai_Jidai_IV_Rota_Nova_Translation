"""Stored mixed scenes: ordinary parity checks plus exact native menu/style proofs."""
import struct
from pathlib import Path
from dk4tool.dialogue.reviewed_actor_style_object_v1 import unpack
from dk4tool.dialogue.reviewed_choice_object_v2 import labels
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load
from scripts import check_editorial_stored_batch_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

def compound_storage(group,block,menu,styles,compiled):
    typed=[];speech=[];page_count=0
    commands={c['offset']:c for c in group['all_target_commands']}
    for item in group.get('native_objects',[]):
        raw=bytes.fromhex(item['compiled_hex']);at=item['new_offset'];command=commands[at]
        assert block[at:at+len(raw)]==raw and command['word']==item['word'] and command['native_extent']==len(raw)
        if item['word'] in [0x2100,0x2200]:
            proof=next(p for p in menu['menus'] if p['block']==group['block'] and p['source_command_offset']==item['old_offset'])
            assert raw.hex()==proof['target_object_hex']
            count=len(labels(raw));assert item['count']==count and item['source_index_order']==list(range(count))
            offsets=struct.unpack_from('<'+str(count)+'H',raw,2);base=2+2*count;refs=[]
            for index,row in enumerate(item['records']):
                assert row['source_index']==index
                value=labels(raw)[index];relative=base+offsets[index];where=at+relative
                assert value==row['english'].encode('ascii') and block[where:where+len(value)+1]==value+b'\0'
                refs.append(dict(id=row['id'],source_index=index,offset=where,length=len(value),stored_hex=value.hex(),record_index=block[:where].count(b'\0')))
            typed.append(dict(block=group['block'],offset=at,object_hex=raw.hex(),word=item['word'],source_index_order=list(range(count)),
                labels=[r['english'] for r in item['records']],label_references=refs,exact_native_provider_andcomplete_planes_reused_from=proof,
                no_new_native_provider_run_for_identical_stored_object=True))
        else:
            assert item['word']==0x4100 and item['count']==8
            proof=next(p for p in styles['objects'] if p['block']==group['block'] and p['source_command_offset']==item['old_offset'])
            assert raw.hex()==proof['target_object_hex']
            offsets,bodies=unpack(raw)
            assert offsets==proof['target_alias_offsets'] and raw[18:20]==bytes.fromhex(proof['source_object_hex'])[18:20]
            for row in item['records']:
                selected=row['source_style_indices'];relative=20+offsets[selected[0]];body=bodies[offsets[selected[0]]]
                assert all(offsets[i]==offsets[selected[0]] for i in selected)
                old=compiled[row['id']];value=bytes.fromhex(old['compiled_hex'])
                assert value[0]==row['source_selector']==raw[19] and value[1:]==body
                assert body.hex()==old['expanded_native_hex'] and block[at+relative:at+relative+len(body)+1]==body+b'\0'
                planes=old['complete_native_English_display']['pages']
                for page in planes:assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                page_count+=len(planes)
                speech.append(dict(id=row['id'],block=group['block'],new_offset=at+relative,new_record_index=block[:at+relative].count(b'\0'),
                    stored_hex=body.hex(),compiled_virtual_prefix_hex=value.hex(),source_style_indices=selected,source_header_hex=row['source_header_hex'],
                    final_header_hex=raw[:20].hex(),final_command_offset=at,virtual_prefix_not_stored=True,
                    complete_stored_native_display=dict(exact_compiled_body_font_runtime_and64_slot_getter_proof_reuse=True),
                    all_stored_planes_equal_directly_viewed_compiled_planes=True,
                    directly_viewed_planes=[dict(path=p['native_plane'],sha256=p['native_plane_sha256']) for p in planes]))
    return typed,speech,page_count

old_loop="""        for choice in group.get('typed_objects',[]):
            raw=bytes.fromhex(choice['compiled_hex']);at=choice['new_offset']
            assert block[at:at+len(raw)]==raw and raw.hex()==menu['native_choice_object_hex']
            command=next(c for c in group['all_target_commands'] if c['offset']==at)
            assert command['word']==0x2100 and command['native_extent']==len(raw)
            assert choice['source_index_order']==[0,1] and choice['count']==2
            typed.append(dict(block=group['block'],offset=at,object_hex=raw.hex(),
                source_index_order=[0,1],labels=[r['english'] for r in choice['records']],
                exact_native_provider_andcomplete_planes_reused_from=rebuilt['menu'],
                no_new_native_provider_run_for_identical_stored_object=True))"""
source=checked_text(previous.source,{
    '    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[]':
        "    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[]\n    styles_path=Path(rebuilt['styles']);assert sha(styles_path.read_bytes())==rebuilt['styles_sha256']\n    styles=load(styles_path);assert styles['runtime']==runtime and styles['manuscript_sha256']==rebuilt['manuscript_sha256']",
    old_loop:
        "        more_typed,more_styles,style_pages=compound_storage(group,block,menu,styles,compiled)\n        typed.extend(more_typed);style_records.extend(more_styles);reused_pages+=style_pages",
    "    assert len(relatives)==rebuilt['relative_sites']":
        "    assert len(relatives)==rebuilt['relative_sites']\n    assert len(style_records)==rebuilt['style_physical_speech_count']==48\n    assert len(rows)+len(style_records)==rebuilt['total_rendered_speech_count']==308\n    assert sum(len(t['labels']) for t in typed)==rebuilt['typed_choice_count']==15",
    '        records=rows,typed_objects=typed,':
        '        records=rows,style_records=style_records,style_proof=rebuilt[\'styles\'],style_proof_sha256=rebuilt[\'styles_sha256\'],typed_objects=typed,',
})
exec(compile(source,__file__+'::stored-ordinary-parity-and-native-compound-proof-reuse','exec'),globals())
