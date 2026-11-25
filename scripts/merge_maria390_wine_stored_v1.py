"""Compose14 fresh stored records with359 exact compatible record and branch proofs."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT=Path('work/Maria_B152_B175_clean_20261109')


def main():
    out=ROOT/'stored_v3';assert not out.exists()
    newpath=ROOT/'reconstruction_v3/reconstruction.json';oldpath=ROOT/'reconstruction_v2/reconstruction.json'
    oldstoredpath=ROOT/'stored_v2/stored_native_verification.json';freshpath=ROOT/'stored_wine_v1/stored_native_verification.json'
    new,old,prior,fresh=map(load,[newpath,oldpath,oldstoredpath,freshpath])
    assert new['previous_wine_reconstruction_sha256']==digest(oldpath) and prior['reconstruction_sha256']==digest(oldpath)
    partial=load(fresh['reconstruction'])
    assert fresh['reconstruction_sha256']==digest(fresh['reconstruction']) and partial['full_reconstruction_sha256']==digest(newpath)
    assert prior['native_sha256']==digest(old['native']) and fresh['native_sha256']==partial['native_sha256']==digest(fresh['native'])
    assert load(fresh['native'])['full_native_proof_sha256']==digest(new['native'])
    assert fresh['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert prior['every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass']
    assert fresh['all_stored_planes_equal_directly_viewed_compiled_planes'] and prior['all_stored_planes_equal_directly_viewed_compiled_planes']
    native=load(new['native']);oldnative=load(old['native'])
    assert native['runtime']==oldnative['runtime']==fresh['runtime']==prior['runtime'] and native['font_sha256']==oldnative['font_sha256']
    for key in ['source_owned_target_page_adapter','source_owned_progressive_macro_adapter']:assert native[key]==oldnative[key]
    image=NdsImage.open(new['research_ROM']);oldimage=NdsImage.open(old['research_ROM'])
    assert digest(new['research_ROM'])==new['research_ROM_sha256'] and digest(old['research_ROM'])==old['research_ROM_sha256']
    for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:assert image.read_file(p)==oldimage.read_file(p)
    bank=IlnkContainer.parse(image.read_file('/data/SC3.DK4')).blocks
    oldbank=IlnkContainer.parse(oldimage.read_file('/data/SC3.DK4')).blocks
    oldgroups={g['block']:g for g in old['groups']};oldrows={r['id']:r for r in prior['records']}
    newrows={r['id']:r for r in fresh['records']};planes={r['id']:r for r in native['records']};oldplanes={r['id']:r for r in oldnative['records']}
    rows=[];relative=[];reused=0
    for group in new['groups']:
        b=group['block'];block=bank[b];assert sha(block)==group['target_sha256']
        if b!=152:
            assert group==oldgroups[b] and block==oldbank[b]
            relative.extend(r for r in prior['relative_cases'] if r['block']==b)
        else:relative.extend(fresh['relative_cases'])
        for text in group['text_records']:
            row=deepcopy(newrows[text['id']] if b==152 else oldrows[text['id']])
            assert row['id']==text['id'] and row['block']==b and row['new_offset']==text['new_offset']
            assert row['new_record_index']==text['new_record_index'] and row['stored_hex']==text['stored_hex']
            assert row['parity_space_added']==text['parity_space_added']
            raw=bytes.fromhex(row['stored_hex']);at=row['new_offset'];assert block[at:at+len(raw)+1]==raw+b'\0'
            assert text['compiled_hex']==planes[row['id']]['compiled_hex']
            display=planes[row['id']]['complete_native_English_display']
            pages=[display] if planes[row['id']]['kind']=='system-FE' else display['pages']
            assert row['all_stored_planes_equal_directly_viewed_compiled_planes'] and len(pages)==len(row['directly_viewed_planes'])
            for existing,page in zip(row['directly_viewed_planes'],pages,strict=True):
                assert digest(existing['path'])==existing['sha256']==page['native_plane_sha256']==digest(page['native_plane'])
            if b!=152:
                assert planes[row['id']]['compiled_hex']==oldplanes[row['id']]['compiled_hex']
                assert planes[row['id']]['expanded_native_hex']==oldplanes[row['id']]['expanded_native_hex']
                row['exact_compatible_stored_record_reuse']=dict(proof=str(oldstoredpath),sha256=digest(oldstoredpath),
                    same_whole_block_ARM9_COMMON_font_macro_andpixel_dependencies=True)
                reused+=1
            rows.append(row)
    assert len(rows)==373 and reused==359 and len(newrows)==14 and len(relative)==new['relative_sites']==122
    newcases=fresh['fresh_relocated_native_relative_cases'];totalcases=sum(len(r['cases']) for r in relative)
    assert totalcases==610 and sum(len(t['labels']) for t in prior['typed_objects'])==17
    out.mkdir();proof=deepcopy(prior)
    proof.update(reconstruction=str(newpath),reconstruction_sha256=digest(newpath),native=new['native'],native_sha256=digest(new['native']),
        records=rows,relative_cases=relative,complete_stored_pages=373,
        fresh_parity_dependent_pages=fresh['fresh_parity_dependent_pages'],
        exact_compiled_pages_reused=373-fresh['fresh_parity_dependent_pages'],
        fresh_relocated_native_relative_cases=newcases,exact_previous_native_relative_cases_reused=totalcases-newcases,
        total_qualified_native_relative_cases=totalcases,exact_previous_stored_records_reused=359,fresh_changed_block_records=14,
        aggregation_of_exact_compatible_proofs_andfresh_changed_block_not_monolithic_replay=True,
        every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass=True,
        all_stored_planes_equal_directly_viewed_compiled_planes=True,new_credit=0,actual_gameplay=False,
        evidence={str(p):digest(p) for p in [newpath,oldpath,oldstoredpath,freshpath,Path(new['native']),Path(old['native']),Path(__file__)]})
    save(out/'stored_native_verification.json',proof)
    print(dict(records=373,exact_stored_records_reused=359,fresh_block_records=14,fresh_parity_pages=fresh['fresh_parity_dependent_pages'],
        fresh_branch_cases=newcases,exact_branch_cases_reused=totalcases-newcases,new_credit=0))


if __name__=='__main__':main()
