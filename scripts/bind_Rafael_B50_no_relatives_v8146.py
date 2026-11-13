"""Bind the genuinely empty relative-operand set; do not manufacture branch-case coverage."""
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B50_archive_tools_v8146')
CURRENT=Path('work/analysis/Rafael_B50_current_v8136/all28_complete_source_current_refs_before_new_English_manuscript.json')
SOURCE=Path('work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json')
if __name__=='__main__':
    assert not ROOT.exists();current,source=map(read,[CURRENT,SOURCE]);g=current['groups'][0]
    assert g['block']==50 and len(g['all_source_commands'])==len(g['all_current_commands'])==37
    pairs=[]
    for a,b in zip(g['all_source_commands'],g['all_current_commands'],strict=True):
        assert a['word']==b['word'] and a['word'] not in [0x100,0x200,0x300,0x400,0x8000,0x8100]
        assert not a['ancestor_0100_offsets'] and not b['ancestor_0100_offsets']
        if a['word']!=0x4000:assert a['whole_command_hex']==b['whole_command_hex'];pairs.append(dict(source=a,current=b))
    assert len(pairs)==9 and source['no_relative_sites_or_raw_predicates_queries_in_this_source_block']
    ROOT.mkdir(parents=True);save(ROOT/'zero_source_current_relative_operands37_commands_nine_nontext_pairs.json',dict(
        current_packet=str(CURRENT),current_packet_sha256=sha(CURRENT.read_bytes()),source_controls=str(SOURCE),source_controls_sha256=sha(SOURCE.read_bytes()),
        current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],operands_requiring_adjustment_when_resizing=[],source_native_relative_skip_cases=[],source_relative_site_count=0,native_relative_cases=0,
        all37_source_current_command_words_andempty_ancestors_bound=True,all_nine_nontext_source_current_pairs=pairs,
        no_relative_orpredicate_execution_claim_for_absent_commands=True,source_effects_item_andscene_bodies_not_newly_executed=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [CURRENT,SOURCE,Path(__file__)]}))
    print('B50 zero relative/predicate/query sites bound across37source/current commands;nine opaque nontext pairs exact.No fabricated branch cases.')
