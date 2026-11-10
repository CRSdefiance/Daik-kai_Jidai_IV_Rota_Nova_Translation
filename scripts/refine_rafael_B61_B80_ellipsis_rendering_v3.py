"""Use consistent English ellipses after directly observing the native CP932 glyph."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael_B61_B80_formatting_20261104')

if __name__=='__main__':
    prior=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v2.json')
    target=Path('translations/rafael_B61_B80_contextual_editorial_manuscript_v3.json')
    output=ROOT/'formatting_input_v3.json';proof_path=ROOT/'ellipsis_native_visual_finding_v1.json'
    assert not any(p.exists() for p in [target,output,proof_path])
    partial=ROOT/'speech_native_v1/B63_checked.json';native={r['id']:r for r in load(partial)['records']}
    panels=[]
    for key,code in [('DK4_MES_B63_R0100',0x8163),('DK4_MES_B63_R0075',46)]:
        page=native[key]['complete_native_English_display']['pages'][0]
        event=next(e for e in page['events'] if e['code']==code)
        image=Image.open(page['preview']).convert('RGB');width=12 if code>127 else 6
        ink=[(x-event['x'],y-event['y']) for y in range(event['y'],event['y']+12)
            for x in range(event['x'],event['x']+width) if image.getpixel((x,y))!=(239,232,201)]
        panels.append(dict(id=key,code=code,event=event,ink_relative=ink,
            preview=page['preview'],preview_sha256=sha(Path(page['preview']).read_bytes())))
    assert panels[0]['ink_relative'] and panels[1]['ink_relative']
    doc=deepcopy(load(prior));changes=[]
    for row in doc['records']:
        if '…' not in row['english']:continue
        assert row['decision']=='retention'
        previous=row['english'];english=previous.replace('…','...')
        reason='Direct native visual review found the retained CP932 ellipsis uses a different midline/tick-like glyph from English periods. Use ordinary ASCII ellipsis for consistent English rendering while preserving exactly the same pause and reaction.'
        changes.append(dict(id=row['id'],previous_English=previous,English=english,reason=reason))
        row.update(english=english,logical_English=english,
            planned_English_markup='{SPEAKER:'+format(row['source_selector'],'02X')+'}'+english,
            prior_macro_normalized_comparison=english,
            font_consistency_refinement=dict(previous_English=previous,reason=reason),
            finding=row['finding']+' '+reason,localization_note=row['localization_note']+' '+reason)
    assert len(changes)==14 and all(r['english'].isascii() for r in doc['records'])
    save(proof_path,dict(source_native_block=str(partial),source_native_block_sha256=sha(partial.read_bytes()),
        directly_viewed_contact_sheet='work/analysis/Rafael_B61_B80_formatting_20261104/contact_B61_B66_v1/sheets/sheet_3.png',
        native_glyph_comparison=panels,scope=changes,
        native_font_andcode_not_modified=True,no_pause_deleted_no_speech_oraction_invented=True,
        original_punctuation_retentions_preserved_as_historical_provenance=True,
        fresh_formatting_andnative_checks_required_for_all14=True,new_credit=0,
        producer_sha256=sha(Path(__file__).read_bytes())))
    doc.update(previous_manuscript=str(prior),previous_manuscript_sha256=sha(prior.read_bytes()),
        source_bound_existing_nonASCII_punctuation={},source_bound_ASCII_ellipsis_refinements=changes,
        ellipsis_finding=str(proof_path),ellipsis_finding_sha256=sha(proof_path.read_bytes()),
        all539_final_English_ASCII_consistent=True,producer_sha256=sha(Path(__file__).read_bytes()))
    save(target,doc)
    save(output,dict(**doc,source_full_manuscript=str(target),source_full_manuscript_sha256=sha(target.read_bytes())))
    preference_path=ROOT/'planned_boundary_preferences_v3.json';preferences=deepcopy(load(preference_path))
    byid={r['id']:r for r in doc['records']}
    for key,value in preferences['records'].items():
        assert value['bindings']=={k:sha(byid[key][k].encode('utf-8')) for k in ['source_hex','current_hex','english']}
    preferences.update(manuscript=str(output),manuscript_sha256=sha(output.read_bytes()),
        previous_preferences=str(preference_path),previous_preferences_sha256=sha(preference_path.read_bytes()),
        all_record_scoped_preferences_exactly_unchanged=True)
    save(ROOT/'planned_boundary_preferences_v4.json',preferences)
    print('14 native-observed ellipsis glyph differences normalized to English dots;539 ASCII paragraphs,all prose/pause meanings andseven layout preferences preserved. Fresh checks required.',flush=True)
