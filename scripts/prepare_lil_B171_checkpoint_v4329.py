"""Prepare exactly one pending-credit checkpoint for37 native-approved B171 records."""
import re
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save

ROOT = Path('work/analysis/lil_B171_checkpoint_tools_v4329')
NEW = Path('scripts/checkpoint_lil_B171_v4329.py')

if __name__ == '__main__':
    assert not ROOT.exists() and not NEW.exists()
    old = Path('scripts/checkpoint_lil_B170_v4279.py')
    text = old.read_text(encoding='utf-8')
    a, b = text.index("NEXT = '"), text.index("if __name__ == '__main__':")
    text = text[:a] + 'from scripts.lil_B171_checkpoint_text_v4329 import NEXT,SUMMARY\n\n' + text[b:]
    changes = {
        'lil_B170_checkpoint_v4279': 'lil_B171_checkpoint_v4329',
        'editorial_handoff_verification_v4259': 'editorial_handoff_verification_v4308b',
        'lil_B170_native_approval_v4278': 'lil_B171_native_approval_v4328',
        'lil_B170_editorial_manuscript_v5': 'lil_B171_editorial_manuscript_v4',
        'Lil-B170-Yifa-collision-apology-Taoist-training-resolve-joining33': 'Lil-B171-Sanghyeon-dream-visit-expulsion-siblinglike-bond-training-work37',
        'B170': 'B171', 'lil_B170': 'lil_B171',
        '[170]': '[171]', 'blocks=[170]': 'blocks=[171]',
        '# Current editorial handoff - V4258': '# Current editorial handoff - V4307',
        'unfinished_editorial_scope_v4258': 'unfinished_editorial_scope_v4307',
        'remaining_B171_B180': 'remaining_B172_B180',
        'V4279': 'V4329', 'v4279': 'v4329',
        'row_count_notes=11': 'row_count_notes=16',
        'Latest V4251 and promoted V4204 unchanged': 'Latest V4303 and promoted V4251 unchanged',
    }
    for key in changes:
        assert key in text, key
    text = re.sub('|'.join(re.escape(k) for k in sorted(changes,key=len,reverse=True)), lambda m: changes[m.group()], text)
    counts = {'5725':'5762','5692':'5725','5728':'5765','5695':'5728','3872':'3909','3839':'3872',
              '4126':'4163','4093':'4126','3614':'3635','2078':'2090','33':'37','21':'24','12':'13','198':'161'}
    text = re.sub(r'(?<!\d)(?:'+'|'.join(re.escape(k) for k in sorted(counts,key=len,reverse=True))+r')(?!\d)', lambda m: counts[m.group()], text)
    assert 'B170' not in text and 'B141' not in text and 'blocks=[171]' in text
    compile(text, str(NEW), 'exec')
    NEW.write_text(text, encoding='utf-8', newline='\n')
    ROOT.mkdir(parents=True)
    save(ROOT / 'source_derivation.json', dict(previous=str(old), previous_sha256=sha(old.read_bytes()), successor=str(NEW), successor_sha256=sha(NEW.read_bytes()),
        expected_fresh=5762, expected_integrated=5725, expected_pending=37, expected_source_prose=5765,
        new_source_prose_reviews=37, new_completed_records=0, no_current_ledger_mutation_yet=True, full_goal_complete=False))
