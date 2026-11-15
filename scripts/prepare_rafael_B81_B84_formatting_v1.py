"""Bind330 complete-exchange decisions and16 scoped names to fresh formatting inputs."""
import struct
from collections import Counter
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_B81_B100_clean_20261105')
OUT=Path('work/analysis/Rafael_B81_B84_formatting_20261105')
FINAL=Path('translations/rafael_B81_B84_contextual_editorial_manuscript_v1.json')
CURRENT=Path('work/analysis/Rafael_B81_B84_current_20261105/current_effective.json')
RELEASE=Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json')
MACROS=Path('work/analysis/Rafael_B61_B80_formatting_20261104/own_default_macros_andsource_qualification_v1.json')
P51=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B51_B60_source_identity_checkpoint_v1.json')
P61=Path('work/analysis/Rafael_B61_B80_clean_20261104/source_identity_event_andterm_checkpoint_v1.json')
Q51=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/dependency_qualification.json')
Q61=Path('work/analysis/Rafael_B61_B80_latest_runtime_20261104/dependency_qualification.json')
FRESH=[Path('work/analysis')/folder/'names.json' for folder in [
    'Rafael_B81_B84_new_name_bindings_20261105','Rafael_B81_B84_Angelo_Gerhard_names_20261105']]

def string(raw,pointer):
    if not pointer:return b''
    at=pointer-BASE;assert 0<=at<len(raw)
    return raw[at:raw.index(0,at)]

def main():
    assert not OUT.exists() and not FINAL.exists()
    parts=[ROOT/'B81_B84_325_whole_exchange_comparisons_v1.json',ROOT/'B84_five_choice_comparisons_v1.json']
    speech,choices,current,metadata,macros=map(load,[*parts,CURRENT,ROOT/'current_name_metadata_andclean_event_context_v1.json',MACROS])
    rows=deepcopy(speech['records']);captions=deepcopy(choices['records'])
    assert len(rows)==325 and len(captions)==5
    # The Japanese transitive clause supplies neither an explicit agent nor an object.
    # Preserve this source ambiguity rather than assert either incompatible old reading.
    row=next(r for r in rows if r['id']=='DK4_MES_B81_R0106')
    assert row['source_Japanese']=='がはははは！\nあのバカ、牛と遊んでやがる！\nうひょー！\u3000投げ飛ばしやがった！'
    row['english']="Ha ha! That fool's playing with the bull! Whoa! What a throw!"
    row['source_meaning']='The patron laughs at the fool playing with the bull and cheers a throw;the final Japanese clause leaves the agent and object unstated.'
    row['finding']=row['localization_note']='Preserve the cheering and throw with What a throw!,without adding either the bull threw him or Emilio threw the bull. The Japanese omits both explicit arguments. The complete B81 scene action/transition sample remains required;this prose decision supplies no visual-action finding.'
    row['review']['localization']=True
    row['concrete_source_action_binding_pending']=True
    row['no_agent_object_orvisual_action_claim']=True
    prior={r['id']:r for g in current['groups'] for r in g['records']}
    assert len(prior)==325
    for r in rows:
        assert r['review']==dict(source=True,context=True,localization=True,naturalness=True,formatting=False)
        assert all(r[k]==prior[r['id']][k] for k in ['source_reference','current_reference','source_hex','current_hex','source_complete_preamble_hex'])
        assert all(ord(c)<128 for c in r['english'])
        assert not any(t in r['english'] for t in ['\n','{LB','{ALIGN','{PAD}'])
        assert all(r['english'].count('{MACRO:'+m+'}')==bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for m in ['FI','FA','FO','FU'])
        r.update(kind='system-FE' if r['source_selector']==254 else 'progressive',
            source_record_index=r['source_reference']['record_index'],source_native_extent=r['native_extent'],
            planned_English_markup='{SPEAKER:'+format(r['source_selector'],'02X')+'}'+r['english'],
            prior_macro_normalized_comparison=r['english'] if r['decision']=='retention' else None,
            current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
            native_name_controls_andterm_binding_pending=False,all_fresh_display_andintegration_pending=True)
        if r['source_selector']==254:
            i=r['source_record_index']
            kind='crowd sound' if r['block']==81 else 'boy dialogue with explicit body label' if r['block']==83 else 'knocking sound' if i==80 else 'stat reward notice' if i in [507,566,577] else 'battle tutorial'
            r['source_FE_presentation_kind']=kind
            r['FE_is_not_an_ordinary_actor_nameplate']=True
    assert sum(r['kind']=='system-FE' for r in rows)==14
    assert (sum(r['decision']=='revision' for r in rows),sum(r['decision']=='retention' for r in rows))==(170,155)
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert ctx.receipt()==current['runtime']
    assert metadata['current_ROM_sha256']==current['current_ROM_sha256']
    old=load(P61);old51=load(P51);q51,q61=map(load,[Q51,Q61])
    assert q51['previous_runtime']==old51['runtime'] and q61['previous_runtime']==old['runtime']
    assert q51['all_SC0_COMMON_font_unowned_components_andcomplete_actor_models_exact']
    assert q51['complete_code_unchanged_except_six_typed_text_data_spans']
    assert q61['all_unowned_ARM9_instructions_allocations_tables_andpointers_exact'] and q61['complete_actor_array_androot_exact']
    assert q61['native_name_consumers_anddefault_Rafael_macro_dependencies_compatible']
    # Latest consumer dependencies are byte-identical to the already qualified d459 runtime.
    compatible=RegisteredRuntime(Path(q61['runtime']['release_proof']),Path(q61['runtime']['startup_proof']),captain=0)
    assert ctx.arm==compatible.arm and ctx.common==compatible.common and ctx.actor_root==compatible.actor_root
    assert ctx.actor_bytes==compatible.actor_bytes
    for font in ['/_pxl/fontpanel.pxl','/_pxl/overfont.pxl']:
        assert ctx.image.read_file(font)==compatible.image.read_file(font)
    assert macros['runtime']==q61['runtime'] and macros['macro_ascii_lengths']==dict(FI=6,FA=6,FO=10)
    assert len(macros['own_native_default_macro_cases']['cases'])==4
    assert all(r['output_hex']==b'Rafael Castor Castor Co.'.hex() for r in macros['own_native_default_macro_cases']['cases'])
    actors=sorted({r['source_selector'] for r in rows}-{254})
    assert actors==[0,4,5,6,7,14,15,16,79,82,95,104,113,147,162,167]
    existing={r['actor_ID']:(r,P61) for r in old['name_bindings']}
    for r in old51['name_bindings']:existing.setdefault(r['actor_ID'],(r,P51))
    fresh={actor:(d,p) for p in FRESH for d in [load(p)] for actor in d['actors']}
    clean=NdsImage.open('work/clean.nds');cleanarm=clean.read_file('/__arm9__.bin')
    table,ctable=[struct.unpack_from('<I',a,0xCDAC0)[0]-BASE for a in [ctx.arm,cleanarm]]
    names=[]
    for actor in actors:
        fields=[]
        for col in [0,4,8]:
            at,cat=table+actor*32+col,ctable+actor*32+col
            p,cp=struct.unpack_from('<I',ctx.arm,at)[0],struct.unpack_from('<I',cleanarm,cat)[0]
            fields.append(dict(column=col,current_field=at,current_pointer=p,current_hex=string(ctx.raw,p).hex(),
                source_field=cat,source_pointer=cp,source_hex=string(cleanarm,cp).hex()))
        if actor in fresh:
            d,path=fresh[actor];assert d['runtime']==ctx.receipt()
            consumers=[r for r in d['current_names']['rows'] if r['actor_ID']==actor]
            qualification='fresh scoped clean/current getters'
        else:
            oldrow,path=existing[actor]
            for f,o in zip(fields,oldrow['source_andcurrent_fields'],strict=True):
                assert all(f[k]==o[k] for k in ['column','current_field','current_pointer','current_hex','source_field','source_hex'])
            oldruntime=load(path)['runtime']
            oldraw=Path(oldruntime['snapshot']['path']).read_bytes()
            obj=ctx.actor_root+4+32*actor-BASE
            assert oldraw[obj:obj+32]==ctx.raw[obj:obj+32]
            consumers=oldrow['current_consumers'];qualification='qualified reuse:exact fields,actor object,and prior two owned-data inverse proofs'
        assert len(consumers)==2 and {c['consumer'] for c in consumers}=={'progressive-nameplate','full-catalogue'}
        names.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=[{k:c[k] for k in ['consumer','text','text_hex']} for c in consumers],
            native_proof=str(path),native_proof_sha256=sha(path.read_bytes()),qualification=qualification,full_catalogue_UI_unvisited=True))
    assert ctx.image.read_file('/data/EV0.DK4')==clean.read_file('/data/EV0.DK4')
    OUT.mkdir()
    identity=OUT/'scoped_names_macro_andconsumer_dependency_qualification_v1.json'
    save(identity,dict(runtime=ctx.receipt(),actors=actors,name_bindings=names,fresh_actors=7,qualified_reused_actors=9,
        complete_ARM9_COMMON_font_andactor_array_exact_to_qualified_runtime=True,
        qualified_prior_name_dependencies=[str(Q51),str(Q61)],same_Rafael_default_macro_proof=str(MACROS),
        same_Rafael_default_macro_proof_sha256=sha(MACROS.read_bytes()),macro_ascii_lengths=dict(FI=6,FA=6,FO=10),
        no_new_macro_execution_orordinary_nameplate_gameplay_claim=True,scoped_name_planes_pending=True,
        global_207_name_approval_not_granted=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [P51,P61,Q51,Q61,MACROS,*FRESH,Path(__file__)]}))
    doc=dict(format='dk4-editorial-prose-packet-v1',translation_policy='natural-dialogue-v2',target_locale='en-US',encoder='dialogue-relocatable-v1',
        file_path='/data/SC0.DK4',blocks=[81,82,83,84],current_ROM=current['current_ROM'],current_ROM_sha256=current['current_ROM_sha256'],
        current_archive_sha256=current['current_archive_sha256'],records=rows+captions,review_gates=['source','context','localization','naturalness','formatting'],
        proposed_revisions=173,wording_retentions=157,complete_four_gate_comparisons=330,physical_speech_objects=325,
        ordinary_speech_objects=311,FE_speech_objects=14,typed_choice_objects=5,typed_choice_commands=2,personality_alternatives=0,
        all_formatting_gates_false=True,no_legacy_wraps_orpadding_copied=True,scoped_fullwidth_Latin_fixes=4,
        scoped_identity_proof=str(identity),scoped_identity_proof_sha256=sha(identity.read_bytes()),
        source_FE_classes=dict(Counter(r['source_FE_presentation_kind'] for r in rows if r['source_selector']==254)),
        source_implicit_throw_preserved_without_agent_orobject_invention=True,B81_original_action_andtransition_sample_pending=True,
        registered_release_andcompletion_credit_pending=True,new_credit=0,guide_photos=False,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*parts,CURRENT,identity,Path(__file__)]})
    assert all(all(r['review'][k] for k in ['source','context','localization','naturalness']) and not r['review']['formatting'] for r in doc['records'])
    save(FINAL,doc)
    save(OUT/'formatting_input.json',dict(**doc,source_full_manuscript=str(FINAL),source_full_manuscript_sha256=sha(FINAL.read_bytes())))
    save(OUT/'initial_preferences_v1.json',dict(records={},no_visual_findings_before_native_pages=True))
    print('Prepared330 four-gate reviews:173 revisions/157 retentions;325 speeches/5 typed labels/16 qualified names;fresh display pending.')

if __name__=='__main__':main()
