"""Keep the same initialized scenes and add measured brief-page capture samples."""
from scripts.prepare_rafael_B61_B80_actual import source as previous
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(previous,{
    'Rafael_B61_B80_actual_fixtures_20261104':'Rafael_B61_B80_actual_fixtures_v12_20261104',
    'Rafael_B61_B80_rebuilt_20261104/reconstruction.json':'Rafael_B61_B80_rebuilt_v12_20261104/reconstruction.json',
    'combined_native_v10.json':'combined_native_v12.json',
    'rom_retention_pins.Rafael_B61_B80_actual.pending.json':'rom_retention_pins.Rafael_B61_B80_actual_v12.pending.json',
    "text_language='reviewed-English', purpose=name, frames=frames,":
        "text_language='reviewed-English', purpose=name, frames=frames,capture_extra=[9498,9504,9510,9518,9528] if whole else [],",
})
exec(compile(source,__file__+'::same-complete-CG-and22-header-six-pagination-fixtures-final-prose','exec'),globals())
