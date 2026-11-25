"""Register the staged candidate with both FE child references under one source credit."""
import sys
from scripts import build_registered_maria328_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.register_source,{
    "bindings.append({**{key: row[key] for key in keys}, 'registered_reference': ref})":
        """native_refs=row.get('planned_integrated_native_pages',[ref])
        assert len(native_refs)==(2 if row['id']=='DK4_MES_B87_R0139' else 1)
        for native_ref in native_refs:
            pos=native_ref['offset'];value=bytes.fromhex(native_ref['exact_stored_hex'])
            assert block[pos:pos+len(value)+1]==value+b'\\0'
            assert native_ref['target_archive_sha256']==staged['target_SC3_sha256']
            if len(native_refs)==2:assert block[pos-5:pos+1].hex()==row['source_complete_preamble_hex']=='0040ffff00fe'
        bindings.append({**{key: row[key] for key in keys},'registered_reference':ref,'registered_native_pages':native_refs})""",
    "r['id']) for r in bindings}) == 328":"r['id']) for r in bindings}) == 328\n    assert sum(len(r['registered_native_pages']) for r in bindings)==329",
    "predecessor=predecessor, qualification=str(QUALIFICATION), qualification_sha256=digest(QUALIFICATION),":
        "predecessor=predecessor,staging_driver='scripts/build_registered_maria328_v2.py',staging_driver_sha256=digest('scripts/build_registered_maria328_v2.py'), qualification=str(QUALIFICATION), qualification_sha256=digest(QUALIFICATION),",
    "'justified_retentions': 185, 'preparation':":
        "'justified_retentions': 185,'physical_body_candidates':314,'native_FE_panels':28,'additional_exact_source_FE_controls':1, 'preparation':",
    'Registered Maria328 with714 entries and49 release checks.':'Registered Maria328 with715 entries and50 release checks.',
})
env={**previous.env,'__file__':__file__}
exec(compile(source,__file__+'::same-registration-with-complete-FE-reference-binding','exec'),env)
if __name__=='__main__':
    assert not sys.argv[1:]
    env['register']()
