"""Bind directly viewed native bodies andcorrect one storage-description finding;wording andgates unchanged."""
from pathlib import Path
from copy import deepcopy
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Hodram_B50_native_review_v8493')
OLD=Path('translations/hodram_B50_editorial_manuscript_v1.json')
DOC=Path('translations/hodram_B50_editorial_manuscript_v2.json')
PAGES=Path('work/analysis/Hodram_B50_pages_v8492b/compiled_native_pages.json')
PREVIOUS=Path('translations/hodram_B49_editorial_manuscript_v4.json')
REASONS={
 7:'The complete retained request fits one native row with its final exclamation intact. Its current raw record contains trailing allocation spaces and no line break. The formatter preserves every word anduses the full216px width;it owns later storage/parity changes.',
 10:'Two automatically balanced rows keep the complete delighted confirmation onrow1 andthe complete gift gesture/cheer/farewell onrow2. Source-scoped phrase preferences keep Here, take this! coherent. Every approved word andpunctuation mark survives atfull216px availablewidth. No manual break,narrowed viewport,shortening orQA waiver.',
 13:'Two complete originalFE rows keep handed over asone verb phrase andthe Heavenly Wristband asone noun phrase. The source bytes andcompiled body areidentical toapproved B49R81. The distinct original null-actor FEconsumer/logical228x48/physical16pitch/288stride andfull216usablewidth remain;actual B50typed view/palette/VRAM/item transition isnot established bythis offline preview.',
}
if __name__=='__main__':
    assert not ROOT.exists() and not DOC.exists();old,pages,previous=map(read,[OLD,PAGES,PREVIOUS]);planpath=Path(pages['plan']);plan=read(planpath)
    assert pages['manuscript_sha256']==plan['manuscript_sha256']==sha(OLD.read_bytes()) and pages['plan_sha256']==sha(planpath.read_bytes())
    sheet=pages['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'] and len(pages['records'])==3
    rows=[];infos=[];corrections=[]
    for original,p,n in zip(old['records'],plan['records'],pages['records'],strict=True):
        assert original['id']==p['id']==n['id'] and original['english']==n['logical_English']==' '.join(p['lines']) and len(n['pages'])==1 and not original['review']['formatting']
        for page in n['pages']:
            for key in ['native_plane','preview']:assert sha(Path(page[key]).read_bytes())==page[key+'_sha256']
            if 'physical_plane' in page:assert sha(Path(page['physical_plane']).read_bytes())==page['physical_plane_sha256']
        for issue in p['base_QA']['issues']:assert issue['severity']=='info' and issue['code']=='line-break-count';infos.append(dict(id=original['id'],issue=issue))
        row=deepcopy(original)
        if row['source_record_index']==7:
            assert '\n' not in row['current_raw_storage_English'] and row['current_raw_storage_English'].endswith(' ')
            finding='The existing startled question andimmediate request convey the arrival andher eagerness naturally. The current raw record contains trailing allocation spaces andno line break;the formatter owns storage andany later wrapping.'
            reason=row['retention_reason'].replace('Remove only legacy ordinary wrapping through the formatter.','The current record hasno line break;its trailing spaces belong tostorage. The formatter owns any later wrapping andparity.')
            assert finding!=row['finding'] and reason!=row['retention_reason'];corrections.append(dict(id=row['id'],field_scope='technical storage-description only',previous_finding=row['finding'],finding=finding,previous_reason=row['retention_reason'],reason=reason,raw_storage_literal=row['current_raw_storage_English'],all_approved_English_source_refs_native_bytes_andreview_gates_unchanged=True))
            row.update(finding=finding,retention_reason=reason,localization_note=reason)
        row.update(compiled_hex=p['encoded_hex'],compiled_bytes=len(bytes.fromhex(p['encoded_hex'])),formatted_markup=p['formatted_markup'],planned_English_markup=p['planning_record']['english'],generated_lines=p['lines'],expected_native_pages=1,qa_waivers=[],qa_waiver_scope=[],native_body_review_reason=REASONS[row['source_record_index']],native_body_review_proof=str(PAGES),native_body_review_proof_sha256=sha(PAGES.read_bytes()),compiled_native_body_review=deepcopy(n),all_stored_controls_actual_effects_headers_FE_geometry_policy_andregistered_release_pending=True)
        assert row['english']==original['english'] and row['source_hex']==original['source_hex'] and row['current_hex']==original['current_hex'] and row['review']==original['review'];rows.append(row)
    prior=next(r for r in previous['records'] if r['id']=='DK4_MES_B49_R0081');assert rows[-1]['source_hex']==prior['source_hex'] and rows[-1]['compiled_hex']==prior['compiled_hex']
    assert len(rows)==len(infos)==3;ROOT.mkdir(parents=True);doc=deepcopy(old);doc.update(records=rows,predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),compiled_plan=str(planpath),compiled_plan_sha256=sha(planpath.read_bytes()),native_body_pages=str(PAGES),native_body_pages_sha256=sha(PAGES.read_bytes()),all_three_complete_native_body_pages_directly_viewed=True,all_three_formatting_gates_still_false=True,three_original_line_count_infos_zero_warnings_waivers=True,source_andcompiled_FE_bytes_exact_to_approved_B49_notice=True,status='contextual-prose-andcompiled-native-body-reviewed-stored-actual-policy-release-pending')
    save(DOC,doc);save(ROOT/'native_body_review.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),predecessor_manuscript=str(OLD),predecessor_manuscript_sha256=sha(OLD.read_bytes()),directly_viewed_sheet=sheet,all_three_complete_bodies_visually_read=True,individual_body_reviews=[dict(id=r['id'],reason=r['native_body_review_reason'],generated_lines=r['generated_lines'],compiled_hex=r['compiled_hex']) for r in rows],original_infos=infos,original_warnings=[],original_QA_not_suppressed=True,no_qa_waivers=True,technical_finding_corrections=corrections,all_approved_words_source_current_references_andreview_gates_preserved=True,full216px_width_font_metrics_pagination_andguard_rules_unchanged=True,body_preview_not_actual_names_scene_FE_palette_VRAM_orconditional_coverage=True,all_three_formatting_gates_false=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [OLD,PAGES,planpath,PREVIOUS,Path(__file__)]}))
    print('B50all3native bodies directlyviewed/12alignments/3line-countinfos/0warnings orwaivers. One storage-description corrected;allEnglish/source/current refs unchanged. Manuscriptv2;formatting/stored/actual/release pending.')
