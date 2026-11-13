"""Qualify exact reviewed startup RGB for a registered SC0-only successor specification."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = Path('scripts/qualify_rafael_B51_B60_identity_startup.py').read_text(encoding='utf-8')
start = source.index("    plan=composition['name_plan'];")
end = source.index('    save(output,',start)
source = checked_text(source, {
    "ROOT=Path('work/analysis/Rafael_B51_B60_identity_coldboot_20261104')\nPARENT=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/own_registered_startup_verification.json')\nCOMPOSITION=Path('work/analysis/Rafael_B51_B60_focused_20261104/composition.json')":
        """import argparse
parser = argparse.ArgumentParser(description=__doc__)
for key in ['capture','parent-startup','preparation']:
    parser.add_argument('--'+key,type=Path,required=True)
args = parser.parse_args()
ROOT, PARENT, COMPOSITION = args.capture, args.parent_startup, args.preparation""",
    "composition['research_ROM_sha256']": "composition['target_ROM_sha256']",
    "assert [p for p,v in previous.iter_components() if current.read_file(p)!=v]==['/__arm9__.bin']":
        "assert [p for p,v in previous.iter_components() if current.read_file(p)!=v]==[]",
    "==list(range(51,61))":
        "==sorted(n for config in composition['configs'] for n in load(config)['blocks'])",
    source[start:end]: "    assert after[44] == before[44]\n    assert current.read_file('/__arm9__.bin') == previous.read_file('/__arm9__.bin')\n",
    "only_ten_later_scene_blocks_andexclusive_Fernan_field_differ=True":
        "only_registered_owned_SC0_blocks_differ_all_ARM9_names_andopening_exact=True",
    "only ten later scenes/Fernan field differ": "only registered ownedSC0 blocks differ;all ARM9/name/opening bytes exact",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::same-ten-reviewed-RGB-pairs-SC0-only-qualified-membership', 'exec'), globals())
