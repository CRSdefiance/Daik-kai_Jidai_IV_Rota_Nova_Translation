"""Create B166 relocation/stored-target successors with the source's single tail end."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B166_relocation_tools_v4092')

if __name__ == '__main__':
    assert not ROOT.exists()
    pairs = []
    pairs.append(derive('scripts/research_lil_B164_relocation_v3986.py',
        'scripts/research_lil_B166_relocation_v4093.py', {
        'Relocate complete speech, actor-style and three-option objects with guards.':
            'Relocate B166 complete speeches and advice labels; preserve eight spans and one tail end.',
        'lil_B164_relocation_v3986': 'lil_B166_relocation_v4093',
        'lil_B164_editorial_manuscript_v9': 'lil_B166_editorial_manuscript_v5',
        'lil_B164_choice_manuscript_v2': 'lil_B166_choice_manuscript_v2',
        'all_routes_combined_v3954': 'all_routes_combined_v4046',
        'assert number==164 and len(end_maps)==2': 'assert number==166 and len(end_maps)==1',
        "        assert end_maps[0]['target_offset']+4<end_maps[1]['target_offset'] # separated advice outcomes,not adjacent suffix":
            "        assert end_maps[0]['source_offset']==2948 # both advice paths rejoin before the sole A000/end",
        "text_records']) for r in results)==47": "text_records']) for r in results)==42",
        "relative_skip_fixups']) for r in results)==4": "relative_skip_fixups']) for r in results)==8",
        "target_native_skip_cases']) for r in results)==20": "target_native_skip_cases']) for r in results)==40",
        "command_map']) for r in results)==61": "command_map']) for r in results)==62",
        '[164]': '[166]',
        'all47speech_and4_relative_operands_preserved': 'all42speech_and8_relative_operands_preserved',
        'all20_relocated_native_skip_cases': 'all40_relocated_native_skip_cases',
        'two_separated_declared_advice_end_words_exact': 'one_declared_tail_end_after_advice_rejoin_exact',
        '61commands/47speech/one2100/4spans/20targetskipcases,two separated endwords,inversebytes and335otherblocks exact.':
            '62commands/42speech/one2100/8spans/40targetskipcases,one tail end,inversebytes and335otherblocks exact.',
    }))
    pairs.append(derive('scripts/prove_lil_B164_stored_v3987.py',
        'scripts/prove_lil_B166_stored_v4094.py', {
        'lil_B164_stored_v3987': 'lil_B166_stored_v4094',
        'lil_B164_editorial_manuscript_v9': 'lil_B166_editorial_manuscript_v5',
        'lil_B164_relocation_v3986': 'lil_B166_relocation_v4093',
        'lil_B164_voices_v3963': 'lil_B166_voices_v4056',
        '[2,9,13]': '[2,9,20,23]',
        'len(cases)==47': 'len(cases)==42', 'fresh+reused==188': 'fresh+reused==168',
        'all47_final_stored_targets188': 'all42_final_stored_targets168',
        'current_final_stored_macro_alignment_cases=188': 'current_final_stored_macro_alignment_cases=168',
        'all47_final_targets': 'all42_final_targets',
        'Bind all47 final stored targets': 'Bind all42 final stored targets',
        'stored_targets=47,progressive=47,FE=0,macro_cases=188':
            'stored_targets=42,progressive=42,FE=0,macro_cases=168',
    }))
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(tools=pairs, source_scope=dict(block=166, speeches=42,
        choice_labels=2, commands=62, relative_sites=8, target_skip_cases=40, stored_macro_cases=168,
        single_tail_end=2948, FI=3, static_actors=[2,9,20,23]), no_ROM_registry_ledger_completion_change=True))
    print('B166 source-bound relocation and stored-target proof successors created.')
