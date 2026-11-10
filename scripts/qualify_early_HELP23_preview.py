"""Bind direct review of all25 native pages; qualify scoped planner guards andHelp-only research image."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.dialogue.reviewed_help_pages_v1 import plan_articles
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_early23_formatting_20261104')
OUT=ROOT/'preview_qualification_v1'
PARENT=Path('out/all_routes_combined_rafael_b61_b80_20261104_candidate.nds')

if __name__=='__main__':
    assert not OUT.exists()
    plan_path=ROOT/'automatic_plans_v1.json';plan=load(plan_path)
    native_path=ROOT/'native_pages_v2/native_help_pages.json';native=load(native_path)
    assert native['plan_sha256']==sha(plan_path.read_bytes()) and native['native_pages']==25
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    manuscript=load(plan['manuscript']);clean=NdsImage.open('work/clean.nds');baseline=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    parent=NdsImage.open(PARENT);file=manuscript['file_path']
    assert sha(PARENT.read_bytes())=='9ace6dcdf45097ad2f779d15597ab06ab85a0e5442486e6ad98c112a422c446e'
    args=[clean.read_file(file),baseline.read_file(file),parent.read_file(file)]
    assert sha(args[-1])==manuscript['source_current_HELP_sha256']
    encoded,positive=plan_articles(manuscript,*args,require_formatting=False)
    assert encoded==Path(plan['research_resource']).read_bytes()
    failures=[]
    def reject(name,edit,production=False):
        doc=deepcopy(manuscript);edit(doc)
        try:plan_articles(doc,*args,require_formatting=production)
        except ValueError as error:failures.append(dict(case=name,rejected=True,error=str(error)))
        else:raise AssertionError('Unsafe proposal accepted: '+name)
    reject('production_requires_fifth_gate',lambda d:None,True)
    reject('full_parent_hash_lock',lambda d:d.update(source_current_HELP_sha256='0'*64))
    reject('individual_current_bytes',lambda d:d['records'][0].update(current_source_hex='00'))
    reject('duplicate_article_ownership',lambda d:d['records'].append(deepcopy(d['records'][0])))
    reject('missing_localization_gate',lambda d:d['records'][0]['review'].update(localization=False))
    reject('authored_early_linebreak',lambda d:d['records'][2].update(english=d['records'][2]['english'].replace(' oceans','\noceans',1)))
    reject('unintended_fullwidth_glyph',lambda d:d['records'][2].update(english=d['records'][2]['english'].replace('Sail','Ｓail',1)))
    reject('wrong_original_binary_link',lambda d:d['records'][0].update(original_link_IDs=[2,11,82,103,143]))
    reject('existing202_owner_bytes',lambda d:next(r for r in d['records'] if r['topic_id']==7)['current_continuation'].update(current_hex='00'))
    reject('semantic_group_changes_words',lambda d:next(r for r in d['records'] if r['topic_id']==7)['semantic_sections'].append('Extra detail.'))
    assert len(failures)==10
    OUT.mkdir()
    visual=[]
    for page,proof in zip(plan['pages'],native['records'],strict=True):
        assert page['topic_id']==proof['topic_id'] and page['encoded_hex']==proof['encoded_hex']
        assert sha(Path(proof['preview']).read_bytes())==proof['preview_sha256']
        visual.append(dict(topic_id=page['topic_id'],source_article_id=page['source_article_id'],page_number=page['page_number'],
            preview=proof['preview'],preview_sha256=proof['preview_sha256'],all_complete_lines_directly_viewed=True,
            finding='Readable complete words andfirst/final characters; automatic width andphrase continuity acceptable. No added manual breaks orprose shortening.',
            semantic_benefit_pagination_justified=page['source_article_id'] in [7,9]))
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    save(OUT/'direct_visual_approval.json',dict(native_proof=str(native_path),native_proof_sha256=sha(native_path.read_bytes()),
        all_seven_readable_sheets_directly_viewed=True,sheets=native['review_sheets'],pages=visual,
        all25_complete_pages_approved=True,actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,encoded)
    rom=OUT/'HELP_early23_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()))
    reread=NdsImage.open(rom)
    assert [p for _,p,b in parent.iter_files() if reread.read_file(p)!=b]==[file]
    assert all(reread.read_file(p)==b for p,b in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,parent.read_file(file));assert bytes(inverse.rom.save())==PARENT.read_bytes()
    entry_source=Path('work/analysis/help_footer_release_v455/semantic_regression_inputs.json')
    inputs=[e for e in load(entry_source) if e['start']<=21001]
    assert inputs[-1]==dict(start=21001,duration=8,buttons=['X'])
    save(OUT/'ordinary_Help_index_entry_inputs.json',inputs)
    save(OUT/'qualification.json',dict(parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),
        research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),only_HELP_changed_complete_parent_inverse_exact=True,
        positive_plan=positive,semantic_rejections=failures,all25_native_pages_anddirect_visual_review_pass=True,
        actual_widget_navigation_andregistered_release_pending=True,all_fifth_gates_pending=True,new_credit=0,
        entry_schedule_source=str(entry_source),entry_schedule_source_sha256=sha(entry_source.read_bytes()),
        source_context_current_refs_unchanged_HELP_ARM9_COMMON_andfonts_equal_verified_parent=True,
        evidence={str(p):sha(p.read_bytes()) for p in [plan_path,native_path,Path(plan['manuscript']),Path(__file__)]}))
    print('25 pages visually approved;10 planner rejects pass;Help-only research ROM andordinary index-entry schedule saved. No completion credit.')
