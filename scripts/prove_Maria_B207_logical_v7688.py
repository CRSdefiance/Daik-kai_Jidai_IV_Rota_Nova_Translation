"""Bind all18 proposed logical paragraphs to the actual Maria native processor."""
import inspect
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.generic_name_macro_owned_v5886b import expand
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/maria_B207_logical_v7688')
MANUSCRIPT=Path('translations/maria_B207_editorial_manuscript_v1.json')
if __name__=='__main__':
    assert not ROOT.exists();doc=read(MANUSCRIPT);inp=Path(doc['current_strict_native_input']);assert sha(inp.read_bytes())==doc['current_strict_native_input_sha256']
    adapter=checked_text(inspect.getsource(expand),{'assert identity==prefix and captain==2':'assert identity==prefix and captain==EXPECTED_CAPTAIN==3'})
    env={**expand.__globals__,'EXPECTED_CAPTAIN':3};exec(compile(adapter,__file__+'::Maria-logical-inputs','exec'),env)
    ROOT.mkdir(parents=True);ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');rows=[]
    for row in doc['records']:
        body=row['english'].split('}',1)[1].encode('cp932');prefix=row['source_selector']
        assert prefix in [19,104] and not any(v in body for v in [b'FI',b'FA',b'FO',b'\n',b'\r',b'\0'])
        result=ctx.execute(env['expand'],body,prefix);ctx.machines.pop()
        assert len(result['cases'])==4 and all(c['output_hex']==body.hex() for c in result['cases'])
        rows.append(dict(id=row['id'],file_path=doc['file_path'],source_selector=prefix,logical_body_hex=body.hex(),native_alignment=result,all_literal_I_andF_bytes_pass_exact_no_substitution_oromission=True))
    assert len(rows)==18 and not ctx.machines
    save(ROOT/'all18_Maria_logical_bodies72_fresh_literal_IF_alignments.json',dict(manuscript=str(MANUSCRIPT),manuscript_sha256=sha(MANUSCRIPT.read_bytes()),records=rows,source_owned_Maria_literal_adapter=adapter,fresh_native_alignment_cases=72,original_captain=3,no_global_guard_macro_I_F_orfont_change=True,logical_processor_checks_not_native_font_render_oractual_UI=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),evidence={str(p):sha(p.read_bytes()) for p in [MANUSCRIPT,Path(expand.__code__.co_filename),Path(__file__)]},new_credit=0,full_goal_complete=False))
    print('18 complete Maria logical bodies:72 fresh native literal I/F alignments pass;no substitutions oromissions.')
