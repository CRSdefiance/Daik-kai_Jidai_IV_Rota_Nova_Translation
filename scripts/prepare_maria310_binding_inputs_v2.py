"""Keep full native extents, including the original optional alignment NUL."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/prepare_maria310_binding_inputs_v1.py').read_text(encoding='utf-8'),{
    "assert command['word']==0x4000 and raw[5:-1]==body and raw[-1:]==b'\\0'":
        "assert command['word']==0x4000 and raw[5:5+len(body)]==body and raw[5+len(body):] in [b'\\0',b'\\0\\0']\n        assert len(raw)==command['native_extent']",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-clean-projection-preserving-complete-native-padding','exec'),globals())
