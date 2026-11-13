"""Bind539 source meanings to exact identities,conditional membership andunresolved visual cues."""
import struct
from pathlib import Path
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.prove_papal_trade_entries_v7628 import parse_events
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime

ROOT=Path('work/analysis/Rafael_B61_B80_clean_20261104')
RELEASE=Path('work/analysis/Shared_tutorial_name_data_release_verified_20261104/registered_release_verification.json')
PRIOR=Path('work/analysis/Rafael_early_story_B36_B41_B51_B60_clean_20261104/B51_B60_source_identity_checkpoint_v1.json')
QUALIFIED=Path('work/analysis/Rafael_B51_B60_current_runtime_20261104/dependency_qualification.json')
FRESH=Path('work/analysis/Rafael_B61_B80_new_name_bindings_20261104/names.json')

def string(raw,pointer):
    if not pointer:return b''
    at=pointer-BASE;assert 0<=at<len(raw)
    return raw[at:raw.index(0,at)]

if __name__=='__main__':
    output=ROOT/'source_identity_event_andterm_checkpoint_v1.json';assert not output.exists()
    packet_path=ROOT/'clean_source_packet.json';meanings_path=ROOT/'all539_clean_meanings_v1.json';fields_path=ROOT/'clean_name_fields_v1.json'
    packet,meanings,source_fields,prior,qualification,fresh=map(load,[packet_path,meanings_path,fields_path,PRIOR,QUALIFIED,FRESH])
    ctx=RegisteredRuntime(RELEASE,RELEASE.with_name('own_registered_startup_verification.json'),captain=0)
    assert ctx.receipt()==qualification['runtime']==fresh['runtime'] and qualification['previous_runtime']==prior['runtime']
    assert qualification['all_SC0_COMMON_font_unowned_components_andcomplete_actor_models_exact']
    clean=NdsImage.open('work/clean.nds');clean_arm=clean.read_file('/__arm9__.bin')
    assert sha(clean_arm)==packet['source_ARM9_sha256']==source_fields['source_ARM9_sha256']
    clean_table,table=[struct.unpack_from('<I',arm,0xCDAC0)[0]-BASE for arm in [clean_arm,ctx.arm]]
    actors=sorted({r['source_selector'] for r in meanings['records']}-{254})
    assert len(actors)==22 and fresh['actors']==[3,10,40,48,80,83,104,106,113,139,147,179]
    existing={r['actor_ID']:r for r in prior['name_bindings']}
    source_by={r['actor_ID']:r for r in source_fields['records']}
    release=load(RELEASE);registry=load('translations/release_stack.json')
    data_config=load(registry['profiles'][release['profile']]['owned_reviewed_text_data'])
    repaired_path=Path(data_config['name_native']);repaired=load(repaired_path)
    # The two repaired catalogue components already have exact native proofs.
    # Undo only the four disjoint tutorial spans to recover that tested image.
    inverse=bytearray(ctx.arm)
    for span in qualification['source_owned_parent_inverse']['changed_records']:
        if span['kind']!='fixed-tutorial-panel':continue
        at,n=span['physical_offset'],span['owned_bytes'];assert inverse[at:at+n].hex()==span['new_hex']
        inverse[at:at+n]=bytes.fromhex(span['old_hex'])
    assert bytes(inverse)==Path(repaired['proposed_ARM9']).read_bytes() and repaired['original_progressive_andfull_name_getters_pass']
    repaired_rows=next(v['names']['rows'] for v in repaired['versions'] if v['version']=='proposed')
    names=[]
    for actor in actors:
        fields=[]
        for col in [0,4,8]:
            at,source_at=table+32*actor+col,clean_table+32*actor+col
            pointer,source_pointer=struct.unpack_from('<I',ctx.arm,at)[0],struct.unpack_from('<I',clean_arm,source_at)[0]
            current,source=string(ctx.raw,pointer),string(clean_arm,source_pointer)
            expected=next(f for f in source_by[actor]['fields'] if f['column']==col)
            assert expected['source_ARM9_field_offset']==source_at and expected['pointer']==source_pointer and expected['hex']==source.hex()
            fields.append(dict(column=col,source_field=source_at,source_pointer=source_pointer,source_hex=source.hex(),source_text=source.decode('cp932') if source else None,
                current_field=at,current_pointer=pointer,current_hex=current.hex(),current_text=current.decode('cp932') if current else None))
        if actor in fresh['actors']:
            consumers=[r for r in fresh['current_names']['rows'] if r['actor_ID']==actor];proof_path=FRESH;kind='fresh-clean-current-original-getters'
        elif actor in [31,34]:
            consumers=[r for r in repaired_rows if r['actor_ID']==actor];proof_path=repaired_path;kind='exact-reused-repaired-component-getters'
        else:
            previous=existing[actor]
            for field,old in zip(fields,previous['source_andcurrent_fields'],strict=True):
                assert field['column']==old['column'] and field['current_field']==old['current_field'] and field['current_pointer']==old['current_pointer'] and field['current_hex']==old['current_hex']
                assert field['source_field']==old['source_field'] and field['source_hex']==old['source_hex']
            consumers=previous['current_consumers'];proof_path=PRIOR;kind='exact-reused-prior-intrinsic-getters'
        assert len(consumers)==2 and {r['consumer'] for r in consumers}=={'progressive-nameplate','full-catalogue'}
        names.append(dict(actor_ID=actor,source_andcurrent_fields=fields,current_consumers=[{k:r[k] for k in ['consumer','text','text_hex']} for r in consumers],
            native_proof=str(proof_path),native_proof_sha256=sha(proof_path.read_bytes()),qualification=kind,full_catalogue_UI_unvisited=True))
    ev=clean.read_file('/data/EV0.DK4');assert ev==ctx.image.read_file('/data/EV0.DK4')
    events=parse_events(ev);event_groups=[]
    for number in range(61,81):
        selected=[r for r in events if r['script_block']==number]
        dependencies={v for r in selected for v in r['must_be_completed']+r['must_not_be_completed'] if v!=65535}
        event_groups.append(dict(block=number,events=selected,prerequisites=[r for r in events if r['event_ID'] in dependencies],
            numeric_block_order_not_chronology=True,natural_activation_unvisited=True,additional_native_eligibility_predicates_not_executed=True))
    bank=IlnkContainer.parse(clean.read_file('/data/SC0.DK4')).blocks
    term='エシュタード';needle=term.encode('cp932');inventory,_,_=scoped_inventory();term_rows=[]
    for number,block in enumerate(bank):
        if needle not in block:continue
        commands,speeches=inventory(clean_arm,block)
        for command in speeches:
            at=command['offset']+5;raw=block[at:block.index(0,at+1)]
            if needle not in raw[1:]:continue
            term_rows.append(dict(block=number,offset=at,record_index=block[:at].count(b'\0'),source_selector=raw[0],
                source_hex=raw.hex(),source_Japanese=raw[1:].decode('cp932'),source_block_sha256=sha(block)))
    assert any(r['block']==77 for r in term_rows)
    scene=next(g for g in packet['groups'] if g['block']==69)
    byindex={r['source_reference']['record_index']:r for r in scene['records']}
    first,last=[byindex[i]['source_reference']['header_offset'] for i in [202,230]]
    gestures=[r for r in scene['all_source_commands'] if first<=r['offset']<last and r['word']!=0x4000]
    assert len(meanings['records'])==539
    save(output,dict(runtime=ctx.receipt(),records=meanings['records'],actors=actors,name_bindings=names,
        source_EV0_sha256=sha(ev),source_event_context=event_groups,fresh_actors=12,fresh_clean_andcurrent_consumers_each=24,
        exact_reused_actor_name_proofs=10,only_four_unowned_tutorial_spans_separate_repaired_name_proof_from_current_ARM9=True,
        source_term=term,source_term_occurrences=term_rows,approved_English_term_binding_pending=True,
        B69_pause_reaction_apology_nontext_context=gestures,B69_exact_visual_action_unconfirmed=True,
        current_story_English_unconsulted=True,current_name_metadata_only_exposed=True,
        no_global_name_approval_ornew_gameplay_orROM_orcompletion_credit=True,new_credit=0,guide_photos=False,
        evidence={str(p):sha(p.read_bytes()) for p in [packet_path,meanings_path,fields_path,PRIOR,QUALIFIED,FRESH,repaired_path,RELEASE,Path(__file__)]}))
    print('Bound539 meanings/22 identities:12 fresh and10 exact-reused name proofs;20 event contexts;source term andvisual-action cues retained.',flush=True)
    print('Terms',[(r['block'],r['record_index'],r['source_Japanese']) for r in term_rows])
    print('B69 action cues',[(r['offset'],hex(r['word']),r['whole_command_hex']) for r in gestures])
