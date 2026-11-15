"""Check reconstructed storage, native relative operands and parity-dependent display."""
import argparse
from pathlib import Path
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import independent_pixels, load, save
from scripts.registered_editorial_runtime import RegisteredRuntime
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.research_lil_B209_native_pages_v6461 import pages as inherited_pages
from scripts import square_shopkeeper_font_oracles_v7020 as old_font
from scripts import Rafael_B45_FE_source_painter_v7894 as source_FE

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('reconstruction','native','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    rebuilt,native=map(load,[args.reconstruction,args.native])
    assert rebuilt['native_sha256']==sha(args.native.read_bytes())
    assert rebuilt['plan_sha256']==native['plan_sha256']
    runtime=native['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'])
    assert ctx.receipt()==runtime and rebuilt['parent_sha256']==runtime['candidate_sha256']
    image=NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']
    assert image.read_file('/__arm9__.bin')==ctx.arm
    font=image.read_file('/GRP/KANJI.FNT');assert sha(font)==native['font_sha256']
    full_native=load(native['previous_native']) if 'previous_native' in native else native
    adapter=full_native['source_owned_target_page_adapter']
    env={**inherited_pages.__globals__,'expected_pixels':independent_pixels,'codes':codes}
    exec(compile(adapter,__file__+'::same-registered-progressive','exec'),env)
    ascii_factory=FunctionType(old_font.make_painter.__code__,
        {**old_font.make_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm)},argdefs=old_font.make_painter.__defaults__)
    factory=FunctionType(source_FE.make_source_painter.__code__,
        {**source_FE.make_source_painter.__globals__,'CURRENT_ARM9':sha(ctx.arm),'ASCII_painter':ascii_factory},
        argdefs=source_FE.make_source_painter.__defaults__)
    painter,calibration=factory(image)
    compiled={r['id']:r for r in native['records']}
    plans={r['id']:r for r in load(rebuilt['plan'])['records']}
    blocks=IlnkContainer.parse(image.read_file(load(rebuilt['manuscript'])['file_path'])).blocks
    args.out.mkdir(parents=True)
    rows,relatives=[],[];fresh_pages=reused_pages=0
    for group in rebuilt['groups']:
        block=blocks[group['block']];assert sha(block)==group['target_sha256']
        for text in group['text_records']:
            row=compiled[text['id']];raw=bytes.fromhex(text['stored_hex']);at=text['new_offset']
            assert block[at:at+len(raw)+1]==raw+b'\0'
            assert text['compiled_hex']==row['compiled_hex']
            expanded=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')
            old=row['complete_native_English_display'];is_FE=raw[0]==254
            old_pages=old['pages'] if not is_FE else [old]
            expected_pages=plans[text['id']]['expected_native_pages']
            if text['parity_space_added']:
                assert expanded==bytes.fromhex(row['expanded_native_hex'])+b' '
                if is_FE:
                    rendered=painter(expanded)
                    new_planes=[rendered.pop('physical')];rendered.pop('logical')
                    assert expected_pages==1
                else:
                    rendered=env['pages'](ctx.arm,font,expanded)
                    assert rendered['complete_consumed_bytes']==len(expanded)
                    new_planes=[bytes.fromhex(p.pop('native_plane_hex')) for p in rendered['pages']]
                    assert len(new_planes)==expected_pages
                assert len(new_planes)==len(old_pages)
                for plane,previous in zip(new_planes,old_pages,strict=True):
                    assert sha(Path(previous['native_plane']).read_bytes())==previous['native_plane_sha256']
                    assert plane==Path(previous['native_plane']).read_bytes()
                fresh_pages+=len(new_planes)
            else:
                assert expanded.hex()==row['expanded_native_hex']
                for page in old_pages:
                    assert sha(Path(page['native_plane']).read_bytes())==page['native_plane_sha256']
                rendered=dict(exact_compiled_bytes_andruntime_reuse=True)
                reused_pages+=len(old_pages)
            rows.append(dict(id=text['id'],block=group['block'],new_offset=at,
                new_record_index=text['new_record_index'],stored_hex=raw.hex(),
                expanded_hex=expanded.hex(),parity_space_added=text['parity_space_added'],
                complete_stored_native_display=rendered,
                all_stored_planes_equal_directly_viewed_compiled_planes=True,
                directly_viewed_planes=[dict(path=p['native_plane'],sha256=p['native_plane_sha256']) for p in old_pages]))
        commands={c['offset']:c for c in group['all_target_commands']}
        boundaries=set(commands)|{group['new_logical_end']}
        for fix in group['relative_fixups']:
            result=ctx.execute(native_skip,block,commands[fix['new_offset']])
            assert result['span']==fix['new_span']
            assert all(c['next_offset'] in boundaries and c['next_offset']==
                (fix['new_target'] if c['taken'] else fix['new_offset']+4) for c in result['cases'])
            relatives.append(dict(block=group['block'],**result))
        print('Stored block',group['block'],'checked',flush=True)
    assert len(rows)==rebuilt['speech_count'] and fresh_pages+reused_pages==native['pages']
    assert len(relatives)==rebuilt['relative_sites']
    save(args.out/'stored_native_verification.json',dict(
        reconstruction=str(args.reconstruction),reconstruction_sha256=sha(args.reconstruction.read_bytes()),
        native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=ctx.receipt(),
        records=rows,relative_cases=relatives,complete_stored_pages=fresh_pages+reused_pages,
        fresh_parity_dependent_pages=fresh_pages,exact_compiled_pages_reused=reused_pages,
        all_stored_planes_equal_directly_viewed_compiled_planes=True,
        fresh_relocated_native_relative_cases=sum(len(r['cases']) for r in relatives),
        every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass=True,
        default_name_expansion_host_model_bound_to_prior_four_native_alignments=True,
        actual_gameplay=False,actual_headers_transitions_loaders_andregistered_release_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [args.reconstruction,args.native,Path(__file__)]},new_credit=0))
    print(dict(records=len(rows),pages=fresh_pages+reused_pages,fresh_parity_pages=fresh_pages,
        reused_pages=reused_pages,relative_cases=sum(len(r['cases']) for r in relatives)),flush=True)

if __name__=='__main__':
    main()
