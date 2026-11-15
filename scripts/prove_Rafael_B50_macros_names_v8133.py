"""Reuse exact known six name getters and execute every actual clean B50 FA/FI paragraph at four alignments."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_macros_names_v8133')
GLOSS=Path('work/analysis/Rafael_B50_clean_gloss_v8131/28_first_clean_glosses_three_source_identities_before_current_English.json')
CLEAN_NAMES=Path('work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json')
OLD=Path('work/analysis/Rafael_B49_names_v8078/seven_static_speakers14_getters_clean_fields28_synthetic_macro_alignments.json')
INPUT=Path('work/analysis/current_V8066_Rafael_native_v8069/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();gloss,clean_names,old,inp=map(read,[GLOSS,CLEAN_NAMES,OLD,INPUT])
    assert gloss['source_only_no_current_B50_English_exposed_no_localized_manuscript']
    assert old['candidate_sha256']==inp['current_ROM_sha256']==sha(Path(inp['current_ROM']).read_bytes())
    assert old['current_native_input_sha256']==sha(INPUT.read_bytes())
    image=NdsImage.open(inp['current_ROM']);arm=image.read_file('/__arm9__.bin')
    previous_clean=read(old['source_name_packet']);known=[]
    for c in clean_names['records']:
        ident=c['source_actor_ID'];prior=next(r for r in previous_clean['records'] if r['source_actor_ID']==ident)
        assert prior['fields']==c['fields']
        fields=next(r for r in old['complete_clean_andcurrent_name_fields'] if r['actor_ID']==ident)
        assert len(fields['original_getters'])==2
        known.append(deepcopy(fields))
    assert [r['actor_ID'] for r in known]==[0,2,9]
    ROOT.mkdir(parents=True);ctx=RouteCurrentContext(INPUT,'unused-no-historical-ROM',ROOT/'current_context')
    adapter=old['source_owned_macro_adapter'];env=dict(expand.__globals__);exec(compile(adapter,__file__+'::exact-unchanged-B49-source-owned-macro','exec'),env)
    rows=[]
    for r in gloss['records']:
        body=bytes.fromhex(r['source_hex'])[1:]
        if not any(token in body for token in [b'FI',b'FA',b'FO']):continue
        assert r['source_selector']==9
        result=ctx.execute(env['expand'],body,r['source_selector']);ctx.machines.pop()
        expected=body.replace(b'FI',b'Rafael').replace(b'FA',b'Castor').replace(b'FO',b'Castor Co.')
        assert len(result['cases'])==4 and all(bytes.fromhex(c['output_hex'])==expected for c in result['cases'])
        rows.append(dict(id=r['id'],source_reference=r['source_reference'],source_complete_preamble_hex=r['source_complete_preamble_hex'],
            source_hex=r['source_hex'],source_selector=r['source_selector'],expanded_source_hex=expected.hex(),expanded_source=expected.decode('cp932'),native_alignment=result))
    assert [r['id'] for r in rows]==['DK4_MES_B50_R0040','DK4_MES_B50_R0061','DK4_MES_B50_R0108'] and not ctx.machines
    save(ROOT/'three_clean_FA_FI_paragraphs12_fresh_alignments_six_exact_reused_name_getters.json',dict(
        source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),clean_names=str(CLEAN_NAMES),clean_names_sha256=sha(CLEAN_NAMES.read_bytes()),
        prior_name_andmacro_proof=str(OLD),prior_name_andmacro_proof_sha256=sha(OLD.read_bytes()),candidate=inp['current_ROM'],candidate_sha256=inp['current_ROM_sha256'],
        current_ARM9_sha256=sha(arm),current_native_input=str(INPUT),current_native_input_sha256=sha(INPUT.read_bytes()),
        exact_reused_clean_current_fields_andgetters=known,exact_reused_name_getters=6,fresh_name_getters=0,
        name_andvoice_reuse_requires_exact_source_fields_current_ROM_input_code_andactor_context=True,
        source_macro_counts=dict(FI=1,FA=2,FO=0),records=rows,fresh_source_macro_alignment_cases=12,
        measured_default_substitutions=dict(FI='Rafael',FA='Castor',FO='Castor Co.'),
        FA_uses_default_surname_Castor_not_given_Rafael_FI_distinct=True,
        original_complete_source_CP932_bytes_except_measured_default_substitutions_preserved=True,
        all12_4MiB_ABI_actor_roles_RNG_input_guards_exact=True,
        source_owned_macro_adapter=adapter,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        native_getter_proof_not_fresh_name_localization_full_catalogue_UI_customnames_oractual_scene_approval=True,
        source_title_総帥_anditem_pigment_context_unnamed_occasion_andcurrent_B50_English_comparison_still_pending=True,
        current_B50_English_dialogue_body_still_unread=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [GLOSS,CLEAN_NAMES,OLD,INPUT,Path(__file__)]}))
    print('B50 source macros:FA=Castor/FI=Rafael in all three exact Japanese paragraphs,12fresh alignment cases. Six identical names/getters reused;title/item/context/current body pending;zero credit.')
