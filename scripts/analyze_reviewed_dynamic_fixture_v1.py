"""Keep complete pixel/order checks while distinguishing source selectors from expected actor IDs."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

def dynamic_headers(source):
    return checked_text(source,{
        '            text = byactor[actor]':
            "            expected_actor=fixture['expected_header_actor_ID_by_selector'][str(actor)]\n            text = byactor[expected_actor]",
        'headers.append(dict(actor_ID=actor, text=text,':
            'headers.append(dict(source_selector=actor,expected_actor_ID=expected_actor,expected_ID_from_offline_role_proof_not_pixels=True,text=text,',
        "{h['actor_ID'] for h in headers} == set(fixture['ordinary_actor_IDs'])":
            "{h['source_selector'] for h in headers} == set(fixture['source_selectors_with_header'])",
        "observed_actor_IDs=sorted({h['actor_ID'] for h in headers})":
            "observed_source_selectors=sorted({h['source_selector'] for h in headers}),numeric_actor_identity_not_inferred_from_header_pixels=True",
    })

source=checked_text(Path('scripts/analyze_reviewed_scene_fixture.py').read_text(encoding='utf-8'),{
    "exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
        "exec(compile(dynamic_headers(source),__file__+'::same-pixels-with-qualified-dynamic-header-expectations','exec'),globals())",
})
exec(compile(source,__file__+'::same-complete-source-order-body-header-andblank-pixel-checks', 'exec'),globals())
