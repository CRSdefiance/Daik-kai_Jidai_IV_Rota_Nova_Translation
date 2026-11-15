"""First B50 current-English exposure after28clean glosses,complete13-speech dye callback,title context,names/macros andnative source entry/end checks."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.inventory_lil_after_crew_items_complete_v3152 import scoped_inventory
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_current_v8136')
SOURCE=Path('work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json')
GLOSS=Path('work/analysis/Rafael_B50_context_v8135/28_refined_glosses_dye_identity_FA_FI_title_context_before_current_B50_English.json')
NAMES=Path('work/analysis/Rafael_B50_names_current_v8136/three_static_speakers_six_reused_getters_three_reused_voices_exact_V8122_binding.json')
if __name__=='__main__':
    assert not ROOT.exists();source,gloss,names=map(read,[SOURCE,GLOSS,NAMES])
    assert read(gloss['first_source_gloss'])['source_packet_sha256']==sha(SOURCE.read_bytes()) and names['source_gloss_sha256']==gloss['first_source_gloss_sha256']
    assert gloss['all28_current_B50_English_bodies_still_unread'] and names['current_English_B50_bodies_still_unread']
    controls=read('work/analysis/Rafael_B50_source_controls_v8132/source_EV0_entry37_commands28_speeches_no_relative_predicate25_seeded_ends.json')
    assert controls['source_packet_sha256']==sha(SOURCE.read_bytes()) and controls['all37_original_commands28_complete_preambles_andseparate_terminal_tail_bound']
    current=NdsImage.open(names['candidate']);assert sha(Path(names['candidate']).read_bytes())==names['candidate_sha256']
    arm=current.read_file('/__arm9__.bin');archive=current.read_file(source['file_path']);blocks=IlnkContainer.parse(archive).blocks
    assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    assert NdsImage.open(source['source_ROM']).read_file('/data/EV0.DK4')==current.read_file('/data/EV0.DK4')
    inv,walker,fn=scoped_inventory();groups=[];rows=[]
    for sg in source['groups']:
        number=sg['block'];now=blocks[number];commands,speeches=inv(arm,now);before=sg['commands']
        assert [c['word'] for c in commands]==[c['word'] for c in before]
        assert len(speeches)==len(sg['records']) and now[:4]==bytes.fromhex(sg['source_header_hex'])[:4]
        logical=8+int.from_bytes(now[4:6],'little');assert commands[-1]['word']==0 and commands[-1]['offset']+commands[-1]['native_extent']==logical
        assert now[logical:]==bytes(len(now)-logical)
        records=[];mapping=[]
        for a,b in zip(before,commands,strict=True):
            av=bytes.fromhex(sg['clean_block_hex'])[a['offset']:a['offset']+a['native_extent']]
            bv=now[b['offset']:b['offset']+b['native_extent']]
            mapping.append(dict(word=a['word'],source_offset=a['offset'],current_offset=b['offset'],source_extent=a['native_extent'],current_extent=b['native_extent'],source_hex=av.hex(),current_hex=bv.hex(),bytes_equal=av==bv,
                nested_extents_not_disjoint_flat_patch_spans=True,native_relocation_semantics_not_approved_here=True))
        for src,cmd in zip(sg['records'],speeches,strict=True):
            at=cmd['offset']+5;raw=now[at:now.index(0,at+1)]
            assert raw[0]==src['source_selector'] and now[at-5:at+1].hex()==src['source_complete_preamble_hex']
            row=deepcopy(next(r for r in gloss['records'] if r['id']==src['id']))
            row.update(kind='system-FE' if src['source_selector']==254 else 'progressive',source_kind='system-FE' if src['source_selector']==254 else 'progressive',current_reference=dict(block=number,offset=at,bytes=len(raw),header_offset=at-5,record_index=now[:at].count(b'\0')),
                current_hex=raw.hex(),current_record_index=now[:at].count(b'\0'),current_native_extent=cmd['native_extent'],
                current_0100_ancestors=cmd['ancestor_0100_offsets'],current_raw_storage_English=raw[1:].decode('cp932'),
                raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
                current_English_body_unread=False,current_English_dialogue_body_still_unread=False,current_English_dialogue_body_now_exposed=True,current_B50_English_body_still_unread=False,current_effective_body_dispatch_andcatalogue_pending=True)
            records.append(row);rows.append(row)
        groups.append(dict(block=number,file_path=source['file_path'],records=records,source_header_hex=sg['source_header_hex'],current_header_hex=now[:8].hex(),
            clean_block_sha256=sg['clean_block_sha256'],current_block_sha256=sha(now),current_block_hex=now.hex(),current_stored_bytes=len(now),current_logical_end=logical,current_tail_bytes=len(now)-logical,
            all_source_commands=before,all_current_commands=commands,all_command_reference_pairs=mapping,
            source_macro_counts={m:sum(bytes.fromhex(r['source_hex'])[1:].count(m.encode()) for r in records) for m in ['FI','FA','FO']},
            current_raw_macro_counts={m:sum(bytes.fromhex(r['current_hex'])[1:].count(m.encode()) for r in records) for m in ['FI','FA','FO']},
            complete_command_word_order_andall_six_byte_speech_preambles_preserved=True,nontext_control_relocation_branch_andUI_effects_pending=True))
    assert len(rows)==28
    ROOT.mkdir(parents=True);save(ROOT/'all28_complete_source_current_refs_before_new_English_manuscript.json',dict(
        current_ROM=names['candidate'],current_ROM_sha256=names['candidate_sha256'],current_ARM9_sha256=sha(arm),
        current_COMMON_sha256=sha(current.read_file('/COMMON/MESFILE.DK4')),current_archive_sha256=sha(archive),file_path=source['file_path'],
        groups=groups,records=rows,all28_clean_whole_context_glosses_precede_current_English_exposure=True,
        source_explicit_completion_dependencies=[],source_explicit_exclusions=[],source_completion_queries=[],source_EV0_file_preserved_not_natural_activation_approval=True,
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),gloss_packet=str(GLOSS),gloss_packet_sha256=sha(GLOSS.read_bytes()),
        names_andmacros_packet=str(NAMES),names_andmacros_packet_sha256=sha(NAMES.read_bytes()),native_inventory_walker=walker,native_inventory_function=fn,
        raw_storage_not_effective_runtime_orprose_approval=True,new_credit=0,new_emulator_runs=0,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,GLOSS,NAMES,Path(__file__)]},full_goal_complete=False))
    for g in groups:
        print('BLOCK',g['block'],'speeches',len(g['records']),'commands',len(g['all_current_commands']),'stored',g['current_stored_bytes'],'macros',g['source_macro_counts'],g['current_raw_macro_counts'])
        for r in g['records']:print(r['source_record_index'],repr(r['raw_storage_comparison_paragraph']))
