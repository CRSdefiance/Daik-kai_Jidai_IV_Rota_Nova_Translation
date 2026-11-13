"""Keep the template path separate from the native memory BASE constant."""
from pathlib import Path
from scripts.check_qualified_scoped_name_planes_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

TEMPLATE = Path('scripts/check_rafael_B61_B80_scoped_name_planes.py')
source = checked_text(previous, {'args.startup,BASE,Path(__file__)': 'args.startup,TEMPLATE,Path(__file__)'})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-native-name-proof-no-evidence-path-constant-collision', 'exec'), globals())
