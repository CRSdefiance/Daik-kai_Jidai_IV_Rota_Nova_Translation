"""Approve six fresh native pages, retain25 exact proofs and plan focused current Help observations."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_pages_v12 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/HELP31_active_terms_20261105');OUT=ROOT/'preview_qualification_v1'

if __name__=='__main__':
    assert not OUT.exists();pp=ROOT/'automatic_plans_v1.json';np=ROOT/'native_pages_v1/native_help_pages.json'
    plan,native=map(load,[pp,np]);assert native['native_pages']==31 and native['fresh_pages']==6 and native['exact_reused_pages']==25
    assert native['plan_sha256']==sha(pp.read_bytes())and native['fresh_page_IDs']==[33,116,117,118,121,126]and len(native['review_sheets'])==2
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']and native['all_executed_current_instruction_bytes_exact']
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    doc=load(plan['manuscript']);parent=NdsImage.open(plan['current_ROM']);clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    args=[clean.read_file(file),base.read_file(file),parent.read_file(file)];resource,compiled=plan_articles(doc,*args,require_formatting=False)
    assert resource==Path(plan['research_resource']).read_bytes()and compiled['pages']==plan['pages']and not compiled['compiler_generated_navigation_pairs']
    target,current=[IlnkContainer.parse(b).blocks for b in [resource,args[-1]]]
    assert len(target)==len(current)==217 and all(target[n]==b for n,b in enumerate(current)if n not in {33,*range(103,133)})
    previous=load('work/analysis/Shared_HELP_T103_T132_formatting_20261104/production_plan_v1.json');old={p['topic_id']:p for p in previous['pages']}
    assert [p['topic_id']for p in compiled['pages']if p['topic_id']in old and p==old[p['topic_id']]]==native['exact_reused_page_IDs']
    rejected=[]
    for topic,good,bad in [(33,'Speech','Social'),(116,'Vigor','Health'),(117,'Speech','Social'),(118,'Guile','Tactics'),(121,'Speech','Social'),(126,'Vigor','Health')]:
        changed=deepcopy(doc);row=next(r for r in changed['records']if r['topic_id']==topic);row['english']=row['english'].replace(good,bad)
        assert changed!=doc
        try:plan_articles(changed,*args,require_formatting=False)
        except ValueError as error:rejected.append(dict(topic_id=topic,rejected=True,error=str(error)))
        else:raise AssertionError('Accepted inactive skill label:'+str(topic))
    OUT.mkdir();pages=[]
    for p in compiled['pages']:
        t=p['topic_id'];r=next(r for r in native['records']if r['topic_id']==t);assert r['encoded_hex']==p['encoded_hex']and sha(Path(r['preview']).read_bytes())==r['preview_sha256']
        pages.append(dict(topic_id=t,preview=r['preview'],preview_sha256=r['preview_sha256'],
            all_complete_words_first_final_glyphs_links_andboundaries_directly_viewed=True,
            visual_scope='fresh direct review'if t in native['fresh_page_IDs']else'exact prior native/visual proof reuse'))
    save(OUT/'direct_visual_approval.json',dict(native_proof=str(np),native_proof_sha256=sha(np.read_bytes()),pages=pages,
        all31_pages_approved=True,six_fresh_pages_andtwo_fresh_sheets_directly_viewed=True,twentyfive_exact_prior_visual_page_proofs_reused=True,
        sheets=native['review_sheets'],no_repeated_unmodified_page_generation_orinspection=True,actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,resource);rom=OUT/'HELP31_active_terms_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()));reread=NdsImage.open(rom)
    assert [(p,q)for(_,p,a),(_,q,b)in zip(parent.iter_files(),reread.iter_files(),strict=True)if p!=q or a!=b]==[(file,file)]
    assert all(reread.read_file(p)==v for p,v in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,args[-1]);assert bytes(inverse.rom.save())==Path(plan['current_ROM']).read_bytes()
    save(OUT/'qualification.json',dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),parent=plan['current_ROM'],parent_sha256=plan['current_ROM_sha256'],
        target_topics=217,source_articles=31,new_source_articles=30,previously_credited_amendments=[33],
        native_pages=31,fresh_native_pages=6,exact_reused_native_pages=25,all_native_andvisual_pages_pass=True,
        explicit_active_skill_rejections=rejected,only_HELP_changed_all_other_components_andcomplete_parent_inverse_exact=True,
        previous_twentyfive_actual_pages_reusable_only_with_exact_page_dependency_binding=True,actual_six_changed_pages_andregistered_integration_pending=True,
        new_credit=0,evidence={str(p):sha(p.read_bytes())for p in [pp,np,Path(plan['manuscript']),Path('dk4tool/dialogue/reviewed_help_pages_v12.py'),Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path);(OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(p['path']).resolve()==rom.resolve()for p in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve corrected active-term Deck30/Coerce33 research. All prior translations/ROMs retained. SHA256 '+sha(rom.read_bytes())))
    temp=pins_path.with_name('rom_retention_pins.HELP31_active.pending.json');assert not temp.exists();save(temp,pins)
    assert pins_path.read_bytes()==before;os.replace(temp,pins_path)
    actions=[dict(open=11),dict(open=26),dict(open=27),dict(remember='letters'),dict(open=33),dict(key='L'),dict(return_to='letters'),dict(key='X'),
        dict(open=103),dict(open=105),dict(open=110),dict(remember='rooms')]
    for t in [116,117,118,121,126]:actions.extend([dict(open=t),dict(key='L'),dict(return_to='rooms')])
    save(ROOT/'focused_itinerary_v1.json',dict(start_frame=21400,required_topics=[33,116,117,118,121,126],actions=actions))
    print('31 native/visual pages qualified:6 fresh/25 exact reuse;six active-term guards reject regressions. Focused six-page observation remains.')
