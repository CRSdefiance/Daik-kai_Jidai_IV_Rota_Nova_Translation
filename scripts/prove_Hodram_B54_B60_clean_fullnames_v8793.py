"""Execute complete original name getters on clean-only ordinary fixtures, with full inverse."""
from pathlib import Path
from types import SimpleNamespace
from copy import deepcopy
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.execute_map_entity_tooltip_copy import machine_for,BASE
from scripts.audit_native_given_name_table import ordinary_getter
from scripts.probe_button_prompt_native import call
from scripts.prove_lil_B167_names_v4124b import names
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B54_B60_clean_names_v8793')
NAMES=Path('work/analysis/Hodram_B54_B60_names_v8792/ten_source_identities_current_getters_voices_andplanes.json')
PRECEDENT=Path('work/analysis/Hodram_actor34_clean_name_composition_v8732/clean_source_full_andprogressive_name_composition.json')

if __name__=='__main__':
    assert not ROOT.exists();prior,precedent=map(read,[NAMES,PRECEDENT]);image=NdsImage.open('work/clean.nds')
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4');assert sha(arm)==precedent['clean_ARM9_sha256'] and prior['current_B54_B60_English_dialogue_bodies_unconsulted']
    actors=[r['actor_ID'] for r in prior['complete_clean_current_static_fields']];root=precedent['source_native_getters'][0]['actor_fixture']-4-32*34
    objects={ident:root+4+32*ident for ident in actors};state={}
    def clean_machine(a,c,r,p):
        assert a==arm and c==common and r==b'' and p=={'explicit_clean_ordinary_name_fixtures':True}
        cpu=machine_for(a)
        # Reuse the original adapter's complete memory-span constant verbatim.
        import ast,inspect
        spans=[n.args[1].value for n in ast.walk(ast.parse(inspect.getsource(names))) if isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr=='mem_read' and len(n.args)==2 and isinstance(n.args[0],ast.Constant) and n.args[0].value==BASE and isinstance(n.args[1],ast.Constant) and type(n.args[1].value)is int]
        assert spans and len(set(spans))==1;whole_length=spans[0]
        before=bytes(cpu.mem_read(BASE,whole_length));executed=set()
        def exact(u,pc,size,unused):
            assert BASE<=pc and pc+size<=BASE+len(a) and bytes(u.mem_read(pc,size))==a[pc-BASE:pc-BASE+size]
            executed.add(pc)
        hook=cpu.hook_add(UC_HOOK_CODE,exact)
        for ident in actors:ordinary_getter(a,ident,machine=cpu)
        constructed=bytes(cpu.mem_read(BASE,whole_length));inverse=bytearray(constructed)
        for actor in objects.values():inverse[actor-BASE:actor-BASE+4]=before[actor-BASE:actor-BASE+4]
        assert bytes(inverse)==before
        def get(offset,*args):
            call(cpu,offset,tuple(args));return cpu.reg_read(UC_ARM_REG_R0)
        state.update(cpu=cpu,before=before,constructed=constructed,whole_length=whole_length,hook=hook,executed=executed)
        return cpu,get,SimpleNamespace(executed_current=executed)
    import inspect
    adapter=checked_text(inspect.getsource(names),{
        'for ident in [2,4,13,23,109]:':'for ident in ACTORS:',
        'actor = root+4+32*ident':'actor = ACTOR_OBJECTS[ident]',
        'all_ten_original_consumers_and_owned_or_readonly_memory_paths_exact':'all_twenty_clean_original_consumers_and_owned_or_readonly_memory_paths_exact',
    })
    env={**names.__globals__,'ACTORS':actors,'ACTOR_OBJECTS':objects,'machine':clean_machine};exec(compile(adapter,__file__+'::clean-ordinary-getters','exec'),env)
    getters=env['names'](arm,common,b'',{'explicit_clean_ordinary_name_fixtures':True});assert len(getters['rows'])==20
    cpu=state['cpu'];assert bytes(cpu.mem_read(BASE,state['whole_length']))==state['constructed']
    for actor in objects.values():cpu.mem_write(actor,state['before'][actor-BASE:actor-BASE+4])
    assert bytes(cpu.mem_read(BASE,state['whole_length']))==state['before'];cpu.hook_del(state['hook'])
    fields={r['actor_ID']:r for r in prior['complete_clean_current_static_fields']}
    bindings=[]
    for row in getters['rows']:
        entry=fields[row['actor_ID']];progressive=next(r for r in getters['rows'] if r['actor_ID']==row['actor_ID'] and r['consumer']=='progressive-nameplate')
        current=next(r for r in prior['fresh_twenty_progressive_andfull_current_getters']['rows'] if (r['actor_ID'],r['consumer'])==(row['actor_ID'],row['consumer']))
        bindings.append(dict(actor_ID=row['actor_ID'],consumer=row['consumer'],clean_text=row['text'],clean_text_hex=row['text_hex'],current_text=current['text'],current_text_hex=current['text_hex'],
            clean_static_fields=deepcopy(entry['clean']),current_static_fields=deepcopy(entry['current']),
            clean_full_equals_progressive=row['text']==progressive['text'],
            actual_current_resolved_actor_object=current['actor_object'],ordinary_clean_fixture_not_actual_captain_orcatalogue_UI=True))
    esp=next(r for r in bindings if r['actor_ID']==36 and r['consumer']=='full-catalogue');assert 'デ' in esp['clean_text'] and 'デ' in esp['current_text']
    ROOT.mkdir(parents=True);save(ROOT/'twenty_clean_full_andprogressive_compositions_current_binding.json',dict(
        clean_ROM='work/clean.nds',clean_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),clean_ARM9_sha256=sha(arm),source_native_getters=getters,
        clean_current_consumer_bindings=bindings,all_clean_constructor_andname_scratch_ring_writes_reversed_to_initial_memory=True,
        every_instruction_exact_clean_ARM9=True,no_current_orhistorical_initialized_RAM_overlay=True,
        original_generic_role_fullgetters_do_not_compose_regional_surname_metadata=True,
        source_ordinary_captain_default_components_not_custom_player_name_oractual_clean_UI=True,
        Geronimo_middle_component_actual_source_fullgetter_contains_de_kana_not_unused=True,
        Geronimo_untranslated_current_middle_component_requires_ownership_consumer_andeditorial_review=True,
        original_name_adapter=adapter,current_B54_B60_English_dialogue_bodies_unconsulted=True,
        no_actual_clean_orcurrent_scene_header_fullcatalogue_UI_all207_orcustomname_approval=True,
        new_credit=0,new_emulator_runs=0,no_ROM_registry_orledger_change=True,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [NAMES,PRECEDENT,Path(__file__)]}))
    print('20clean original name compositions/current binding pass;all constructor/ring writes reversed. Generic regional fields unused inlabels;Geronimo デ iscomposed inactual fullgetter. No gameplay,ROM orcredit.',flush=True)
