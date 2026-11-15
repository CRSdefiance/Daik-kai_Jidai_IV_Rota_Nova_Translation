"""Clean source and original consumers for Market advice and contract refusal."""

import struct
from pathlib import Path

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R5, UC_ARM_REG_R6, UC_ARM_REG_R7, UC_ARM_REG_R11, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/market_contract_v758')
CURRENT = Path('out/all_routes_combined_v757_candidate.nds')
IDS = tuple(range(754, 762))
TEXT = {
    754: 'This time, we may be able to get larger quantities of certain goods by paying double.',
    755: "Looks like they'll sell us larger quantities of some goods this time if we pay double.",
    756: 'I think we can buy larger quantities of some goods this time by paying double.',
    757: 'Looks like we can get bigger quantities of some goods right now by paying double.',
    758: "It seems they'll sell us larger quantities of some goods this time if we pay double.",
    759: "If we pay double, I bet they'll sell us lots more of some goods this time!",
    760: 'It appears we can buy larger quantities of certain goods this time by paying double.',
    761: 'Sorry. Please sign a contract at the %s, then come back.',
}
GLOSS = {
    754: 'Polite adviser: there seem to be certain goods this time that the merchant will sell in larger quantities if double the money is paid.',
    755: 'Conversational adviser: there seem to be certain goods this time that the merchant will sell in larger quantities if double the money is paid.',
    756: 'Conversational feminine-register adviser: there seem to be certain goods this time that can be bought in larger quantities if double the money is paid.',
    757: 'Rough informal adviser: right now there seem to be certain goods that can be bought in larger quantities if double the money is paid.',
    758: 'Older measured-register adviser: there seem to be certain goods this time that the merchant will sell in larger quantities if double the money is paid.',
    759: 'Upbeat youthful-register adviser: thinks there are certain goods this time that the merchant will sell in large quantities if double the money is paid.',
    760: 'Older polite-register adviser: there seem to be certain goods this time that the merchant will sell in larger quantities if double the money is paid.',
    761: 'Merchant apologetically refuses and asks the player to make a contract at the supplied governor office or palace before returning.',
}


def context_cases(arm):
    u = machine(arm)
    voices = []
    for index in range(8):
        def choose(cpu, address, size, unused):
            if address == BASE + 0x7E988:
                cpu.reg_write(UC_ARM_REG_R0, index)
                cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
        hook = u.hook_add(UC_HOOK_CODE, choose)
        try:
            call(u, 0x53F4C, (3, 0x02118480))
        finally:
            u.hook_del(hook)
        selected = u.reg_read(UC_ARM_REG_R0)
        assert selected == (754 if index in (0, 1) else 753 + index)
        voices.append({'supplied_original_voice_index': index, 'selected_message': selected})
    conditions = []
    for available in (0, 1):
        u.reg_write(UC_ARM_REG_R0, available)
        calls = []
        def stop(cpu, address, size, unused):
            if address == BASE + 0x53D44:
                calls.append([cpu.reg_read(UC_ARM_REG_R0), cpu.reg_read(UC_ARM_REG_R1)])
                cpu.emu_stop()
            elif address == BASE + 0xBB26C:
                cpu.emu_stop()
        hook = u.hook_add(UC_HOOK_CODE, stop)
        try:
            u.emu_start(BASE + 0xBB258, BASE + 0xBB26C + 4, count=20)
        finally:
            u.hook_del(hook)
        assert calls == ([[3, 0x02118480]] if available else [])
        conditions.append({'supplied_extra_stock_predicate': available, 'native_voice_dispatch': calls})
    refusal = []
    for flag, literal in ((0, 0xBA47C), (64, 0xBA480)):
        # Original B507C(town,6) returns either0 or64; its result is supplied.
        # BA318..334 initializes object state and conditionally chooses Palace.
        governor = struct.unpack_from('<I', arm, 0xBA47C)[0]
        u.reg_write(UC_ARM_REG_R0, flag)
        u.reg_write(UC_ARM_REG_R5, governor)
        u.reg_write(UC_ARM_REG_R11, 0x02450000)  # sb is r9, set separately below
        from unicorn.arm_const import UC_ARM_REG_R9
        u.reg_write(UC_ARM_REG_R9, 0x02450000)
        u.emu_start(BASE + 0xBA318, BASE + 0xBA334, count=30)
        pointer = u.reg_read(UC_ARM_REG_R5)
        assert pointer == struct.unpack_from('<I', arm, literal)[0]
        raw = bytes(u.mem_read(pointer, 64)).split(b'\0')[0]
        u.reg_write(UC_ARM_REG_R6, 0x02451000)
        u.reg_write(UC_ARM_REG_R11, 761)
        seen = []
        def offer(cpu, address, size, unused):
            if address == BASE + 0x53FE4:
                seen.append([cpu.reg_read(UC_ARM_REG_R1), cpu.reg_read(UC_ARM_REG_R2)])
                cpu.emu_stop()
        hook = u.hook_add(UC_HOOK_CODE, offer)
        try:
            u.emu_start(BASE + 0xBA41C, BASE + 0xBA42C, count=20)
        finally:
            u.hook_del(hook)
        assert seen == [[761, pointer]]
        refusal.append({'supplied_facility_bit6': flag, 'argument_hex': raw.hex(), 'pointer': pointer, 'native_call': seen[0]})
    return {'voice_index_cases': voices, 'advice_predicate_cases': conditions, 'contract_facility_cases': refusal}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    current, clean, canonical = [NdsImage.open(p) for p in (CURRENT, 'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds')]
    assert sha(CURRENT.read_bytes()) == read('out/editorial_review_latest.json')['sha256']
    arms = [r.read_file('/__arm9__.bin') for r in (clean, current)]
    spans = ((0xBA2C8, 0xBA494), (0xBB238, 0xBB3C4), (0x53D44, 0x53DCC), (0x53F4C, 0x53F9C))
    assert all(arms[0][a:b] == arms[1][a:b] for a, b in spans)
    source, accepted, before = [common_message_entries(r.read_file('/COMMON/MESFILE.DK4'), r.read_file('/__arm9__.bin'), clean=(r is clean)) for r in (clean, canonical, current)]
    jp, en = map(context_cases, arms)
    assert jp['voice_index_cases'] == en['voice_index_cases'] and jp['advice_predicate_cases'] == en['advice_predicate_cases']
    save(ROOT / 'native_context.json', {'source_ROM': 'work/clean.nds', 'source_sha256': sha(clean.source.read_bytes()),
        'current_ROM': str(CURRENT), 'current_sha256': sha(CURRENT.read_bytes()), 'source': jp, 'current': en,
        'unchanged_executable_spans': [{'lo': a, 'hi': b, 'sha256': sha(arms[0][a:b])} for a, b in spans],
        'supplied_indices_predicates_and_facility_flags_not_earned_advice_or_contract_progress': True,
        'Govt_is_source_governor_office_not_city_argument': True, 'producer_sha256': sha(Path(__file__).read_bytes())})
    records = []
    for n in IDS:
        records.append({'id': f'COMMON_MESSAGE_{n}', 'message_id': n, 'source_hex': source[n].text.hex(),
            'japanese': source[n].text.decode('cp932'), 'canonical_source_hex': accepted[n].text.hex(),
            'current_text_hex': before[n].text.hex(), 'current_English': before[n].text.decode('cp932'),
            'english': TEXT[n] + '{PAD}', 'source_meaning': GLOSS[n], 'decision': 'revise',
            'localization_note': ('Preserve uncertainty, larger quantities of only certain goods, double payment and current occasion. Use the source register without assigning an unverified character identity.' if n < 761 else
                                  'Restore the return instruction and natural at the location. The native argument is Palace or governor office, not a town. Expand Govt only in this bound dialogue provider; retain other UI text. Generated wrapping budgets both full names.'),
            'speaker': 'Original fleet adviser selected by native voice chooser' if n < 761 else 'Original contextual Market Trader',
            'context': ('Original BB238 uses predicate BAA74 and dispatches voice table2118480 with role3 through53D44. Original53F4C maps eight voice results onto seven advice texts, including the missing-index fallback. Not all actual advice prerequisites are claimed.' if n < 761 else
                        'Original BA2C8 selects governor office/Palace through town flag6. Trade menu choice0 with no local market share reaches BA41C, passing761 and the building pointer to53FE4; actual old Palace refusal appears in the V754 baseline probe. Source says contract there and return.'),
            'source_reference': {'block': source[n].block, 'record': source[n].record_index, 'offset': source[n].block_offset},
            'current_reference': {'block': before[n].block, 'record': before[n].record_index, 'offset': before[n].block_offset},
            'review': {k: k != 'formatting' for k in ('source', 'context', 'localization', 'naturalness', 'formatting')},
            'status': 'source-context-prose-reviewed-formatting-integration-gameplay-pending'})
    save('translations/market_contract_manuscript_v1.json', {'format': 'dk4-common-entry-manuscript-v1',
        'translation_policy': 'natural-dialogue-v2', 'encoder': 'dialogue-fixed-v1', 'target_locale': 'en-US',
        'review_gates': ['source', 'context', 'localization', 'naturalness', 'formatting'], 'file_path': '/COMMON/MESFILE.DK4',
        'source_clean_COMMON_sha256': sha(clean.read_file('/COMMON/MESFILE.DK4')),
        'source_canonical_COMMON_sha256': sha(canonical.read_file('/COMMON/MESFILE.DK4')),
        'source_ROM_sha256': sha(clean.source.read_bytes()), 'current_ROM_sha256': sha(CURRENT.read_bytes()),
        'context_evidence': str(ROOT / 'native_context.json'), 'records': records, 'status': 'draft-not-integrated'})
    save(ROOT / 'source_and_neighbors.json', [{'id': n, 'japanese': source[n].text.decode('cp932'),
        'current': before[n].text.decode('cp932'), 'source_hex': source[n].text.hex(), 'current_hex': before[n].text.hex()} for n in range(745, 768)])
    save(ROOT / 'unmapped_750_752_prose_DRAFT.json', {'status': 'source-prose-only-context-activation-unmapped',
        'records': [{'id': n, 'source_hex': source[n].text.hex(), 'japanese': source[n].text.decode('cp932'),
                     'current_hex': before[n].text.hex(), 'draft_english': text} for n, text in
                    ((750, 'Are you sure you want to start over?'), (751, 'What a hassle.'), (752, "I'm busy. Spare me the jokes."))],
        'not_integrated_or_counted_complete': True,
        'note': 'No confirmed native activation mapped. Aligned full-word literal scans do not locate751/752;750 has a lone data coincidence. Do not infer unused status or speaker identity from this search alone. Further caller/packed-script context audit remains open.'})
    print('Eight source/consumer-reviewed drafts; three reset/cancellation drafts remain context-unmapped.', flush=True)


if __name__ == '__main__':
    main()
