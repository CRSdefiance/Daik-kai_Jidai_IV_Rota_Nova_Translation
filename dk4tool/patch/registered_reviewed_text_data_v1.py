"""Compose four checked tutorial slots and two exclusive name fields, data only."""
import struct
from copy import deepcopy
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.owned_name_fields_v2 import plan_arm9_name_fields
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load
from scripts.shared_deck_formatting_v1 import compile_paragraph, PREFERENCES


def plan_release(image, config_path):
    conf = load(config_path)

    def need(value, message):
        if not value:
            raise ValueError('Registered reviewed text data: ' + message)

    need(conf['format'] == 'dk4-registered-reviewed-text-data-v1', 'schema')
    for path, digest in conf['dependencies'].items():
        need(sha(Path(path).read_bytes()) == digest, 'changed dependency: ' + path)
    before = bytes(image.rom.save())
    need(sha(before) == conf['parent_ROM_sha256'], 'complete ordered predecessor')
    need(sha(Path(conf['clean_ROM']).read_bytes()) == conf['clean_ROM_sha256'], 'clean Japanese input')
    clean = NdsImage.open(conf['clean_ROM']).read_file('/__arm9__.bin')
    arm = image.read_file('/__arm9__.bin')
    panels, names = map(load, [conf['panels'], conf['names']])
    native, connected, actual, visual, name_native, name_visual = map(load, [
        conf['panel_native'], conf['panel_connected'], conf['panel_actual'], conf['panel_visual'],
        conf['name_native'], conf['name_visual']])
    for doc, count in [(panels, 4), (names, 2)]:
        validate_natural_dialogue_batch(doc)
        need(len(doc['records']) == count, 'complete individually reviewed record set')
        need(all(all(r['review'][k] is True for k in ['source', 'context', 'localization', 'naturalness', 'formatting'])
                 for r in doc['records']), 'five individual review gates')
    need(set(r['id'] for r in panels['records']) == set(PREFERENCES), 'exact four tutorial panels')
    need(panels['one_terminology_revision'] == 1 and panels['justified_retentions'] == 3, 'individual editorial decisions')
    need(visual['final_review_sha256'] == sha(Path(conf['panels']).read_bytes()) and
         visual['all_four_final_native_panels_andtwo_actual_QA_sheets_directly_viewed'], 'direct panel visual approval')
    need(name_visual['final_review_sha256'] == sha(Path(conf['names']).read_bytes()) and
         name_visual['two_individual_full_name_editorial_reviews_complete'] and
         name_visual['all12_prior_native_planes_direct_view_reused'], 'direct complete name review')
    for proof in [native, connected, name_visual]:
        need(proof['runtime']['ARM9_sha256'] == sha(arm) and
             proof['runtime']['COMMON_sha256'] == sha(image.read_file('/data/COMMON.DK4')), 'exact relevant current dependencies')
    need(len(native['cases']) == len(connected['cases']) == 8 and len(native['plans']) == 4, 'all native panel modes')
    need(all(r['complete_first_internal_final_glyphs_andnative_pixels_andblank_guards_exact'] and
             r['all_main4MiB_unchanged'] and r['ABI_text_pixel_canaries_exact'] for r in native['cases']), 'complete panel pixels and guards')
    need(native['all31_pointer_values_andallocation_starts_unchanged'] and
         native['complete_parent_inverse_andall_unowned_ARM9_bytes_exact'] and native['allocation_shortfall_bytes'] == 0,
         'fixed panel ownership and allocation')
    need(connected['native_sha256'] == sha(Path(conf['panel_native']).read_bytes()) and
         connected['all8_complete_current_native_constructor_selector_copy_raster_andfont_cases_pass'], 'connected stored panel consumer')
    need(actual['actual_frames'] == 21400 and actual['complete_body_texture_andRGB_comparisons'] == 7 and
         actual['same_current168x108_native_Refit_constructor_palette_pitch_andglyph_consumer_observed'] and
         actual['four_revised_special_static_paragraphs_not_activated_or_claimed_observed'], 'honest representative live consumer scope')
    need(not any(actual[k] for k in ['natural_activation', 'full_route', 'hardware']), 'no unobserved coverage claim')
    proposed_panels = Path(native['proposed_ARM9']).read_bytes()
    need(sha(proposed_panels) == native['proposed_ARM9_sha256'] == connected['proposed_ARM9_sha256'], 'exact tested panel image')
    target = bytearray(arm)
    records = []
    plans = {p['id']: p for p in native['plans']}

    def add_span(ident, kind, at, old, new, source_reference):
        need(0 <= at <= len(arm) - len(old) and len(old) == len(new) and len(old) > 0, 'fixed valid span')
        need(arm[at:at + len(old)] == old, 'exact complete current span')
        need(all(at + len(old) <= r['physical_offset'] or at >= r['physical_offset'] + r['owned_bytes']
                 for r in records), 'disjoint typed spans')
        target[at:at + len(old)] = new
        records.append(dict(id=ident, file_path='/__arm9__.bin', kind=kind, physical_offset=at,
                            owned_bytes=len(old), old_hex=old.hex(), new_hex=new.hex(), source_reference=source_reference))

    for r in panels['records']:
        source, current, planned = r['source_reference'], r['current_reference'], r['planned_integrated_reference']
        p = plans[r['id']]
        at, capacity = planned['offset'], planned['capacity']
        need(source['file_path'] == current['file_path'] == planned['file_path'] == '/__arm9__.bin', 'typed panel component')
        need(clean[source['offset']:source['offset'] + source['capacity']].hex() == r['source_hex'], 'exact clean Japanese panel')
        need(source['pointer_field'] == current['pointer_field'] and
             struct.unpack_from('<I', arm, current['pointer_field'])[0] == current['pointer'], 'unchanged typed panel pointer')
        need((at, capacity) == (p['current_offset'], p['allocation']) and at == current['offset'], 'tested fixed allocation')
        old = arm[at:at + capacity]
        need(old[:current['length']].hex() == r['current_hex'] and old[current['length']] == 0, 'complete current panel string')
        compiled, lines = compile_paragraph(r['english'].removesuffix('{PAD}'), record_id=r['id'])
        need(compiled.hex() == p['compiled_hex'] == planned['compiled_hex'] and lines == p['lines'], 'fresh deterministic text formatting')
        need(compiled.endswith(b'\0') and len(compiled) <= capacity and len(lines) <= 5 and
             all(len(line) <= 27 for line in lines), 'complete terminator, width and pagination')
        new = compiled.ljust(capacity, b'\0')
        need(new.hex() == planned['padded_hex'] and proposed_panels[at:at + capacity] == new, 'tested stored panel bytes')
        add_span(r['id'], 'fixed-tutorial-panel', at, old, new, source)
    inverse_panels = bytearray(proposed_panels)
    for r in records:
        at = r['physical_offset']
        inverse_panels[at:at + r['owned_bytes']] = bytes.fromhex(r['old_hex'])
    need(bytes(inverse_panels) == arm, 'whole tested panel inverse')
    proposal = load(conf['name_proposal'])
    name_arm, name_plan = plan_arm9_name_fields(arm, proposal, clean)
    need(name_plan == name_native['name_data_plan'] == name_visual['complete_native_name_data_plan'] and
         name_arm == Path(name_native['proposed_ARM9']).read_bytes(), 'exact tested exclusive-field plan')
    need(name_native['original_progressive_andfull_name_getters_pass'] and len(name_native['negative_cases_rejected']) == 8,
         'complete name getters and rejected alias/control cases')
    reviewed = {(r['actor_ID'], r['reviewed_owned_field']['column']): r for r in names['records']}
    need(set(reviewed) == {(31, 8), (34, 8)} and len(proposal['fields']) == 2, 'exact two complete source identities')
    for field, p in zip(proposal['fields'], name_plan['fields'], strict=True):
        row = reviewed[p['actor'], p['column']]
        need(row['reviewed_owned_field'] == field and row['progressive_nameplate_unchanged'] and
             row['full_catalogue_UI_unvisited'], 'reviewed field and honest unvisited catalogue scope')
        add_span(row['id'], 'exclusive-name-component', p['physical_offset'], bytes.fromhex(p['old_hex']),
                 bytes.fromhex(p['new_hex']), row['source_reference'])
    target = bytes(target)
    inverse = bytearray(target)
    for r in records:
        at = r['physical_offset']
        inverse[at:at + r['owned_bytes']] = bytes.fromhex(r['old_hex'])
    need(len(records) == 6 and len(target) == len(arm) and bytes(inverse) == arm, 'six-span complete ARM9 inverse')
    need(sha(target) == conf['target_ARM9_sha256'], 'exact composed target ARM9')
    result = deepcopy(image)
    result.replace_file('/__arm9__.bin', target)
    need(sha(bytes(result.rom.save())) == conf['target_ROM_sha256'], 'exact complete target ROM')
    need(all(result.read_file(p) == value for _, p, value in image.iter_files()), 'all unowned files')
    need([p for p, value in image.iter_components() if result.read_file(p) != value] == ['/__arm9__.bin'], 'only ARM9 data component')
    need(bytes(image.rom.save()) == before, 'pure caller preservation')
    return target, dict(changed_records=records, parent_ARM9_sha256=sha(arm), target_ARM9_sha256=sha(target),
                        complete_six_disjoint_source_owned_spans_and_parent_target_inverse=True,
                        all_code_fonts_pointer_tables_allocations_andunowned_bytes_exact=True,
                        four_target_panels_andfull_catalogue_UI_live_unvisited=True,
                        representative_live_consumer_bodies=7, new_completion_credit=0, no_promotion=True)
