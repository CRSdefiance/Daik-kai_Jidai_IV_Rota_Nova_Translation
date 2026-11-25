"""Compare the compact transcription with original caller,context and wait logic."""
from pathlib import Path
import inspect
import struct

from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_PC, UC_ARM_REG_LR

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import research_duel_scope_names_v1117b as original
from scripts.duel_renderer_thumb_v1124 import START, END, ROOT as PROPOSAL
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_thumb_equivalence_v1124')
BASE = 0x02000000


def runner(arm, raw, replacement, proposed, delay, key, font_return):
    observations = []

    def machine(source, snapshot):
        cpu, get = get_machine(source, snapshot)
        if proposed:
            cpu.mem_write(START, replacement)
        events, contexts = [], []

        def engine(u, pc, size, data):
            args = [u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)]
            events.append({'entry': pc, 'arguments': args})
            u.reg_write(UC_ARM_REG_R0, key if pc == BASE + 0xCF534 else 0)
            u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

        for pc in (0xCA890, 0xC9D98, 0xCF534, 0xC9C48):
            cpu.hook_add(UC_HOOK_CODE, engine, begin=BASE + pc, end=BASE + pc)

        def capture(u, pc, size, data):
            context = u.reg_read(UC_ARM_REG_R0)
            contexts.append({'complete_native_context_hex': bytes(u.mem_read(context, 0x4C)).hex(),
                             'complete_private_widget_hex': bytes(u.mem_read(0x02460214, 0x200)).hex()})

        cpu.hook_add(UC_HOOK_CODE, capture, begin=BASE + 0xD5404, end=BASE + 0xD5404)
        observations.append({'engine_calls': events, 'native_contexts': contexts, 'cpu': cpu})
        return cpu, get

    text=inspect.getsource(original.execute)
    changes={'BASE + 0xDAC4':str(font_return),
             'sp + 0x47C':f'sp + {0x47C}',
             'sp + 0x4A4':f'sp + {0x4A4}',
             'controller, side, 60,':f'controller, side, {delay},'}
    for before,after in changes.items():
        assert text.count(before)==1,before
        text=text.replace(before,after)
    namespace={**original.execute.__globals__,'get_machine':machine,
               'selected_scope':lambda lr,parent,table:lr==font_return and
               parent==BASE+0xD4BC and table in original.TABLES}
    exec(compile(text,'explicit_source_scoped_duel_caller_probe','exec'),namespace)
    function=namespace['execute']
    return function, observations


def main():
    assert not ROOT.exists()
    plan = read(PROPOSAL / 'assembly_proposal.json')
    arm = NdsImage.open(original.ROM).read_file('/__arm9__.bin')
    proposed = (PROPOSAL / 'proposed_ARM9_RESEARCH_ONLY.bin').read_bytes()
    assert sha(arm) == plan['source_ARM9_sha256'] and sha(proposed) == plan['research_ARM9_sha256']
    replacement = proposed[START - BASE:END - BASE]
    instructions = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(replacement[8:plan['transcription_bytes']], START + 8))
    calls = [instruction for instruction in instructions
             if instruction.mnemonic == 'blx' and instruction.op_str == '#0x20d5404']
    assert len(calls) == 1
    font_return = (calls[0].address + calls[0].size) | 1
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    records = {row['message_id']: row for row in read('translations/duel_editorial_manuscript_v3.json')['records']}
    tables = {'challenge': 0x02117340, 'acceptance': 0x02117360, 'threat': 0x021174E0,
              'named_escape_negative': 0x02117500, 'admiral_escape_negative': 0x02117620}
    cpu, get = get_machine(arm, raw)
    representatives = {}
    for row in catalog['names']:
        for family, table in tables.items():
            number = get(0x53F4C, row['object'], table)
            representatives.setdefault((family, number), (row['object'], bytes.fromhex(row['name_hex'])))
    corpus = [(family, tables[family], number, obj, name, False)
              for (family, number), (obj, name) in sorted(representatives.items())]
    obj, name = representatives[('challenge', 1931)]
    corpus += [('direct_negative', 0, number, obj, name, True) for number in range(1931, 1951)]
    assert len(corpus) == 53
    results = []
    ROOT.mkdir(parents=True)
    for timing, delay, key in (('timed60', 60, 0), ('wait61_no_key', 0, 0), ('wait_key_first', 0, 1)):
        source_call, source_observations = runner(arm, raw, replacement, False, delay, key, BASE + 0xDAC4)
        target_call, target_observations = runner(arm, raw, replacement, True, delay, key, font_return)
        for family, table, number, obj, name, direct in corpus:
            text = records[number]['english'].encode('ascii')
            a = source_call(arm, raw, obj, name, family, table, number, text, direct=direct)
            b = target_call(arm, raw, obj, name, family, table, number, text, direct=direct)
            left, right = source_observations[-1], target_observations[-1]
            assert len(left['native_contexts']) == len(right['native_contexts']) == 1
            assert left['native_contexts'] == right['native_contexts'], (timing, family, number, 'native context/widget differs')
            assert left['engine_calls'] == right['engine_calls'], (timing, family, number, 'wait logic differs')
            assert a['expanded_hex'] == b['expanded_hex'] and a['selected_by_proposed_scope'] == b['selected_by_proposed_scope']
            assert bytes(left['cpu'].mem_read(0x02460214, 0x200)) == bytes(right['cpu'].mem_read(0x02460214, 0x200))
            if timing == 'timed60':
                assert not left['engine_calls']
            elif timing == 'wait61_no_key':
                assert len(left['engine_calls']) == 61 * 3
            else:
                assert len(left['engine_calls']) == 4 and left['engine_calls'][-1]['entry'] == BASE + 0xC9C48
                assert left['engine_calls'][-1]['arguments'][0] == 0x9F0
            results.append({'timing': timing, 'family': family, 'message_ID': number,
                'native_context_and_complete_widget_before_and_after_exact': True,
                'native_expanded_text_exact': True, 'full_callee_saved_and_stack_ABI_pass': True,
                'same_original_wait_or_key_branch_calls_and_arguments': len(left['engine_calls']),
                'source_font_return': a['font_return'], 'research_font_return': b['font_return']})
            # Release CPU objects promptly;retain all verification facts.
            left.pop('cpu'); right.pop('cpu')
        print(f'Original/research{timing}:53 caller/context/wait pairs pass.', flush=True)
    assert len(results) == 159
    save(ROOT / 'original_vs_thumb_equivalence.json', {
        'source_proposal': str(PROPOSAL / 'assembly_proposal.json'), 'source_ARM9_sha256': sha(arm),
        'research_ARM9_sha256': sha(proposed), 'cases': results,
        'all159_original_vs_research_context_widget_macro_scope_and_timing_pairs_pass': True,
        'original_function308_research_transcription200_remaining_tail108': True,
        'original_stack_footprint_and_all76_allocated_context_bytes_exact':True,
        'earlier80byte_probe_read4bytes_beyond_original_context_allocation':True,
        'new_Thumb_font_return': font_return, 'new_outer_parent_font_SP_offset': 0x47C,
        'new_saved_voice_table_font_SP_offset': 0x4A4,
        'boundary_models': ['reviewed native-message CPU loader', 'SDK clear', 'widget registration',
                            'font entry capture', 'engine yield/event/key/sound boundaries'],
        'timing_control_models_match_both_paths_not_actual_engine_or_gameplay_verification': True,
        'remaining_tail_not_yet_approved_without_incoming_reference_and_ownership_census': True,
        'earlier_multiline_counterexample':'work/analysis/duel_renderer_thumb_v1123/multiline_condition_failure.json',
        'Thumb_MOVS_precedes_CMP_so_BNE_uses_original_line_count_condition':True,
        'no_formatter_implementation_ROM_registry_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('159 paired native transcription checks pass;ownership and formatter still pending.')


if __name__ == '__main__':
    main()
