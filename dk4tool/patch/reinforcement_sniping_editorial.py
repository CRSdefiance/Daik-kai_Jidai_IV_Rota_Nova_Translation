"""Source-reviewed20 reinforcement, covering-fire and shot paragraphs."""
import struct
from pathlib import Path
from types import FunctionType

from ndspy.code import MainCodeFile
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.battle_declaration_editorial import current_entries as previous_entries
from dk4tool.patch.common_single_cache_v861 import SINGLE, entries, repack
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from dk4tool.script import common_message_table as parser
from scripts import reinforcement_sniping_runtime_v1025 as runtime
from scripts.reinforcement_sniping_layout_v1024 import IDS, PROFILE, compiled
from scripts.verify_village_wrap_v608 import read

SOURCE_COMMON = 'c89951623064574f5f2e8369b922e11721023cb798e3850d4fdb9afe848bad00'
SOURCE_ARM = '42a31b92893961132530ab4ef86ec64e99969fe37a7a3bc56f7984a47edc74db'
CONFIG = 'translations/reinforcement_sniping_editorial_release_v1.json'


def plan(common, arm, doc):
    assert sha(common) == SOURCE_COMMON and sha(arm) == SOURCE_ARM
    validate_natural_dialogue_batch(doc)
    assert doc['translation_policy'] == 'natural-dialogue-v2' and doc['target_locale'] == 'en-US'
    assert doc['encoder'] == 'dialogue-relocatable-v1' and doc['consumer_layout_profile'] == PROFILE
    assert tuple(r['message_id'] for r in doc['records']) == IDS
    assert doc['current_COMMON_sha256'] == SOURCE_COMMON and doc['current_ARM9_sha256'] == SOURCE_ARM
    clean, canonical = map(NdsImage.open, ('work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds'))
    assert sha(Path('work/clean.nds').read_bytes()) == doc['source_clean_ROM_sha256']
    assert sha(Path('out/raphael_natural_v2_accepted_base.nds').read_bytes()) == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    jp = parser.common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), clean.read_file('/__arm9__.bin'))
    accepted = parser.common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    before = previous_entries(common, arm)
    authored = {}
    for row in doc['records']:
        n = row['message_id']
        assert row['source_hex'] == jp[n].text.hex() and row['canonical_source_hex'] == accepted[n].text.hex()
        assert row['current_text_hex'] == before[n].text.hex()
        args = int(n < 1924)
        assert row['native_argument_count'] == jp[n].text.count(b'%s') == args
        assert row['source_native_macros'] == []
        assert row['source_family'] == ('reinforcement' if n < 1917 else 'covering_fire' if n < 1924 else 'admiral_shot')
        assert all(row['review'].get(gate) for gate in ('source', 'context', 'localization', 'naturalness', 'formatting'))
        payload = compiled(row)
        assert b'\n' not in payload and payload.hex() == row['compiled_hex']
        authored[n] = payload
    authored = {n: raw for n, raw in authored.items() if raw != before[n].text}
    pack = FunctionType(repack.__code__, {**repack.__globals__, 'previous_entries': previous_entries})
    before, blocks, first, last, selected, opaque, groups, attempts = pack(common, arm, authored)
    runtime_arm, runtime_plan = runtime.apply(arm)
    # Native text metadata is independent of the three already-owned runtime
    # spans. Start from the exact verified runtime image,then update only native
    # table/directory fields emitted by the original single-cache repacker.
    target, rebuilt, fields = bytearray(runtime_arm), list(blocks), []
    for block, (group, body) in zip(range(first, last+1), groups, strict=True):
        rebuilt[block] = body
        at = parser.DIRECTORY_OFFSET+block*4
        struct.pack_into('<HH', target, at, group[0][0], len(body))
        fields.append((at, 4))
        for n, offset, payload in group:
            at = parser.TABLE_OFFSET+n*2
            struct.pack_into('<H', target, at, offset)
            fields.append((at, 2))
    c, a = IlnkContainer(rebuilt).to_bytes(), bytes(target)
    directory = sha(a[parser.DIRECTORY_OFFSET:parser.TABLE_OFFSET])
    after = entries(c, a, directory)
    assert len(before) == len(after) == 3668
    assert all(b.text == authored.get(e.message_id, e.text) for e, b in zip(before, after, strict=True))
    assert all(blocks[b] == rebuilt[b] for b in range(41) if not first <= b <= last)
    for n, payload in opaque.items():
        row = after[n]
        assert rebuilt[row.block][row.block_offset:row.copy_end] == payload
    restored = bytearray(a)
    for at, size in fields:
        assert runtime_arm[at:at+size] == arm[at:at+size]
        restored[at:at+size] = runtime_arm[at:at+size]
    assert bytes(restored) == runtime_arm and cache_plan(a) == cache_plan(arm)
    old_code, new_code = MainCodeFile(arm, 0x02000000), MainCodeFile(a, 0x02000000)
    shape = lambda code: [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    assert shape(old_code) == shape(new_code)
    assert all(old_code.sections[n].data == new_code.sections[n].data for n in (1, 2, 3))
    assert len(new_code.sections[3].data)-48 == 123040
    return c, a, {'changed_records': [f'COMMON_MESSAGE_{n}' for n in IDS if before[n].text != after[n].text],
        'reviewed_native_IDs': list(IDS), 'metadata_fields': fields, 'directory_sha256': directory,
        'repacked_block_range': [first, last], 'packing_attempts': attempts,
        'repacked_native_IDs': [e.message_id for e in selected],
        'repacked_block_lengths': [len(rebuilt[b]) for b in range(first, last+1)],
        'runtime_source_and_exact_owned_changes': runtime_plan,
        'all3648_unselected_message_strings_and_opaque_payloads_exact': True,
        'opaque_payload_IDs': sorted(opaque), 'all_unselected_blocks_exact': True,
        'all_other_ARM9_bytes_except_native_metadata_and_three_proven_runtime_spans_exact': True,
        'all20_paragraphs_have_no_LF_before_original_macro_or_literal_processing': True,
        'existing_single_cache_code_hex_preserved': SINGLE.hex(),
        'single8192_input_reuses_original_two4096_allocation': True,
        'output512_and216x36_Deck_crop_unchanged': True,
        'all_sections_BSS_cache_arenas_and_entire123040_staged_payload_unchanged': True,
        'actual_RGB_geometry_choices_and_gameplay_not_proven_by_this_stage': True,
        'experimental': True, 'full_goal_complete': False}


def current_entries(common, arm):
    config = read(CONFIG)
    assert sha(common) == config['target_common_sha256'] and sha(arm) == config['target_arm9_sha256']
    return entries(common, arm, config['directory_sha256'])


def apply_release(common, arm, path):
    config = read(path)
    assert config['format'] == 'dk4-reinforcement-sniping-editorial-v1'
    assert sha(common) == config['source_common_sha256'] == SOURCE_COMMON
    assert sha(arm) == config['source_arm9_sha256'] == SOURCE_ARM
    for name, digest in config['dependencies'].items():
        assert sha(Path(name).read_bytes()) == digest, name
    manuscript = Path(config['manuscript'])
    assert sha(manuscript.read_bytes()) == config['manuscript_sha256']
    doc = read(manuscript)
    for key in ('reviewed_research_manuscript', 'native_context_proof', 'source_context_supplement',
                'native_font_proof', 'visual_review_proof', 'native_runtime_proof'):
        assert sha(Path(doc[key]).read_bytes()) == doc[key+'_sha256'], key
    draft = read(doc['reviewed_research_manuscript'])
    assert [(r['message_id'], r['english'], r['source_meaning']) for r in doc['records']] == [(r['message_id'], r['english'], r['source_meaning']) for r in draft['records']]
    context, supplement, font, visual, rt = [read(doc[key]) for key in ('native_context_proof', 'source_context_supplement', 'native_font_proof', 'visual_review_proof', 'native_runtime_proof')]
    assert len(context['all624_actor_voice_selections']) == 624
    assert len(context['all24_original_role_wrapper_cases']) == 24
    assert len(context['all_original_reinforcement_argument_fragments']) == 40
    assert len(context['all_original_covering_fire_argument_fragments']) == 57
    assert len(context['all20_native_complete_company_labels']) == 20
    assert supplement['reinforcement_percent_s_is_complete_faction_label']
    assert supplement['covering_fire_percent_s_is_compact_commander_label']
    assert context['covering_fire_source_scan_requires_other_player_faction_fleet_and_original_join_predicates']
    assert context['source_rng2000_comparison_against_stat_divided_by10_and_original_outcome_after_message_not_overridden']
    assert len(font['cases']) == font['complete_native_font_canvases'] == 694
    assert visual['native_font_proof_sha256'] == doc['native_font_proof_sha256']
    assert visual['all20_templates_and_representative_extreme_name_canvases_visually_reviewed']
    assert not visual['visual_review_pending'] and not visual['blocking_errors'] and not visual['unwaived_warnings']
    assert len(visual['compiler_rejection_controls']) == 15 and all(visual['compiler_rejection_controls'].values())
    assert rt['old_and_new_complete_scope_cases_each'] == 56696 and rt['all3668_modal_outputs_and_wrap_choices_exact']
    assert rt['all140_status8MiB_ABI_guards_pass'] and rt['public212_and_ITCM128_byte_footprints_unchanged']
    records = {row['message_id']: row for row in doc['records']}
    for case in font['cases']:
        assert compiled(records[case['message_ID']]).hex() == case['compiled_hex']
        assert case['whole228x64_native_independent_font_and_input_bitmap_guards_pass']
        assert case['all_leading_trailing_and_CP932_name_glyphs_complete']
        assert sha(Path(case['preview']).read_bytes()) == case['preview_sha256']
    c, a, proof = plan(common, arm, doc)
    assert proof['runtime_source_and_exact_owned_changes']['research_ARM9_sha256'] == rt['research_ARM9_sha256']
    assert sha(c) == config['target_common_sha256'] and sha(a) == config['target_arm9_sha256']
    assert proof['directory_sha256'] == config['directory_sha256']
    copies, audit = read(config['native_copy_proof']), read(config['native_consumer_audit'])
    assert copies['complete_native_copies'] == 7336 and len(copies['sequenced_cache_cases']) == 178
    assert copies['COMMON_sha256'] == sha(c) and copies['ARM9_sha256'] == sha(a)
    assert copies['all_full_span_plus_NUL_and_entire8192_input_bytes_and_output_guard_pass']
    assert copies['callee_saved_ABI_and_stack_pass']
    assert audit['batch_sha256'] == sha(manuscript.read_bytes())
    assert audit['blocking_errors'] == audit['unwaived_warnings'] == 0 and len(audit['records']) == 20
    assert audit['target_COMMON_sha256'] == sha(c) and audit['target_ARM9_sha256'] == sha(a)
    return c, a, proof
