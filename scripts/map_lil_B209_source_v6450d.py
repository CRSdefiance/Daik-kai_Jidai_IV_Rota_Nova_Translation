"""Bind exact source/current references for the complete letter exchange and all voice alternatives."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save
from scripts.lil_B209_source_span_binding_v6450c import source_span_matches_registered_renderer_branches
ROOT=Path('work/analysis/lil_B209_source_v6450d')
PRIOR=Path('work/analysis/editorial_handoff_verification_v6445/verified_handoff.json')
GLOSS=Path('work/analysis/lil_B209_clean_context_v6448/all20_clean_letter_and_voice_alternative_glosses.json')
INPUT=Path('work/analysis/current_V6439_native_v6449/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,gloss=read(PRIOR),read(GLOSS);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256']
    ledger=read(lp);candidate=ledger['current_integrated_candidate'];known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==6452 and sha(Path(candidate['path']).read_bytes())==candidate['sha256']==prior['candidate_sha256']==read(INPUT)['current_ROM_sha256']
    clean,current=[NdsImage.open(p) for p in ['work/clean.nds',candidate['path']]];original,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]]
    source,target=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[209] for im in [clean,current]]
    inventory,walker,invsource=scoped_inventory();old,spoken=inventory(original,source);now,translated=inventory(arm,target)
    shape=lambda cs:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in cs]
    assert shape(old)==shape(now) and len(old)==18 and len(spoken)==5
    packet=Path(gloss['source']);raw=read(packet);assert sha(packet.read_bytes())==gloss['source_sha256'] and sha(source)==raw['source_block_sha256'] and old==raw['commands'] and gloss['prior_English_unread']
    byid={r['id']:r for r in gloss['records']};rows=[];alternatives=[];objects=[]
    for c,t in zip(spoken,translated,strict=True):
        sa,ca=c['offset']+5,t['offset']+5;value=target[ca:target.index(0,ca+1)];ident=f'DK4_MES_B209_R{source[:sa].count(bytes([0])):04d}'
        r=deepcopy(byid[ident]);assert source[sa-5:sa+1]==target[ca-5:ca+1] and bytes.fromhex(r['source_hex'])==source[sa:source.index(0,sa+1)]
        r.update(source_complete_preamble_hex=source[sa-5:sa+1].hex(),current_reference=dict(block=209,offset=ca,bytes=len(value),header_offset=ca-5,record_index=target[:ca].count(bytes([0]))),current_hex=value.hex(),current_record_index=target[:ca].count(bytes([0])),current_native_extent=t['native_extent'],source_native_extent=c['native_extent'],source_prose_or_completion_credit_added=0,current_native_voice_macro_entry_and_context_pending=True)
        rows.append(r)
    for obj in raw['actor_style_objects']:
        at=obj['command']['offset'];c=next(c for c in now if c['offset']==at);assert c['word']==0x4100
        value=bytes.fromhex(c['whole_command_hex']);assert value[:20]==bytes.fromhex(obj['source_complete_header_hex'])
        out=deepcopy(obj);out['source_command']=out.pop('command');out['current_command']=c;out['command_offset']=at;out['source_alias_groups']={str(r['source_reference']['offset']-at):r['style_indices'] for r in obj['records']};out['records']=[]
        for record in obj['records']:
            r=deepcopy(byid[record['id']]);sa=r['source_reference']['offset'];relative=sa-at;currenthex=value[relative:value.index(0,relative)].hex();assert currenthex
            r.update(current_reference=dict(block=209,offset=sa,bytes=len(bytes.fromhex(currenthex)),command_offset=at),current_hex=currenthex,current_record_index=target[:sa].count(bytes([0])),source_prose_or_completion_credit_added=0,current_actor_role_style_voice_macro_dispatch_and_native_display_pending=True)
            alternatives.append(r);out['records'].append(r)
        objects.append(out)
    assert len(rows)==5 and len(alternatives)==15 and not known&{historical_key(r) for r in rows+alternatives}
    assert (len(source),len(target),8+struct.unpack_from('<H',source,4)[0],8+struct.unpack_from('<H',target,4)[0])==(1148,1148,1148,1148)
    for a,b in [(0x2425C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x7E988,0x7E9A0)]:assert source_span_matches_registered_renderer_branches(arm,original,a,b)
    nontext=[c for c in old if c['word'] not in [0x4000,0x4100]]
    structural=lambda c:(c['offset'],c['whole_command_hex'][:8] if c['word']==0x100 else c['whole_command_hex'])
    assert [structural(c) for c in nontext]==[structural(c) for c in now if c['word'] not in [0x4000,0x4100]]
    assert clean.read_file('/data/EV2.DK4')==current.read_file('/data/EV2.DK4')
    group=dict(block=209,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=len(source),current_bytes=len(target),source_logical_end=1148,current_logical_end=1148,source_tail_bytes=0,current_tail_bytes=0,source_native_commands=old,current_native_commands=now,all_clean_native_commands=old,all_current_native_commands=now,source_current_command_shape_exact=True,records=rows,actor_style_objects=objects,choices=[],physical_speeches=5,typed_stored_alternatives=15)
    ROOT.mkdir(parents=True);save(ROOT/'all20_clean_current_letter_and_voice_alternative_context.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=candidate['path'],current_ROM_sha256=candidate['sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),current_strict_native_input=str(INPUT),current_strict_native_input_sha256=sha(INPUT.read_bytes()),whole_clean_exchange_context_notes=str(GLOSS),whole_clean_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),blocks=[group],records=rows,typed_actor_style_records=alternatives,typed_choice_records=[],total_editorial_objects=20,ordinary_source_speeches=5,system_FE_panels=0,source_static_actor_selectors=[2,11,12],source_dynamic_selectors=[208],source_typed_commands=2,source_style_slots=16,source_typed_stored_alternatives=15,source_native_commands=18,source_relative_sites=sum(c['word'] in [0x100,0x200,0x300,0x400] for c in old),source_predicates=sum(c['word'] in [0x8000,0x8100] for c in old),source_A000=sum(c['word']==0xA000 for c in old),all20_source_glosses_precede_old_English_comparison=True,all20_complete_source_current_references_bound=True,raw_current_command_hex_structural_evidence_not_translation_source=True,all_voices_dynamic_roles_controls_conditions_names_macros_native_layout_reference_actual_and_release_gates_pending=True,source_only_context_does_not_prove_natural_event209_activation=True,new_review_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [Path('scripts/lil_B209_source_span_binding_v6450c.py'),PRIOR,GLOSS,packet,INPUT,Path(__file__)]},full_goal_complete=False))
    for r in rows+alternatives:print(r['id'],bytes.fromhex(r['current_hex'])[1 if r['kind']=='progressive' else 0:].decode('cp932').replace('\n',' / '))
    print('20 disjoint source/current objects bound to V6439. Full current consumers/effective prose and editorial decisions pending;no credit.')
