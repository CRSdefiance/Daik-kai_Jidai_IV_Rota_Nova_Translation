"""Bind C281's actual unchanged execution and complete Lil/Camille names to unmasked captured frames."""
from pathlib import Path
from PIL import Image,ImageDraw
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Rafael_B49_actual_focus_v8110')
ACTUAL=Path('work/analysis/Rafael_B49_actual_v8107/paired_source_English_observed_path_complete_pages_names_C281_andreturn.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL);assert not actual['unresolved']
    sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet);groups=[]
    for j,g in enumerate(actual['groups']):
        report=read(g['capture_report']);photos={p['frame']:p for p in report['frames_captured']}
        c=next(p for p in g['command_pairs'] if p['word']==0xC281)
        assert c['start']==4016 and c['returned']==4017 and c['canonical_source_offset']==72
        assert c['decoded_length']==2 and c['native_result']==[3,0]
        assert c['before_RNG']==c['after_RNG']
        actors=sorted({s['source_selector'] for s in g['speech_observations']});assert actors==[0,2,5,9]
        named=[next(s for s in g['speech_observations'] if s['source_selector']==actor) for actor in [2,9]]
        assert all(s['complete_body_holds'] and all(h['complete_name_mask_equal'] for h in s['complete_body_holds']) for s in named)
        frames=[3970,4030,named[0]['complete_body_holds'][-1]['frame'],named[1]['complete_body_holds'][-1]['frame'],g['speech_observations'][-1]['complete_body_holds'][-1]['frame'],g['normal_return_sample_frame']]
        refs=[]
        for i,f in enumerate(frames):
            p=photos[f];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
            draw.text((i*256+3,j*410+3),f"{g['version']} frame{f}",fill='white')
            sheet.paste(Image.open(p['path']).convert('RGB'),(i*256,j*410+24));refs.append(p)
        groups.append(dict(version=g['version'],C281_command=c,frames=refs,
            actual_complete_Lil_Camille_nameplates=[dict(actor_ID=s['source_selector'],name=s['actual_name'],holds=s['complete_body_holds']) for s in named],
            native_only_nameplate_actors=[4,6,8],observed_nameplate_actors=actors,
            original_C281_effect_body_executed_in_core_no_opaque_bridge=True,
            first_exchange_complete_andnormal_return_verified=True))
    assert groups[0]['C281_command']['UI_before']==groups[1]['C281_command']['UI_before']
    assert groups[0]['C281_command']['UI_after']==groups[1]['C281_command']['UI_after']
    ROOT.mkdir(parents=True);path=ROOT/'C281_Lil_Camille_complete_names_andnormal_return.png';sheet.save(path)
    save(ROOT/'focused_actual_C281_names_return_sheet.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),groups=groups,
        sheet=str(path),sheet_sha256=sha(path.read_bytes()),visual_review_pending=True,
        no_invented_page_turn_all61_source_andEnglish_paragraphs_single_page=True,
        disclosed_ROM_entry_fixture_not_natural_event49_selection_Amsterdam_visit_orhardware=True,
        no_new_emulator_run_orcredit=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('C281 executes at4016-4017 in both languages; complete Lil/Camille headers and normal return bound. Visual review pending.')
