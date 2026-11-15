"""Carry forward the already-qualified native captain getter dependency check."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/prepare_maria328_formatting_v1.py').read_text(encoding='utf-8'), {
    "assert now.raw[0x7f244:0x7f248] == old.raw[0x7f244:0x7f248] == b'\\x03\\0\\0\\0'":
        "assert now.arm[0x7f244:0x7f248] == old.arm[0x7f244:0x7f248]\n    assert now.expected_captain == old.expected_captain == now.startup['actual_captain_getter'] == old.startup['actual_captain_getter'] == 3",
    'captain3_word=True':'captain3_original_native_getter=True',
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::previously-qualified-getter-instructions-andnative-result-guard','exec'),globals())
