"""Register complete V307 inheritance plus native-verified condition names."""

import copy
import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_sailing_conditions_v309 import CONFIG, ROOT


def main():
    proof = json.loads((ROOT / 'native_proof.json').read_text(encoding='utf-8'))
    config = json.loads(CONFIG.read_text(encoding='utf-8'))
    assert len(proof['native_selector_cases']) == 30 and len(proof['complete_native_label_rasters']) == 26
    assert proof['target_arm9_sha256'] == config['target_arm9_sha256']
    assert sha((ROOT / 'v307_before_builder.nds').read_bytes()) == sha(Path('out/all_routes_combined_v307_candidate.nds').read_bytes())
    path = Path('translations/release_stack.json')
    stack = json.loads(path.read_text(encoding='utf-8'))
    profile = copy.deepcopy(stack['profiles']['all-routes-unified-v307'])
    profile['sailing_condition_names_release'] = str(CONFIG)
    profile['status'] = 'experimental'
    profile['note'] = ('Complete V307 stack plus26 original shared sailing-condition names in owned staged text memory. '
                       'All30 native selector cases and26 complete native font rasters verified; actual reef warning replay pending. '
                       'All18 plaque audits and broader graphics display gates remain open; low resolution Online images exempt.')
    prior = stack['profiles'].get('all-routes-unified-v309')
    assert prior is None or prior == profile
    stack['profiles']['all-routes-unified-v309'] = profile
    path.write_text(json.dumps(stack, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('V309 registered with all470 inherited batches and26 source-reviewed shared labels.')


if __name__ == '__main__':
    main()
