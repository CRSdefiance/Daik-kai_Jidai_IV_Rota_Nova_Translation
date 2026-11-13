"""Use the observer's actual commands.json path;preserve the first runner draft."""
from pathlib import Path
if __name__=='__main__':
    draft=Path('scripts/run_lil_B164_display_fixture_v3993.py');text=draft.read_text(encoding='utf-8');assert text.count("'native_script_observation.json'")==1;text=text.replace("'native_script_observation.json'","'commands.json'");exec(compile(text,__file__,'exec'),dict(__name__='__main__',__file__=__file__))
