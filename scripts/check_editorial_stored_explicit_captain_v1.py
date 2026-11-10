"""Preserve stored native guards with explicit current-captain macro dependencies."""
import inspect
from pathlib import Path
from scripts import check_editorial_stored_batch_v3 as previous
from scripts.source_locked_derivation_v5118 import checked_text

compound_env = dict(previous.compound_storage.__globals__)
compound_source = checked_text(inspect.getsource(previous.compound_storage), {
    'exact_compiled_body_font_runtime_and64_slot_getter_proof_reuse':
        'exact_compiled_body_font_runtime_and_source_bound_slot_getter_proof_reuse',
})
exec(compile(compound_source, __file__+'::same-complete-compound-storage-guards', 'exec'), compound_env)
compound_storage = compound_env['compound_storage']
source = checked_text(previous.source, {
    'from scripts.registered_editorial_runtime import RegisteredRuntime':
        'from scripts.registered_editorial_runtime_v2 import RegisteredRuntime',
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--captain',type=int,choices=range(4),required=True)\n    parser.add_argument('--macro-proof',type=Path,required=True)\n    args=parser.parse_args();assert not args.out.exists()",
    "runtime=native['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'])":
        """runtime=native['runtime'];ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=args.captain)
    macros=load(args.macro_proof)
    assert macros['runtime']==runtime and macros['default_macro_all_four_alignment_cases_pass']
    defaults={k:v['text'] for k,v in macros['defaults'].items()}
    assert {k:len(v) for k,v in defaults.items()}==macros['macro_ascii_lengths']
    def expand_body(body):
        for token,value in defaults.items():body=body.replace(token.encode(),value.encode())
        return body""",
    "    adapter=full_native['source_owned_target_page_adapter']":
        "    assert full_native['source_owned_progressive_macro_adapter']==macros['source_owned_progressive_adapter']\n    adapter=full_native['source_owned_target_page_adapter']",
    '    painter,calibration=factory(image)':
        "    if any(bytes.fromhex(r['compiled_hex'])[0]==254 for r in native['records']):\n        painter,calibration=factory(image)\n    else:\n        painter,calibration=None,dict(not_executed_no_FE_records=True,no_FE_approval_inferred=True)",
    "expanded=raw[1:].replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')":
        'expanded=expand_body(raw[1:])',
    "rebuilt['style_physical_speech_count']==48": "rebuilt['style_physical_speech_count']",
    "rebuilt['total_rendered_speech_count']==308": "rebuilt['total_rendered_speech_count']",
    "rebuilt['typed_choice_count']==15": "rebuilt['typed_choice_count']",
    'args.reconstruction,args.native,Path(__file__)': 'args.reconstruction,args.native,args.macro_proof,Path(__file__)',
})
exec(compile(source, __file__+'::same-stored-glyph-canary-pagination-branch-guards-explicit-captain', 'exec'), globals())
