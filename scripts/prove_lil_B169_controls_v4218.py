"""Bind three source membership predicates, five opaque leaves and all eight path shapes."""
import inspect
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_lil_B139_B140_conditionals_v3461c import probe
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/lil_B169_controls_v4218')
SOURCE = Path('work/analysis/lil_B169_source_v4211/all36_clean_current_complete_context.json')
BRANCH = Path('work/analysis/lil_B169_branches_v4215/original_relative_skip_operand_proof.json')
if __name__ == '__main__':
    assert not ROOT.exists()
    packet, branch = read(SOURCE), read(BRANCH)
    group = packet['blocks'][0]
    image = NdsImage.open(packet['current_ROM'])
    block = IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[169]
    leaves, pred_commands = [], []
    for clean, current in zip(group['all_clean_native_commands'], group['all_current_native_commands'], strict=True):
        if clean['word'] in [0x4000,0x100,0x200,0x300,0x400]:
            continue
        assert clean['whole_command_hex'] == current['whole_command_hex']
        leaves.append(dict(block=169,offset=clean['offset'],word=clean['word'],native_extent=clean['native_extent'],source_current_hex=clean['whole_command_hex']))
        if clean['word'] == 0x8000:
            pred_commands.append(current)
    assert len(leaves) == 5
    assert [(row['offset'],row['whole_command_hex']) for row in pred_commands] == [(1136,'0080ffff06fe0030'),(1234,'0080ffff15fe0030'),(1320,'0080ffff14fe0030')]
    assert [(row['offset'],row['source_current_hex']) for row in leaves if row['word'] == 0xA000] == [(2550,'00a0ffff29000100')]
    assert [row['offset'] for row in leaves if row['word'] == 0] == [2558]
    ROOT.mkdir(parents=True)
    ctx = CurrentContext('work/analysis/lil_B169_voices_v4213/current_native_input.json', packet['historical_snapshot_ROM'], ROOT / 'current_context')
    predicates = []
    for command in pred_commands:
        predicates.append(dict(block=169, **ctx.execute(probe, block, command)))
        ctx.machines.pop()
    assert not ctx.machines
    assert branch['source_context_sha256'] == sha(SOURCE.read_bytes()) and len(branch['cases']) == 120
    commands = {command['offset']: command for command in group['all_clean_native_commands']}
    by_at = {row['source_reference']['header_offset']: row for row in packet['records']}
    def path(julio, ian, fernando):
        cursor, last = 8, 0
        visited, spoken, queries = [], [], []
        while True:
            command = commands[cursor]
            word = command['word']
            visited.append(cursor)
            if word == 0:
                return dict(Julio6_membership_result=julio,Ian21_membership_result=ian,Fernando20_membership_result=fernando,
                    native_command_offsets=visited,spoken_source_record_indices=spoken,membership_query_offsets=queries,
                    source_end_offset=cursor,not_actual_UI_or_full_VM_execution=True)
            if word in [0x100,0x200,0x300,0x400]:
                cases = [row for row in branch['cases'] if row['version'] == 'current' and row['offset'] == cursor and row['last_choice_or_result'] == last]
                assert len(cases) == 1
                cursor = cases[0]['original_next_command_offset']
                continue
            if word == 0x8000:
                queries.append(cursor)
                last = {1136:julio,1234:ian,1320:fernando}[cursor]
            elif word == 0x4000:
                spoken.append(by_at[cursor]['source_record_index'])
            cursor += command['native_extent']
    paths = [path(j,i,f) for j in [0,1] for i in [0,1] for f in [0,1]]
    assert [len(row['spoken_source_record_indices']) for row in paths] == [33,34,34,35,34,35,35,36]
    assert all(row['source_end_offset'] == 2558 and row['membership_query_offsets'] == [1136,1234,1320] for row in paths)
    save(ROOT / 'three_predicates_five_leaves_and_eight_source_paths.json', dict(candidate=packet['current_ROM'],candidate_sha256=packet['current_ROM_sha256'],
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),source_predicate_cases=predicates,
        original_Julio6_Ian21_Fernando20_membership_queries=True,complete_source_membership_paths=paths,
        all5_source_current_nonrelative_nonspeech_leaves=leaves,source_owned_membership_adapter=inspect.getsource(probe),
        source_declared_end_offsets=[2558],one_later_A000_at2550_after_give_and_take_and_before_end=True,
        A000_source_numeric_arguments_29_0001_preserved_without_recruitment_or_earned_flag_claim=True,
        no_source_FE_2100_4100_2000_resources_or_other_presentation_commands=True,
        source_A000_full_effect_VM_natural_eligibility_and_actual_displays_unexecuted_by_these_probes=True,
        native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(path):sha(path.read_bytes()) for path in [SOURCE,BRANCH,Path(__file__)]},new_emulator_runs=0,
        source_prose_or_completion_credit_added=0,no_ROM_registry_ledger_change=True,full_goal_complete=False))
    print(dict(predicates=[row['native_result'] for row in predicates],source_relative_cases=120,leaves=5,
        path_speech_counts=[len(row['spoken_source_record_indices']) for row in paths],effect_and_actual_display_unexecuted=True,credit=0))
