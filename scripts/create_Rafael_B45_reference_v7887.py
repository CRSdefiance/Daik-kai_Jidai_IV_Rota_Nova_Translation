"""Pin the exact Rafael B45 research image for native loader andfocused source/English scene checks."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_reference_v7887')
PLAN=Path('work/analysis/Rafael_B45_relocation_v7884/one_block12_speeches5_relative_fixups25_cases_exact_full_inverse.json')
STORED=Path('work/analysis/Rafael_B45_stored_v7885/all12_stored_bodies28_fresh20_reused_alignments_exact_viewed_planes.json')
CONTROLS=Path('work/analysis/Rafael_B45_relocated_controls_v7886/12_stored_dispatches25_relocated_relative_cases_predicate25_seeded_ends.json')
VIEW=Path('work/analysis/Rafael_B45_native_review_v7883/native_visual_review_andexact_plan_guard_rebinding.json')
PARENT=Path('out/all_routes_combined_v7857_candidate.nds')
ROM=Path('out/Rafael_B45_reference_v7887_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored,controls,view=map(read,[PLAN,STORED,CONTROLS,VIEW])
    ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert sha(PARENT.read_bytes())==candidate['sha256']==plan['candidate_sha256']==stored['candidate_sha256']==controls['candidate_sha256']
    assert candidate['profile']=='all-routes-unified-v7857' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==632 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['relocation_sha256']==sha(PLAN.read_bytes()) and stored['all12_native_ink_planes_exact_to_already_viewed']
    assert len(view['direct_visual_review'])==2 and all(s['directly_viewed'] for s in view['direct_visual_review']) and len(controls['final_dispatches'])==12
    archive=Path(plan['target_archive']).read_bytes();assert sha(archive)==plan['target_archive_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);assert sha(parent.read_file(plan['file_path']))==plan['source_archive_sha256']
    image.replace_file(plan['file_path'],archive);image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC0.DK4']
    assert all(saved.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file(plan['file_path'])).blocks for im in [parent,saved]]
    assert len(a)==len(b)==343 and [i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]==[45]
    for group in plan['groups']:assert sha(b[group['block']])==group['target_block_sha256']
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);oldvalues=list(values)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='Rafael SC0B45 full12-speech contextual research reference from current V7857;exact clean/predecessor inverse,five relocated relative controls,12 viewed complete native pages andseven zero-ink stored parity tails. Only B45 changes;342other SC0 blocks andallother files/components exact. Unregistered focused-test research,not the canceled separate unified test package,new parent orpromotion. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    assert values[:-1]==oldvalues
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==values
    save(ROOT/'research_image_receipt.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),
        only_changed_files=['/data/SC0.DK4'],only_changed_blocks=[45],all342_otherSC0_blocks_andall_other_files_components_exact=True,
        all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        registered_candidate=False,not_for_handoff_ornew_parent=True,no_registry_ledger_main_promotion_orcredit_change=True,
        source_headers_andall_controls_preserved_except_mapped_lengths_andreviewed_prose=True,
        full_loader_caller_actual_policy_production_registered_release_andstartup_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,STORED,CONTROLS,VIEW,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Pinned B45 research reference;342other SC0 blocks/allother files/components exact.CurrentV7857/mainV4701 unchanged.')
