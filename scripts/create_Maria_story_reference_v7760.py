"""Pin the exact three-block research image for native loader andfocused scene checks."""
import json,os
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_reference_v7760')
PLAN=Path('work/analysis/maria_story_final_relocation_v7758/three_blocks67_speeches20_fixups100_native_target_cases_exact_inverse.json')
STORED=Path('work/analysis/maria_story_final_stored_v7759/67_final_v3_stored_pages33_tails_two_new_dispatches65_exact_reuse.json')
CONTROLS=Path('work/analysis/maria_story_final_controls_v7745/67_final_dispatches_numeric_leaves_opaque_controls_resources_pause_C200_ends.json')
VIEW=Path('work/analysis/maria_story_final_native_v7757b/67_final_v3_native_pages_andfully_bound_logical_lineage.json')
PARENT=Path('out/all_routes_combined_v7717_candidate.nds')
ROM=Path('out/maria_story_reference_v7760_RESEARCH_ONLY.nds')
if __name__=='__main__':
    assert not ROOT.exists() and not ROM.exists();plan,stored,controls,view=map(read,[PLAN,STORED,CONTROLS,VIEW])
    ledger=read('translations/editorial_review_current_v1.json');candidate=ledger['current_integrated_candidate'];registry=read('translations/release_stack.json');manifest=read(candidate['manifest'])
    assert sha(PARENT.read_bytes())==candidate['sha256']==plan['candidate_sha256']==stored['candidate_sha256']==controls['candidate_sha256']
    assert candidate['profile']=='all-routes-unified-v7717' and manifest['release_stack_sha256']==sha(Path('translations/release_stack.json').read_bytes())
    assert len(manifest['batches'])==629 and len(manifest['checks'])==18 and all(manifest['checks'].values())
    assert len(registry['accepted_layers'])==114 and registry['latest_promoted_build']['profile']=='all-routes-unified-v4701'
    assert stored['relocation_map_sha256']==sha(PLAN.read_bytes()) and stored['all67_final_stored_targets_equal_reviewed_complete_native_ink']
    assert view['all67_single_native_four_row_pages_complete_glyph_bounds_andconsumption'] and len(controls['final_dispatches'])==67
    archive=Path(plan['target_archive']).read_bytes();assert sha(archive)==plan['target_archive_sha256']
    parent,image=NdsImage.open(PARENT),NdsImage.open(PARENT);assert sha(parent.read_file(plan['file_path']))==plan['source_archive_sha256']
    image.replace_file(plan['file_path'],archive);image.save(ROM);saved=NdsImage.open(ROM)
    assert [p for _,p,v in parent.iter_files() if saved.read_file(p)!=v]==['/data/SC3.DK4']
    assert all(saved.read_file(p)==v for p,v in parent.iter_components())
    a,b=[IlnkContainer.parse(im.read_file(plan['file_path'])).blocks for im in [parent,saved]]
    assert len(a)==len(b)==303 and [i for i,(old,new) in enumerate(zip(a,b,strict=True)) if old!=new]==[34,35,108]
    for group in plan['groups']:assert sha(b[group['block']])==group['target_block_sha256']
    ROOT.mkdir(parents=True);pins=Path('translations/rom_retention_pins.json');before=pins.read_bytes();values=json.loads(before);oldvalues=list(values)
    assert all(Path(v['path']).resolve()!=ROM.resolve() for v in values)
    values.append(dict(path=str(ROM.resolve()),reason='Maria SC3B34/B108/B35 full67-speech contextual research reference from complete V7717;exact inverse,20 relative fixes,67 complete final-v3 native pages and33 zero-ink stored parity tails. Only these3 blocks change;300other SC3 blocks andallother files/components exact. Unregistered research,not a separate handoff package,new parent orpromotion. Preserve every ROM. SHA256 '+sha(ROM.read_bytes())))
    assert values[:-1]==oldvalues
    encoded=(json.dumps(values,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf8')
    (ROOT/'pins.before.json').write_bytes(before);assert pins.read_bytes()==before
    with pins.open('r+b') as stream:stream.write(encoded);stream.truncate();stream.flush();os.fsync(stream.fileno())
    assert json.loads(pins.read_bytes())==values
    save(ROOT/'research_image_receipt.json',dict(
        parent=str(PARENT),parent_sha256=sha(PARENT.read_bytes()),research_ROM=str(ROM),research_ROM_sha256=sha(ROM.read_bytes()),
        source_relocation_plan=str(PLAN),source_relocation_plan_sha256=sha(PLAN.read_bytes()),stored_proof=str(STORED),stored_proof_sha256=sha(STORED.read_bytes()),
        only_changed_files=['/data/SC3.DK4'],only_changed_blocks=[34,35,108],all300_otherSC3_blocks_andall_other_files_components_exact=True,
        all_prior_ROM_pins_preserved=True,pins_before_sha256=sha(before),pins_after_sha256=sha(encoded),
        registered_candidate=False,not_for_handoff_ornew_parent=True,no_registry_ledger_main_promotion_orcredit_change=True,
        source_headers_andall_controls_preserved_except_mapped_lengths_andreviewed_prose=True,
        full_loader_caller_actual_policy_production_registered_release_andstartup_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in [PLAN,STORED,CONTROLS,VIEW,Path(__file__)]},new_credit=0,new_emulator_runs=0,full_goal_complete=False))
    print('Pinned three-block Maria research reference;300other SC3 blocks/allother files/components exact.CurrentV7717/mainV4701 unchanged.')
