"""Pure registered scene integration with independently qualified typed choices."""
from pathlib import Path
from dk4tool.dialogue.reviewed_two_choice_object_v1 import compile_choices
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('dk4tool/patch/reviewed_scene_batch_v2.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    'from dk4tool.script.reviewed_scene_rebuild import rebuild_block':
        'from dk4tool.script.reviewed_scene_rebuild_v2 import rebuild_block',
    "'dk4-reviewed-scene-release-v2'":"'dk4-reviewed-scene-release-v3'",
    "    require(len(compiled) == len(approved['records']) and not layout['failures'], 'unique complete plans')":
    """    speech_rows=[r for r in approved['records'] if r['kind'] in ('progressive','system-FE')]
    typed_rows=[r for r in approved['records'] if r['kind']=='typed-choice-label']
    require(len(speech_rows)==conf['speech_count']==approved['physical_speech_objects'], 'complete speech membership')
    require(len(typed_rows)==conf['typed_choice_count']==approved['typed_choice_objects']==2, 'both typed source captions')
    require(len(compiled)==len(speech_rows) and not layout['failures'], 'unique complete speech plans')
    menu=load(conf['typed_menu']);pixels=load(conf['focused_pixels'])
    require(menu['offline_visual_approved'] and not menu['direct_view_pending'] and menu['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass'], 'typed complete native display')
    require(menu['native_provider_alignments']==6 and menu['bridged_modal_returns']==18 and menu['complete_English_caption_style_planes']==8, 'typed provider and style coverage')
    require(len(pixels['menu_samples'])==7 and len(pixels['name_headers'])==7 and len(pixels['rejection_pages'])==2, 'focused actual glyph comparisons')
    for case in pixels['menu_samples']:
        require(len(case['labels'])==2 and all(c['complete_caption_glyphs_andblank_guards_exact'] and c['background_andhighlight_exact'] for c in case['labels']), 'complete actual typed captions')
    require({c['visible_selected_option'] for c in pixels['menu_samples']} >= {0,1}, 'both actual ordinary controller highlights')
    require(len(native['typed_objects'])==1 and native['typed_labels_checked']==2, 'stored menu binding')
    first=typed_rows[0]
    typed=compile_choices(bytes.fromhex(first['source_choice_object_hex']),bytes.fromhex(first['current_choice_object_hex']),typed_rows)
    require(typed.hex()==menu['native_choice_object_hex']==native['typed_objects'][0]['object_hex'], 'exact stored native choice object')""",
    "    for row in approved['records']:\n        plan = compiled[row['id']]":
        "    for row in speech_rows:\n        plan = compiled[row['id']]",
    "visual['final_pages'] == conf['native_pages']":"visual['pages'] == conf['native_pages']",
    "actual['representative_progressive_FE_pagination_andscene_transition_observed']":
        "actual['representative_progressive_pagination_menu_name_andscene_transition_observed']",
    "    path = approved['file_path']":
    """    require(actual['FE_new_batch_bodies_not_observed_in_gameplay'] and actual['FE_distinct_behavior_reference'], 'honest FE behavior reuse')
    fe_reference=Path(actual['FE_distinct_behavior_reference'])
    require(sha(fe_reference.read_bytes())==actual['FE_distinct_behavior_reference_sha256'] and load(fe_reference)['representative_progressive_FE_pagination_andscene_transition_observed'], 'bound completed FE gameplay precedent')
    path = approved['file_path']""",
    "        rows = [r for r in approved['records'] if r['block'] == number]\n        target, proof = rebuild_block(image.read_file('/__arm9__.bin'), clean_blocks[number],\n                                      blocks[number], rows, compiled, inventory)":
    """        rows = [r for r in speech_rows if r['block'] == number]
        choices=[]
        for obj in group['typed_objects']:
            bound=[r for r in typed_rows if r['block']==number]
            require(len(bound)==len(obj['records'])==2, 'whole original menu membership')
            for row,old in zip(bound,obj['records'],strict=True):
                for key in ['id','source_index','english','source_reference','current_reference','source_hex','current_hex','source_choice_object_hex','current_choice_object_hex']:
                    require(row[key]==old[key], 'final choice source/prose binding:'+key)
            require(compile_choices(bytes.fromhex(obj['source_hex']),bytes.fromhex(obj['current_hex']),bound).hex()==obj['compiled_hex'], 'fresh reviewed typed compilation')
            choices.append(dict(id=obj['id'],offset=obj['old_offset'],current_hex=obj['current_hex'],source_hex=obj['source_hex'],compiled_hex=obj['compiled_hex'],records=obj['records']))
        target, proof = rebuild_block(image.read_file('/__arm9__.bin'), clean_blocks[number],
                                      blocks[number], rows, compiled, inventory,choices)""",
    "        blocks[number] = target\n        for row in proof['text_records']:":
    """        blocks[number] = target
        for obj in proof['typed_objects']:
            for row in obj['records']:
                changes.append(dict(id=row['id'],file_path=path,block=number,source_index=row['source_index'],old_command_offset=obj['old_offset'],new_command_offset=obj['new_offset'],typed_choice=True,stored_object_sha256=sha(bytes.fromhex(obj['compiled_hex']))))
        for row in proof['text_records']:""",
})
exec(compile(source,__file__+'::pure-speech-and-native-menu-integration','exec'),globals())
