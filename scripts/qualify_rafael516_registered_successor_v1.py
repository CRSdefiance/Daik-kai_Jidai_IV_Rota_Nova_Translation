"""Qualify two ordered adapters and the new mixed consumers without repeating native characterization."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/qualify_plain_SC0_registered_successor_v1.py').read_text(encoding='utf-8'), {
    "len(prep['new_extension_specs']) == len(prep['configs']) == 1":
        "len(prep['new_extension_specs']) == len(prep['configs']) == 2",
    "spec = prep['new_extension_specs'][0]": "spec = prep['new_extension_specs'][-1]",
    "conf = load(prep['configs'][0])": "conf = load(prep['configs'][-1])",
    "    assert len(reports) == 1 and all(reports[0][k] == v for k,v in direct.items())":
        """    prefix_direct = load('work/analysis/Rafael261_registered_preparation_v2_20261105/positive_prepublication_plan.json')
    assert len(reports) == 2 and all(reports[-1][k] == v for k,v in direct.items())
    assert all(reports[0][k] == v for k,v in prefix_direct.items())""",
    "prep['ordered_canonical_targets'][0]['sha256']": "prep['ordered_canonical_targets'][-1]['sha256']",
    "('changed-logical-prose','manuscript'),('wrong-control-only-membership',None)":
        "('changed-logical-prose','manuscript'),('changed-style-alias','manuscript'),('stored-virtual-style-prefix','manuscript'),('wrong-control-only-membership',None)",
    "set(config['blocks'])|{89}": "set(config['blocks'])|{106}",
    "doc['offline_only_source_speeches'] = 0": "doc['offline_only_speech_variants'] = 0",
    "            elif kind == 'changed-logical-prose':":
        """            elif kind == 'changed-style-alias':
                next(r for r in doc['records'] if r.get('source_style_indices') == [0,1])['source_style_indices'] = [0]
            elif kind == 'stored-virtual-style-prefix':
                next(r for r in doc['records'] if r.get('native_object_kind') == '4100-style-alternative')['planned_integrated_reference']['virtual_prefix_not_stored'] = False
            elif kind == 'changed-logical-prose':""",
    "planner(image,base,cp)":
        "planner(NdsImage.open(prep['ordered_canonical_targets'][0]['path']),base,cp)",
    "assert len(rejections) == 8": "assert len(rejections) == 10",
    "One shared source-bound transaction/eight semantic andordering rejections pass;all eight final stage contracts exact. Build next.":
        "Two shared source-bound transactions/ten semantic andordering rejections pass;all eight final stage contracts exact. Build next.",
})
if __name__ == '__main__':
    exec(compile(source, __file__+'::two-ordered-adapters-native-style-alias-andvirtual-prefix-rejections', 'exec'), globals())
