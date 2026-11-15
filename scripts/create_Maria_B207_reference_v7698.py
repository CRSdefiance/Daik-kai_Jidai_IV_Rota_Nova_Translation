"""Pin an exact reversible Maria single-block research reference; no playable handoff or promotion."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_reference_v7698')
PLAN=Path('work/analysis/maria_B207_relocation_v7696/Maria18_speeches20_commands_exact_clean_andpredecessor_inverse_RESEARCH.json')
STORED=Path('work/analysis/maria_B207_stored_v7697/Maria18_stored_targets72_alignments7_zero_ink_tails18_complete_pages.json')
PARENT=Path('out/all_routes_combined_v7660_candidate.nds')
ROM=Path('out/maria_B207_reference_v7698_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored=map(read,[PLAN,STORED]);ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate'];manifest=read(candidate['manifest']);registry=read('translations/release_stack.json')
    digest=sha(PARENT.read_bytes());assert digest==plan['candidate_sha256']==stored['candidate_sha256']==candidate['sha256']
    assert candidate['profile']=='all-routes-unified-v7660' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes()) and len(manifest['batches'])==628 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['relocation_map_sha256']==sha(PLAN.read_bytes()) and stored['all18_final_stored_targets_equal_reviewed_complete_ink']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT)
    for g in plan['groups']:
        data=Path(g['target_archive']).read_bytes();assert sha(data)==g['target_archive_sha256'] and sha(parent.read_file(g['file_path']))==g['source_archive_sha256']
        image.replace_file(g['file_path'],data)
    image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(saved.read_file(p)==v for p,v in parent.iter_components())
    for g in plan['groups']:
        a,b=[IlnkContainer.parse(im.read_file(g['file_path'])).blocks for im in [parent,saved]]
        assert len(a)==len(b) and [i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]==[g['block']]
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');old=pins.read_bytes();values=json.loads(old)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='Maria SC3B207 full18-speech contextual review,distinct CS0101 header,exact clean/predecessor inverse andstored native proofs. Only this block changes from complete V7660. Not a registered release, handoff, test package ornew parent. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8');(ROOT/'pins.before.json').write_bytes(old);assert pins.read_bytes()==old
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    save(ROOT/'research_image_receipt.json',dict(parent=str(PARENT),parent_sha256=digest,research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_target_proof=str(STORED),stored_target_proof_sha256=sha(STORED.read_bytes()),only_changed_files=['/data/SC3.DK4'],only_changed_blocks=[dict(file_path=g['file_path'],block=g['block'],unchanged_other_blocks=g['unchanged_other_block_count']) for g in plan['groups']],all_other_files_components_andprior_ROMs_exact=True,all_prior_pins_preserved=True,pins_before_sha256=sha(old),pins_after_sha256=sha(encoded),registered_candidate=False,not_for_handoff_ornew_parent=True,no_registry_ledger_orpromotion_change=True,external_references_representative_actual_atomic_release_andstartup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Pinned reversible Maria B207 research reference from complete V7660;302 other SC3 blocks/allother files andcomponents exact. Current/main unchanged;no handoff package.')
