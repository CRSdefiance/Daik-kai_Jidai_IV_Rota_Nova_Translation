"""Clean-source editorial review:five empty searches,five foraging reports,loss312."""
from copy import deepcopy
from dataclasses import asdict
from pathlib import Path
import struct
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from dk4tool.patch.hot_spring_notice_editorial import current_entries
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/search_reports_source_v1653')
OUT = Path('translations/search_reports_editorial_manuscript_v1.json')
ROM = Path('out/all_routes_combined_v1637_candidate.nds')
IDS = [312, *range(2217, 2222), *range(2229, 2234)]
PROSE = {
    312: ('Lost %s sailors.', 'The number of sailors decreased by the supplied amount.',
          'Use idiomatic concise game-status wording. Lost does not specify death or its cause. Preserve the single original numeric substitution;remove the old line break and four trailing alignment spaces.'),
    2217: ("The expedition is back! It looks like there's nothing around here.",
           'The expedition has returned;there appears to be nothing nearby.',
           'Restore the omitted return and tentative finding. A brisk complete report suits the exclamation;do not turn an apparent absence into a categorical worldwide claim.'),
    2218: ("The expedition's back. Doesn't look like they found anything worthwhile.",
           'The expedition is back;it seems there was nothing noteworthy.',
           'Keep the casual voice and the distinction between nothing worthwhile and literally nothing. The conversational omitted subject is natural American dialogue.'),
    2219: ("The expedition's back, but there doesn't seem to be anything nearby.",
           'The expedition returned,but there seems to be nothing nearby.',
           'Preserve the return,but contrast and tentative observation. Convey the older speaker naturally without invented dialect or archaic English.'),
    2220: ("The expedition's back. They say there's nothing around here.",
           'The expedition has returned;they say there is nothing in this area.',
           'Preserve the explicit hearsay and conversational voice. Keep the report limited to this area.'),
    2221: ("The expedition has returned. There doesn't seem to be anything around here.",
           'The expedition has returned;there seems to be nothing around here.',
           'Keep a measured report and tentative judgment. Restore the missing return without inventing a rank,address or discovery.'),
    2229: ('The expedition found %s barrels of water and %s barrels of food.',
           'The expedition discovered the supplied barrel counts of water and food,in that order.',
           'Restore the expedition as subject and found as the action;use natural English coordination. Preserve two original%s values,water first,food second,and barrels for both.'),
    2230: ('The expedition found %s barrels of water and %s barrels of food!',
           'The expedition found the supplied barrel counts of water and food;casual report.',
           'Use an upbeat informal report without inventing extra supplies. Preserve water then food,two%s substitutions and both barrel units.'),
    2231: ('The expedition found %s barrels of water and %s barrels of food!',
           'The expedition discovered the supplied barrel counts of water and food;exclamatory announcement.',
           'Keep the discovery and energetic tone. Use a complete idiomatic report;preserve the two quantities,order and barrel units.'),
    2232: ("The expedition's found %s barrels of water and %s barrels of food!",
           'The expedition discovered the supplied barrel counts of water and food;assertive informal report.',
           'Use a natural contraction and confident exclamation rather than a literal Japanese final particle. Preserve quantities,order and units.'),
    2233: ('The expedition found us %s barrels of water and %s barrels of food!',
           'The expedition found the supplied barrel counts of water and food;casual report.',
           'Use a conversational report. Us refers to the reporting fleet receiving the supplies in the original caller,not a new recipient. Preserve both%s values in water-food order and both barrel units.'),
}

if __name__ == '__main__':
    assert not ROOT.exists() and not OUT.exists()
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    ca, cc = clean.read_file('/__arm9__.bin'), clean.read_file('/COMMON/MESFILE.DK4')
    arm, common = current.read_file('/__arm9__.bin'), current.read_file('/COMMON/MESFILE.DK4')
    source, entries = common_message_entries(cc, ca), current_entries(common, arm)
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    base = common_message_entries(canonical.read_file('/COMMON/MESFILE.DK4'), canonical.read_file('/__arm9__.bin'), clean=False)
    tables = {0x02116EC0: [2217, -1, 2218, -1, -1, 2219, 2220, 2221],
              0x02116E80: [2229, -1, 2230, -1, 2231, 2232, 2233, -1]}
    for address, values in tables.items():
        assert list(struct.unpack_from('<8i', ca, address - 0x02000000)) == values
        assert arm[address - 0x02000000:address - 0x02000000 + 32] == ca[address - 0x02000000:address - 0x02000000 + 32]
    spans = [(0x79E98, 0x79FD0), (0x796A4, 0x79728)]
    disassembler = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    callers = []
    for lo, hi in spans:
        assert arm[lo:hi] == ca[lo:hi]
        callers.append({'start': 0x02000000 + lo, 'end_exclusive': 0x02000000 + hi,
                        'clean_code_hex': ca[lo:hi].hex(),
                        'disassembly': [f'{i.address:08X} {i.mnemonic} {i.op_str}' for i in disassembler.disasm(ca[lo:hi], 0x02000000 + lo)]})
    rows = []
    for n in IDS:
        english, gloss, note = PROSE[n]
        count = 1 if n == 312 else 2 if n >= 2229 else 0
        assert english.count('%s') == source[n].text.count(b'%s') == count
        assert '\n' not in english and english == english.strip() and '  ' not in english
        table = 0x02116EC0 if 2217 <= n <= 2221 else 0x02116E80 if n >= 2229 else None
        role = 1 if 2217 <= n <= 2221 else 7 if n >= 2229 else None
        context = ('Original generic sailor-reduction modal;Search helper796A4 supplies a positive clamped loss via ABF50 and546B8. Other callers remain to audit.' if n == 312 else
                   'Original unsuccessful Search:role1/table2116EC0 via79F98,then original fatigue+3/status308. Preserve returned-expedition and tentative/hearsay distinctions.' if n <= 2221 else
                   'Original successful forage Search:role7/table2116E80 via79F5C,r2=ABF50(water r5),r3=ABF50(food r6),then34C98 adds the same counts to the existing fleet. Values and units must retain their order.')
        row = {'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_Japanese': source[n].text.decode('cp932'),
               'source_hex': source[n].text.hex(), 'source_reference': {k: v for k, v in asdict(source[n]).items() if k != 'text'},
               'current_English': entries[n].text.decode('cp932'), 'current_text_hex': entries[n].text.hex(),
               'current_reference': {k: v for k, v in asdict(entries[n]).items() if k != 'text'},
               'canonical_source_hex': base[n].text.hex(), 'english': english, 'source_meaning': gloss,
               'localization_note': note, 'speaker': 'Original speakerless system modal' if n == 312 else f'Original role{role} speaker with original voice-table selection',
               'context': context, 'source_role': role, 'source_table': table, 'native_argument_count': count,
               'source_native_macros': [], 'editorial_decision': 'revise', 'authored_as_one_unwrapped_paragraph': True,
               'review': {'source': True, 'context': True, 'localization': True, 'naturalness': True, 'formatting': False},
               'status': 'source-context-prose-reviewed;native-font-release-and-revised-gameplay-pending'}
        rows.append(row)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    assert (ledger['records_editorially_completed'], ledger['records_with_source_and_prose_pass'], len(ledger['reviewed_but_incomplete_COMMON_IDs'])) == (1350, 1508, 158)
    assert not set(IDS) & set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    assert not any(set(IDS) & set(f.get('native_message_IDs', [])) for f in ledger['completed_editorial_families'])
    ROOT.mkdir(parents=True)
    save(ROOT / 'coverage_before_review.json', deepcopy(ledger))
    context_path = ROOT / 'clean_source_and_original_consumers.json'
    save(context_path, {'source_clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()), 'candidate': str(ROM),
                        'candidate_sha256': sha(ROM.read_bytes()), 'tables': {str(a): v for a, v in tables.items()},
                        'callers': callers, 'records_and_neighbors': [
                            {'message_id': n, 'Japanese': source[n].text.decode('cp932'), 'source_hex': source[n].text.hex(),
                             'current_English': entries[n].text.decode('cp932'), 'current_hex': entries[n].text.hex()}
                            for n in [311, 312, 313, *range(2216, 2235)]],
                        'actual_old_wording_only_reference': 'hot_spring_notice_resilient_v1645_1637 frames24400,24550,26531,28461,40011;identical old templates do not prove every alternative voice individually activated',
                        'not_a_native_compilation_release_or_revised_gameplay_proof': True})
    doc = {'format': 'dk4-native-common-editorial-v1', 'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
           'encoder': 'dialogue-relocatable-v1', 'file_path': '/COMMON/MESFILE.DK4',
           'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'], 'formatting_review_pending': True,
           'source_clean_ROM_sha256': sha(Path('work/clean.nds').read_bytes()), 'current_ROM': str(ROM),
           'current_ROM_sha256': sha(ROM.read_bytes()), 'current_COMMON_sha256': sha(common), 'current_ARM9_sha256': sha(arm),
           'source_context': str(context_path), 'source_context_sha256': sha(context_path.read_bytes()), 'records': rows,
           'revised': 11, 'retained': 0, 'no_authored_line_breaks_or_alignment': True,
           'no_runtime_argument_added_removed_or_reordered': True, 'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(OUT, doc)
    ledger['records_with_source_and_prose_pass'] += 11
    ledger['records_with_source_prose_drafts'] += 11
    ledger['source_prose_reviewed_counts_by_file']['/COMMON/MESFILE.DK4'] += 11
    ledger['reviewed_but_incomplete_COMMON_IDs'] = sorted(ledger['reviewed_but_incomplete_COMMON_IDs'] + IDS)
    drafts = ledger['active_source_prose_drafts']
    drafts['native_message_IDs'] = sorted(drafts['native_message_IDs'] + IDS)
    drafts['manuscripts'].append(str(OUT))
    drafts['manuscript_record_subsets_pending'][str(OUT)] = IDS
    ledger['coverage_units'].append({'id': 'Shared-Search-reports11-source-prose', 'native_message_IDs': IDS,
                                     'status': 'source-context-prose-reviewed;native-font-release-and-revised-gameplay-pending',
                                     'manuscript': str(OUT), 'completed_entries_added': 0})
    ledger['formatting_watchlist']['Search_reports11'] = {'status': 'source-prose-only;not-integrated',
        'manuscript': str(OUT), 'native_message_IDs': IDS, 'native_roles1_and7_and_modal_are_distinct': True,
        'preserve_two_fullwidth_amounts_water_then_food': True, 'no_authored_indents_LFs_or_trailing_padding_in_new_prose': True,
        'full_native_fonts_compiler_bounds_copies_patch_and_actual_revised_scenes_pending': True}
    ledger['latest_checkpoint'] = 'V1653 source/prose reviews11 Search reports:1350 complete,1519 source/prose reviewed,169 reviewed-incomplete COMMON. Hot-spring14 still pending actual optional branch;V1637 experimental,V1492 promoted. Separate graphics/all18 plaques and broader editorial goal open.'
    receipt = ROOT / 'source_prose_review_receipt.json'
    ledger['research_checkpoints'].append({'id': 'V1653-Search-reports11-source-prose', 'proof': str(receipt),
                                           'source_prose_reviews_added': 11, 'completed_entries_added': 0, 'full_goal_complete': False})
    save(ledger_path, ledger)
    save(receipt, {'manuscript': str(OUT), 'manuscript_sha256': sha(OUT.read_bytes()), 'source_context': str(context_path),
                   'source_context_sha256': sha(context_path.read_bytes()), 'completed': 1350, 'source_prose': 1519,
                   'reviewed_incomplete_COMMON': 169, 'completed_entries_added': 0,
                   'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('Reviewed11 Search reports against clean Japanese:1519 source/prose,1350 complete,169 pending. Natural drafts preserve omitted return/hearsay,water-food amounts and original roles. Formatting/release/gameplay remain pending.')
