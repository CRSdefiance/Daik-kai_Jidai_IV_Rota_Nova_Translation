"""Bind the held complete exchange to the current release and its qualified FE continuation."""
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.generic_name_macro_owned_v5886b import expand

ROOT=Path('work/Maria_B50_FE_resolution_20261109_v3')
OLD=Path('work/Maria_B37_B50_clean_20261109')

def main():
    assert not ROOT.exists()
    release_path=Path('work/maria270_release_v1/registered_release_verification.json');release=load(release_path)
    ctx=RegisteredRuntime(release_path,release['own_registered_startup'],captain=3)
    assert digest('translations/release_stack.json')==release['registry_sha256']
    parent_path=OLD/'formatting_v1/formatting_input.json';parent=load(parent_path)
    old_macros_path=OLD/'formatting_v1/native_macro_measurements.json';macros=deepcopy(load(old_macros_path))
    rows=deepcopy([r for r in parent['records'] if r['block']==50]);assert len(rows)==16
    archive=ctx.image.read_file('/data/SC3.DK4');old=NdsImage.open(parent['current_ROM'])
    clean=NdsImage.open('work/clean.nds')
    nowblocks=IlnkContainer.parse(archive).blocks
    oldblocks=IlnkContainer.parse(old.read_file('/data/SC3.DK4')).blocks
    cleanblocks=IlnkContainer.parse(clean.read_file('/data/SC3.DK4')).blocks
    assert nowblocks[50]==oldblocks[50]
    # The intervening market delta and SC3-only append preserve all macro/name
    # instructions and data. Keep inherited proof identities; bind current FI.
    old_release=load(release['parent'].replace('all_routes_market_goods_info_fix_candidate.nds','registered_release_verification.json'))
    assert ctx.arm==NdsImage.open(release['parent']).read_file('/__arm9__.bin')
    assert old.read_file('/COMMON/MESFILE.DK4')==ctx.image.read_file('/COMMON/MESFILE.DK4')
    assert old.read_file('/GRP/KANJI.FNT')==ctx.image.read_file('/GRP/KANJI.FNT')
    from dk4tool.patch.market_goods_info_terminator_v1 import transform
    transformed,marketproof=transform(old.read_file('/__arm9__.bin'))
    assert transformed==ctx.arm and marketproof['whole_serialized_parent_inverse_exact']
    original_runtime=macros['runtime']
    macro_env={**expand.__globals__}
    exec(compile(macros['source_owned_progressive_adapter'],__file__+'::same-original-progressive-FI-ABI','exec'),macro_env)
    fi=ctx.execute(macro_env['expand'],b'FI',3)
    fe_env={**expand.__globals__}
    exec(compile(macros['source_owned_FE_adapter'],__file__+'::same-original-null-actor-FI-ABI','exec'),fe_env)
    fe=ctx.execute(fe_env['expand'],b'FI')
    assert len(fi['cases'])==len(fe['cases'])==4
    assert all(bytes.fromhex(c['output_hex'])==b'Maria' for proof in [fi,fe] for c in proof['cases'])
    macros.update(runtime=ctx.receipt(),inherited_default_macro_receipt=str(old_macros_path),
        inherited_default_macro_receipt_sha256=digest(old_macros_path),inherited_runtime=original_runtime,
        inherited_alignment_cases_retain_actual_old_identity=True,current_progressive_FI_preflight=fi,current_FE_null_actor_FI_preflight=fe,
        only_FI_used_by_source_B50=True,exact_market_ARM9_delta=marketproof,
        current_B50_block_andCOMMON_font_name_code_preserved=True,new_credit=0)
    for row in rows:
        sr,cr=row['source_reference'],row['current_reference'];a,b=bytes.fromhex(row['source_hex']),bytes.fromhex(row['current_hex'])
        assert cleanblocks[50][sr['offset']:sr['offset']+len(a)+1]==a+b'\0'
        assert nowblocks[50][cr['offset']:cr['offset']+len(b)+1]==b+b'\0'
        head=bytes.fromhex(row['source_complete_preamble_hex'])
        assert head[:5]==bytes.fromhex('0040ffff00') and head[5]==a[0]==b[0]==row['source_selector']
        assert cleanblocks[50][sr['offset']-5:sr['offset']+1]==nowblocks[50][cr['offset']-5:cr['offset']+1]==head
        assert all(row['review'][k] for k in ['source','context','localization','naturalness']) and not row['review']['formatting']
    source=deepcopy(parent);source.update(records=rows,blocks=[50],runtime=ctx.receipt(),
        current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],current_archive_sha256=sha(archive),
        physical_speech_objects=16,ordinary_speech_objects=16,progressive_speech_objects=4,FE_speech_objects=12,
        typed_choice_objects=0,typed_choice_commands=0,source_editorial_objects=16,
        source_full_manuscript=str(parent_path),source_full_manuscript_sha256=digest(parent_path),
        complete_held_exchange_not_a_new_source_orprose_pass=True,new_credit=0)
    ident='DK4_MES_B50_R0043';owner=next(r for r in rows if r['id']==ident)
    marker=', England';assert owner['english'].count(marker)==1
    split=owner['english'].index(marker)+1
    parts=[owner['english'][:split],owner['english'][split+1:]]
    assert ' '.join(parts)==owner['english'] and parts[0].endswith('Far East,') and parts[1].startswith('England might')
    children=[];physical=[]
    for row in rows:
        if row['id']!=ident:physical.append(deepcopy(row));continue
        assert row['source_selector']==254 and not any(row['native_literal_token_counts'].values())
        for i,part in enumerate(parts,1):
            child=deepcopy(row);child.update(id=ident+f'_FE_PAGE_{i}',english=part,
                planned_English_markup='{SPEAKER:FE}'+part,source_editorial_ID=ident,
                native_child_page=i,native_child_page_count=2,source_complete_paragraph=row['english'],
                virtual_formatting_child_not_another_source_editorial_record=True,prior_macro_normalized_comparison=None)
            children.append(child);physical.append(child)
    pagination=dict(source_ID=ident,source_reference=owner['source_reference'],current_reference=owner['current_reference'],
        complete_source_preamble_hex=owner['source_complete_preamble_hex'],source_hex=owner['source_hex'],current_hex=owner['current_hex'],
        unchanged_logical_English=owner['english'],child_IDs=[r['id'] for r in children],page_segments=parts,
        semantic_boundary_reason='The complete unrealized conditional premise ends at Far East,;the following panel states its possible consequence. The unchanged139-character paragraph exceeds the safe four-row static FE consumer. Keep every word and punctuation;repeat the exact source FE control using the established tutorial continuation planner. One source object/two native panels,not two editorial credits.',
        synthetic_command_count=1,source_control_repeated_exactly_not_a_new_actor_orengine_change=True)
    target=deepcopy(source);target.update(records=physical,physical_speech_objects=17,FE_speech_objects=13,
        ordinary_speech_objects=17,source_editorial_objects=16,pagination_owners=[pagination],
        virtual_children_not_extra_source_coverage=True,source_owner_manuscript=str(ROOT/'source16_manuscript.json'))
    ROOT.mkdir();save(ROOT/'source16_manuscript.json',source)
    target['source_owner_manuscript_sha256']=digest(ROOT/'source16_manuscript.json')
    save(ROOT/'physical17_manuscript.json',target);save(ROOT/'pagination_owners.json',dict(owners=[pagination],new_credit=0))
    save(ROOT/'native_macro_measurements.json',macros)
    save(ROOT/'role_bindings.json',dict(runtime=ctx.receipt(),source_records=[],native_roles=dict(rows=[]),no_dynamic_selectors_in_source_batch=True,FE_not_resolved_as_actor254_orfallback208=True,new_credit=0))
    preferences=deepcopy(load(OLD/'formatting_v1/preferences_v4_candidates.json'))
    preferences['records']={k:v for k,v in preferences['records'].items() if k in {r['id'] for r in physical}}
    for child in children:
        preferences['records'][child['id']]=dict(FE_planning_cells=36,one_page=True,
            reason=pagination['semantic_boundary_reason'],bindings={k:sha(child[k].encode()) for k in ['source_hex','current_hex','english']})
    save(ROOT/'preferences_v1.json',preferences)
    save(ROOT/'source_and_runtime_binding.json',dict(runtime=ctx.receipt(),records=16,physical_native_candidates=17,
        source_editorial_objects=16,unchanged_B50_block_sha256=sha(nowblocks[50]),clean_B50_block_sha256=sha(cleanblocks[50]),
        full_prose_preserved=True,no_authored_wraps_or_font_viewport_engine_changes=True,
        exact_intervening_market_transform=marketproof,all_source_current_references_andcomplete_preambles_bound=True,
        parent_release=str(release_path),parent_release_sha256=digest(release_path),new_credit=0,
        evidence={str(p):digest(p) for p in [parent_path,old_macros_path,ROOT/'source16_manuscript.json',ROOT/'physical17_manuscript.json',ROOT/'pagination_owners.json',ROOT/'native_macro_measurements.json',Path(__file__)]}))
    print('Bound16 source objects/17 native panel candidates;full paragraph andexact FE controls preserved;fresh current FI/null-actor proofs pass.')
if __name__=='__main__':main()
