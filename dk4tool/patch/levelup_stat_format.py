"""Registered, source-owned stat-result formatting; unchanged prose and assets."""

from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.ceremony_editorial import current_entries as previous_entries
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts.levelup_format_runtime_v819 import BASE,START,END,HOOK,apply,assembled
from scripts.verify_village_wrap_v608 import read

CONFIG='translations/levelup_stat_format_release_v1.json'


def current_entries(common,arm):
    cfg=read(CONFIG)
    assert sha(common)==cfg['common_sha256'] and sha(arm)==cfg['target_arm9_sha256']
    restored=bytearray(arm)
    for row in cfg['owned_patches']:
        at=row['address']-BASE;before=bytes.fromhex(row['before_hex']);after=bytes.fromhex(row['after_hex'])
        assert arm[at:at+len(after)]==after
        restored[at:at+len(before)]=before
    assert sha(bytes(restored))==cfg['source_arm9_sha256']
    return previous_entries(common,bytes(restored))


def apply_release(common,arm,path):
    cfg=read(path);assert cfg['format']=='dk4-levelup-stat-format-v1'
    assert sha(common)==cfg['common_sha256'] and sha(arm)==cfg['source_arm9_sha256']
    for name,h in cfg['dependencies'].items():assert sha(Path(name).read_bytes())==h,name
    new=apply(arm);assert sha(new)==cfg['target_arm9_sha256']
    before,after=[MainCodeFile(a,BASE) for a in (arm,new)]
    assert [(s.ramAddress,len(s.data),s.bssSize) for s in before.sections]==[(s.ramAddress,len(s.data),s.bssSize) for s in after.sections]
    assert cache_plan(arm)==cache_plan(new)
    assert all(bytes(a.data)==bytes(b.data) for a,b in zip(before.sections[1:],after.sections[1:],strict=True))
    assert len(after.sections[3].data)-48==123040
    assert new[0x7E240:0x7E244]==arm[0x7E240:0x7E244]
    assert new[0x7E4C0:0x7E4C4]==arm[0x7E4C0:0x7E4C4]
    header=read(cfg['header_proof']);compound=read(cfg['compound_proof']);parent=read(cfg['full_parent_proof'])
    assert header['count']==634 and compound['count']==4095 and parent['count']==48
    assert parent['maximum_actual_native_builder_rows']==6
    assert len(compound['full_native_fonts'])==63 and compound['maximum_output_bytes']==151
    assert all(c['original_tail_print_once'] and c['ABI_RNG_768_byte_ownership_and_canaries_pass'] for c in compound['cases'])
    gameplay=read(cfg['ordinary_gameplay_proof']);maximum=read(cfg['maximum_gameplay_proof'])
    assert len(gameplay['complete_stat_holds'])==2 and len(gameplay['whole_screen_controls'])==17
    assert len(gameplay['state_pairs'])==19 and gameplay['synthetic_growth_not_used_in_this_run']
    assert maximum['maximum_six_stat_rows_paginate_four_then_two']
    assert len(maximum['complete_actual_page_holds'])==4
    prior=previous_entries(common,arm);final=current_entries(common,new)
    assert len(prior)==len(final)==3668 and all(a.text==b.text for a,b in zip(prior,final,strict=True))
    return new,dict(source_arm9_sha256=sha(arm),target_arm9_sha256=sha(new),common_sha256=sha(common),
        changed_records=[],owned_code_span=[START,END],compound_callsite=HOOK,helper=assembled()[1],
        all3668_COMMON_strings_including676_677_and335_336_exact=True,
        original_source_owned_768_byte_local_buffer_capacity_preserved=True,
        no_staged_payload_cache_BSS_arena_or_other_section_growth=True,
        all_other_ARM9_bytes_exact_and_both_test_fixture_instructions_absent=True,
        native_header_cases=634,compound_cases=4095,whole_parent_cases=48,native_font_planes=63,
        actual_ordinary_stat_holds=2,ordinary_state_and_PRNG_pairs=19,
        separate_synthetic_six_stat_page_holds=4,
        original_pager_and_actual_A_input_four_plus_two_rows_verified=True,
        original_header97_wording_retained_not_editorially_approved=True,
        ceremony_world_state_issue_remains_open=True,full_goal_complete=False)
