"""Bind relocated B197 dispatches,three picture boundaries and all eleven source leaves."""
import inspect
from collections import Counter
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.source_locked_derivation_v5118 import native_numbers
from scripts.map_lil_B197_source_v5647 import choice_getters3
from scripts.prepare_lil_B197_research_v5676 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_relocated_controls_v5681')
DOC=Path('translations/lil_B197_editorial_manuscript_v3.json')
MENU=Path('translations/lil_B197_choice_manuscript_v2.json')
FUNDS=Path('work/analysis/lil_B197_funds_v5660/one_exact8500_source_price_one_unforced_and_five_offline_payment_boundaries.json')
if __name__=='__main__':
    assert not ROOT.exists()
    doc,menu,plan=map(read,[DOC,MENU,PLAN]);packet=read(doc['source_context'])
    dp,cp=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract']])
    images=[NdsImage.open(p) for p in [PARENT,ROM]];arm=images[1].read_file('/__arm9__.bin')
    assert images[0].read_file('/__arm9__.bin')==arm
    cleanarm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0x29F80:0x2A210]==cleanarm[0x29F80:0x2A210]
    assert sha(PARENT.read_bytes())==doc['current_ROM_sha256']==plan['candidate_sha256']==cp['candidate_sha256']
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[197] for im in images]
    spec=plan['blocks'][0];assert len(plan['blocks'])==1 and sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    namespace={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),namespace)
    namespace['CATALOG_LOOKUP'],binding=namespace['bind_current_catalog'](images[1])
    # The actual original 47xx dispatch is distinct from historical exact4700.
    # Preserve all old instruction-address constants and add only its separately
    # source-observed return address. No executable ROM byte is changed.
    source=inspect.getsource(picture_base.picture);adapter=source
    changes={
        '[0x4821,0x4822,0x4823,0x4700]':'[0x4821,0x4822,0x4823,0x4700,0x4720,0x4735]',
        'if word==0x4700:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+0x29FEC;desc=None;layout=None':
        'if word in [0x4700,0x4720,0x4735]:assert pc==BASE+0x28A8C and u.reg_read(UC_ARM_REG_LR)==BASE+(0x29FEC if word==0x4700 else 0x2A1EC);assert word==0x4700 or args[1]==word;desc=None;layout=None',
        '(2 if word==0x4700 else 4)':'(2 if word in [0x4700,0x4720,0x4735] else 4)'}
    for a,b in changes.items():assert adapter.count(a)==1;adapter=adapter.replace(a,b)
    compile(adapter,__file__+'::source47xx','exec')
    before,after=map(native_numbers,[source,adapter]);assert not before-after and after-before==Counter({0x2A1EC:1})
    for c in cp['source_A000_and47xx_structural_pairs']:
        if c['word'] not in [0x4720,0x4735]:continue
        for version in c['versions']:
            bridge=version['opaque_effect_bridges'];assert len(bridge)==1
            assert bridge[0]['PC']==picture_base.BASE+0x28A8C and bridge[0]['LR']==picture_base.BASE+0x2A1EC
            assert bridge[0]['args'][1]==c['word']
    env={**picture_base.__dict__};exec(compile(adapter,__file__+'::source47xx','exec'),env)
    ROOT.mkdir(parents=True);ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];pictures=[]
    source_leaves={r['offset']:r for r in dp['source_current_opaque_nonrelative_control_leaves']}
    for r in spec['text_records']:
        value=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(value)]==value
        result=ctx.execute(namespace['dispatch'],value[0],value[1:]);ctx.machines.pop()
        expected,match=namespace['expanded_current_body'](value[1:]);assert match is None
        actor=None if value[0]==254 else rows[r['id']]['source_selector']
        assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==expected.hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        if actor is None:assert result['FE_original_null_actor_calls'] and b'FI' not in value[1:]
        dispatches.append(dict(id=r['id'],new_offset=at,stored_target_hex=value.hex(),**result))
    for c in spec['command_map']:
        word=c['word'];a,b=c['old_offset'],c['new_offset']
        if word in [0x4000,0x100,0x200,0x300,0x400,0x2200]:continue
        raw=new[b:b+c['new_extent']];assert raw==old[a:a+c['old_extent']]
        ref=source_leaves[a];assert ref['word']==word and ref['native_extent']==len(raw) and ref['clean_current_hex']==raw.hex()
        leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        if word in [0x4821,0x4720,0x4735]:
            versions=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                command=dict(offset=at,word=word,native_extent=len(raw),whole_command_hex=raw.hex())
                result=ctx.execute(env['picture'],block,command);ctx.machines.pop();versions.append(dict(version=label,**result))
            assert versions[0]['original_picture_boundary_calls']==versions[1]['original_picture_boundary_calls']
            if word==0x4821:assert versions[0]['original_picture_boundary_calls']==cp['source_picture_pairs'][0]['cases'][1]['original_picture_boundary_calls']
            pictures.append(dict(word=word,old_offset=a,new_offset=b,cases=versions))
    typed=spec['choice_commands'][0];at=typed['new_offset'];raw=new[at:at+typed['new_length']]
    assert len(menu['records'])==3 and all(r['typed_target_object_hex']==raw.hex() for r in menu['records'])
    getters=choice_getters3(arm,dict(offset=at,word=0x2200,native_extent=len(raw),whole_command_hex=raw.hex()))
    assert all(p['count']==3 and [r['text'] for r in p['labels']]==["Let's buy it",'Pass','You decide'] for p in getters)
    assert len(dispatches)==21 and sum(r['resolved_actor_ID'] is None for r in dispatches)==1
    assert len(leaves)==11 and len(pictures)==3 and not ctx.machines
    assert sum(r['word']==0xA000 for r in leaves)==5 and sum(r['word']==0 for r in leaves)==1
    funds=read(FUNDS);assert funds['candidate_sha256']==doc['current_ROM_sha256']
    assert funds['source8500_price_matches_exact_native_payment_amount'] and len(funds['cases'])==6
    save(ROOT/'all21_dispatches_three_picture_pairs_one_menu_and11_exact_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),ARM9_sha256=sha(arm),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all11_source_current_target_nonrelative_nonspeech_nonchoice_leaves=leaves,
        picture_and47xx_current_relocated_pairs=pictures,relocated_three_option_getters=getters,
        source_derived_picture47xx_adapter=adapter,original_high_instruction_constants_preserved_and_only_original_47xx_return_address_added=True,
        original47xx_entire_word_argument_and_source_return_address_exact=True,
        twenty_progressive_actors_one_null_actor_FE_no_macros=True,one_three_option_menu_and_common_end_preserved=True,
        six_payment_boundaries_ten632E_ten6003_boundaries_and_seven_opaque_structural_pairs_reused=True,
        reuse_requires_identical_whole_ARM9_original_snapshot_and_complete_command_bytes=True,
        picture_resource_item_Charm_and6003_bodies_not_executed_by_this_probe=True,
        no_visual_semantics_guessed_from_short47xx_words=True,actual_English_selection_association_and_scene_transition_pending=True,
        registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MENU,PLAN,FUNDS,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]},
        new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('B19721 dispatches,three picture/current-target pairs,one2200 and11 exact leaves pass.4720/4735 native caller/whole-word argument bound;effect/visual bodies unexecuted. English actual next.')
