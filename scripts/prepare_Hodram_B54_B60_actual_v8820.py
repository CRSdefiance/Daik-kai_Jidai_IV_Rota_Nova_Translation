"""Extend source-locked complete glyph/flow audit to every observed native page."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive,checked_text
from scripts.verify_village_wrap_v608 import save

if __name__=='__main__':
    root=Path('work/analysis/Hodram_B54_B60_actual_tools_v8820');assert not root.exists()
    source=Path('scripts/audit_Hodram_B31_B53_actual_v8742b.py');text=source.read_text(encoding='utf-8')
    start="            record=records[at];actor=record['source_selector'];FE=actor==254;width=228 if FE else 216;model=native[record['id']];assert len(model['pages'])==1;page=model['pages'][0]"
    a=text.index(start);z=text.index('\n        ids=[',a);old=text[a:z];lines=old.splitlines();assert lines[-1].lstrip().startswith('speeches.append(')
    body='\n'.join(lines[1:-1]);body=checked_text(body,{
        'native_page=1':'native_page=page[\'page\']',
        "partial.append(dict(frame=frame,body_differences=":"partial.append(dict(frame=frame,native_page=page['page'],body_differences=",
        "id=record['id'],kind='no-complete-body-and-name-orFE-absent-header-hold'":"id=record['id'],native_page=page['page'],kind='no-complete-body-and-name-orFE-absent-header-hold'",
    }) if False else body
    # The fragment is indented inside a surrounding loop, so qualify exact tokens
    # textually, then compile and compare native constants on the complete source.
    replacements={'native_page=1':"native_page=page['page']",
        'partial.append(dict(frame=frame,body_differences=':"partial.append(dict(frame=frame,native_page=page['page'],body_differences=",
        "id=record['id'],kind='no-complete-body-and-name-orFE-absent-header-hold'":"id=record['id'],native_page=page['page'],kind='no-complete-body-and-name-orFE-absent-header-hold'"}
    for key,value in replacements.items():assert body.count(key)==1;body=body.replace(key,value)
    replacement=start.replace(";assert len(model['pages'])==1;page=model['pages'][0]",'')+'\n'
    replacement+="            allholds=[];allpartial=[];allnameholds=[];page_selections=[]\n            for page in model['pages']:\n"
    replacement+='\n'.join('    '+line for line in body.splitlines())+'\n'
    replacement+="""                allholds.extend(holds);allpartial.extend(partial);allnameholds.extend(nameholds)
                page_selections.append(dict(native_page=page['page'],complete_holds=holds,selected_capture=holds[-1] if holds else None))
            nameholds=list({h['frame']:h for h in allnameholds}.values())
            speeches.append(dict(id=record['id'],source_selector=actor,name=None if FE else n['text'],start=entry['frame'],returned=row['frame'],pages=len(model['pages']),kind='system-FE' if FE else 'progressive',complete_holds=allholds,nameholds=nameholds,partial_ortransition_samples=allpartial,page_selections=page_selections,selected_capture=allholds[-1] if allholds else None))"""
    extra="""    for original_speech in groups[0]['speeches']:
        translated=next((s for s in groups[1]['speeches'] if s['id']==original_speech['id']),None)
        if not translated or translated['pages']<=1 or not original_speech['selected_capture']:continue
        selected_pages=[s for s in translated['page_selections'] if s['selected_capture']]
        if not selected_pages:continue
        sheet=Image.new('RGB',(1024,410*len(selected_pages)),'#263238');draw=ImageDraw.Draw(sheet)
        for index,page in enumerate(selected_pages):
            for column,photo in enumerate([original_speech['selected_capture'],page['selected_capture']]):
                pic=Image.open(photo['capture']).convert('RGB')
                draw.text((column*512+3,index*410+3),original_speech['id']+(' source complete' if column==0 else f' English page{page["native_page"]}')+f' frame{photo["frame"]}',fill='white')
                sheet.paste(pic.resize((512,768),Image.Resampling.NEAREST).crop((0,384,512,768)),(column*512,index*410+24))
        path=root/(original_speech['id']+'_all_English_pages.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),all_selected_English_pages=len(selected_pages)))
"""
    save_anchor="    save(root/'paired_actual_dialogue_headers_flow_returns.json'"
    result=derive(source,'scripts/audit_Hodram_B54_B60_actual_v8820.py',{
        'Hodram_B31_B53_actual_v8742b':'Hodram_B54_B60_actual_v8820',
        'Hodram_B31_B53_fixtures_v8739/four_whole_scripts.json':'Hodram_B54_B60_fixtures_v8815/twelve_whole_scripts.json',
        'Hodram_B31_B53_models_v8741/native_models.json':'Hodram_B54_B60_models_v8817/native_models.json',
        'Hodram_B31_B53_scene_runs_v8740':'Hodram_B54_B60_scene_runs_v8816',
        'choices=[31,53]':'choices=[54,57,58,59,60]',
        '{31:6001,53:6001}':'{54:6001,57:9001,58:16001,59:10001,60:10001}',
        old:replacement,save_anchor:extra+save_anchor,
    })
    root.mkdir(parents=True);save(root/'source_locked_all_native_pages_audit.json',dict(derivation=result,
        all_original_singlepage_masks_andreadonly_residentpayload_flow_inputs_returns_name_guards_preserved=True,
        complete_body_match_required_separately_for_each_native_page=True,missing_page_appends_concrete_unresolved_record=True,
        extra_paired_review_sheet_for_each_multipage_English_record=True,normal_end_resultword_distinct_from_interpreter_mode_preserved=True,
        conditional_rows_are_actual_only_if_observed_not_forced=True,no_new_capture_orcompletion_credit=True,new_credit=0,full_goal_complete=False))
