"""Bind remaining active labels and focused ordinary item/crew observations without extra visits."""
import struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load, save

ROOT = Path('work/analysis/Shared_HELP_T133_T201_clean_20261105')
ACTIVE = Path('work/analysis/HELP_active_skill_labels_20261105/active_terms_binding_v2.json')
TERMS = [('六分儀','Sextant',0x15BC28,0x11EDC8),('原産物','Product',0x13C288,0x13C350),
    ('通常','Normal',0x15633C,0x156460),('戦争','War',0x156354,0x156430),
    ('疫病','Plague',0x156344,0x156434),('飢饉','Famine',0x15634C,0x156438),
    ('好景気','Boom',0x156364,0x15643C),('不景気','Slump',0x15635C,0x156440),
    ('品不足','Shortage',0x14C2A4,0x8D848)]

if __name__ == '__main__':
    target=ROOT/'remaining_active_terms_andcontrols_v1.json'; assert not target.exists()
    active=load(ACTIVE); ram=Path(active['own_RAM']['path']).read_bytes()
    assert sha(ram)==active['own_RAM']['sha256']
    arm=NdsImage.open(active['current_ROM']).read_file('/__arm9__.bin')
    clean=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'); terms=[]
    for jp,en,at,field in TERMS:
        source=clean[at:].split(b'\0',1)[0]
        assert source==jp.encode('cp932') and struct.unpack_from('<I',clean,field)[0]==0x2000000+at
        assert arm[field:field+4]==ram[field:field+4]
        pointer=struct.unpack_from('<I',ram,field)[0];assert 0x2000000<=pointer<0x2400000
        text=ram[pointer-0x2000000:].split(b'\0',1)[0];assert text==en.encode('ascii')
        terms.append(dict(Japanese=jp,English=en,source_offset=at,active_pointer_field=field,
            current_pointer=pointer,source_hex=source.hex(),current_hex=text.hex(),active_own_RAM_reference=True))
    observations=[
        ('HELP138_139_current_controls_20261105',10600,{
            8200:'Riga has no items; empty-items notice, no equipment action coverage.',
            8400:'A returns to shared commands.',8600:'Ordinary selection highlights Crew Setup.',
            8800:'Assign Sailors displays Need, Now, Max and Y Auto / X Finish.',
            9000:'Y opens Flagship, Even and Minimum policies.',9200:'DOWN highlights Even.',
            9400:'A applies Even and opens Sailors assigned evenly notice.',9600:'A dismisses notice.',
            9800:'RIGHT with no unassigned sailors does not increase assignment.',
            10000:'LEFT releases a sailor, leaving one Unassigned.',10200:'RIGHT restores the assignment.',
            10400:'X opens confirmation.',10600:'A confirms and returns to shared commands.'}),
        ('HELP138_equipment_controls_20261105',5200,{
            3200:'Existing Istanbul battery loaded; no newly earned equipment claim.',3400:'X opens shared commands.',
            3600:'Ordinary selection highlights Items.',3800:'Items shows Golden Cutlass equipped by Hodram; Y Remove.',
            4000:'Y removes Golden Cutlass; actual confirmation names Hodram Joakim Bergstrom.',
            4200:'A dismisses; Y Equip is available.',4400:'Y opens Who will equip it? selector.',
            4600:'A equips Golden Cutlass to Hodram again.',4800:'A dismisses; equipped state restored.',
            5000:'RIGHT selects Blue Oak Shield.',5200:"RIGHT selects Rocco's Sailing Guide; equipment footer still Y Remove."})]
    runs=[]
    for folder,frames,notes in observations:
        root=Path('work/analysis')/folder; pp=root/'run_plan_v1.json';rp=root/'capture_v1/capture_report.json'
        plan,report=map(load,[pp,rp]);assert report['frames']==frames and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==plan['ROM_sha256']==sha(Path(plan['ROM']).read_bytes())
        assert sha(Path(plan['battery']).read_bytes())==plan['battery_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert NdsImage.open(plan['ROM']).read_file('/__arm9__.bin')==arm
        for row in report['frames_captured']:assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
        for row in report['read_only_pause_RAM_snapshots']:
            assert sha(Path(row['path']).read_bytes())==row['sha256']
        runs.append(dict(run_plan=str(pp),run_plan_sha256=sha(pp.read_bytes()),report=str(rp),report_sha256=sha(rp.read_bytes()),
            frames=frames,distinct_reviewed_navigation_frames=len(notes),observations=[dict(frame=f,finding=note,
                capture=next(r for r in report['frames_captured'] if r['frame']==f and 'navigation' in r['path'])) for f,note in notes.items()],
            final_duplicate_frame_not_extra_coverage=True,original_battery_unchanged=True))
    save(target,dict(active_binding=str(ACTIVE),active_binding_sha256=sha(ACTIVE.read_bytes()),active_reference_terms=terms,
        focused_actual_runs=runs,observed_controls=dict(item_equipment='Y',crew_auto='Y',crew_adjustment='Left/Right',crew_finish='X'),
        observed_crew_policy_labels=['Flagship','Even','Minimum'],sixteen_role_thresholds_andall_current_skills_bound_by=active['supersedes_static_skill_label_inference_in_prior_binding'],
        active_skills_attributes_moods_conditions_rooms_bound_by=str(ACTIVE),
        consumable_use_andred_name_warning_source_bound_not_freshly_activated=True,
        historical_equipment_acquisition_provenance_not_revalidated=True,no_new_fixture_savestate_orRafael_progress=True,
        alternate_city_states_Sextant_Product_not_newly_visited=True,full_playthrough=False,hardware=False,guide_photos=False,
        new_credit=0,producer_sha256=sha(Path(__file__).read_bytes())))
    print('67-help labels bound; two ordinary UI probes complete:15800 frames,24 distinct reviewed navigation states. No consumable or earned-equipment claim.')
