"""Twelve native macro alignments for B31/B53's three one-paragraph English drafts; typed choices remain separate."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B52_registered_route_context_v8707 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/Hodram_B31_B53_logical_v8724')
DOC = Path('translations/hodram_B31_B53_editorial_manuscript_v1.json')
SOURCE = Path('work/analysis/Hodram_B31_B53_source_display_v8720/source_display_andbranch_paths.json')
INPUT = Path('work/analysis/current_V8704_Hodram_native_v8707/current_native_input.json')

if __name__ == '__main__':
    assert not ROOT.exists()
    doc, source = map(read, [DOC, SOURCE])
    assert read(doc['current_packet'])['source_native_display_sha256'] == sha(SOURCE.read_bytes()) and len(doc['records']) == 3
    env = dict(progressive_expand.__globals__)
    exec(compile(source['source_owned_progressive_adapter'], __file__ + '::unchanged-captain1-progressive', 'exec'), env)
    ROOT.mkdir(parents=True)
    ctx = RouteCurrentContext(INPUT, 'unused-no-historical-ROM', ROOT / 'current_context')
    rows = []
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source', 'context', 'localization', 'naturalness']) and not row['review']['formatting']
        body, prefix = row['english'].encode('cp932'), row['source_selector']
        assert prefix in [34,113] and body and not any(v in body for v in [b'\0', b'\n', b'\r', b'%'])
        assert not any(m in body or m in bytes.fromhex(row['source_hex'])[1:] for m in [b'FI', b'FA', b'FO'])
        result = ctx.execute(env['expand'], body, prefix)
        ctx.machines.pop()
        assert len(result['cases']) == 4 and all(c['output_hex'] == body.hex() for c in result['cases'])
        rows.append(dict(id=row['id'], file_path=row['file_path'], source_reference=row['source_reference'], current_reference=row['current_reference'],
            source_selector=prefix, kind=row['kind'], logical_body_hex=body.hex(), expected_expanded_hex=body.hex(), native_alignment=result))
    assert len(rows) == 3 and not ctx.machines
    save(ROOT / 'logical_paragraphs.json', dict(manuscript=str(DOC), manuscript_sha256=sha(DOC.read_bytes()), records=rows,
        fresh_native_alignment_cases=12, progressive_alignment_cases=12, FE_null_actor_alignment_cases=0,
        source_macro_counts=dict(FI=0, FA=0, FO=0), measured_default_FI6_FA9_FO15_reused=True,
        all_literal_leading_internal_trailing_bytes_ABI_scratch_ownership_andunowned4MiB_exact=True,
        source_owned_progressive_adapter=source['source_owned_progressive_adapter'],
        logical_byte_checks_not_compiled_wrap_fonts_bounds_pagination_stored_oractual_scene=True,
        all_three_formatting_gates_remain_false=True, actual_context_custom_player_names_policy_andregistered_release_pending=True,
        current_native_input=str(INPUT), native_context_plan=str(ctx.proof_path), native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0, new_emulator_runs=0, full_goal_complete=False, evidence={str(p): sha(p.read_bytes()) for p in [DOC, SOURCE, INPUT, Path(__file__)]}))
    print('B31/B53 logical: twelve progressive guarded alignments, zero source macros. All literal bytes, full4MiB and ABI/scratch guards pass; formatting and release pending.')
