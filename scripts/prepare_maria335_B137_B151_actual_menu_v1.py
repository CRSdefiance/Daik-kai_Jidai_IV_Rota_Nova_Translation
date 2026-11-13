"""Select the repaired captions with their complete native proof, without replay."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria330_actual_menu_v1.py').read_text(encoding='utf-8'),{
    'scripts.meaning_maria330_clean_v1':'scripts.meaning_maria335_B137_B151_v1',
    "r['block']==102 and r['source_command_offset']==210":"r['block']==138 and r['source_command_offset']==1274",
    'records=rows,blocks=[102]':'records=rows,blocks=[138]',
    'B102 captions':'B138 captions',
})
if __name__=='__main__':exec(compile(source,__file__+'::same-exact-caption-projection-no-provider-replay','exec'),globals())
