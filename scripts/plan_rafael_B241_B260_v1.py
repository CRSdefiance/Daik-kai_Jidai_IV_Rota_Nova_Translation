"""Prepare the first native Rafael B241–B260 body wraps and keep two signature footers separate."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text
from scripts import write_rafael_B241_B260_contextual_v1 as batch

parent = Path(__file__).with_name('plan_rafael_B221_B240_v1.py')
source = checked_text(parent.read_text(encoding='utf-8'), {
    'from scripts.write_rafael_B221_B240_contextual_v1 import BLOCKS, OUT as PROSE, ROOT, digest':
        'from scripts.write_rafael_B241_B260_contextual_v1 import BLOCKS, OUT as PROSE, ROOT\nfrom scripts.write_rafael_B221_B240_contextual_v1 import digest',
    "CURRENT = ROOT / 'current_effective.json'": "CURRENT = ROOT / 'current_effective.json/current_effective.json'",
    '(259, 4, 7)': '(284, 2, 6)',
    "STYLE for row in ordinary) == 29": "STYLE for row in ordinary) == 14",
    "row['kind'] == 'system-FE' for row in ordinary) == 2": "row['kind'] == 'system-FE' for row in ordinary) == 7",
    "'ordinary_speech_objects': 230, 'style_physical_speech_objects': 29, 'style_command_objects': 4":
        "'ordinary_speech_objects': 270, 'style_physical_speech_objects': 14, 'style_command_objects': 2",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::native-formatting-for-current-batch','exec'),globals())

