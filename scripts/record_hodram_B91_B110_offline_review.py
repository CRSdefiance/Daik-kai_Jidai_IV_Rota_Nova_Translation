"""Bind direct visual review to every final page, menu and proposed name plane."""
from copy import deepcopy
from pathlib import Path
import struct
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.make_unique_editorial_page_sheets import pages

ROOT=Path('work/analysis/Hodram_B91_B110_visual_20261101')
NATIVE=Path('work/analysis/Hodram_B91_B110_native_20261101e/compiled_native_pages.json')
MENU=Path('work/analysis/Hodram_B91_B110_menu_20261101/menu_provider_and_planes.json')
NAMES=Path('work/analysis/Hodram_B91_B110_name_native_20261101/native_name_fields_verification.json')

if __name__=='__main__':
    out=ROOT/'visual_review.json';assert not out.exists()
    pending=load(ROOT/'visual_coverage_pending.json');initial=load(ROOT/'initial_visual_review.json')
    assert initial['fresh_unique_pages']==199 and len(initial['directly_viewed_sheets'])==17
    approved={r['native_plane_sha256']:dict(initial_id=r['id'],page=r['page'],initial_review=str(ROOT/'initial_visual_review.json')) for r in pending['records']}
    # These exact sheets were opened after the initial pass. Unviewed intermediate
    # B103_d is deliberately excluded; B103_e is the final corrected layout.
    fresh=[]
    for suffix,blocks in [('c',[95,100,104]),('d',[102]),('e',[103])]:
        path=Path(f'work/analysis/Hodram_B91_B110_native_20261101{suffix}/fresh/compiled_native_pages.json')
        report=load(path)
        for sheet in report['review_sheets']:
            if sheet['block'] in blocks:
                assert sha(Path(sheet['path']).read_bytes())==sheet['sha256'];fresh.append(sheet)
        for row,num,page,key in pages(report):
            if row['block'] in blocks:approved[key[-1]]=dict(id=row['id'],page=num,direct_native_report=str(path))
    native=load(NATIVE);coverage=[]
    for row,num,page,key in pages(native):
        assert key[-1] in approved,(row['id'],num)
        coverage.append(dict(id=row['id'],page=num,native_plane=page['native_plane'],native_plane_sha256=key[-1],visual_binding=approved[key[-1]]))
    assert len(coverage)==215 and len({r['id'] for r in coverage})==209
    save(out,dict(native=str(NATIVE),native_sha256=sha(NATIVE.read_bytes()),records=coverage,pages=215,
        initial_visual=str(ROOT/'initial_visual_review.json'),initial_visual_sha256=sha((ROOT/'initial_visual_review.json').read_bytes()),
        final_changed_directly_viewed_sheets=fresh,all_final_pages_directly_viewed_or_exact_plane_reuse=True,
        resolved_page_findings=list(initial['findings']),documented_page_retentions=initial['two_page_retentions'],
        source_bound_cape_andrepeated_far_phrase_coherent=True,B103_opening_sentence_andconditional_offer_coherent=True,
        no_clipping_orincomplete_glyphs=True,no_authored_ordinary_breaks=True,actual_gameplay=False,new_credit=0))
    for filename in [MENU,NAMES]:
        reviewed=deepcopy(load(filename));assert reviewed['direct_view_pending']
        sheet=reviewed['review_sheet'];assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
        reviewed.update(direct_view_pending=False,offline_visual_approved=True,original_pending_report=str(filename),original_pending_report_sha256=sha(filename.read_bytes()),
            visual_review_note='Directly viewed the complete legible native sheet;all first/last glyphs andspacing are intact. This is offline evidence only.')
        target=filename.with_name(filename.stem+'_reviewed.json');assert not target.exists();save(target,reviewed)
    source_root=Path('work/analysis/Hodram_B91_B110_clean_20261101')
    terms_path=source_root/'source_bound_item_terminology.json';terms=deepcopy(load(terms_path))
    batch=load(terms['approved_item_batch']);record=next(r for r in batch['records'] if r.get('id')=='DK4_ITEM_POINTER_063')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin');at=record['offset'];pointer=struct.unpack_from('<I',clean,at)[0]
    assert clean[at:at+4].hex().lower()==record['source_hex'].lower()
    raw=clean[pointer-0x02000000:].split(b'\0')[0]
    assert raw.decode('cp932')=='抜け忍の黒装束' and record['english']=='Ninja Garb'
    terms['records'].append(dict(item_catalogue_index=63,blocks=[97],approved_record=record,clean_pointer_field_offset=at,
        clean_source_name=dict(pointer=pointer,offset=pointer-0x02000000,hex=raw.hex(),text=raw.decode('cp932'),byte_length=len(raw),status='printable-static-string'),
        use_full_existing_approved_title_when_the_source_names_this_item=True,generic_Katzbalger_type_not_full_item_title=False))
    terms.update(previous=str(terms_path),previous_sha256=sha(terms_path.read_bytes()),new_credit=0)
    save(source_root/'source_bound_item_terminology_v2.json',terms)
    prior=Path('translations/confirmed_name_editorial_v289.json');stat=next(r for r in load(prior)['records'] if r['id']=='DK4_MES_B91_R0109')
    assert 'Spirit rose by 1!' in stat['english'] and '精神' in stat['clean_Japanese']
    save(source_root/'Spirit_source_term_binding.json',dict(prior_batch=str(prior),prior_batch_sha256=sha(prior.read_bytes()),record=stat,
        semantic_term_reuse_only_not_new_technical_orcompletion_credit=True,source_meaning='精神 is Spirit in this one-point stat notice; Luck remains a different stat.',new_credit=0))
    print(dict(final_speech_pages=215,all_visual_approved=True,typed_labels=2,name_planes=10,item_terms=9,new_credit=0))
