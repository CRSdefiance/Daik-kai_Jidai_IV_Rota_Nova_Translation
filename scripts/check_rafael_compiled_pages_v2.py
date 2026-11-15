"""Bind FE expected substitutions to verified Rafael defaults; retain all native guards."""
from scripts import check_rafael_early_tutorial_compiled_pages as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
validate_documented_layouts=previous.validate_documented_layouts
source=checked_text(previous.source,{
    "    fe_env=dict(FE_expand.__globals__)":
        """    fe_adapter=checked_text(macros['source_owned_FE_adapter'],{
        "b'Hodram'":"b'Rafael'","b'Bergstrom'":"b'Castor'","b'Bergstrom Fleet'":"b'Castor Co.'",
    })
    fe_env=dict(FE_expand.__globals__)""",
    "exec(compile(macros['source_owned_FE_adapter'],":
        "exec(compile(fe_adapter,",
    'FE_factory_calibration=calibration,':
        "FE_factory_calibration=calibration,source_owned_FE_expected_value_adapter=fe_adapter,FE_expected_defaults=dict(FI='Rafael',FA='Castor',FO='Castor Co.'),",
})
exec(compile(source,__file__+'::same-null-source-actor-ABI-with-own-Rafael-expected-defaults','exec'),globals())
