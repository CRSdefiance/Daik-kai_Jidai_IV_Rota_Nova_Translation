"""All original B74 relative skips in clean and current native parsers."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = Path('scripts/prove_lil_london_branches_v1885.py')
SOURCE_SHA = '620a8a7728a3d3aa1981d216e02c7a7b404b8c9eda2e5ec60b5126c31bd34e10'

if __name__ == '__main__':
    assert sha(SOURCE.read_bytes()) == SOURCE_SHA
    text = SOURCE.read_text(encoding='utf-8')
    changes = {
        'lil_London_branches_v1885':'lil_Hamburg_branches_v1957',
        'work/analysis/lil_London_source_v1879b/all111_clean_current_native_source_context.json':
            'work/analysis/lil_Hamburg_source_v1949/all79_source_native_context_and_two_choices.json',
        "'block':26":"'block':74",
    }
    for old,new in changes.items():
        assert text.count(old) == 1,old
        text = text.replace(old,new)
    exec(compile(text,str(SOURCE),'exec'),{'__name__':'__main__','__file__':__file__})
