"""Retain the first partial preparation and use the selected native receipt's actual guards."""
from scripts.prepare_maria303_registered_v1 import source as previous_source
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(previous_source, {"ROOT/'registered_preparation_v1'": "ROOT/'registered_preparation_v2'"})
exec(compile(source, __file__+'::same-frozen-inputs-selected-native-guard-contract', 'exec'), globals())
