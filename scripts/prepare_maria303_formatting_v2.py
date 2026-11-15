"""Use the verified native captain getter, not its instruction address as a raw-data offset."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(Path('scripts/prepare_maria303_formatting_v1.py').read_text(encoding='utf-8'),{
    "assert now.raw[0x7f244:0x7f248]==old.raw[0x7f244:0x7f248]==b'\\x03\\0\\0\\0'":
    "assert now.expected_captain==old.expected_captain==now.startup['actual_captain_getter']==old.startup['actual_captain_getter']==3",
    'captain3_word=True':'captain3_original_native_getter=True',
})
if __name__=='__main__':exec(compile(source,__file__+'::exact-native-captain-getter-dependency-reuse','exec'),globals())
