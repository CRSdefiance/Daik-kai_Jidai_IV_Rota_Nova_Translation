"""Final B201 source-owned dispatches,typed menu,opaque leaves and mapped picture/47xx calls."""
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_build_native_context_v4774 import CurrentContext
from scripts import prove_lil_shrines_temples_controls_v3168c as dispatch_base
from scripts import prove_lil_B145_picture_controls_v3587 as picture_base
from scripts.map_lil_B122_B127_source_v3260c import choice_getters
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.prepare_lil_B201_reference_tools_v5934 import ROM,PARENT,PLAN
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_relocated_controls_v5938')
DOC=Path('translations/lil_B201_editorial_manuscript_v6.json')
MENU=Path('translations/lil_B201_choice_manuscript_v3.json')

if __name__=='__main__':
    assert not ROOT.exists();doc,menu,plan=map(read,[DOC,MENU,PLAN]);packet=read(doc['source_context'])
    dp,cp=map(read,[doc['control_contract'],doc['source_effect_and_predicate_contract']]);images=[NdsImage.open(p) for p in [PARENT,ROM]]
    arm=images[1].read_file('/__arm9__.bin');assert arm==images[0].read_file('/__arm9__.bin')
    old,new=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[201] for im in images];spec=plan['blocks'][0]
    assert sha(old)==spec['source_block_sha256'] and sha(new)==spec['research_block_sha256']
    env={**dispatch_base.__dict__,'SOURCE':Path(doc['source_context']),'CATALOG_LOOKUP':{}}
    for name,text in dp['source_owned_adapters'].items():exec(compile(text,__file__+'::'+name,'exec'),env)
    env['CATALOG_LOOKUP'],binding=env['bind_current_catalog'](images[1])
    pic=checked_text(cp['native_adapters']['picture47xx'],{'0x4830,0x4735':'0x4830,0x4735,0x4720,0x4721','[0x4700,0x4735]':'[0x4700,0x4735,0x4720,0x4721]'})
    pe=dict(picture_base.__dict__);exec(compile(pic,__file__+'::source-short-picture-calls','exec'),pe)
    ROOT.mkdir(parents=True);ctx=CurrentContext(dp['native_input'],packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};dispatches=[];leaves=[];pictures=[];menus=[]
    for r in spec['text_records']:
        raw=bytes.fromhex(r['target_hex']);at=r['new_offset'];assert new[at:at+len(raw)]==raw
        result=ctx.execute(env['dispatch'],raw[0],raw[1:]);ctx.machines.pop();expected,match=env['expanded_current_body'](raw[1:]);assert match is None
        actor=None if raw[0]==254 else rows[r['id']]['source_selector'];assert result['resolved_actor_ID']==actor and result['registered_catalog_match'] is None
        assert result['boundaries'][1]['text_hex']==expected.hex() and result['all4MiB_actor_role_RNG_input_and_ABI_guards_exact']
        for m in [b'FI',b'FA',b'FO']:assert raw[1:].count(m)==bytes.fromhex(rows[r['id']]['source_hex'])[1:].count(m)
        if actor is None:assert result['FE_original_null_actor_calls']
        dispatches.append(dict(id=r['id'],new_offset=at,stored_target_hex=raw.hex(),**result))
    for c in spec['command_map']:
        word=c['word'];a,b=c['old_offset'],c['new_offset']
        if word in [0x4000,0x100,0x200,0x300,0x400,0x2100]:continue
        raw=new[b:b+c['new_extent']];assert raw==old[a:a+c['old_extent']]
        original=next(r for r in cp['all15_source_current_nonrelative_nonspeech_nonchoice_leaves'] if r['offset']==a)
        assert original['whole_command_hex']==raw.hex();leaves.append(dict(word=word,old_offset=a,new_offset=b,source_current_target_hex=raw.hex()))
        if word in [0x4830,0x4720,0x4721]:
            versions=[]
            for label,block,at in [('current',old,a),('relocated',new,b)]:
                command=dict(offset=at,word=word,native_extent=len(raw),whole_command_hex=raw.hex());result=ctx.execute(pe['picture'],block,command);ctx.machines.pop();versions.append(dict(version=label,**result))
            left,right=[v['original_picture_boundary_calls'] for v in versions]
            if word==0x4830:assert left==right
            else:
                assert len(left)==len(right)==1
                assert {k:v for k,v in left[0].items() if k!='args'}=={k:v for k,v in right[0].items() if k!='args'}
                assert left[0]['args'][:3]==right[0]['args'][:3] and left[0]['args'][3]==0x02660000+a and right[0]['args'][3]==0x02660000+b
            pictures.append(dict(word=word,old_offset=a,new_offset=b,cases=versions))
    for c in spec['choice_commands']:
        raw=new[c['new_offset']:c['new_offset']+c['new_length']];assert raw.hex()==c['target_hex']
        command=dict(offset=c['new_offset'],word=0x2100,native_extent=len(raw),whole_command_hex=raw.hex())
        getters=choice_getters(arm,command);assert all(p['count']==2 and [r['text'] for r in p['labels']]==['Buy','Pass'] for p in getters)
        menus.append(dict(old_offset=c['old_offset'],new_offset=c['new_offset'],native_getter_phases=getters,record_IDs=c['record_IDs']))
    assert len(dispatches)==24 and sum(r['resolved_actor_ID'] is None for r in dispatches)==3 and len(leaves)==15 and len(pictures)==3 and len(menus)==1 and not ctx.machines
    assert sum(r['word']==0xA000 for r in leaves)==6 and sum(r['word']==0 for r in leaves)==1
    assert len(cp['source632E_thirty_boundary_cases'])==30 and len(cp['two_source6003_twenty_boundary_cases'])==20 and len(cp['six_A000_and_two_short47xx_structural_pairs'])==8
    save(ROOT/'all24_dispatches_two_FI_one_picture_two47xx_menu_and15_exact_leaves.json',dict(
        candidate=str(PARENT),candidate_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        manuscript=str(DOC),manuscript_sha256=sha(DOC.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),
        relocated_dispatch_cases=dispatches,all15_source_current_target_control_leaves=leaves,picture_and_short47xx_pairs=pictures,relocated_menu_getters=menus,
        all21_progressive_three_null_actor_FE_and_two_FI_preserved=True,
        original30_resource20_audio_boundaries_and_eight_structural_pairs_reused_by_exact_bytes_and_current_snapshot=True,
        original_four_relative_sites20_target_skip_cases_and_one_two_option_menu_preserved=True,
        six_A000_and_picture_operands_not_promoted_to_complete_item_stat_or_affordability_semantics=True,
        source_owned_short_picture_adapter=pic,registered_catalog_binding=binding,native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        evidence={str(p):sha(p.read_bytes()) for p in [DOC,MENU,PLAN,Path(doc['control_contract']),Path(doc['source_effect_and_predicate_contract']),Path(__file__)]},
        actual_English_scene_and_menu_association_pending=True,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False))
    print('24 relocated dispatches/twoFI/threeFE,one picture/two short47xx pairs,one menu and15 exact leaves pass;resource/audio/effect boundaries reused by exact bytes.')
