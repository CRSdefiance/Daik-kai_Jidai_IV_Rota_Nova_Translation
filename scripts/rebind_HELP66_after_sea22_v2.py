"""Rebind unchanged reviewed Fleet66 pages after the independently reviewed22-article layer."""
import os
from copy import deepcopy
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.dialogue.reviewed_help_fleet66_amendment_v1 import plan_articles
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save

ROOT=Path('work/analysis/HELP66_Command_amendment_20261104')
OUT=ROOT/'after_sea22_v2'
OLD=Path('translations/help_fleet66_Command_contextual_amendment_v1.json')
FINAL=Path('translations/help_fleet66_Command_contextual_amendment_v2.json')
SEA=Path('work/analysis/Shared_HELP_T81_T102_formatting_20261104/preview_qualification_v1/qualification.json')
VERIFIED=Path('work/analysis/Shipyard_HELP37_release_verified_20261104/registered_release_verification.json')

if __name__=='__main__':
    assert not OUT.exists() and not FINAL.exists()
    sea,verified=map(load,[SEA,VERIFIED]);old=load(OLD);doc=deepcopy(old)
    assert verified['clean_input_patch_byte_exact'] and not verified['own_registered_startup_pending']
    assert verified['candidate_sha256']==old['current_ROM_sha256']==sea['parent_sha256']
    parent=Path(sea['research_ROM']);assert sha(parent.read_bytes())==sea['research_ROM_sha256']
    image=NdsImage.open(parent);prior=NdsImage.open(old['current_ROM'])
    file=doc['file_path'];raw=image.read_file(file);blocks=IlnkContainer.parse(raw).blocks;old_blocks=IlnkContainer.parse(prior.read_file(file)).blocks
    assert len(blocks)==len(old_blocks)==217 and all(blocks[t]==old_blocks[t]for t in [66,216,67,68,69,70])
    assert all(image.read_file(p)==prior.read_file(p)for p in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT'])
    row=doc['records'][0]
    row['current_reference']=dict(file_path=file,block=66,archive_offset=int.from_bytes(raw[272:276],'little'),bytes=len(blocks[66]),offset_table_slot=272)
    row['current_source_hex']=row['current_hex']=blocks[66].hex()
    row['current_continuations']=[dict(topic_id=216,current_hex=blocks[216].hex())]
    doc.update(current_ROM=str(parent),current_ROM_sha256=sha(parent.read_bytes()),source_current_HELP_sha256=sha(raw),
        review_gates=['source','context','localization','naturalness','formatting'],
        previous_manuscript=str(OLD),previous_manuscript_sha256=sha(OLD.read_bytes()),
        registered_parent_build_pending=True,source37_parent_now_registered_verified=True,
        approved_page_bytes_andnative_actual_proofs_unchanged=True)
    clean=NdsImage.open('work/clean.nds');base=NdsImage.open('out/raphael_natural_v2_accepted_base.nds')
    resource,plan=plan_articles(doc,clean.read_file(file),base.read_file(file),raw)
    previous=load(ROOT/'production_plan_v1.json')
    assert plan['pages']==previous['pages'] and len(plan['pages'])==2
    encoded=IlnkContainer.parse(resource).blocks
    assert [t for t in range(217)if encoded[t]!=blocks[t]]==[66]
    for p in row['planned_stored_pages']:
        t=p['block'];data=encoded[t]
        assert data.hex()==p['exact_stored_hex']
        p.update(archive_offset=int.from_bytes(resource[8+4*t:12+4*t],'little'),bytes=len(data),offset_table_slot=8+4*t,target_archive_sha256=sha(resource))
    OUT.mkdir();target=OUT/'HELP66_after_sea22_RESEARCH_ONLY.DK4';target.write_bytes(resource)
    image.replace_file(file,resource);rom=OUT/'HELP66_after_sea22_RESEARCH_ONLY.nds';rom.write_bytes(bytes(image.rom.save()))
    restored=NdsImage.open(rom);restored.replace_file(file,raw);assert bytes(restored.rom.save())==parent.read_bytes()
    evidence=[OLD,SEA,VERIFIED,ROOT/'native_term_binding_v1.json',ROOT/'production_plan_v1.json',
        Path(doc['native_proof']),Path(doc['actual_proof']),Path(doc['native_visual_approval']),Path(doc['actual_visual_approval']),Path(__file__)]
    doc['evidence']={str(p):sha(p.read_bytes())for p in evidence}
    save(FINAL,doc)
    save(OUT/'production_plan_v2.json',dict(**plan,manuscript=str(FINAL),manuscript_sha256=sha(FINAL.read_bytes()),
        research_resource=str(target),current_ROM=str(parent),current_ROM_sha256=sha(parent.read_bytes()),
        exact_reused_native_andactual_pages=2,all_unowned_including_sea22_pages_exact=True,new_credit=0))
    save(OUT/'metadata_rebinding_receipt_v2.json',dict(previous_manuscript=str(OLD),previous_sha256=sha(OLD.read_bytes()),
        final_manuscript=str(FINAL),final_sha256=sha(FINAL.read_bytes()),research_ROM=str(rom),research_ROM_sha256=sha(rom.read_bytes()),
        source_after_sea22=str(parent),source_after_sea22_sha256=sha(parent.read_bytes()),
        both_page_bytes_all_widget_link_destinations_runtime_COMMON_font_andall_five_gates_exact=True,
        only_full_archive_offsets_hashes_andparent_refs_rebound=True,review_gate_schema_added_without_new_approval=True,
        no_prose_orlayout_change_no_repeated_gameplay_orcredit=True,evidence=doc['evidence']))
    pins_path=Path('translations/rom_retention_pins.json');before=pins_path.read_bytes();pins=load(pins_path);(OUT/'pins.before.json').write_bytes(before)
    assert not any(Path(p['path']).resolve()==rom.resolve()for p in pins)
    pins.append(dict(path=str(rom.resolve()),reason='Preserve qualified Fleet66 Command amendment after reviewed sea22. SHA256 '+sha(rom.read_bytes())))
    temporary=pins_path.with_name('rom_retention_pins.HELP66_after_sea22.pending.json');assert not temporary.exists();save(temporary,pins)
    assert pins_path.read_bytes()==before;os.replace(temporary,pins_path)
    print('Fleet66 rebound after reviewed sea22:exact two page bytes/runtime/native/actual proofs reused, no new credit.')
