"""Fresh shipped entry census and123-command/20-span B74 mapping."""
from pathlib import Path

SOURCE = Path('scripts/verify_lil_speyer_references_v1931.py')

if __name__ == '__main__':
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'scripts.prepare_lil_speyer_research_v1929':'scripts.prepare_lil_hamburg_research_v1961',
        'lil_Speyer_reference_census_v1931':'lil_Hamburg_reference_census_v1963',
        'work/analysis/lil_Speyer_loader_v1930/whole_SC2_and_B25_B128_initial_entry_proof.json':
            'work/analysis/lil_Hamburg_loader_v1962/whole_SC2_and_B74_initial_entry_proof.json',
        'if n not in (25,128)':'if n != 74',
        'expected = 15 if number==25 else 122':'expected = 123',
        '(8 if number==25 else 40)':'20',
        '==137':'==123',
        '==48':'==20',
        '==240':'==100',
        'all137_commands48_relative_sites_and_shipped_entry_census.json':'all123_commands20_relative_sites_and_shipped_entry_census.json',
        'all334_other_SC2_blocks_preserved':'all335_other_SC2_blocks_preserved',
        'all137_clean_current_target_commands_and48_relative_sites_reexecuted':'all123_clean_current_target_commands_and20_relative_sites_reexecuted',
        'native_commands_each=137,relative_sites=48,target_native_skip_cases=240':'native_commands_each=123,relative_sites=20,target_native_skip_cases=100',
    }
    for old,new in changes.items():
        assert text.count(old) == 1,(old,text.count(old))
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
