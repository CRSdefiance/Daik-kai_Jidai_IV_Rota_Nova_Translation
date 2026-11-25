"""Record all28 direct visual approvals,qualify new continuation guards andpin Help-only research ROM."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v3 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T21_T43_formatting_20261104')
OUT=ROOT/'preview_qualification_v2'
if __name__=='__main__':
    assert not OUT.exists();plan_path=ROOT/'refined_v2/automatic_plans_v1.json';plan=load(plan_path)
    native_path=ROOT/'refined_native_v2/native_help_pages.json';native=load(native_path)
    assert len(plan['pages'])==native['native_pages']==28 and (native['fresh_pages'],native['exact_reused_pages'])==(10,18)
    assert native['plan_sha256']==sha(plan_path.read_bytes()) and native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    doc=load(plan['manuscript']);parent=NdsImage.open(plan['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    file=doc['file_path'];args=[clean.read_file(file),base.read_file(file),parent.read_file(file)]
    resource,compiled=plan_articles(doc,*args,require_formatting=False);assert resource==Path(plan['research_resource']).read_bytes()
    target,parent_blocks=[IlnkContainer.parse(r).blocks for r in [resource,args[-1]]]
    assert target[205]==parent_blocks[205] and [r for r in compiled['compiler_generated_navigation_pairs'] if r['article']==37]==[dict(article=37,page_ids=[37,204])]
    assert all(a==b for a,b in zip(target[:21],parent_blocks[:21],strict=True))
    rejected=[]
    for kind in ['wrong-current204','arbitrary-semantic-section24','lost-military-words','foreign-owner205']:
        manuscript=deepcopy(doc);current=args[-1]
        if kind=='wrong-current204':next(r for r in manuscript['records'] if r['topic_id']==37)['current_continuations'][0]['current_hex']='00'
        elif kind=='arbitrary-semantic-section24':
            row=next(r for r in manuscript['records'] if r['topic_id']==24);first,rest=row['english'].split(' ',1)
            row.update(semantic_sections=[first,rest],semantic_section_reason='Arbitrary sentence split.')
        elif kind=='lost-military-words':next(r for r in manuscript['records'] if r['topic_id']==37)['semantic_sections'][1]='Missing.'
        else:
            blocks=deepcopy(parent_blocks);blocks[181]=blocks[181].rstrip(b'\0')+b'{foreign:'+bytes([205])+b'}\n\0'
            current=IlnkContainer(blocks).to_bytes();manuscript['source_current_HELP_sha256']=sha(current)
        try:plan_articles(manuscript,args[0],args[1],current,require_formatting=False)
        except ValueError as error:rejected.append(dict(case=kind,rejected=True,error=str(error)))
        else:raise AssertionError('Accepted invalid new continuation/paragraph case:'+kind)
    assert len(rejected)==4
    OUT.mkdir();records=[]
    for page,receipt in zip(plan['pages'],native['records'],strict=True):
        assert page['topic_id']==receipt['topic_id'] and page['encoded_hex']==receipt['encoded_hex']
        assert sha(Path(receipt['preview']).read_bytes())==receipt['preview_sha256']
        records.append(dict(topic_id=page['topic_id'],source_article_id=page['source_article_id'],preview=receipt['preview'],
            preview_sha256=receipt['preview_sha256'],all_complete_page_words_first_final_glyphs_andboundaries_directly_viewed=True,
            specific_refinement={22:'A Purser grammar andwhole source tips withmarkers.',25:'Complete letter-use instruction starts the continuation paragraph.',34:'Keep press B together as a plain English phrase.',37:'All full benefits nowfit the second page;body words retained andunused old205 preserved.',38:'Complete100-percent exception andprohibitions together.',39:'Complete100-percent exception andprohibitions together.'}.get(page['source_article_id'],'Readable full wording,logical width,complete links andpage boundaries;no additional refinement needed.')))
    save(OUT/'direct_visual_approval.json',dict(native_proof=str(native_path),native_proof_sha256=sha(native_path.read_bytes()),
        all_seven_refined_sheets_directly_viewed=True,all28_complete_pages_approved=True,sheets=native['review_sheets'],pages=records,
        initial29_pages_all_eight_sheets_also_viewed_but_findings_required_refinement=True,
        six_article_specific_display_refinements_andone_grammar_correction=True,one_needless_page_removed_without_shortening_body_prose=True,
        body_retention_count=4,prose_revision_count=19,actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,resource)
    rom=OUT/'HELP_town23_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()));reread=NdsImage.open(rom)
    assert [p for _,p,v in parent.iter_files() if reread.read_file(p)!=v]==[file] and all(reread.read_file(p)==v for p,v in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,args[-1]);assert bytes(inverse.rom.save())==Path(plan['current_ROM']).read_bytes()
    save(OUT/'qualification.json',dict(parent=plan['current_ROM'],parent_sha256=plan['current_ROM_sha256'],research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        only_HELP_changed_all_other_components_exact_complete_parent_inverse=True,source_articles=23,pages=28,target_topics=216,
        existing205_retained_exact_after_removing_redundant_third_page=True,new_semantic_rejections=rejected,
        all28_native_anddirect_visual_pages_pass=True,fresh_native_pages=10,exact_reused_native_pages=18,
        actual_widgets_archive_load_navigation_andregistered_integration_pending=True,all_fifth_gates_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [plan_path,native_path,Path(plan['manuscript']),Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    (OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(r['path']).resolve()==rom.resolve() for r in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve reviewed town Help23 research216-topic image;all prior ROMs retained. SHA256 '+sha(rom.read_bytes())))
    temp=pins_path.with_name('rom_retention_pins.town_HELP23_preview.pending.json');assert not temp.exists();save(temp,pins)
    assert pins_path.read_bytes()==before;os.replace(temp,pins_path)
    print('28 native/directly viewed pages approved;four new semantic guards reject;Help-only216-topic research ROM pinned. Actual/release gates remain.')
