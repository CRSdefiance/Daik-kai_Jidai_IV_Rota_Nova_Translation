"""Replay the preserved prose matrix with actual research type-getter outputs."""

import inspect
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts import probe_item_diplomacy_layout_v784 as prior
from scripts.prepare_item_type_provider_v786 import ROOT
from scripts.verify_village_wrap_v608 import read, save

OUT = ROOT/'provider_layouts'
ARM = ROOT/'NOMINAL_PROVIDER_RESEARCH_ONLY.bin'


def initialized(cpu, arm):
    for section in MainCodeFile(arm, 0x02000000).sections:
        cpu.mem_write(section.ramAddress, bytes(section.data))
    cpu.mem_write(0x02387A20, bytes(MainCodeFile(arm, 0x02000000).sections[3].data[:-48]))


def main():
    proof = read(ROOT/'nominal_provider_research.json')
    assert sha(ARM.read_bytes()) == proof['target_research_ARM9_sha256']
    phrases = [row['text'] for row in proof['native_getter_cases'] if row['getter'] == 0x02093D5C and row['type'] < 6]
    assert len(phrases) == 6
    source = inspect.getsource(prior.main)
    replacements = {
        "arm = rom.read_file('/__arm9__.bin')": "arm = ARM.read_bytes()\n    assert sha(arm) == PROVIDER['target_research_ARM9_sha256']",
        "u.mem_write(0x02000000, raw)": "u.mem_write(0x02000000, raw)\n    initialized(u, arm)",
        "phrases = [s.encode('ascii') for s in TYPE_PHRASES]":
            "phrases = [text(get(0x93D5C, (kind,))) for kind in range(6)]\n    assert phrases == [s.encode('ascii') for s in TYPE_PHRASES]",
        "'DRAFT_English_type_phrase_values'": "'actual_research_getter_type_phrase_values'",
        "'these_type_phrases_are_not_current_getter_output'": "'these_research_values_are_not_current_ROM_getter_output'",
        "'type_phrases_are_explicit_proposed_inputs_not_current_getter_output'": "'type_phrases_are_actual_research_getter_outputs_not_current_ROM'",
        "'candidate_sha256'": "'source_candidate_sha256'",
    }
    for before, after in replacements.items():
        assert source.count(before) == 1, before
        source = source.replace(before, after)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT/'effective_layout_producer.py').write_text(source, encoding='utf-8')
    context = {**prior.__dict__, 'ARM': ARM, 'PROVIDER': proof, 'TYPE_PHRASES': phrases,
        'OUT': OUT, 'initialized': initialized, '__file__': str(Path(__file__).resolve())}
    exec(compile(source, __file__, 'exec'), context)
    context['main']()
    verification = read(OUT/'verification.json')
    matrix = read(OUT/'native_layout_matrix.json')
    assert matrix['count'] == 2774 and not matrix['findings']
    assert len(verification['complete_font_planes']) == 76 and len(verification['preview_sheets']) == 7
    verification.update({'research_ARM9_sha256': sha(ARM.read_bytes()),
        'provider_proof': str(ROOT/'nominal_provider_research.json'),
        'provider_proof_sha256': sha((ROOT/'nominal_provider_research.json').read_bytes()),
        'frozen_layout_producer': str(Path(prior.__file__)),
        'frozen_layout_producer_sha256': sha(Path(prior.__file__).read_bytes()),
        'effective_layout_program_sha256': sha(source.encode()),
        'all76_paragraphs_remain_unmodified_V784_manuscript_drafts': True,
        'complete_generic_virtual_consumer_scoped_dispatch_and_gameplay_approval_pending': True})
    save(OUT/'verification.json', verification)
    print('Actual research type-provider values feed2774 native layouts and76 independent fonts. Visual review and production/gameplay gates remain.', flush=True)


if __name__ == '__main__':
    main()
