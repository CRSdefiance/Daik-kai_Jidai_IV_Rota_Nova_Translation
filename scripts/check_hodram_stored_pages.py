"""Check all final stored pages and moved native relative operands on the current runtime."""
import argparse
import inspect
from pathlib import Path
from types import FunctionType, SimpleNamespace

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import independent_pixels, load, save
from scripts.prove_Maria_story_branches_v7741 import native_skip
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.research_lil_B209_native_pages_v6461 import pages as inherited_pages
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_ordinary_name_fidelity_research import initialized


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--reconstruction', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    assert not args.out.exists()
    rebuilt = load(args.reconstruction)
    glyph_path = Path('work/analysis/Hodram_B61_B70_glyphs_20261101/glyph_review.json')
    glyphs = load(glyph_path)
    assert glyphs['runtime_inverse_exact_to_previous_reviewed_ARM9']
    image = NdsImage.open(rebuilt['research_ROM'])
    assert sha(Path(rebuilt['research_ROM']).read_bytes()) == rebuilt['research_ROM_sha256']
    arm, font = image.read_file('/__arm9__.bin'), image.read_file('/GRP/KANJI.FNT')
    assert sha(arm) == glyphs['current_ARM9_sha256']
    source_path = Path('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
    source = load(source_path)
    old_native_path = Path('work/analysis/Hodram_B61_B70_pages_v8894/compiled_native_pages.json')
    old_native = load(old_native_path)
    old_arm = old_native['ARM9_sha256']
    adapter = checked_text(source['source_owned_target_page_adapter'], {old_arm: sha(arm)})
    namespace = {**inherited_pages.__globals__, 'expected_pixels': independent_pixels, 'codes': codes}
    exec(compile(adapter, __file__ + '::current-bounds-runtime-pages', 'exec'), namespace)
    pages = namespace['pages']
    def relative_machine(arm, common, raw, plan):
        return initialized(arm), None, SimpleNamespace(executed_current=set())
    skip = FunctionType(native_skip.__code__, {**native_skip.__globals__, 'machine': relative_machine},
                        argdefs=native_skip.__defaults__)
    plans = {r['id']: r for r in load(rebuilt['plan'])['records']}
    previous = {r['id']: r for r in old_native['records']}
    changed = {r['id']: r for r in glyphs['changed']}
    blocks = IlnkContainer.parse(image.read_file('/data/SC1.DK4')).blocks
    args.out.mkdir(parents=True)
    rows, relative = [], []
    identical_pages, total = 0, 0
    for group in rebuilt['groups']:
        block = blocks[group['block']]
        assert sha(block) == group['target_sha256']
        for text in group['text_records']:
            stored = bytes.fromhex(text['stored_hex'])
            at = text['new_offset']
            assert block[at:at + len(stored) + 1] == stored + b'\0'
            expanded = stored[1:].replace(b'FI', b'Hodram').replace(b'FA', b'Bergstrom').replace(b'FO', b'Bergstrom Fleet')
            rendered = pages(arm, font, expanded)
            assert len(rendered['pages']) == plans[text['id']]['expected_native_pages']
            assert rendered['complete_consumed_bytes'] == len(expanded)
            for page in rendered['pages']:
                pixels = bytes.fromhex(page.pop('native_plane_hex'))
                filename = args.out / (text['id'] + f'_page{page["page"]}.bin')
                filename.write_bytes(pixels)
                page.update(native_plane=str(filename), native_plane_sha256=sha(pixels))
                if text['id'] not in changed:
                    old = previous[text['id']]['complete_native_English_display']['pages'][page['page'] - 1]
                    assert sha(Path(old['native_plane']).read_bytes()) == old['native_plane_sha256']
                    assert pixels == Path(old['native_plane']).read_bytes()
                    page['direct_view_reused_through_exact_plane'] = old['preview']
                    identical_pages += 1
                else:
                    pic = Image.new('RGB', (216, 64))
                    colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
                    pic.putdata([colors[v] for v in pixels])
                    png = filename.with_suffix('.png')
                    pic.save(png)
                    # The two new stored pages must equal the just-viewed compiled pages.
                    assert Image.open(changed[text['id']]['preview']).tobytes() == pic.tobytes()
                    page['direct_view_reused_through_exact_plane'] = changed[text['id']]['preview']
                total += 1
            rows.append(dict(id=text['id'], block=group['block'], new_offset=at,
                             stored_hex=stored.hex(), expanded_hex=expanded.hex(),
                             complete_stored_native_display=rendered))
        commands = {c['offset']: c for c in group['all_target_commands']}
        boundaries = set(commands) | {group['new_logical_end']}
        for fix in group['relative_fixups']:
            result = skip(arm, None, None, None, block, commands[fix['new_offset']])
            result.pop('current_executed_instruction_addresses')
            assert result['span'] == fix['new_span']
            assert all(c['next_offset'] in boundaries and c['next_offset'] ==
                       (fix['new_target'] if c['taken'] else fix['new_offset'] + 4) for c in result['cases'])
            relative.append(dict(block=group['block'], **result))
        print('Stored block', group['block'], 'checked', flush=True)
    assert len(rows) == 224 and total == 229 and identical_pages == 227
    assert len(relative) == 60 and sum(len(r['cases']) for r in relative) == 300
    save(args.out / 'stored_native_verification.json', dict(reconstruction=str(args.reconstruction),
        reconstruction_sha256=sha(args.reconstruction.read_bytes()),
        research_ROM=rebuilt['research_ROM'], research_ROM_sha256=rebuilt['research_ROM_sha256'],
        ARM9_sha256=sha(arm), source_page_adapter_sha256=sha(adapter.encode()),
        current_source_bound_page_adapter=adapter, records=rows, relative_cases=relative,
        complete_stored_pages=229, unchanged_directly_viewed_planes_reused_exactly=227,
        changed_stored_planes_match_two_new_directly_viewed_pages=True,
        every_byte_consumed_andall_first_internal_final_glyphs_bounds_canaries_andpagination_pass=True,
        fresh_relocated_native_relative_cases=300, actual_gameplay=False,
        default_names_host_expanded_with_existing_unchanged_macro_dependency_evidence=True,
        source_controls_retained_andprior_macro_alignments_reused_not_reexecuted=True,
        original_empty_set_trace_counter_omitted_no_new_instruction_coverage_claim=True,
        actual_headers_transitions_loaders_andregistered_release_pending=True,
        evidence={str(p): sha(p.read_bytes()) for p in [source_path, old_native_path, glyph_path, Path(__file__)]},
        new_credit=0))
    print('224 stored records /229 complete pages /300 native relative cases pass; all previous view evidence reused by exact pixels.')


if __name__ == '__main__':
    main()
