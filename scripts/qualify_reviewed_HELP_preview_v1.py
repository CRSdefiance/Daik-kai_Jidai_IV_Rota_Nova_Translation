"""Seal directly reviewed Help sheets and make a pinned, reversible Help-only research image."""
import argparse
import importlib
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for key in ['plan','native','guards','out']:parser.add_argument('--'+key,type=Path,required=True)
    parser.add_argument('--compiler',required=True)
    parser.add_argument('--all-fresh-sheets-directly-reviewed',action='store_true',required=True)
    args=parser.parse_args();assert not args.out.exists()
    plan,native,guards=map(load,[args.plan,args.native,args.guards]);doc=load(plan['manuscript'])
    assert native['plan_sha256']==sha(args.plan.read_bytes())
    assert guards['plan_sha256']==sha(args.plan.read_bytes()) and guards['all72_logical_prose_pagecounts_andownership_exact']
    assert len(guards['rejections'])==13 and all(r['rejected'] for r in guards['rejections'])
    compiler=importlib.import_module(args.compiler);compiler_path=Path(compiler.__file__)
    assert compiler_path.resolve()==Path(guards['compiler']).resolve() and sha(compiler_path.read_bytes())==guards['compiler_sha256']
    prior_guard_path=Path(guards['previous_guard_proof']);prior_guard=load(prior_guard_path)
    assert sha(prior_guard_path.read_bytes())==guards['previous_guard_proof_sha256']
    prior_compiler_path=Path(prior_guard['compiler']);assert sha(prior_compiler_path.read_bytes())==prior_guard['compiler_sha256']
    prior_module=importlib.import_module('.'.join(prior_compiler_path.with_suffix('').parts))
    assert compiler.SOURCE==prior_module.SOURCE and guards['rejections']==prior_guard['rejections']
    assert native['all_complete_glyph_codes_font_pixels_link_requests_row_coordinates_input_header_andpixel_guards_pass']
    assert native['all_executed_current_instruction_bytes_exact'] and native['native_pages']==len(plan['pages'])
    assert native['fresh_pages']==9 and native['exact_reused_pages']==63 and len(native['review_sheets'])==3
    assert native['fresh_page_IDs']==guards['changed_page_IDs']
    for sheet in native['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    parent=NdsImage.open(plan['current_ROM']);assert sha(Path(plan['current_ROM']).read_bytes())==plan['current_ROM_sha256']
    clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds');file=doc['file_path']
    resource,compiled=compiler.plan_articles(doc,clean.read_file(file),base.read_file(file),parent.read_file(file),require_formatting=False)
    assert resource==Path(plan['research_resource']).read_bytes() and compiled['pages']==plan['pages']
    assert len(compiled['articles'])==67 and compiled['target_topic_count']==217
    blocks=IlnkContainer.parse(resource).blocks;records=[]
    for page in plan['pages']:
        t=page['topic_id'];nr=next(r for r in native['records'] if r['topic_id']==t)
        assert nr['encoded_hex']==page['encoded_hex']==blocks[t].hex()
        assert sha(Path(nr['preview']).read_bytes())==nr['preview_sha256']
        if 'exact_native_andvisual_reuse' in nr:
            proof=nr['exact_native_andvisual_reuse'];prior_visual_path=Path(proof['visual'])
            assert sha(prior_visual_path.read_bytes())==proof['visual_sha256']
            assert next(r for r in load(prior_visual_path)['pages'] if r['topic_id']==t)['formatting_approved']
        records.append(dict(topic_id=t,preview=nr['preview'],preview_sha256=nr['preview_sha256'],
            all_complete_words_first_final_glyphs_links_andboundaries_directly_viewed=True))
    args.out.mkdir(parents=True)
    save(args.out/'direct_visual_approval.json',dict(native_proof=str(args.native),native_proof_sha256=sha(args.native.read_bytes()),
        pages=records,all72_pages_approved=True,all18_initial_andthree_fresh_refinement_sheets_directly_viewed=True,
        nine_phrase_tail_refinements_resolved=True,exact_unchanged_native_andvisual_pages_reused=63,
        sheets=native['review_sheets'],actual_gameplay=False,new_credit=0))
    image=deepcopy(parent);image.replace_file(file,resource);rom=args.out/'HELP67_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()))
    reread=NdsImage.open(rom)
    assert [(p,q) for (_,p,a),(_,q,b) in zip(parent.iter_files(),reread.iter_files(),strict=True) if p!=q or a!=b]==[(file,file)]
    assert all(reread.read_file(p)==v for p,v in parent.iter_components())
    inverse=deepcopy(reread);inverse.replace_file(file,parent.read_file(file));assert bytes(inverse.rom.save())==Path(plan['current_ROM']).read_bytes()
    save(args.out/'qualification.json',dict(research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),parent=plan['current_ROM'],parent_sha256=plan['current_ROM_sha256'],
        target_topics=217,source_articles=67,native_pages=72,all_native_andvisual_pages_pass=True,
        only_HELP_changed_all_other_components_andcomplete_parent_inverse_exact=True,formatter_guards=str(args.guards),formatter_guards_sha256=sha(args.guards.read_bytes()),
        all_five_existing_continuation_owners_preserved=True,no_added_topics=True,actual_representative_navigation_pending=True,registered_integration_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [args.plan,args.native,args.guards,Path(plan['manuscript']),compiler_path,Path(__file__)]}))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path)
    (args.out/'pins.before.json').write_bytes(before);assert not any(Path(p['path']).resolve()==rom.resolve() for p in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve remaining67 Help editorial/display research; all prior ROMs retained. SHA256 '+sha(rom.read_bytes())))
    staged=pins_path.with_name('rom_retention_pins.HELP67.pending.json');assert not staged.exists();save(staged,pins)
    assert pins_path.read_bytes()==before;os.replace(staged,pins_path)
    print('67 articles/72 fresh native and visually approved pages;217 topics/all five old continuations preserved. Focused navigation and registered integration pending.')

if __name__=='__main__':main()
