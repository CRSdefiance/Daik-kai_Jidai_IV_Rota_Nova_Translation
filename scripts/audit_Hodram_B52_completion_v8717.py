"""Independently audit exactly five B52 credits, direct ROM references and preserved full scope."""
import gzip,json
from collections import Counter
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import complete_Hodram_B52_v8715 as completion
from scripts.reconcile_contextual_mood_retentions_v2482 import historical_key
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B52_completion_audit_v8717')

if __name__=='__main__':
    assert not ROOT.exists();plan=read(completion.ROOT/'staged_completion.json')
    old=json.loads(gzip.decompress((completion.ROOT/'ledger.before.json.gz').read_bytes()))
    new=read(plan['files'][0]['planned']);final=read(completion.FINAL);doc=read(completion.DOC)
    assert completion.restore(new)==old and [new[k]-old[k] for k in completion.COUNTERS]==[5,5,5,2,3]
    oldkeys={historical_key(r) for f in old['completed_editorial_families'] for r in f['records']}
    newkeys={historical_key(r) for f in new['completed_editorial_families'] for r in f['records']}
    rows,approved=final['records'],doc['records']+doc['typed_choice_records']
    assert len(oldkeys)==7229 and len(newkeys)==7234 and newkeys-oldkeys=={historical_key(r) for r in rows}
    assert len(rows)==5 and Counter(r['decision'] for r in rows)==dict(revision=2,retention=3)
    assert [r['id'] for r in rows]==[r['id'] for r in approved]
    current=NdsImage.open(final['candidate']);clean=NdsImage.open('work/clean.nds');predecessor=NdsImage.open(doc['current_ROM'])
    blocks=[IlnkContainer.parse(i.read_file('/data/SC1.DK4')).blocks[52] for i in [clean,predecessor,current]]
    for row,before in zip(rows,approved,strict=True):
        assert row['pre_integration_review_record_preserved']==before
        assert all(row[k]==before[k] for k in ['id','english','source_reference','source_hex','source_meaning','context','localization_note','decision','retention_reason','review','final_reference','final_hex'])
        assert all(row[k] is False for k in completion.PENDING_FLAGS if k in row)
        assert row['current_reference']==before['final_reference'] and row['predecessor_reference']==before['current_reference']
        for bank,ref,raw in [(blocks[0],row['source_reference'],bytes.fromhex(row['source_hex'])),
                             (blocks[1],row['predecessor_reference'],bytes.fromhex(row['predecessor_hex'])),
                             (blocks[2],row['current_reference'],bytes.fromhex(row['current_hex']))]:
            at=ref['offset'];assert bank[at:at+len(raw)+1]==raw+b'\0' and bank[:at].count(b'\0')==ref['record_index']
        assert row['integrated_reference']['ROM_sha256']==sha(Path(final['candidate']).read_bytes())
        assert row['all_current_editorial_formatting_policy_atomic_registered_requirements_completed']
        assert not row['individually_activated_in_current_build'] and row['actual_initialized_source_andEnglish_selected_paths_observed']
        assert row['actual_live_owner_RAM_VRAM_palette_andunowned_backing_byte_identity_unobserved']
    typed=next(r for r in rows if r['id']=='DK4_MES_B52_R0013')
    assert typed['source_reference']['record_index']==13 and typed['current_reference']['record_index']==12 and typed['predecessor_choice_command_offset']==68 and typed['current_choice_command_offset']==72
    scope=read(completion.RELEASE)['actual_scope_limits']
    assert scope['actual_unique_speech_IDs']==['DK4_MES_B52_R0006','DK4_MES_B52_R0021','DK4_MES_B52_R0033']
    assert (scope['complete_page_occurrences'],scope['complete_body_name_holds'],scope['total_actual_frames'])==(12,138,50406)
    assert [g['later_RGB_difference_count'] for g in scope['measured_comparisons']]==[46,13,0]
    assert [g['whole_actors_equal'] for g in scope['measured_comparisons']]==[False,True,True]
    pending=new[completion.NEXT_KEY]
    assert pending['blocks']==[31,53] and pending['physical_speeches']==3 and pending['typed_choice_labels']==0 and pending['completion_credit_added']==0 and pending['current_English_forboth_blocks_still_unconsulted']
    pendingkeys={historical_key(r) for group in pending['source_groups'] for r in group['records']}
    assert len(pendingkeys)==3 and not pendingkeys&newkeys
    assert new['current_integrated_candidate']['sha256']==final['candidate_sha256'] and new['goal_status']=='active' and not new['full_goal_complete']
    assert new['completed_editorial_record_counts_by_file']['/data/SC1.DK4']==154
    assert all(new['completed_editorial_record_counts_by_file'][p]==old['completed_editorial_record_counts_by_file'][p] for p in old['completed_editorial_record_counts_by_file'] if p!='/data/SC1.DK4')
    for index,row in enumerate(plan['files']):
        assert sha(Path(row['target']).read_bytes())==row['before_sha256'] and sha(Path(row['planned']).read_bytes())==row['planned_sha256']
        if index:
            original=gzip.decompress((completion.ROOT/f'{index:02d}.before.gz').read_bytes())
            assert Path(row['planned']).read_bytes().endswith(original)
    ROOT.mkdir(parents=True)
    save(ROOT/'independent_staged_completion_audit.json',dict(exact_full_prior_ledger_inverse=True,five_disjoint_new_keys_only=True,counter_deltas=[5,5,5,2,3],
         three_speeches_two_typed_choices_exact_source_predecessor_final_ROM_references=True,
         canonical_choice_ID13_preserved_despite_final_physical_record12=True,
         all_approved_words_reasons_glosses_andindividual_gates_exact=True,
         all_actual_vs_offline_long_divergence_andfocused_agreement_limits_preserved=True,
         no_natural_activation_orlive_backing_scope_upgrade=True,
         next_three_B31_B53_clean_glosses_disjoint_uncredited_older_English_unread=True,
         full_goal_active_every_prior_family_lead_counter_candidate_anddocument_preserved=True,
         no_shared_ledger_ROM_orregistry_mutation=True,full_goal_complete=False,
         evidence={str(p):sha(Path(p).read_bytes()) for p in [__file__,completion.ROOT/'staged_completion.json',completion.FINAL,completion.DOC,completion.RELEASE]}))
    print('Independent B52 completion audit:exactly5new keys/2revisions/3retentions;all directROMrefs andwhole priorinverse. Choice13->physical12 preserved;three nextglosses uncredited. Full scope active.')
