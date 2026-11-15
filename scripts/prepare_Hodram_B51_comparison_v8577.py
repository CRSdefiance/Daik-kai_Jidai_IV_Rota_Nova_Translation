"""Preserve original bounded timing/RNG/state/RGB comparisons for observed B51."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import save

if __name__ == '__main__':
    root = Path('work/analysis/Hodram_B51_comparison_tools_v8577')
    assert not root.exists()
    source = Path('scripts/compare_Hodram_B50_actual_v8509.py').read_text('utf-8')
    oldscope = source[source.index('        for g in [old,new]:'):source.index('        reports=')]
    newscope = '''        for g in [old,new]:
            assert len(g['command_pairs'])==23 and len({s['id'] for s in g['speeches']})==4
            assert [s['id'] for s in g['speeches']]==['DK4_MES_B51_R0006','DK4_MES_B51_R0010','DK4_MES_B51_R0014','DK4_MES_B51_R0039']
            assert all(s['kind']=='progressive' and s['source_selector']!=254 for s in g['speeches'])
            queries=[c for c in g['command_pairs'] if c['word'] in [0x8000,0x8100]]
            assert [(q['canonical_source_offset'],q['word'],q['native_result']) for q in queries]==[(230,0x8100,[2,0]),(242,0x8000,[2,0])]
            assert [c['canonical_source_offset'] for c in g['command_pairs'] if c['source_command_ordinal'] is not None]==[8,10,12,106,132,230,234,242,250,258,294,318,326,334,336]
'''
    resource = source[source.index('        if number==50:'):source.index('        sheet=Image.new')]
    result = derive('scripts/compare_Hodram_B50_actual_v8509.py', 'scripts/compare_Hodram_B51_actual_v8577.py', {
        'Hodram_B50_comparison_v8509': 'Hodram_B51_comparison_v8577',
        'Hodram_B50_actual_v8507': 'Hodram_B51_actual_v8576',
        'for number in [50]': 'for number in [51]',
        "len(old['unvisited_conditional_text_IDs'])==0": "old['unvisited_conditional_text_IDs']==['DK4_MES_B51_R0032']",
        "len(old['speeches'])==len(new['speeches'])==3": "len(old['speeches'])==len(new['speeches'])==4",
        oldscope: newscope,
        resource: '',
        'original4800_4700_actual=resource': 'source_has_no_picture_orhide_sites=True',
        'current_registered_V8475_andmainV4701_unchanged': 'current_registered_V8543_andmainV4701_unchanged',
    })
    root.mkdir(parents=True)
    save(root / 'derivation.json', dict(derivation=result, all_native_addresses_metrics_andhigh_constant_multiplicity_preserved=True,
        four_observed_speeches_both_original_unforced_queries_andcomplete_path_are_required=True,
        Charles_conditional_line_recorded_unvisited_not_forced=True,
        no_capture_replay_state_seed_result_orinput_retiming=True, no_ROM_write_orcredit=True))
