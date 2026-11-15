"""Keep strict current instructions while binding captain3 and the declared unlock-only save."""
from pathlib import Path
from scripts.prepare_lil_B156_layout_v3705 import derive
from scripts.verify_village_wrap_v608 import save

UNLOCK="""        battery=report['battery_save_preloaded']
        assert battery['copied_byte_exact_before_cold_boot'] and not battery['savestate_loaded']
        assert battery['source_sha256']==sha(Path(battery['source']).read_bytes())=='295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949'
        fp=Path(context['existing_system_unlock_manifest']);fixture=read(fp)
        assert sha(fp.read_bytes())==context['existing_system_unlock_manifest_sha256']
        assert fixture['only_system_low_four_bits_and_original_checksum_changed'] and fixture['all_six_route_save_slots_and_footer_unchanged'] and not fixture['earned_unlock_verified']
        assert report['synthetic_gallery_fixtures']==[dict(preloaded_save_manifest=str(fp),manifest_sha256=sha(fp.read_bytes()),synthetic_gallery_fixture=True,earned_unlock_verified=False,validated_selected_supported_site_ids=None)]
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_gallery_fixtures')"""
if __name__=='__main__':
    root=Path('work/analysis/current_Maria_context_tools_v4999');assert not root.exists()
    tool=derive('scripts/current_build_native_context_v4774.py','scripts/current_maria_native_context_v4999.py',{
        "        assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))":UNLOCK,
        'assert get(0x7F244)==2':'assert get(0x7F244)==3',
        'snapshot_is_current_opening_not_B180_activation':'snapshot_is_current_Maria_opening_not_B97_activation',
    })
    root.mkdir(parents=True);save(root/'prepared_tools.json',dict(tool=tool,current_ROM_report_snapshot_sections_and123040_pool_locks_retained=True,
        only_declared_existing_unlock_save_allowed_no_RAM_actor_or_code_fixtures=True,new_editorial_credit=0,full_goal_complete=False))
