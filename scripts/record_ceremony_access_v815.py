"""Record partial real ceremony verification without whole-family completion credit."""

import shutil
import struct
from pathlib import Path

from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/ceremony_access_v810')
DOC = Path('docs/ceremony_access_v815_checkpoint.md')
LEDGER = Path('translations/editorial_review_current_v1.json')
ROM = Path('out/all_routes_combined_v809_candidate.nds')
SUMMARY = ('V810-V815 completes original Cappadocia prerequisites in isolated saves and verifies four ceremony families in V809: '
    '26 actual complete glyph holds across21 IDs,83 strict whole-screen controls and97 original state pairs. '
    'Site prayer/chant advance192 ticks;Temple preparation/Church prayer48;tested cancellations0. '
    'Source-bound calendar,facility,discovery,cargo and map fixtures preserve original handlers and donors. '
    'The first misleading Temple-named folder is correctly classified as site chant after a cached Gate selection. '
    'A new source-confirmed open SC1 finding records the omitted large-quantity sulfur qualifier. '
    'Alternate Temple chant,site dance/fast/climb and other protagonist reactions remain;Athens Town19/site7/start21 is the next original location. '
    'V809 ROM/exact patch and all registered dependencies remain unchanged;V803 stays the last whole-batch verified reference. '
    '550 completed/605 COMMON source-prose/55 pending unchanged;full editorial and separate graphics audits remain open.')


def main():
    assert sha(ROM.read_bytes()) == '4b85eae04e1f1654022433c2a9a2aafd8b719daf10cc5f2120a32f9781728ae2'
    cfg = read('translations/ceremony_editorial_release_v1.json')
    for path, expected in cfg['dependencies'].items():
        assert sha(Path(path).read_bytes()) == expected, path
    paths = [ROOT/'prayer_gameplay_verification_v814.json',
             *(ROOT/(name+'_gameplay_verification_v815.json') for name in
               ('site_chant', 'temple_preparations', 'church_prayer'))]
    proofs = [read(p) for p in paths]
    for index, proof in enumerate(proofs):
        script = 'scripts/verify_ceremony_prayer_gameplay_v814.py' if index == 0 else 'scripts/verify_ceremony_families_gameplay_v815.py'
        assert proof['producer_sha256'] == sha(Path(script).read_bytes())
        assert proof['candidate_sha256'] == sha(ROM.read_bytes()) and not proof['full_goal_complete']
    holds = [h for proof in proofs for h in proof['complete_scene_holds']]
    ids = sorted({h['message_id'] for h in holds})
    assert len(holds) == 26 and len(ids) == 21
    assert sum(len(p['full_screen_controls']) for p in proofs) == 83
    assert sum(len(p['original_state_pairs']) for p in proofs) == 97
    for name, expected in (
        ('V751 disposable Istanbul donor.dsv', 'd991cb3bcdf74eed7aeb58c9a75957766b7c820d002423fd2b55cc8493cf8132'),
        ('V811 Cappadocia gate unlocked after story.dsv', 'b26b71dda7db349d4df996b6ddcbfaf4dded4e46a47bc483148cb14eaf92006e'),
        ('V813 Cappadocia rockfall cleared.dsv', '1de062be7b19a84c07e59a2ff5dad877afda81a3e9daa86e179c927be04aa2dc'),
        ('V814 Cappadocia story cleared after prayer.dsv', 'e5beeb4e4be5ecab1ee5312daab1bc81bc9904c5f4b6de45004d401356d8113b')):
        assert sha((Path('E:/Rota Nova translations/Saves/Test fixtures')/name).read_bytes()) == expected
    arm = NdsImage.open(ROM).read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert arm[0xB5170:0xB5188] == clean[0xB5170:0xB5188]
    raw = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ceremony_v809_map_probe/frame_016200_arm9_ram.bin').read_bytes()
    u = machine(arm); u.mem_write(0x02000000, raw)

    def get(fn, args=()):
        call(u, fn, args, instruction_limit=500000)
        return u.reg_read(UC_ARM_REG_R0)

    def word(at):
        return struct.unpack('<I', u.mem_read(at, 4))[0]

    town = get(0xCB178)+4+19*108
    name_ptr = get(word(word(town)+8)-0x02000000, (town,))
    assert bytes(u.mem_read(name_ptr, 64)).split(b'\0')[0] == b'Athens'
    site = get(0xB5170, (town,)); assert site == 7
    next_context = dict(town_ID=19, original_name='Athens', site_ID=site, ceremony_start_day=((19+1)%28)+1,
        original_town_site_getter=0x020B5170, original_getter_code_exact=True,
        current_ARM9_sha256=sha(arm), source_RAM_sha256=sha(raw),
        source_branch_proof='work/analysis/ceremony_context_v806/native_context.json',
        next='Normal docking via isolated ship-coordinate approach, then verified access/date inputs; Temple chant and site dance/fast/climb.')
    assert next_context['ceremony_start_day'] == 21
    save(ROOT/'next_Athens_original_context_v815.json', next_context)
    guide = Path('E:/Rota Nova translations/Guide screenshots/Editorial V809')
    guides = []
    for proof_path, proof in zip(paths, proofs, strict=True):
        destination = guide/proof_path.stem
        destination.mkdir(parents=True, exist_ok=True)
        for hold in proof['complete_scene_holds']:
            source = Path(hold['capture']['path'])
            target = destination/f"COMMON{hold['message_id']}_frame_{hold['frame']:06d}.png"
            if target.exists():
                assert sha(target.read_bytes()) == sha(source.read_bytes())
            else:
                shutil.copyfile(source, target)
            guides.append(dict(path=str(target), sha256=sha(target.read_bytes()), message_ID=hold['message_id'],
                frame=hold['frame'], verification=str(proof_path), verification_sha256=sha(proof_path.read_bytes()),
                original_capture=hold['capture']['path']))
    save(guide/'ceremony_v815_provenance.json', dict(ROM=str(ROM.resolve()), ROM_sha256=sha(ROM.read_bytes()),
        actual_targeted_emulator_captures_not_full_playthrough_or_hardware=True,
        isolated_prerequisite_fixtures_not_earned_campaign_progress=True, captures=guides))
    ledger = read(LEDGER)
    assert ledger['goal_status'] == 'active' and not ledger['full_goal_complete']
    assert ledger['records_editorially_completed'] == 550 and ledger['records_with_source_and_prose_pass'] == 605
    backup = ROOT/'editorial_ledger_before_v815_checkpoint.json'
    if not backup.exists():
        shutil.copyfile(LEDGER, backup)
    detail = dict(documentation=str(DOC), proofs=[str(p) for p in paths], actual_holds=26,
        actual_native_message_IDs=ids, whole_screen_controls=83, original_state_pairs=97,
        guide_provenance=str(guide/'ceremony_v815_provenance.json'),
        completion_credit=0, next_original_location_context=str(ROOT/'next_Athens_original_context_v815.json'),
        remaining='Alternate Temple chant,site dance/fast/climb,other protagonist reactions and remaining choice/return coverage.',
        full_goal_complete=False)
    ledger['actual_ceremony_gameplay_v815'] = detail
    ledger['pending_registered_ceremony_candidate'].update(
        status='registered-native-patch-startup-and-partial-actual-ceremony-verified;whole-family-pending',
        actual_partial_gameplay=detail)
    ledger['next_ceremony_source_packet'].update(
        status='21-distinct-IDs-actual-partial-family-verified;remaining-branches-pending',
        actual_partial_gameplay=detail, next=next_context['next'])
    ledger['active_source_prose_drafts'].update(
        status='750-752-context-unmapped;ceremony52-integrated-native-and-partial-actual-verified',
        note='51 production paragraphs have201 native layouts/fonts;26 actual holds cover21 distinct IDs. Whole52 family remains open;3 older750-752 contexts remain. No additional completion credit.')
    finding = read(ROOT/'route_editorial_finding_sulfur_v815.json')
    if not any(r['id'] == finding['id'] for r in ledger['findings']):
        ledger['findings'].append(dict(id=finding['id'], status=finding['status'], file='/data/SC1.DK4',
            row_id='DK4_MES_B296_R0063', proof=str(ROOT/'route_editorial_finding_sulfur_v815.json'),
            detail=finding['issue'], no_COMMON_completion_or_source_count_credit=True))
    key = 'V815-actual-ceremony-access-and-four-partial-families'
    if not any(r['id'] == key for r in ledger['research_checkpoints']):
        ledger['research_checkpoints'].append(dict(id=key, documentation=str(DOC),
            new_source_prose_reviewed=0, new_editorially_completed=0, new_ROM=False,
            actual_holds=26, distinct_actual_IDs=21, full_goal_complete=False))
    ledger['latest_checkpoint'] = SUMMARY
    assert ledger['next_integrated_profile_for_goal_continuation'] == 'all-routes-unified-v809'
    save(LEDGER, ledger)
    for name in ('translation_progress.md', 'known_issues.md', 'todo.md', 'editorial_review_goal.md'):
        path = Path('docs')/name; text = path.read_text(encoding='utf-8')
        heading = '## V815: actual ceremony scenes and access fixtures'
        if heading not in text:
            path.write_text(text+'\n\n'+heading+'\n\n'+SUMMARY+' See [V815 checkpoint](ceremony_access_v815_checkpoint.md).\n', encoding='utf-8')
    archive = Path('E:/Rota Nova translations/Editorial review/V815 Ceremony actual scenes')
    sources = [DOC, LEDGER, Path(__file__), *ROOT.glob('*.json'), *ROOT.glob('*.jsonl'),
        *(p for p in Path('scripts').glob('*ceremony*v81*.py'))]
    artifacts = []
    for source in sources:
        folder = archive/('scripts' if source.parent.name == 'scripts' else 'evidence' if source.parent == ROOT else 'checkpoint')
        folder.mkdir(parents=True, exist_ok=True)
        target = folder/source.name
        shutil.copyfile(source, target)
        assert sha(source.read_bytes()) == sha(target.read_bytes())
        artifacts.append(dict(source=str(source), archived=str(target), sha256=sha(target.read_bytes())))
    save(archive/'archive_manifest.json', dict(artifacts=artifacts, actual_holds=26,
        distinct_actual_IDs=ids, guide_provenance=str(guide/'ceremony_v815_provenance.json'),
        ROM_unchanged=True, canonical_not_promoted=True, completion_credit=0, full_goal_complete=False))
    print(f'Recorded26 verified holds across21 IDs,83 screen controls,97 state pairs; archived{len(artifacts)} artifacts and26 guide images.550 complete;goal active.', flush=True)


if __name__ == '__main__':
    main()
