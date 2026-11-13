"""Prepare35 compiler rejection cases and one exact optional hook after fullV3416."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import save
if __name__=='__main__':
    a=Path('scripts/register_lil_B137_v3408b.py');b=Path('scripts/register_lil_B138_v3449.py');assert not b.exists();t=a.read_text(encoding='utf-8')
    changes=[('Register63 guarded reviews after the complete V3300 cumulative stack.','Register44 guarded reviews after the complete V3416 cumulative stack.'),('lil_B137_editorial_v2','lil_B138_editorial_v1'),('lil_B137_registration_v3408b','lil_B138_registration_v3449'),('all-routes-unified-v3409','all-routes-unified-v3450'),('all-routes-unified-v3372','all-routes-unified-v3416'),('all_routes_combined_v3372_candidate','all_routes_combined_v3416_candidate'),('lil_B137_editorial_manuscript_v8','lil_B138_editorial_manuscript_v8'),('lil_B137_editorial_relocation_map_v1','lil_B138_editorial_relocation_map_v2'),('lil_B137_profile','lil_B138_profile'),('lil_B137_layout_v3','lil_B138_layout_v2'),('lil_B137_reference_approval_v3406b','lil_B138_reference_approval_v3446c'),('lil_B137_loader_v3403','lil_B138_loader_v3443b'),('editorial_handoff_verification_v3400','editorial_handoff_verification_v3448b'),('lil_B137_relocation_v3401b','lil_B138_relocation_v3441'),("len(proof['changed_records'])==48","len(proof['changed_records'])==44"),("if '{MACRO:FI}' in r['english']","if '{MACRO:FO}' in r['english']"),(".replace('SPEAKER:02','SPEAKER:09')",".replace('SPEAKER:02','SPEAKER:0E')"),('missing_source_FI','missing_source_FO'),(".replace('{MACRO:FI}','Lil')",".replace('{MACRO:FO}','Argot Co.')"),('source_complete_preamble_hex=\'0040ffff0009\'','source_complete_preamble_hex=\'0040ffff000e\''),('all12_relocated_predicate_pairs_preserve_source_operands_results_and_unowned_RAM','all10_predicates_and1_query_current_relocated_results_and_source_operands_equal'),('all48_active_speech_targets_preserved','all44_active_speech_targets_preserved'),('release_stack_v3408_pending','release_stack_v3449_pending'),('lil_B137_editorial','lil_B138_editorial'),('B137 must run once after the complete V3372 stack','B138 must run once after the complete V3416 stack'),('dk4-lil-B137-editorial-release-v1','dk4-lil-B138-editorial-release-v1')]
    for x,y in changes:assert x in t,x;t=t.replace(x,y)
    begin=t.index("    deps.update(['scripts/research_");end=t.index('    for path in list(deps):',begin)
    names=['research_lil_B138_relocation_v3441','prepare_lil_B138_research_v3442b','verify_lil_B138_loader_v3443b','verify_lil_B138_references_v3444b','prove_lil_B138_relocated_controls_v3445b','seal_lil_B138_references_v3446','correct_lil_B138_reference_metadata_v3448c','verify_editorial_handoff_v3448b','verify_lil_B138_fonts_v3437','approve_lil_B138_native_v3438','author_lil_B138_v3432','lil_B138_dignity_prose_v3432','read_lil_B138_clean_context_v3428','reconcile_lil_B138_terms_v3429','refine_lil_B138_company_complaint_v3434','refine_lil_B138_phrase_flow_v3436','prove_lil_B138_conditional_contract_v3426d','prove_lil_B138_controls_v3426e','prove_lil_crew_items_controls_v3114']
    t=t[:begin]+'    deps.update('+repr(['scripts/'+n+'.py' for n in names])+')\n'+t[end:]
    marker="    changes=[";assert marker in t
    t=t.replace(marker,"    CONTROL=Path(doc['relocated_control_proof'])\n    def ian(d):return next(r for r in d['records'] if r['source_selector']==21)\n    def question(d):return next(r for r in d['records'] if r['id']=='DK4_MES_B138_R0078')\n    def raw2(d):return next(p for p in d['relocated_predicate_pairs'] if p['cases'][0]['source_command_hex']=='0080ffff200301a1')\n"+marker,1)
    marker='    for label,path,key,mutate in changes:';assert marker in t
    extra="""    changes.extend([
      ('missing_original_query',MAP,'reference_map',lambda d:d.update(original_event_queries=[])),
      ('changed_query_operand',MAP,'reference_map',lambda d:d['original_event_queries'][0].update(source_command_hex='00818a00')),
      ('lost_static_Ian21',DOC,'manuscript',lambda d:ian(d).update(source_selector=20)),
      ('changed_wordless_question',DOC,'manuscript',lambda d:question(d).update(english='{SPEAKER:02}!')),
      ('changed_raw_result2',CONTROL,'relocated_control_proof',lambda d:[p['native_result'].__setitem__(1,1) for p in raw2(d)['cases']]),
      ('missing_portable_predicate_constants',CONTROL,'relocated_control_proof',lambda d:d['portable_source_owned_adapters'].update(predicate='def predicate(): pass')),
      ('wrong_source_result_constant',CONTROL,'relocated_control_proof',lambda d:d['source_predicate_result_constants'].update({'0080ffff200301a1':1})),
    ])
"""
    t=t.replace(marker,extra+marker)
    marker="        cp=ROOT/(label+'_config.json')";assert marker in t
    extra="""        if key=='relocated_control_proof':
            d=read(DOC);d.update(relocated_control_proof=str(mp),relocated_control_proof_sha256=sha(mp.read_bytes()));p2=ROOT/(label+'_manuscript.json');save(p2,d);cfg['manuscript']=str(p2);cfg['dependencies'][str(p2)]=sha(p2.read_bytes())
"""
    t=t.replace(marker,extra+marker).replace('len(changes)==24 and len(negatives)==28','len(changes)==31 and len(negatives)==35')
    begin=t.index('    profile.update(');end=t.index("    registry['profiles'][PROFILE]",begin)
    t=t[:begin]+"    profile.update(lil_B138_editorial=owned.CONFIG,description='Complete V3416 cumulative stack plus44 contextual B138 reviews.',note='16 revisions/28 justified retentions;44 progressive speeches,seven static actors/FO1,ten raw predicates/one query137,111 commands/45 spans/225 skips.44 planes/352 logical-compiled/176 final macro cases,six viewed/hash-exact sheets,21 narrow row-count notes. Source raw result2,wordless questions and map/leaf descriptions preserved.35 compiler rejection tests before mutation. Registered build/exact clean patch/fresh startup pending. Experimental;no promotion;preserve every ROM/translation.')\n"+t[end:]
    marker="    after=before.replace(anchor,stage+anchor);compile(after,str(builder),'exec')";assert marker in t
    t=t.replace(marker,marker+"\n    import ast\n    imports=[n.module for n in ast.walk(ast.parse(stage.decode('utf-8'))) if isinstance(n,ast.ImportFrom)]\n    assert imports==[owned.__name__],(imports,owned.__name__)\n    assert stage.count(owned.__name__.encode())==1")
    # Stage indentation belongs to the builder; parse its body as one synthetic scope.
    t=t.replace("ast.parse(stage.decode('utf-8'))","ast.parse('if True:\\n'+stage.decode('utf-8'))")
    t=t.replace('negative_cases=28,','negative_cases=35,stage_key=\'lil_B138_editorial\',compiler=str(Path(owned.__file__)),compiler_sha256=sha(Path(owned.__file__).read_bytes()),stage_import_module=owned.__name__,')
    t=t[:t.rindex('    print(')]+"    print('Registered V3450 B138 stage;35 compiler negatives reject before mutation. Exact hook imports the positively reconstructed compiler. Full V3416/114 accepted layers/V1492 preserved.')\n"
    compile(t,str(b),'exec');b.write_text(t,encoding='utf-8');root=Path('work/analysis/lil_B138_registration_tools_v3449');assert not root.exists();root.mkdir(parents=True)
    save(root/'provenance.json',dict(previous=str(a),previous_sha256=sha(a.read_bytes()),successor=str(b),successor_sha256=sha(b.read_bytes()),producer_sha256=sha(Path(__file__).read_bytes()),no_ROM_registry_or_ledger_mutation=True,full_goal_complete=False))
