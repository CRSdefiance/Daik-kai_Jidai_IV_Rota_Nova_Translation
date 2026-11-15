"""Prepare exact residual-SC0 bindings and reuse the validated paragraph formatter."""
import re
import sys
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from scripts import plan_rafael_B121_B140_withstyles_v1 as planner
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.generic_name_macro_owned_v5886b import expand as original_expand
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_rafael_B0_B34_contextual_v1 import CURRENT, OUT as PROSE
from scripts.seal_rafael_B0_B34_clean_v1 import ROOT


NAMES=ROOT/'native_names_v1.json/names.json'
TERMS=ROOT/'scoped_terms_and_name_field_leads_v1.json'
IDENTITY=ROOT/'scoped_runtime_v1.json'
FORMATTING=ROOT/'ordinary_formatting_manuscript_v1.json'
PREFERENCES=ROOT/'ordinary_visual_preferences_v1.json'
MACROS=ROOT/'native_macro_measurements_v1.json'
ADAPTERS=Path('work/analysis/Rafael_early_tutorial_B42_B43_source_display_20261104/40_native_selectors_macros_andcomplete_preamble_bindings.json')
TOKEN=re.compile(r'\b(FI|FA|FO|FU)\b')


def prepare():
    assert not any(p.exists() for p in (IDENTITY,FORMATTING,PREFERENCES,MACROS))
    prose,current,names,terms=map(load,(PROSE,CURRENT,NAMES,TERMS))
    runtime=current['runtime']; assert names['runtime']==terms['runtime']==runtime
    assert prose['records_count']==len(prose['records'])==283 and prose['remaining_current_comparisons']==0
    assert all(digest(p)==value for p,value in prose['evidence'].items())
    ctx=RegisteredRuntime(runtime['release_proof'],runtime['startup_proof'],captain=0)
    assert ctx.receipt()==runtime and digest('translations/release_stack.json')==ctx.release['registry_sha256']
    assert ctx.release['all_predecessor_stage_dependencies_preserved'] and ctx.release['all_other_files_components_graphics_names_andruntime_exact_to_parent']
    adapter=load(ADAPTERS)['source_owned_progressive_adapter']
    env=dict(original_expand.__globals__)
    exec(compile(adapter,__file__+'::original-registered-macro-wrapper','exec'),env)
    expand=env['expand']
    measured=dict(FI='Rafael',FA='Castor',FO='Castor Co.',FU='Rafael Castor')
    defaults={}
    for token,text in measured.items():
        proof=ctx.execute(expand,token.encode(),0)
        assert len(proof['cases'])==4 and all(c['output_hex']==text.encode().hex() for c in proof['cases'])
        defaults[token]=proof
    checks=[]
    for row in prose['records']:
        assert all(row['review'][g] for g in ('source','context','localization','naturalness')) and not row['review']['formatting']
        if not row['native_literal_tokens']:
            continue
        expected=TOKEN.sub(lambda m:measured[m[0]],row['english']).encode().hex()
        proof=ctx.execute(expand,row['english'].encode(),row['source_selector'])
        assert len(proof['cases'])==4 and all(c['output_hex']==expected for c in proof['cases']),row['id']
        checks.append(dict(id=row['id'],source_reference=row['source_reference'],current_reference=row['current_reference'],
            expected_hex=expected,native_wrapper=proof))
    assert len(checks)==16 and any(r['id']=='DK4_MES_B26_R0124' for r in checks)
    lengths={k:len(v) for k,v in measured.items()}
    save(MACROS,dict(runtime=runtime,macro_ascii_lengths=lengths,current_default_expansions=defaults,
        complete_ARM9_COMMON_font_andactor0_macro_dependencies_qualified=True,sixteen_logical_macro_records=checks,
        source_owned_progressive_adapter=adapter,all_combined_FI_FA_tokens_expanded_in_original_order=True,
        evidence={str(p):digest(p) for p in (PROSE,ADAPTERS)},new_credit=0))
    bindings=[]
    for row in terms['scoped_actor_fields']:
        actor=row['actor_ID']
        forms=[r for r in names['current_names']['rows'] if r['actor_ID']==actor]
        assert {r['consumer'] for r in forms}=={'progressive-nameplate','full-catalogue'}
        bindings.append(dict(actor_ID=actor,source_andcurrent_fields=row['source_andcurrent_fields'],current_consumers=forms,fresh=True))
    save(IDENTITY,dict(runtime=runtime,name_bindings=bindings,actors=names['actors'],dynamic_selectors=[],
        macro_ascii_lengths=lengths,all_scoped_getters_fresh_on_registered_ARM9=True,
        name_editorial_andplane_proofs_separate=True,exact_unchanged_actor0_macro_dependencies=True,
        evidence={str(p):digest(p) for p in (NAMES,TERMS,MACROS)},new_credit=0))
    rows=[]
    for original in prose['records']:
        row=dict(original)
        assert TOKEN.findall(row['english'])==row['native_literal_tokens']
        row.update(kind='progressive',source_record_index=row['source_reference']['record_index'],
            editorial_logical_English=row['english'],prior_macro_normalized_comparison=None)
        row['english']=TOKEN.sub(lambda m:'{MACRO:'+m[0]+'}',row['english'])
        row['planned_English_markup']=f"{{SPEAKER:{row['source_selector']:02X}}}"+row['english']
        rows.append(row)
    save(FORMATTING,{**prose,'records':rows,'runtime':runtime,'file_path':current['file_path'],
        'current_ROM':current['current_ROM'],'current_ROM_sha256':current['current_ROM_sha256'],
        'current_archive_sha256':current['current_archive_sha256'],'blocks':list(range(35)),
        'physical_speech_objects':283,'ordinary_speech_objects':283,'style_physical_speech_objects':0,
        'style_command_objects':0,'typed_choice_objects':0,'pending_staged_merge':[],
        'all_individual_four_prose_gates_pass':True,'manuscript_sha256':digest(PROSE),
        'scoped_identity_proof_sha256':digest(IDENTITY),'reused_macro_proof_sha256':digest(MACROS),
        'no_prose_changes_or_manual_breaks':True})
    save(PREFERENCES,dict(records={},progressive_width_px=216,FE_physical_width_px=228,
        no_old_record_specific_guard_orsemantic_preference_inherited=True,author_inserted_ordinary_breaks=0,new_credit=0))
    print('Prepared 283 logical paragraphs and measured all 16 macro-bearing records, including combined FI/FA.')


def qualify_source(doc):
    current,prose,identity=map(load,(CURRENT,PROSE,IDENTITY))
    assert doc['runtime']==current['runtime']==identity['runtime']
    assert doc['manuscript_sha256']==digest(PROSE) and doc['scoped_identity_proof_sha256']==digest(IDENTITY)
    assert doc['reused_macro_proof_sha256']==digest(MACROS)
    assert current['all_source_preambles_andcommand_kinds_preserved'] and doc['blocks']==list(range(35))
    assert doc['all_individual_four_prose_gates_pass'] and doc['physical_speech_objects']==283
    assert digest('work/clean.nds')=='f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    image=NdsImage.open(doc['current_ROM']); clean=NdsImage.open('work/clean.nds')
    assert digest(doc['current_ROM'])==doc['current_ROM_sha256']==current['runtime']['candidate_sha256']
    assert sha256(image.read_file('/__arm9__.bin')).hexdigest()==current['runtime']['ARM9_sha256']
    archive=doc['file_path']; assert archive=='/data/SC0.DK4'
    assert sha256(image.read_file(archive)).hexdigest()==doc['current_archive_sha256']
    jp,bank=[IlnkContainer.parse(im.read_file(archive)).blocks for im in (clean,image)]
    originals={r['id']:r for g in current['groups'] for r in g['records']}
    reviewed={r['id']:r for r in prose['records']}; zeros=set(); bindings=[]
    for row in doc['records']:
        original=originals[row['id']]; approved=reviewed[row['id']]
        assert all(row[k]==original[k] for k in ('source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'))
        assert row['editorial_logical_English']==approved['english']
        assert row['english']==TOKEN.sub(lambda m:'{MACRO:'+m[0]+'}',approved['english'])
        assert row['planned_English_markup']==f"{{SPEAKER:{row['source_selector']:02X}}}"+row['english']
        assert row['kind']=='progressive' and row['source_selector'] in identity['actors']
        sr,cr=row['source_reference'],row['current_reference']; n=row['block']
        raw,stored=map(bytes.fromhex,(row['source_hex'],row['current_hex']))
        head=bytes.fromhex(row['source_complete_preamble_hex'])
        assert head[:5]==bytes.fromhex('0040ffff00') and len(head)==6 and head[-1]==raw[0]==stored[0]==row['source_selector']
        assert jp[n][sr['header_offset']:sr['offset']+len(raw)+1]==head[:5]+raw+b'\0'
        assert bank[n][cr['header_offset']:cr['offset']+len(stored)+1]==head[:5]+stored+b'\0'
        assert b'\0' not in raw[1:] and b'\0' not in stored[1:]
        if raw[0]==0: zeros.add(raw)
        bindings.append(dict(id=row['id'],source_reference=sr,current_reference=cr,
            complete_source_header_hex=head.hex(),source_body_sha256=sha256(raw).hexdigest(),
            scoped_identity_binding=str(IDENTITY),scoped_identity_binding_sha256=digest(IDENTITY),
            source_object_binding=str(CURRENT),macro_dependency_reuse=str(MACROS),macro_dependency_reuse_sha256=digest(MACROS),
            no_new_native_dispatch_orconditional_activation_claim=True))
    assert len(bindings)==len(originals)==len(reviewed)==283 and {r['id'] for r in bindings}==set(originals)
    return zeros,bindings


if __name__=='__main__':
    if sys.argv[1:]==['--prepare']:
        prepare()
    else:
        FunctionType(planner.main.__code__,{**planner.env,'qualify_source':qualify_source,'__file__':__file__})()
