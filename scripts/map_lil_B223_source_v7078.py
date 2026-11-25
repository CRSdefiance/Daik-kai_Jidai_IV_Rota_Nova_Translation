"""Compare old English only after seventeen whole-exchange clean glosses; inverse all source bytes."""
import struct
from copy import deepcopy
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.lil_B223_source_span_binding_v7078 import source_span_matches_registered_renderer_branches
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_source_v7078')
PRIOR=Path('work/analysis/editorial_handoff_verification_v7073/verified_handoff.json')
GLOSS=Path('work/analysis/lil_B223_clean_context_v7076/all17_clean_Timur_armor_letter_reaction_and_notice_glosses_before_old_English.json')
INPUT=Path('work/analysis/current_V7067_native_v7077/current_native_input.json')
if __name__=='__main__':
    assert not ROOT.exists();prior,gloss=read(PRIOR),read(GLOSS);lp=Path('translations/editorial_review_current_v1.json');assert sha(lp.read_bytes())==prior['ledger_sha256']
    ledger=read(lp);known={historical_key(r) for r in ledger['contextual_story_natural_dialogue_pass_v1871']['record_keys']}
    assert len(known)==6635 and gloss['all17_clean_objects_read_before_prior_English'] and sha(Path(prior['candidate']).read_bytes())==prior['candidate_sha256']==read(INPUT)['current_ROM_sha256']
    clean,current=[NdsImage.open(p) for p in ['work/clean.nds',prior['candidate']]];original,arm=[im.read_file('/__arm9__.bin') for im in [clean,current]]
    source,target=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks[223] for im in [clean,current]]
    inventory,walker,invsource=scoped_inventory();old,spoken=inventory(original,source);now,translated=inventory(arm,target)
    shape=lambda cs:[(c['offset'],c['word'],c['native_extent'],c['ancestor_0100_offsets']) for c in cs]
    assert shape(old)==shape(now) and len(old)==22 and len(spoken)==len(translated)==10
    packet=Path(gloss['source']);raw=read(packet);assert sha(packet.read_bytes())==gloss['source_sha256'] and sha(source)==raw['source_block_sha256'] and old==raw['commands']
    byid={r['id']:r for r in gloss['records']};rows=[];alternatives=[];objects=[];inverse=bytearray(target);regions=[]
    for c,t in zip(spoken,translated,strict=True):
        sa,ca=c['offset']+5,t['offset']+5;value=target[ca:target.index(0,ca+1)];ident=f'DK4_MES_B223_R{source[:sa].count(bytes([0])):04d}';r=deepcopy(byid[ident])
        assert source[sa-5:sa+1]==target[ca-5:ca+1] and bytes.fromhex(r['source_hex'])==source[sa:source.index(0,sa+1)]
        r.update(source_complete_preamble_hex=source[sa-5:sa+1].hex(),current_reference=dict(block=223,offset=ca,bytes=len(value),header_offset=ca-5,record_index=target[:ca].count(bytes([0]))),current_hex=value.hex(),current_record_index=target[:ca].count(bytes([0])),current_native_extent=t['native_extent'],source_native_extent=c['native_extent'],source_prose_or_completion_credit_added=0,current_English_not_read=False,current_native_voice_macro_entry_and_context_pending=True)
        rows.append(r);a,b=c['offset'],c['offset']+c['native_extent'];inverse[a:b]=source[a:b];regions.append(dict(offset=a,bytes=b-a,source_sha256=sha(source[a:b]),current_sha256=sha(target[a:b])))
    for obj in raw['actor_style_objects']:
        at=obj['command']['offset'];c=next(c for c in now if c['offset']==at);assert c['word']==0x4100
        value=bytes.fromhex(c['whole_command_hex']);assert value[:20]==bytes.fromhex(obj['source_complete_header_hex'])
        out=deepcopy(obj);out['source_command']=out.pop('command');out['current_command']=c;out['command_offset']=at;out['source_alias_groups']={str(r['source_reference']['offset']-at):r['style_indices'] for r in obj['records']};out['records']=[]
        for record in obj['records']:
            r=deepcopy(byid[record['id']]);sa=r['source_reference']['offset'];relative=sa-at;currenthex=value[relative:value.index(0,relative)].hex();assert currenthex
            r.update(current_reference=dict(block=223,offset=sa,bytes=len(bytes.fromhex(currenthex)),command_offset=at),current_hex=currenthex,current_record_index=target[:sa].count(bytes([0])),source_prose_or_completion_credit_added=0,current_English_not_read=False,current_actor_role_style_voice_macro_dispatch_and_native_display_pending=True)
            alternatives.append(r);out['records'].append(r)
        objects.append(out);end=at+obj['source_command']['native_extent'] if 'source_command' in obj else at+obj['command']['native_extent'];inverse[at:end]=source[at:end];regions.append(dict(offset=at,bytes=end-at,source_sha256=sha(source[at:end]),current_sha256=sha(target[at:end])))
    assert len(rows)==10 and len(alternatives)==7 and len(objects)==1 and not known&{historical_key(r) for r in rows+alternatives}
    assert (len(source),len(target),8+struct.unpack_from('<H',source,4)[0],8+struct.unpack_from('<H',target,4)[0])==(1316,1316,1316,1316) and source[1316:]==target[1316:]==bytes(0) and bytes(inverse)==source
    for a,b in [(0x2425C,0x243A0),(0x29BD0,0x29D34),(0x2A154,0x2A1D8),(0x7E988,0x7E9A0)]:assert source_span_matches_registered_renderer_branches(arm,original,a,b)
    structural=lambda c:(c['offset'],c['whole_command_hex'][:8] if c['word']==0x100 else c['whole_command_hex'])
    assert [structural(c) for c in old if c['word'] not in [0x4000,0x4100]]==[structural(c) for c in now if c['word'] not in [0x4000,0x4100]]
    assert clean.read_file('/data/EV2.DK4')==current.read_file('/data/EV2.DK4')
    macros={m:sum(bytes.fromhex(r['source_hex'])[1 if r['kind']=='progressive' else 0:].count(m.encode()) for r in rows+alternatives) for m in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=0)
    group=dict(block=223,clean_block_sha256=sha(source),current_block_sha256=sha(target),source_bytes=1316,current_bytes=1316,source_logical_end=1316,current_logical_end=1316,source_tail_bytes=0,current_tail_bytes=0,source_native_commands=old,current_native_commands=now,all_clean_native_commands=old,all_current_native_commands=now,source_current_command_shape_exact=True,all_control_headers_operands_ends_and_complete1316_byte_inverse_exact=True,source_current_prose_container_regions=regions,records=rows,actor_style_objects=objects,choices=[],physical_speeches=10,typed_stored_alternatives=7,source_macro_counts=macros)
    ROOT.mkdir(parents=True);save(ROOT/'all17_clean_current_letter_notices_reactions_full1316_inverse.json',dict(format='dk4-editorial-source-context-packet-v1',file_path='/data/SC2.DK4',source_ROM='work/clean.nds',source_ROM_sha256=sha(Path('work/clean.nds').read_bytes()),current_ROM=prior['candidate'],current_ROM_sha256=prior['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),source_SC2_sha256=sha(clean.read_file('/data/SC2.DK4')),current_SC2_sha256=sha(current.read_file('/data/SC2.DK4')),current_strict_native_input=str(INPUT),current_strict_native_input_sha256=sha(INPUT.read_bytes()),whole_clean_exchange_context_notes=str(GLOSS),whole_clean_exchange_context_notes_sha256=sha(GLOSS.read_bytes()),blocks=[group],records=rows,typed_actor_style_records=alternatives,typed_choice_records=[],total_editorial_objects=17,ordinary_source_speeches=10,system_FE_panels=0,source_static_actor_selectors=[2,13,21],source_dynamic_selectors=[208],source_typed_commands=1,source_style_slots=8,source_typed_stored_alternatives=7,source_native_commands=22,source_relative_sites=sum(c['word'] in [0x100,0x200,0x300,0x400] for c in old),source_predicates=sum(c['word'] in [0x8000,0x8100] for c in old),source_A000=sum(c['word']==0xA000 for c in old),source_macro_counts=macros,all17_source_glosses_precede_old_English_comparison=True,all17_complete_source_current_references_bound=True,raw_current_command_hex_structural_evidence_not_translation_source=True,all_voices_dynamic_roles_controls_conditions_names_macros_native_layout_reference_actual_and_release_gates_pending=True,source_only_context_does_not_prove_natural_event223_activation=True,new_review_credit=0,new_emulator_runs=0,evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,GLOSS,packet,INPUT,Path('scripts/lil_B223_source_span_binding_v7078.py'),Path(__file__)]},full_goal_complete=False))
    for r in rows+alternatives:print(r['id'],repr(bytes.fromhex(r['current_hex'])[1 if r['kind']=='progressive' else 0:].decode('cp932')))
    print('17 disjoint source/current objects; full1316-byte inverse. Effective consumers and editorial decisions pending; no credit.')
