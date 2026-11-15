"""Bind all30 viewed native pages and qualify the Deck Help research image and focused itinerary."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v10 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Shared_HELP_T103_T132_formatting_20261104')
OUT=ROOT/'preview_qualification_v1'

if __name__=='__main__':
    assert not OUT.exists();plan_path=ROOT/'refined_v3/automatic_plans_v1.json';native_path=ROOT/'native_pages_v1/native_help_pages.json'
    plan,native=map(load,[plan_path,native_path]);assert len(plan['pages'])==native['native_pages']==native['complete_articles']==30
    assert native['plan_sha256']==sha(plan_path.read_bytes())and len(native['review_sheets'])==8
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']and native['all_executed_current_instruction_bytes_exact']
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    doc=load(plan['manuscript']);parent=NdsImage.open(plan['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    args=[clean.read_file(file),base.read_file(file),parent.read_file(file)];resource,compiled=plan_articles(doc,*args,require_formatting=False)
    assert resource==Path(plan['research_resource']).read_bytes()and not compiled['compiler_generated_navigation_pairs']
    old,target=[IlnkContainer.parse(v).blocks for v in [args[-1],resource]]
    assert len(old)==len(target)==217 and all(target[i]==r for i,r in enumerate(old)if i not in range(103,133))
    assert len(next(p for p in compiled['pages']if p['topic_id']==110)['links'])==16
    for topic,phrase in [(117,'Social 160 or higher.'),(121,'Social 100 or higher.'),(116,'Health 130 or higher.'),(126,'Health 30 or higher.')]:
        assert any(phrase in line for line in next(p for p in compiled['pages']if p['topic_id']==topic)['visible_lines'])
    rejected=[]
    for case in ['missing-topic132','wrong-room-link110','unreviewed-DS-control106']:
        changed=deepcopy(doc)
        if case=='missing-topic132':changed['records'].pop()
        elif case=='wrong-room-link110':next(r for r in changed['records']if r['topic_id']==110)['english']=next(r for r in changed['records']if r['topic_id']==110)['english'].replace('[[126|Deck]]','[[127|Deck]]')
        else:next(r for r in changed['records']if r['topic_id']==106)['review']['localization']=False
        try:plan_articles(changed,*args,require_formatting=False)
        except ValueError as error:rejected.append(dict(case=case,rejected=True,error=str(error)))
        else:raise AssertionError(case)
    OUT.mkdir();viewed=[]
    for page,receipt in zip(plan['pages'],native['records'],strict=True):
        assert page['topic_id']==receipt['topic_id']and page['encoded_hex']==receipt['encoded_hex']
        assert sha(Path(receipt['preview']).read_bytes())==receipt['preview_sha256']
        viewed.append(dict(topic_id=page['topic_id'],preview=receipt['preview'],preview_sha256=receipt['preview_sha256'],
            all_complete_words_first_final_glyphs_links_andboundaries_directly_viewed=True))
    save(OUT/'direct_visual_approval.json',dict(native_proof=str(native_path),native_proof_sha256=sha(native_path.read_bytes()),
        all_eight_sheets_directly_viewed=True,all30_complete_pages_approved=True,pages=viewed,sheets=native['review_sheets'],
        all30_single_pages_no_prose_shortening=True,complete_skill_thresholds_role_names_andshort_tails_approved=True,
        body_retention_count=17,prose_revision_count=13,actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,resource);rom=OUT/'HELP_deck30_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()));reread=NdsImage.open(rom)
    assert [(p,q)for(_,p,b),(_,q,c)in zip(parent.iter_files(),reread.iter_files(),strict=True)if p!=q or b!=c]==[(file,file)]
    assert all(reread.read_file(p)==v for p,v in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,args[-1]);assert bytes(inverse.rom.save())==Path(plan['current_ROM']).read_bytes()
    previous=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104/preview_qualification_v1/qualification.json')
    assert len(load(previous)['new_formatter_andindividual_gate_rejections'])==7
    save(OUT/'qualification.json',dict(parent=plan['current_ROM'],parent_sha256=plan['current_ROM_sha256'],research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        source_articles=30,pages=30,target_topics=217,only_HELP_changed_all_other_components_exact_complete_parent_inverse=True,
        all_unowned_topics_andprevious_continuations_exact=True,new_formatter_andindividual_gate_rejections=rejected,
        previous_unchanged_source_parser_guards=str(previous),previous_unchanged_source_parser_guards_sha256=sha(previous.read_bytes()),
        all30_native_anddirect_visual_pages_pass=True,actual_widgets_archive_load_navigation_andregistered_integration_pending=True,
        all_fifth_gates_pending=True,new_credit=0,evidence={str(p):sha(p.read_bytes())for p in [plan_path,native_path,Path(plan['manuscript']),Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path);(OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(p['path']).resolve()==rom.resolve()for p in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve reviewed Deck Help30 research image, all prior ROMs retained. SHA256 '+sha(rom.read_bytes())))
    staged=pins_path.with_name('rom_retention_pins.HELP_deck30_preview.pending.json');assert not staged.exists();save(staged,pins)
    assert pins_path.read_bytes()==before;os.replace(staged,pins_path)
    actions=[dict(open=103),dict(remember='shared'),dict(open=104),dict(key='L'),dict(return_to='shared'),dict(key='R'),dict(key='X'),
        dict(open=103),dict(open=105),dict(open=106),dict(remember='setup')]
    for t in [107,108,109]:actions.extend([dict(open=t),dict(key='L'),dict(return_to='setup')])
    actions.extend([dict(key='X'),dict(open=103),dict(open=105),dict(open=110),dict(remember='workrooms')])
    for t in range(111,127):actions.extend([dict(open=t),dict(key='L'),dict(return_to='workrooms')])
    actions.extend([dict(key='X'),dict(open=103),dict(open=105),dict(open=127),dict(remember='holds')])
    for t in range(128,133):actions.extend([dict(open=t),dict(key='L'),dict(return_to='holds')])
    save(ROOT/'focused_itinerary_v1.json',dict(start_frame=21400,required_topics=list(range(103,133)),actions=actions))
    print('30 native/viewed pages approved;three new scope/link/control guards pass,seven unchanged guards reused. Research image pinned; actual Help traversal remains.')
