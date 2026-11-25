"""Correct three historical decimal metadata lists; preserve original ROM command bytes."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_operand_notation_v4243')

if __name__ == '__main__':
    assert not ROOT.exists()
    source = IlnkContainer.parse(NdsImage.open('work/clean.nds').read_file('/data/SC2.DK4')).blocks[169]
    command = source[2550:2558]
    assert command.hex() == '00a0ffff29000100'
    values = list(struct.unpack_from('<2H',command,4))
    assert values == [41,1]
    histories = [
        ('work/analysis/lil_B169_relocation_tools_v4233/source_derivation.json',['source_scope','numeric_A000_operands']),
        ('work/analysis/lil_B169_research_tools_v4235/source_derivation.json',['numeric_A000_operands']),
        ('work/analysis/lil_B169_display_tools_v4241/source_derivation.json',['later_A000_numeric_operands']),
    ]
    corrections = []
    for path,keys in histories:
        obj = read(path)
        for key in keys:
            obj = obj[key]
        assert obj == [29,1]
        corrections.append(dict(path=path,sha256=sha(Path(path).read_bytes()),field=keys,
            historical_erroneous_decimal_list=obj,superseding_decimal_values=values,
            actual_little_endian_operand_hex=['2900','0100'],actual_hex_values=['0029','0001'],
            historical_producer_and_proof_preserved=True))
    relocated = read('work/analysis/lil_B169_relocated_controls_v4240/all36_progressive_dispatches_three_predicates_and5_leaves.json')
    leaves = [r for r in relocated['all5_source_current_target_nonrelative_nonspeech_leaves'] if r['word']==0xA000]
    assert len(leaves)==1 and leaves[0]['source_current_target_hex']==command.hex()
    fixture = read('work/analysis/lil_B169_display_fixture_v4241/complete_effect_preserving_B22_fixtures.json')
    for version in fixture['fixtures']:
        effect = [c for c in version['selected_original_objects'] if c['source_word']==0xA000]
        assert len(effect)==1 and effect[0]['source_offset']==2550 and effect[0]['whole_command_hex']==command.hex()
    ROOT.mkdir(parents=True)
    save(ROOT/'source_A000_hex0029_0001_decimal41_1_metadata_correction.json',dict(
        block=169,clean_command_offset=2550,source_command_hex=command.hex(),
        operand_hex_values=['0029','0001'],operand_decimal_values=values,
        explanation='Source word0029 is hexadecimal41 decimal. Three new derivation metadata lists accidentally treated the displayed hex29 as decimal29. This amendment supersedes only those metadata lists. Existing prose numeric29/0001 means the hexadecimal words; use explicit hex0029/0001 henceforth.',
        historical_corrections=corrections,relocated_and_both_fixture_command_bytes_already_source_exact=True,
        no_recruitment_rank_or_earned_event_flag_semantics_inferred=True,
        no_ROM_prose_registry_ledger_orcredit_change=True,new_emulator_runs=0,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('A000 notation amended:hex0029/0001=decimal41/1. All source/current/relocated/fixture bytes were already exact;historical metadata preserved.')
