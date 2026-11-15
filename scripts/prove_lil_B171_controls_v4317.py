"""Bind B171's eight leaves,one resource,C200,four presentation sites and two ends."""
import inspect
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts import prove_lil_B141_controls_v3538b as resource_base
from scripts.prove_lil_B139_C200_v3461e import C200
from scripts.research_wedding_command_v676 import walk
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B171_controls_v4317')
SOURCE = Path('work/analysis/lil_B171_source_v4311/all37_clean_current_complete_context.json')
BRANCH = Path('work/analysis/lil_B171_branches_v4314/original_relative_skip_operand_proof.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    packet, branch = map(read, [SOURCE, BRANCH])
    group = packet['blocks'][0]
    images = [NdsImage.open('work/clean.nds'), NdsImage.open(packet['current_ROM'])]
    blocks = [IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[171] for im in images]
    commands = group['all_current_native_commands']
    assert len(commands) == 45 and sum(c['word'] == 0x4000 for c in commands) == 37
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x2100,0x4100,0x2000,0xA000] for c in commands)
    assert branch['source_context_sha256'] == sha(SOURCE.read_bytes()) and not branch['cases'] and not branch['operands_requiring_adjustment_when_resizing']
    leaves = []
    for a, b in zip(group['all_clean_native_commands'], commands, strict=True):
        if a['word'] == 0x4000:
            continue
        assert a['offset'] == b['offset'] and a['whole_command_hex'] == b['whole_command_hex']
        leaves.append(dict(block=171, offset=a['offset'], word=a['word'], native_extent=a['native_extent'], source_current_hex=a['whole_command_hex']))
    assert [(r['offset'], r['word'], r['source_current_hex']) for r in leaves] == [
        (8,0x6000,'0060'),(10,0x4500,'004500000021'),(1252,0x4621,'21467e80'),(1256,0x61FF,'ff61'),
        (1306,0x6325,'2563'),(2110,0xC200,'00c2'),(2112,0,'00000000'),(2116,0,'00000000')]
    text = inspect.getsource(resource_base.control630A)
    for old, new in [('previous,boundary_return):', 'previous,boundary_return,word):'),
                     ("value=bytes.fromhex('0a63')", "assert word==0x6325;value=struct.pack('<H',word)"),
                     ('[0x02386EFC,10,2,1]', '[0x02386EFC,word&255,2,1]')]:
        assert old in text
        text = text.replace(old, new)
    env = dict(resource_base.__dict__)
    exec(compile(text, __file__ + '::source6325', 'exec'), env)
    ROOT.mkdir(parents=True)
    ctx = CurrentContext('work/analysis/lil_B171_voices_v4312/current_native_input.json', packet['historical_snapshot_ROM'], ROOT / 'current_context')
    resources = []
    for previous in [0,1,2,3,0xFFFFFFFF]:
        for result in [0,0xFFFFFFFF]:
            resources.append(dict(source_word=0x6325, **ctx.execute(env['control630A'], previous, result, 0x6325)))
            ctx.machines.pop()
    ui_command = next(c for c in commands if c['word'] == 0xC200)
    uis = []
    for label, block in zip(['clean','current'], blocks, strict=True):
        uis.append(dict(version=label, **ctx.execute(C200, block, ui_command)))
        ctx.machines.pop()
    assert len(resources) == 10 and not ctx.machines
    assert uis[0]['source_owned_UI_request_words'] == uis[1]['source_owned_UI_request_words'] == [1,0,13,0,0,0,1]
    assert uis[0]['source_owned_UI_writes'] == uis[1]['source_owned_UI_writes']
    structural = []
    for row in [r for r in leaves if r['word'] in [0x6000,0x4500,0x4621,0x61FF]]:
        raw = bytes.fromhex(row['source_current_hex'])
        synthetic = b'CS\0\1' + struct.pack('<H', len(raw)) + bytes(2) + raw
        versions = []
        for label, image in zip(['clean','current'], images, strict=True):
            result = walk(image.read_file('/__arm9__.bin'), synthetic)
            assert result['error'] is None and result['stopped_offset'] == result['logical_end'] == len(synthetic)
            assert len(result['rows']) == 1 and result['rows'][0]['word'] == row['word'] and result['rows'][0]['native_extent'] == row['native_extent']
            versions.append(dict(version=label, **result))
        assert versions[0]['rows'] == versions[1]['rows'] and versions[0]['opaque_effect_bridges'] == versions[1]['opaque_effect_bridges']
        structural.append(dict(source_site=row, versions=versions, isolated_synthetic_offset8_not_original_cursor=True,
            nondecode_callees_bridged_zero_return_not_body_or_display_execution=True))
    assert len(structural) == 4
    save(ROOT / 'one_resource_C200_four_presentations_two_ends_and8_source_leaves.json', dict(
        candidate=packet['current_ROM'], candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE), source_context_sha256=sha(SOURCE.read_bytes()), source_predicate_cases=[],
        all8_source_current_nonrelative_nonspeech_leaves=leaves, one_resource_word10_boundary_cases=resources,
        source_C200_pairs=[dict(block=171, source_offset=2110, cases=uis)], four_presentation_structural_cases=structural,
        source_pause_resume_pairs=[], source_declared_end_offsets=[2112,2116], first_end_terminates_linear_path_second_end_preserved=True,
        source_linear_path_command_offsets=[c['offset'] for c in commands if c['offset'] <= 2112], all37_speeches_on_linear_source_path=True,
        no_source_A000_2000_pause_FE_2100_4100_or_membership_predicate_and_no_relative_sites=True,
        source_4500_4621_61FF_6325_and_C200_whole_commands_preserved=True,
        source_resources_presentation_full_VM_and_actual_displays_unexecuted_by_these_probes=True,
        source_owned_adapters=dict(source6325=text, C200=inspect.getsource(C200), isolated_walk=inspect.getsource(walk)),
        native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p): sha(p.read_bytes()) for p in [SOURCE,BRANCH,Path(__file__)]}, new_emulator_runs=0,
        source_prose_or_completion_credit_added=0, no_ROM_registry_ledger_change=True, full_goal_complete=False))
    print(dict(leaves=8, resource_cases=10, C200_clean_current_pairs=1, presentation_sites=4,
        ends=[2112,2116], no_A000_or2000_pause=True, actual_scene_unexecuted=True, credit=0))
