"""Use this menu's actual original backing;preserve the caught tight-bitmap first-T failure."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.source_locked_derivation_v5118 import checked_text,derive
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_menu_model_v6285');OWNER=Path('work/analysis/lil_B206_menu_owner_v6284/actual_caption_context_view_and_backing.json')
if __name__=='__main__':
    assert not ROOT.exists();owner=read(OWNER);assert not owner['errors'] and not owner['mismatches'] and len(owner['rows'])==5 and owner['all_host_slots_restored_and_core_file_exact']
    assert all(r['context_words'][3:5]==[114,12] and r['context_words'][12]==8 and r['view_words'][10:12]==[114,12] and r['bitmap_header_words'][:3]==[4,64,36] and r['backing_bytes']==4608 and r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in owner['rows'])
    armhash=read('translations/shady_man_label_manuscript_v2.json')['target_ARM9_sha256']
    helper=derive('scripts/native_menu_backing_surface_v4080.py','scripts/native_B206_menu_backing_v6285.py',{
      'def paint(arm,text,style,width,origin):':'def paint(arm,text,style,width,origin):\n    assert sha(arm)=='+repr(armhash),
      'expected[(y+yy)*backing_width+x+index*6+xx]':'expected[(y+yy+1)*backing_width+x+index*6+xx]',
    })
    source=Path('scripts/prove_lil_B206_choices_v6281.py');target=Path('scripts/prove_lil_B206_choices_v6286.py');original=source.read_text('utf-8');a=original.index('    painter = inspect.getsource(prior.paint)');b=original.index('    cases,pictures = [],[]',a);segment=original[a:b]
    oldenv="        env = {**prior.__dict__,'LABEL_WIDTH':width,'sha':sha,'CURRENT_ARM9':CURRENT_ARM9}\n        exec(compile(painter,'source_derived_B122_B127_choice_painter_v3279','exec'),env)"
    changes={
      'lil_B206_choices_v6281':'lil_B206_choices_v6286',
      'from scripts.verify_village_wrap_v608 import read, save':'from scripts.verify_village_wrap_v608 import read, save\nfrom scripts import native_B206_menu_backing_v6285 as BACKING',
      segment:"    painter=Path(BACKING.__file__).read_text('utf-8')\n",
      oldenv:"        env={'paint':lambda arm,text,style:BACKING.paint(arm,text,style,width,(0,index*12))}",
      'for style in (1,15):':'for style in (1,8,15):',
      "Image.new('RGB',(width,20))":"Image.new('RGB',(width,12))",
      'all_four_style_label_planes':'all_six_style_label_planes',
      'eight_complete_native_style_label_planes':'twelve_complete_native_style_label_planes',
      'native_label_planes=8':'native_label_planes=12',
      'complete_current_and_reviewed_style_label_planes=16':'complete_current_and_reviewed_style_label_planes=24',
      "source_derived_text_canvas_width=width,all_four_style_label_planes=planes,":"source_derived_text_canvas_width=width,observed_backing_width=256,observed_backing_height=36,logical_caption_height=12,all_six_style_label_planes=planes,",
      "save(ROOT/'original_choice_decoder_VM_geometry_and_native_pixels.json',dict(":"save(ROOT/'original_choice_decoder_VM_geometry_and_native_pixels.json',dict(source_owned_backing_proof="+repr(str(OWNER))+",source_owned_backing_proof_sha256=sha(Path("+repr(str(OWNER))+").read_bytes()),preserved_failed_tight_bitmap_probe='scripts/prove_lil_B206_choices_v6281.py',",
    }
    proof=derive(str(source),str(target),changes);ROOT.mkdir(parents=True);save(ROOT/'actual_native_backing_corrected_model_and_preserved_failures.json',dict(actual_owner_proof=str(OWNER),actual_owner_proof_sha256=sha(OWNER.read_bytes()),actual_logical_view=[114,12],actual_backing=[256,36],actual_style=8,source_bound_helper=helper,native_menu_verifier_derivation=proof,tight114px_bitmap_failure_eight_T_stem_pixels_preserved=True,no_wording_padding_ROM_font_viewport_native_metrics_or_guard_change=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,full_goal_complete=False));print('B206 model now matches own actual114x12 view/256x36 backing/current one-pixel font offset. Tight-bitmap failure preserved;no ROM or wording change.')
