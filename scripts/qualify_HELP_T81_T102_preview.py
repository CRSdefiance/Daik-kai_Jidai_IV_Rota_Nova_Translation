"""Approve22 viewed native pages andguard new phrase/link behavior;pin only a research image."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v7 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104');OUT=ROOT/'preview_qualification_v1'
if __name__=='__main__':
    assert not OUT.exists();plan_path=ROOT/'refined_v2/automatic_plans_v1.json';native_path=ROOT/'native_pages_v1/native_help_pages.json'
    plan,native=map(load,[plan_path,native_path]);assert len(plan['pages'])==native['native_pages']==native['complete_articles']==22
    assert native['plan_sha256']==sha(plan_path.read_bytes()) and native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact'] and len(native['review_sheets'])==6
    for s in native['review_sheets']:assert sha(Path(s['path']).read_bytes())==s['sha256']
    doc=load(plan['manuscript']);parent=NdsImage.open(plan['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    args=[clean.read_file(file),base.read_file(file),parent.read_file(file)];resource,compiled=plan_articles(doc,*args,require_formatting=False)
    assert resource==Path(plan['research_resource']).read_bytes() and not compiled['compiler_generated_navigation_pairs']
    target,old=[IlnkContainer.parse(r).blocks for r in [resource,args[-1]]]
    assert len(target)==len(old)==217 and all(target[i]==r for i,r in enumerate(old) if i not in range(81,103))
    assert all(not line.endswith('[Tip]')for p in compiled['pages']for line in p['visible_lines'])
    assert next(p for p in compiled['pages']if p['source_article_id']==94)['visible_lines'][1:]==['Defeat the monster.','You may receive an item.']
    assert next(p for p in compiled['pages']if p['source_article_id']==98)['visible_lines'][-1]=='Deck positions.'
    rejected=[]
    for case in ['unreviewed-controls83','wrong-current97','arbitrary-paragraph85','lost-logical-words83','authored-line-break95','changed-Deck-link98','missing-topic102']:
        changed=deepcopy(doc)
        if case=='unreviewed-controls83':next(r for r in changed['records']if r['topic_id']==83)['review']['localization']=False
        elif case=='wrong-current97':next(r for r in changed['records']if r['topic_id']==97)['current_source_hex']='00'
        elif case=='arbitrary-paragraph85':
            r=next(r for r in changed['records']if r['topic_id']==85);a,b=r['english'].split(' ',1);r.update(semantic_sections=[a,b],semantic_section_reason='Arbitrary split.')
        elif case=='lost-logical-words83':
            r=next(r for r in changed['records']if r['topic_id']==83);r.update(semantic_sections=[r['english'][:10],'Missing.'],semantic_section_reason='Lost source words.')
        elif case=='authored-line-break95':
            r=next(r for r in changed['records']if r['topic_id']==95);r['english']=r['english'].replace('You lose','You\nlose')
        elif case=='changed-Deck-link98':
            r=next(r for r in changed['records']if r['topic_id']==98);r['english']=r['english'].replace('[[126|Deck]]','[[127|Deck]]')
        else:changed['records']=[r for r in changed['records']if r['topic_id']!=102]
        try:plan_articles(changed,*args,require_formatting=False)
        except ValueError as error:rejected.append(dict(case=case,rejected=True,error=str(error)))
        else:raise AssertionError('Accepted invalid new formatter/source case:'+case)
    OUT.mkdir();records=[]
    for page,receipt in zip(plan['pages'],native['records'],strict=True):
        assert page['topic_id']==receipt['topic_id'] and page['encoded_hex']==receipt['encoded_hex']
        assert sha(Path(receipt['preview']).read_bytes())==receipt['preview_sha256']
        records.append(dict(topic_id=page['topic_id'],source_article_id=page['source_article_id'],preview=receipt['preview'],preview_sha256=receipt['preview_sha256'],
          all_complete_page_words_first_final_glyphs_andboundaries_directly_viewed=True,
          specific_finding='Reviewed phrase/marker/single-word-tail refinement,allprose retained.'if page['source_article_id']in[86,87,90,94,95,96,98,101]else'Readable full wording,complete linked labels andlogical available width.'))
    save(OUT/'direct_visual_approval.json',dict(native_proof=str(native_path),native_proof_sha256=sha(native_path.read_bytes()),
      all_six_sheets_directly_viewed=True,all22_complete_pages_approved=True,sheets=native['review_sheets'],pages=records,
      eight_wrap_refinements_no_prose_shortening_oradded_pages=True,body_retention_count=5,prose_revision_count=17,actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,resource);rom=OUT/'HELP_sea22_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()));reread=NdsImage.open(rom)
    assert[p for _,p,v in parent.iter_files()if reread.read_file(p)!=v]==[file]and all(reread.read_file(p)==v for p,v in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,args[-1]);assert bytes(inverse.rom.save())==Path(plan['current_ROM']).read_bytes()
    save(OUT/'qualification.json',dict(parent=plan['current_ROM'],parent_sha256=plan['current_ROM_sha256'],research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
      only_HELP_changed_all_other_components_exact_complete_parent_inverse=True,source_articles=22,pages=22,target_topics=217,
      all_unowned_topics_including_previous83_reviewed_topics_andall_appended_pages_exact=True,new_formatter_andindividual_gate_rejections=rejected,
      all22_native_anddirect_visual_pages_pass=True,actual_widgets_archive_load_navigation_andregistered_integration_pending=True,all_fifth_gates_pending=True,new_credit=0,
      evidence={str(p):sha(p.read_bytes())for p in[plan_path,native_path,Path(plan['manuscript']),Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path);(OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(r['path']).resolve()==rom.resolve()for r in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve reviewed sea Help22 research217-topic image;allpreviousROMs retained.SHA256 '+sha(rom.read_bytes())))
    staged=pins_path.with_name('rom_retention_pins.sea_HELP22_preview.pending.json');assert not staged.exists();save(staged,pins)
    assert pins_path.read_bytes()==before;os.replace(staged,pins_path)
    print('22 native/directly viewed pages approved;seven new guards pass;Help-only217-topic research ROM pinned.Actual/release gates remain.')
