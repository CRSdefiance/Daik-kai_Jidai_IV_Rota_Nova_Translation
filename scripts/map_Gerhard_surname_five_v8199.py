"""Bind five prior-completed surname consumers after whole clean-context review;not new dialogue credit."""
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_surname_five_v8199')
CENSUS=Path('work/analysis/Gerhard_surname_consumers_v8196/all20_current_Latin_occurrences_five_whole_clean_exchanges.json')
INPUT=Path('work/analysis/current_V8172_Lil_native_v8198/current_native_input.json')
CONTEXTS={
('/data/SC0.DK4',84):'126 clean speeches read completely:town inquiry/Janus hears the surname/Claudio recognizes Gerhard;retired pirate-hunter andVelus betrayal/confidence crisis;conditional persuasion/refusal/return to sea andtraining branches. Same surname,without transferring this retirement/backstory into Hodram-only circumstances. Source titles remain contextual,not a new universal rank.',
('/data/SC0.DK4',85):'10 clean speeches read completely:crew suggests approaching the admiral again;Rafael goes alone,presents himself,requests help andmay gain acceptance after effort. The name is the same family identity across conditional revisit,not a new person.',
('/data/SC2.DK4',27):'51 clean speeches read completely:Lil confronts Hodram,Camille apologizes,Gerhard introduces himself andHodram recognizes the pirate hunter;courteous discussion andlater Camille apology/reassurance/confidentiality. Retain respectful recognition/identity anddo not invent kinship orromance.',
('/data/SC2.DK4',74):'79 clean speeches read completely:Camille leads Lil to a respected former acquaintance;misunderstood wife question is denied;insults,defense ofCamille andGerhard apology;formal introduction/conditional joining;admiral-to-Gerhard address correction andbattle lesson. Preserve the changing address andaspiration forfuture guidance,not a new title ormarriage fact.',
('/data/SC3.DK4',59):'29 clean speeches read completely:Maria andJanus ask townspeople,visit the retired navigator,request his skill andearn acceptance through respectful confidence. Same surname;no Claudio/Velus circumstances grafted into this route.',
}
if __name__=='__main__':
    assert not ROOT.exists();census,inp=map(read,[CENSUS,INPUT]);image=NdsImage.open(inp['current_ROM'])
    assert census['candidate_sha256']==inp['current_ROM_sha256']==sha(Path(inp['current_ROM']).read_bytes())
    ledger=read('translations/editorial_review_current_v1.json');assert ledger['records_editorially_completed']==7171
    groups=[];rows=[]
    for group in census['groups']:
        assert (group['file_path'],group['block']) in CONTEXTS
        if group['file_path']!='/data/SC2.DK4':continue
        number=group['block'];block=IlnkContainer.parse(image.read_file(group['file_path'])).blocks[number]
        selected=[r for r in group['complete_clean_source_records'] if r.get('contains_current_surname')]
        for original in selected:
            row=deepcopy(original);ref=row['current_reference'];raw=bytes.fromhex(row['current_hex'])
            assert block[ref['offset']:ref['offset']+len(raw)+1]==raw+b'\0' and row['current_variants']==['Ardelknatts']
            command=next(c for c in group['all_current_commands'] if c['offset']==ref['header_offset'])
            historical=[(f,r) for f in ledger['completed_editorial_families'] for r in f['records'] if r.get('file_path',f.get('file_path'))==row['file_path'] and r.get('id')==row['id']]
            assert len(historical)==1 and historical[0][1]['decision']=='revised-and-integrated'
            row.update(kind='progressive',source_kind='progressive',current_native_extent=command['native_extent'],current_0100_ancestors=command['ancestor_0100_offsets'],
                current_raw_storage_English=raw[1:].decode('cp932'),raw_storage_comparison_paragraph=' '.join(raw[1:].decode('cp932').split()),
                prior_completed_family=historical[0][0]['id'],already_editorially_completed=True,previous_credit_classification='revised-and-integrated',
                source_context=CONTEXTS[row['file_path'],number],discovery_current_fragments_exposed_before_complete_clean_context_read=True,
                whole_clean_context_now_reread_before_new_English_authoring=True,current_effective_body_dispatch_andcatalogue_pending=True)
            rows.append(row)
        groups.append(dict(file_path=group['file_path'],block=number,records=selected,source_header_hex=group['clean_block_hex'][:16],current_header_hex=block[:8].hex(),
            clean_block_sha256=group['clean_block_sha256'],clean_block_hex=group['clean_block_hex'],current_block_sha256=sha(block),current_block_hex=block.hex(),
            all_source_commands=group['all_clean_commands'],all_current_commands=group['all_current_commands']))
    assert len(rows)==5 and {r['source_selector'] for r in rows}=={1,9,16}
    ROOT.mkdir(parents=True)
    save(ROOT/'five_prior_completed_source_current_refs_andwhole295_source_context_receipt.json',dict(
        current_ROM=inp['current_ROM'],current_ROM_sha256=inp['current_ROM_sha256'],current_ARM9_sha256=inp['current_ARM9_sha256'],current_COMMON_sha256=inp['current_COMMON_sha256'],
        current_archive_sha256=sha(image.read_file('/data/SC2.DK4')),file_path='/data/SC2.DK4',groups=groups,records=rows,
        complete_clean_context_reviews=[dict(file_path=p,block=b,speeches=len(next(g for g in census['groups'] if g['file_path']==p and g['block']==b)['complete_clean_source_records']),review=note) for (p,b),note in CONTEXTS.items()],
        all295_clean_records_reviewed_for_name_identity_context_not_full_new_prose_credit=True,
        correction_scope_one_ARM9_name_slot_five_previously_completed_SC2_records=True,
        fourteen_existing_Adernkatz_occurrences_protected=True,
        new_selected_project_spelling='Adernkatz',decision='Existing Adernkatz follows the clean a-de-ru-n-ka-ttsu sequence andalready serves the same person in14current occurrences. Standardize six inconsistent consumers tothat established form. No definitive official Latin spelling,historical identity ornew biography is claimed.',
        discovery_was_not_a_blind_new_translation=True,subsequent_full_clean_context_is_authority_before_new_English=True,
        current_Hodram_B137_B45_B46_body_English_still_unconsulted=True,
        new_source_prose_credit=0,new_completed_record_credit=0,unique_revised_retained_counts_unchanged_allfive_were_already_revisions=True,
        effective_consumer_profile_layout_native_names_actual_atomic_registered_correction_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CENSUS,INPUT,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Bound5previously revised surname records;295clean-context name review complete.Adernkatz chosen consistently;one name slot/five bodies pending.No duplicate credit.')
