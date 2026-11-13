"""Expose current English only after complete clean exchanges and first glosses; no ROM writes or credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.gloss_Hodram_B137_B45_B46_v8183 import ROOT as GLOSS_ROOT,PACKETS
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B137_B45_B46_current_v8239')
GLOSS=GLOSS_ROOT/'28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json'
NAMES=Path('work/analysis/Hodram_B137_B45_B46_names_v8192/six_static_speakers12_getters_clean_fields24_synthetic_macro_alignments.json')

if __name__=='__main__':
    assert not ROOT.exists()
    gloss,names=map(read,[GLOSS,NAMES]);packets={b:read(p) for b,p in PACKETS.items()}
    assert names['source_gloss_sha256']==sha(GLOSS.read_bytes())
    assert all(r['current_English_body_not_yet_consulted'] for r in gloss['records'])
    ledger=read('translations/editorial_review_current_v1.json')
    assert ledger['records_editorially_completed']==7171 and not ledger['full_goal_complete']
    image=NdsImage.open(names['candidate']);assert sha(Path(names['candidate']).read_bytes())==names['candidate_sha256']
    arm=image.read_file('/__arm9__.bin');archive=image.read_file('/data/SC1.DK4');blocks=IlnkContainer.parse(archive).blocks
    assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    inv,walker,fn=scoped_inventory();groups=[];rows=[]
    for number in [137,45,46]:
        source=packets[number];sg=source['groups'][0];now=blocks[number];clean=bytes.fromhex(sg['clean_block_hex'])
        assert source['file_path']=='/data/SC1.DK4' and sg['block']==number
        assert NdsImage.open(source['source_ROM']).read_file('/data/EV1.DK4')==image.read_file('/data/EV1.DK4')
        commands,speeches=inv(arm,now);before=sg['commands']
        assert [c['word'] for c in commands]==[c['word'] for c in before]
        assert len(speeches)==len(sg['records']) and now[:4]==clean[:4]
        logical=8+int.from_bytes(now[4:6],'little')
        assert commands[-1]['word']==0 and commands[-1]['native_extent']==4 and commands[-1]['offset']+4==logical
        assert now[logical:]==bytes(len(now)-logical)
        mapping=[];records=[]
        for a,b in zip(before,commands,strict=True):
            av=clean[a['offset']:a['offset']+a['native_extent']];bv=now[b['offset']:b['offset']+b['native_extent']]
            mapping.append(dict(word=a['word'],source_offset=a['offset'],current_offset=b['offset'],source_extent=a['native_extent'],current_extent=b['native_extent'],source_hex=av.hex(),current_hex=bv.hex(),bytes_equal=av==bv,
                source_0100_ancestors=a['ancestor_0100_offsets'],current_0100_ancestors=b['ancestor_0100_offsets'],native_relocation_semantics_not_approved_here=True))
        for src,cmd in zip(sg['records'],speeches,strict=True):
            at=cmd['offset']+5;raw=now[at:now.index(0,at+1)]
            assert raw[0]==src['source_selector'] and now[at-5:at+1].hex()==src['source_complete_preamble_hex']
            row=deepcopy(next(r for r in gloss['records'] if r['id']==src['id']))
            row.update(kind='progressive',source_kind='progressive',current_reference=dict(file_path='/data/SC1.DK4',block=number,offset=at,bytes=len(raw),header_offset=at-5,record_index=now[:at].count(b'\0')),
                current_hex=raw.hex(),current_record_index=now[:at].count(b'\0'),current_native_extent=cmd['native_extent'],current_0100_ancestors=cmd['ancestor_0100_offsets'],
                current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
                current_English_body_unread=False,current_English_body_not_yet_consulted=False,current_English_dialogue_body_now_exposed=True,
                current_effective_body_dispatch_andcatalogue_pending=True,source_presentation_consumer_not_yet_approved=False,
                source_preamble_andstatic_actor_mapping_bound=True,formatting_actual_andregistered_release_pending=True)
            assert not row['already_contextually_completed']
            records.append(row);rows.append(row)
        groups.append(dict(block=number,file_path='/data/SC1.DK4',records=records,source_header_hex=sg['source_header_hex'],current_header_hex=now[:8].hex(),clean_block_hex=sg['clean_block_hex'],
            clean_block_sha256=sg['clean_block_sha256'],current_block_sha256=sha(now),current_block_hex=now.hex(),current_stored_bytes=len(now),current_logical_end=logical,current_tail_bytes=len(now)-logical,
            all_source_commands=before,all_current_commands=commands,all_command_reference_pairs=mapping,
            source_event_records=sg['source_event_records'],source_macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in records) for m in ['FI','FA','FO']},
            current_raw_macro_counts={m:sum(bytes.fromhex(r['current_hex'])[1:].count(m.encode()) for r in records) for m in ['FI','FA','FO']},
            complete_command_word_order_andall_six_byte_speech_preambles_preserved=True,nontext_control_relocation_actual_effects_pending=True))
    assert len(rows)==28 and sum(len(g['all_current_commands']) for g in groups)==60
    assert {r['source_selector'] for r in rows}=={1,2,9,16,18,113}
    ROOT.mkdir(parents=True)
    save(ROOT/'28_exact_clean_current_refs_after_whole_source_glosses.json',dict(current_ROM=names['candidate'],current_ROM_sha256=names['candidate_sha256'],current_ARM9_sha256=sha(arm),
        current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),current_archive_sha256=sha(archive),file_path='/data/SC1.DK4',groups=groups,records=rows,
        clean_whole_exchanges_and27_prior_B44_source_callbacks_read_before_current_English=True,source_gloss=str(GLOSS),source_gloss_sha256=sha(GLOSS.read_bytes()),
        explicit_event_graph=gloss['explicit_event_graph'],raw_storage_not_effective_runtime_orprose_approval=True,
        name_asset_dependency='Gerhard Adernkatz correction must be explicitly registered before this batch integrates;V8172 still has Ardelknatts.',
        native_inventory_walker=walker,native_inventory_function=fn,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*PACKETS.values(),GLOSS,NAMES,Path(__file__)]}))
    for g in groups:
        print('BLOCK',g['block'],'speeches',len(g['records']),'commands',len(g['all_current_commands']))
        for r in g['records']:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))
