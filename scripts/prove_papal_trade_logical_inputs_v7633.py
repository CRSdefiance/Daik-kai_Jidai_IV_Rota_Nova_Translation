"""Bind all36 new logical paragraphs to each actual route's native processor."""
import inspect
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.draft_papal_trade_prose_v7631 import MANUSCRIPTS
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/papal_trade_logical_inputs_v7633')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);groups=[]
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and EXPECTED_CAPTAIN in [0,1] and captain==EXPECTED_CAPTAIN'})
    for route,path in MANUSCRIPTS.items():
        doc=read(path);inp=Path(doc['current_strict_native_input']);assert sha(inp.read_bytes())==doc['current_strict_native_input_sha256']
        ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',ROOT/f'route{route}_current_context')
        env={**expand.__globals__,'EXPECTED_CAPTAIN':route};exec(compile(adapter,__file__+'::route-logical-inputs','exec'),env)
        rows=[]
        for row in doc['records']:
            body=row['english'].split('}',1)[1].encode('cp932');prefix=row['source_selector']
            assert prefix in [19,104] and not any(v in body for v in [b'FI',b'FA',b'FO',b'\n',b'\r',b'\0'])
            result=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
            assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
            rows.append(dict(id=row['id'],file_path=doc['file_path'],source_selector=prefix,logical_body_hex=body.hex(),native_alignment=result,all_literal_I_andF_bytes_pass_exact_no_substitution_oromission=True))
        assert len(rows)==18 and not ctx.machines
        groups.append(dict(route=route,route_identity=doc['route_identity'],manuscript=str(path),manuscript_sha256=sha(path.read_bytes()),records=rows,fresh_native_alignment_cases=72,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes())))
    save(ROOT/'all36_new_logical_bodies144_fresh_native_literal_IF_alignment_cases.json',dict(groups=groups,source_owned_route_literal_adapter=adapter,fresh_native_alignment_cases=144,original_captains=[0,1],no_global_guard_macro_I_F_orfont_change=True,failed_7632_default_literal_F_guard_preserved_no_plan_output_orapproval=True,logical_processor_checks_not_native_font_render_oractual_UI=True,evidence={str(p):sha(p.read_bytes()) for p in [*MANUSCRIPTS.values(),Path(expand.__code__.co_filename),Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('36 complete new logical bodies:144 fresh strict-route literal I/F alignment cases pass; no substitution, omission, global policy change or actual UI claim.')
