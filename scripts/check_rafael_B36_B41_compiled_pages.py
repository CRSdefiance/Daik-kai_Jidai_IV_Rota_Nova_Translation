"""Retain complete native page checks and bind the measured full-name substitution."""
from pathlib import Path
from scripts import check_rafael_early_tutorial_compiled_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
validate_documented_layouts=previous.validate_documented_layouts
MEASURED=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B36_B41_source_identity_andFU_checkpoint_v1.json')

source=checked_text(previous.source,{
    "replace(b'FO',b'Castor Co.')":"replace(b'FO',b'Castor Co.').replace(b'FU',b'Rafael Castor')",
    "replace('{MACRO:FO}','Castor Co.')":"replace('{MACRO:FO}','Castor Co.').replace('{MACRO:FU}','Rafael Castor')",
    "    assert doc['current_ROM_sha256']==sha(ctx.rompath.read_bytes())":
        """    assert doc['current_ROM_sha256']==sha(ctx.rompath.read_bytes())
    measurement=load(MEASURED)
    assert measurement['runtime']==ctx.receipt() and measurement['default_macro_lengths']==dict(FI=6,FA=6,FO=10,FU=13)
    assert doc['file_path']=='/data/SC0.DK4' and doc['blocks']==list(range(36,42))
    assert doc['physical_speech_objects']==175 and not any(r['kind']!='progressive' for r in doc['records'])""",
    'Path(source_FE.__file__),Path(old_font.__file__),Path(__file__)]':
        'Path(source_FE.__file__),Path(old_font.__file__),MEASURED,Path(__file__)]',
})
exec(compile(source,__file__+'::same-source-proven-native-pages-with-full-FU','exec'),globals())
