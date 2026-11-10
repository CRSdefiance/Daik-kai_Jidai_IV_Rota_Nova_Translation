"""Check exact live menu pixels and returns against the scoped menu approval."""

from scripts.analyze_rafael_B201_B220_menu_actual_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text


source = checked_text(previous, {
    "Path(exact['native_receipt'])==proofpath and sha(proofpath.read_bytes())==exact['native_receipt_sha256']":
        "Path(exact['proof'])==proofpath and sha(proofpath.read_bytes())==exact['proof_sha256']",
})


if __name__ == '__main__':
    exec(compile(source, __file__, 'exec'), globals())
