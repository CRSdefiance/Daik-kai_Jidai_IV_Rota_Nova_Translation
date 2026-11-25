"""Combine disjoint checked text blocks;reuse exact local proofs without replaying them."""
import gc
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/Rafael867_combined_research_v1_20261105')
PRIOR=Path('work/analysis/Rafael516_combined_research_v1_20261105/reconstruction.json')
NEW=Path('work/analysis/Rafael351_rebuilt678_v2_20261105/reconstruction.json')
REVIEW=Path('translations/rafael_B121_B140_contextual_final_review_v1.json')
PLAN=Path('work/analysis/Rafael351_checked_v1_20261105/release_plans.json')
FINAL=Path('translations/rafael_B121_B140_cumulative867_refs_v1.json')
PREP=Path('work/analysis/Rafael516_registered_preparation_v1_20261105/registered_preparation.json')
CHECKED=Path('work/analysis/Rafael351_checked_v1_20261105/research_completion.json')

if __name__=='__main__':
    assert not ROOT.exists() and not FINAL.exists()
    prior,new,doc,plan,prep,checked=map(load,[PRIOR,NEW,REVIEW,PLAN,PREP,CHECKED])
    assert checked['all_individual_five_gates_pass'] and checked['records']==351 and checked['manuscript_sha256']==sha(REVIEW.read_bytes())
    validate_natural_dialogue_batch(doc)
    assert prior['research_ROM_sha256']==prep['target_ROM_sha256']==sha(Path(prior['research_ROM']).read_bytes())
    assert new['parent_sha256']=='cc71ec06ce5345dcc71f8b631232f4d8d501152f6989374741616260fa0ca448'
    assert sha(Path(new['parent']).read_bytes())==new['parent_sha256'] and sha(Path(new['research_ROM']).read_bytes())==new['research_ROM_sha256']
    parent,verified,own=map(NdsImage.open,[prior['research_ROM'],new['parent'],new['research_ROM']])
    file=doc['file_path'];before=parent.read_file(file);original=verified.read_file(file);own_archive=own.read_file(file)
    assert sha(before)==prior['target_archive_sha256'] and sha(original)==new['source_archive_sha256'] and sha(own_archive)==new['target_archive_sha256']
    previous,original_blocks,new_blocks=[IlnkContainer.parse(x).blocks for x in [before,original,own_archive]]
    assert len(previous)==len(original_blocks)==len(new_blocks)==343
    prior_changed=[i for i,(a,b) in enumerate(zip(previous,original_blocks,strict=True)) if a!=b]
    assert len(prior_changed)==29 and len(new['changed_blocks'])==18 and not set(prior_changed)&set(new['reviewed_blocks'])
    receipts=[]
    for group in new['groups']:
        n=group['block'];assert previous[n]==original_blocks[n] and sha(previous[n])==group['current_sha256']
        assert sha(new_blocks[n])==group['target_sha256'] and new_blocks[n]==Path(group['target_block']).read_bytes()
        receipts.append(dict(block=n,current_block_sha256=sha(previous[n]),target_block_sha256=sha(new_blocks[n]),
            complete_local_commands_offsets_relatives_macro_inputs_andnative_proof_bytes_exact=True))
    blocks=list(previous)
    for n in new['changed_blocks']:blocks[n]=new_blocks[n]
    all_changed=sorted(prior_changed+new['changed_blocks'])
    assert len(all_changed)==47 and [i for i,(a,b) in enumerate(zip(blocks,original_blocks,strict=True)) if a!=b]==all_changed
    combined=IlnkContainer(blocks).to_bytes()
    inverse=list(blocks)
    for n in new['changed_blocks']:inverse[n]=previous[n]
    assert IlnkContainer(inverse).to_bytes()==before
    inverse=list(blocks)
    for n in prior_changed:inverse[n]=original_blocks[n]
    assert IlnkContainer(inverse).to_bytes()==own_archive
    for resource in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
        assert parent.read_file(resource)==verified.read_file(resource)==own.read_file(resource)
    ROOT.mkdir(parents=True);archive=ROOT/'combined_SC0.DK4';archive.write_bytes(combined)
    parent.replace_file(file,combined)
    assert [p for _,p,v in verified.iter_files() if parent.read_file(p)!=v]==[file]
    assert all(parent.read_file(p)==v for p,v in verified.iter_components())
    rom=ROOT/'combined_RESEARCH_ONLY.nds';parent.save(rom)
    restored=NdsImage.open(rom);restored.replace_file(file,before);assert bytes(restored.rom.save())==Path(prior['research_ROM']).read_bytes()
    restored.replace_file(file,own_archive);assert bytes(restored.rom.save())==Path(new['research_ROM']).read_bytes()
    restored.replace_file(file,original);assert bytes(restored.rom.save())==Path(new['parent']).read_bytes()
    del restored,parent,own,verified;gc.collect()
    for row in doc['records']:
        ref=row['planned_integrated_reference'];assert ref['target_archive_sha256']==new['target_archive_sha256']
        at=ref['offset'];raw=bytes.fromhex(ref['exact_stored_hex']);assert blocks[row['block']][at:at+len(raw)+1]==raw+b'\0'
        ref['target_archive_sha256']=sha(combined)
    doc.update(research_review_before_rebase=str(REVIEW),research_review_before_rebase_sha256=sha(REVIEW.read_bytes()),
        current_comparison_stays_bound_to_verified678_owned_blocks=True,
        only_whole_archive_reference_digest_changed_no_new_prose_layout_orcoverage=True)
    validate_natural_dialogue_batch(doc);save(FINAL,doc)
    plan.update(manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()));save(ROOT/'release_plans.json',plan)
    rebased=deepcopy(new);rebased.update(parent=prior['research_ROM'],parent_sha256=prior['research_ROM_sha256'],
        source_archive_sha256=sha(before),target_archive=str(archive),target_archive_sha256=sha(combined),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),plan=str(ROOT/'release_plans.json'),plan_sha256=sha((ROOT/'release_plans.json').read_bytes()),
        original_storage_reconstruction=str(NEW),original_storage_reconstruction_sha256=sha(NEW.read_bytes()),
        parent_is_qualified_unregistered516_research_not_a_registered_release=True,registered_predecessor_is_verified678=True,
        prior_cumulative_changed_blocks=prior_changed,all_cumulative_changed_blocks=all_changed)
    save(ROOT/'reconstruction.json',rebased)
    save(ROOT/'dependency_reuse.json',dict(previous516_reconstruction=str(PRIOR),previous516_reconstruction_sha256=sha(PRIOR.read_bytes()),
        original351_reconstruction=str(NEW),original351_reconstruction_sha256=sha(NEW.read_bytes()),
        rebased_reconstruction=str(ROOT/'reconstruction.json'),rebased_reconstruction_sha256=sha((ROOT/'reconstruction.json').read_bytes()),
        original_review=str(REVIEW),original_review_sha256=sha(REVIEW.read_bytes()),rebased_review=str(FINAL),rebased_review_sha256=sha(FINAL.read_bytes()),
        all20_local_source_andtarget_blocks=receipts,prior_owned_blocks=prior_changed,new_owned_blocks=new['changed_blocks'],cumulative_owned_blocks=all_changed,
        full_ARM9_COMMON_font_names_andall_unowned_files_components_exact=True,
        three_complete_serialized_inverses_exact=True,original_display_storage_catalogue_andlocal_loader_inputs_exact=True,
        no_new_native_execution_startup_gameplay_orcoverage_claim=True,
        original_516_failure_andfrozencontracts_preserved=True,two_catalogue_particles_still_pending=True,
        not_registered_or_approved_release=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in [PRIOR,NEW,REVIEW,PLAN,PREP,CHECKED,Path(__file__)]}))
    pins=Path('translations/rom_retention_pins.json');before_pins=pins.read_bytes();values=load(pins)
    assert not any(Path(v['path']).resolve()==rom.resolve() for v in values)
    values.append(dict(path=str(rom.resolve()),reason='Preserve complete qualified867 research target andall three inverse proofs. SHA256 '+sha(rom.read_bytes())))
    (ROOT/'pins.before.json').write_bytes(before_pins);pending=pins.with_name('rom_retention_pins.Rafael867.pending.json');assert not pending.exists()
    save(pending,values);assert pins.read_bytes()==before_pins;os.replace(pending,pins)
    print('Combined516+351 reviews across47 disjoint blocks;all20 new source/target blocks exact andthree full serialized inverses pass. Research only;no repeated native tests,newcredit orpromotion.')
