"""Prepare an exact current-parent Lil opening snapshot with ordinary inputs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_lil382_current_context_v1.py').read_text(encoding='utf-8'), {
    'Lil382_residual_A_clean_20261110':'Lil269_B243_B282_clean_20261110',
    'maria315_B286_B302_release_v1':'lil382_residual_A_release_v1',
    'sealed_382_clean_drafts':'sealed_269_clean_drafts',
    'opening_not_new_382_optional_event_activation':'opening_not_new_269_optional_event_activation',
    'onregistered Maria315':'onregistered Lil382',
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-exact-current-parent-ordinary-Lil-input-contract','exec'),globals())
