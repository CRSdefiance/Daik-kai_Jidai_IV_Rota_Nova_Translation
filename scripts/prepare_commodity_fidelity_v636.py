"""Correct the source meaning of ヤシ油; preserve V635 as rejected research."""

from pathlib import Path

from dk4tool.patch.commodity_fidelity import CHANGES_V2
from scripts import prepare_commodity_fidelity_v635 as prepare
from scripts.verify_village_wrap_v608 import read, save


def main():
    root = Path('work/analysis/commodity_fidelity_v636')
    root.mkdir(parents=True, exist_ok=True)
    old = read('work/analysis/commodity_fidelity_v635/packing_plan.json')
    old['names']['15'] = 'Coconut Oil'
    old['changed_labels']['15'] = 'Coconut Oil'
    old['root_offsets'].pop('15', None)
    old['identical_full_name_alias'] = {'index': 15, 'shared_root_index': 120, 'English': 'Coconut Oil'}
    save(root / 'packing_plan.json', old)
    prepare.ROOT = root
    prepare.CONFIG = Path('translations/commodity_fidelity_v2.json')
    prepare.MANUSCRIPT = Path('translations/commodity_fidelity_manuscript_v2.json')
    prepare.FORMAT = 'dk4-commodity-fidelity-v2'
    prepare.PROFILE = 'all-routes-unified-v636'
    prepare.CHANGES = CHANGES_V2
    prepare.NOTES = {**prepare.NOTES,
                     15: 'Coconut oil. Japanese ヤシ油 and the separate ココナッツ油 entry120 name the same material;both use Coconut Oil while their original IDs/gameplay metadata remain distinct. Do not expand the old P. Oil abbreviation into an unsupported palm-oil distinction. Primary terminology: https://www.mext.go.jp/b_menu/shingi/gijyutu/gijyutu3/attach/1299201.htm and https://www.oil.or.jp/kiso/seisan/seisan01_02.html'}
    prepare.main()


if __name__ == '__main__':
    main()
