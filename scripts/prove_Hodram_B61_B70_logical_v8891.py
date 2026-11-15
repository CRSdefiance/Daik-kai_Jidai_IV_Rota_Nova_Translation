"""Fresh default-name expansion of all reviewed English paragraphs at four alignments."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Hodram_B54_B60_registered_route_context_v8868 import RouteCurrentContext
from scripts.generic_name_macro_owned_v5886b import expand as progressive_expand
from scripts.verify_lil_clifford_north_new_world_FE_v2980 import expand as original_FE_expand
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/Hodram_B61_B70_logical_v8891')
DOC=Path('translations/hodram_B61_B70_editorial_manuscript_v1.json')
SOURCE=Path('work/analysis/Hodram_B61_B70_source_display_v8881/224_complete_source_dispatches_alignments_pages_andmacro_binding.json')
INPUT=Path('work/analysis/current_V8865_Hodram_native_v8868/current_native_input.json')

def native_body(text):
    for token in ['FI','FA','FO']: text=text.replace('{MACRO:'+token+'}', token)
    assert '{' not in text and '}' not in text
    return text.encode('cp932')

def expanded_body(text):
    return native_body(text).replace(b'FI',b'Hodram').replace(b'FA',b'Bergstrom').replace(b'FO',b'Bergstrom Fleet')

if __name__=='__main__':
    assert not ROOT.exists()
    doc,source=map(read,[DOC,SOURCE])
    assert doc['source_native_view_sha256']==sha(Path(doc['source_native_view']).read_bytes())
    assert read(doc['current_packet'])['source_native_display_sha256']==sha(SOURCE.read_bytes())
    assert len(doc['records'])==224 and doc['source_macro_counts']==dict(FI=15,FA=3,FO=0)
    pe=dict(progressive_expand.__globals__)
    exec(compile(source['source_owned_progressive_adapter'],__file__+'::current-progressive','exec'),pe)
    fe=dict(original_FE_expand.__globals__)
    exec(compile(source['source_owned_FE_adapter'],__file__+'::current-null-actor-FE','exec'),fe)
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    rows=[]
    for row in doc['records']:
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
        body=native_body(row['english']);expected=expanded_body(row['english']);prefix=row['source_selector'];is_FE=prefix==254
        assert body and not any(b in body for b in [b'\0',b'\n',b'\r',b'%'])
        assert not body.startswith(b' ') and not body.endswith(b' ')
        aligned=ctx.execute(fe['expand'] if is_FE else pe['expand'],body,*(() if is_FE else (prefix,)));ctx.machines.pop()
        assert len(aligned['cases'])==4 and all(c['output_hex']==expected.hex() for c in aligned['cases'])
        rows.append(dict(id=row['id'],file_path=row['file_path'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            source_selector=prefix,kind=row['kind'],logical_body_hex=body.hex(),expected_expanded_hex=expected.hex(),native_alignment=aligned))
        if len(rows)%10==0:print('English logical paragraphs complete',len(rows),flush=True)
    assert len(rows)==224 and not ctx.machines
    save(ROOT/'logical_paragraphs.json',dict(manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),records=rows,
        fresh_native_alignment_cases=896,progressive_alignment_cases=896,FE_null_actor_alignment_cases=0,
        source_macro_counts=doc['source_macro_counts'],measured_default_FI6_FA9_FO15_reused=True,
        all_literal_leading_internal_trailing_bytes_ABI_scratch_ownership_andunowned4MiB_exact=True,
        source_owned_progressive_adapter=source['source_owned_progressive_adapter'],source_owned_FE_adapter=source['source_owned_FE_adapter'],
        logical_byte_checks_not_compiled_wrap_fonts_bounds_pagination_stored_oractual_scene=True,
        all224_formatting_gates_remain_false=True,custom_player_names_andactual_scene_policy_registered_release_pending=True,
        current_native_input=str(INPUT),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,SOURCE,INPUT,Path(__file__)]}))
    print('224 English logical paragraphs / 896 default-name native alignments pass; no wrapping or completion approval.',flush=True)
