"""Rebind the proven40-byte prebattle location fixture to the exact V1520 ROM."""
import inspect
from pathlib import Path
from scripts import native_stronger_fleet_location_v1471 as previous
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v1520_candidate.nds')
ROOT = Path('work/analysis/retreat_transfer_fixture_v1523')


def apply_fixture(arm, raw, request):
    source = inspect.getsource(previous.apply_fixture)
    old = 'work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json'
    assert source.count(old) == 1
    source = source.replace(old, 'work/analysis/retreat_transfer_release_v1519/registered_release_verification.json')
    old = "    assert census['candidate_sha256']==release['candidate_sha256']"
    new = """    ancestor=read('work/analysis/ship_loss_surrender_release_v1455/registered_release_verification.json')
    config=read('translations/retreat_transfer_editorial_release_v1.json')
    parent=read('work/analysis/battle_reaction_release_v1491/registered_release_verification.json')
    assert census['candidate_sha256']==ancestor['candidate_sha256']
    assert config['source_arm9_sha256']==parent['ARM9_sha256']
    assert config['target_arm9_sha256']==release['ARM9_sha256']==sha(arm)
    old_arm=NdsImage.open(ancestor['candidate']).read_file('/__arm9__.bin')
    assert all(arm[lo:hi]==old_arm[lo:hi] for lo,hi in census['original_getter_spans'])
    assert release['all_routes_graphics_fonts_other_components_and_opaque_duel_prefix_exact']"""
    assert source.count(old) == 1
    source = source.replace(old, new)
    old = "    assert not get(0x36C70,enemy+12)"
    new = old + """
    for expected in target['ships']:
        model=get(0x36C94,enemy+12+8*expected['slot'])
        assert model==expected['model']
        assert get(0x1856C,model)==expected['original_cannon_type']
        assert [get(0x183A0,model),get(0x181BC,model)]==expected['stored_Hull_Crew']"""
    assert source.count(old) == 1
    source = source.replace(old, new)
    env = {**previous.__dict__, '__file__': __file__, 'ROM': ROM}
    exec(compile(source, __file__, 'exec'), env)
    after, receipt = env['apply_fixture'](arm, raw, request)
    receipt['census_to_current_release_binding'] = 'Original V1456 fleet census, V1492->V1520 exact config bridge, unchanged original getters and NPC models/cannons/stored Hull/Crew.'
    return after, receipt


if __name__ == '__main__':
    assert not ROOT.exists()
    report = read('E:/Rota Nova translations/Generated/work/emulation_v193/stronger_fleet_anchor_v1502_1492/capture_report.json')
    snapshot = next(r for r in report['read_only_pause_RAM_snapshots'] if r['frame'] == 4800)
    raw = Path(snapshot['path']).read_bytes()
    assert sha(raw) == snapshot['sha256']
    after, receipt = apply_fixture(NdsImage.open(ROM).read_file('/__arm9__.bin'), raw, {'ship_sinking_context': 'five_ship_approach'})
    ROOT.mkdir(parents=True)
    save(ROOT / 'prebattle_fixture_preflight.json', receipt)
    print('V1520 prebattle fixture: only40 original own-position bytes; all NPC data and other4MiB bytes exact.')
