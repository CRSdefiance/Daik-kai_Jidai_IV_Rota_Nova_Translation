"""Keep complete body/header/order guards for the disclosed Maria unlock fixture."""
from pathlib import Path
from scripts.analyze_reviewed_dynamic_fixture_v1 import dynamic_headers
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest


def verified_existing_unlock(report):
    prior = load('work/Maria_current_context_20261109_v1/run_plan.json')
    battery = report['battery_save_preloaded']
    assert Path(battery['source']) == Path(prior['donor'])
    assert battery['source_sha256'] == digest(prior['donor']) == prior['donor_sha256']
    assert battery['copied_byte_exact_before_cold_boot'] and not battery['savestate_loaded']
    assert len(report['synthetic_gallery_fixtures']) == 1
    fixture = report['synthetic_gallery_fixtures'][0]
    assert digest(fixture['preloaded_save_manifest']) == fixture['manifest_sha256']
    unlock = load(fixture['preloaded_save_manifest'])
    assert unlock['production_ROM_sha256'] == report['ROM_sha256']
    assert unlock['fixture_save_sha256'] == battery['source_sha256']
    assert unlock['only_system_low_four_bits_and_original_checksum_changed']
    assert unlock['all_six_route_save_slots_and_footer_unchanged'] and not unlock['earned_unlock_verified']
    return True


def maria_source(source):
    source = dynamic_headers(source)
    return checked_text(source, {
        " and not report.get('battery_save_preloaded')": ' and verified_existing_unlock(report)',
        "byactor = {r['actor_ID']: r['english'] for r in load(decisions_path)['records']}":
            "byactor = {r['actor_ID']: next(c['text'] for c in r['current_consumers'] if c['consumer']=='progressive-nameplate') for r in load(decisions_path)['records']}",
        'actual_gameplay=True, disclosed_initialized_fixture=True,':
            'actual_gameplay=True, disclosed_initialized_fixture=True, existing_system_only_unlock_not_earned=True,',
    })


source = checked_text(Path('scripts/analyze_reviewed_scene_fixture.py').read_text(encoding='utf-8'), {
    "exec(compile(source,__file__+'::same-ordered-calls-complete-pixels-andblank-guards','exec'),globals())":
        "exec(compile(maria_source(source),__file__+'::same-pixels-header-order-guards-explicit-Maria-unlock','exec'),globals())",
})

if __name__ == '__main__':
    exec(compile(source, __file__+'::same-body-header-native-plane-guards-Maria', 'exec'), globals())
