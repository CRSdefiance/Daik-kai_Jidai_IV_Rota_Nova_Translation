"""Run the exact original providers and ASCII planes on the four tutorial menus."""
from scripts import check_rafael_two_choice_batch_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(previous.source, {
    'scripts/check_rafael_two_choice_display_v2.py': 'scripts/check_rafael_B177_B180_two_choice_display_v1.py',
    "    assert groups and all(len(rows) == 2 for rows in groups.values())":
        "    assert set(groups)=={(177,2278),(178,356),(179,1452),(180,152)} and all(len(rows)==2 for rows in groups.values())",
    "    objects = []": "    objects = []\n    planes = 0",
    "        proof = load(receipt)":
        "        proof = load(receipt)\n        assert sum(r['version']=='reviewed-English' for r in proof['records'])==4\n        planes += len(proof['records'])",
    "    save(args.out / 'complete_choice_objects.json', dict(": "    assert planes==28\n    save(args.out / 'complete_choice_objects.json', dict(",
    'complete_caption_style_planes=8 * len(objects),':
        'complete_caption_style_planes=planes,complete_reviewed_caption_style_planes=4*len(objects),',
})
exec(compile(source, __file__+'::same-native-four-two-choice-batch-and-observed-plane-count', 'exec'), globals())
