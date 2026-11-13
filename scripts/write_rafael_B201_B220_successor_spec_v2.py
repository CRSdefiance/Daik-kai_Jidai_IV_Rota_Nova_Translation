"""Bind the corrected mixed release validator and separately version all new contracts."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


parent=Path(__file__).with_name('write_rafael_B201_B220_successor_spec_v1.py')
source=checked_text(parent.read_text(encoding='utf-8'),{
    'rafael_B201_B220_registered_successor_spec_v1.json':'rafael_B201_B220_registered_successor_spec_v2.json',
    'dk4tool.patch.rafael_story_b201_b220_release_v1':'dk4tool.patch.rafael_story_b201_b220_release_v2',
    'rafael_B201_B220_editorial_release_v1.json':'rafael_B201_B220_editorial_release_v2.json',
    "{stage}_{KEY}_release_v1.json":"{stage}_{KEY}_release_v2.json",
    "set(evidence.values()) | {str(Path(__file__)),str(RELEASE),":
        """set(evidence.values()) | {str(Path(__file__)),str(RELEASE),
        'dk4tool/patch/rafael_story_b201_b220_release_v1.py',
        'scripts/write_rafael_B201_B220_successor_spec_v1.py',
        'scripts/prepare_rafael_B201_B220_registered_v2.py',""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-403-object-append-new-validator-binding','exec'),globals())

