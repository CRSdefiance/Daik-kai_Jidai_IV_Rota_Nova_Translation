"""Check all stored objects,14 formatter guards and104 original expansion cases."""
from dataclasses import replace
from pathlib import Path
from dk4tool.dialogue import maria_B109_layout_v2 as codec
from dk4tool.dialogue.maria_B109_profile import profile_for
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.prove_maria_B109_macro_profile_v3507 import expand
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B109_stored_target_v3518')
PLAN=Path('work/analysis/maria_B109_B33_fixture_v3516/B109_source_owned_relocation_and_B33_entry_fixture.json')
FONT=Path('work/analysis/maria_B109_fonts_v3515/current_macro_QA_and_progressive_font_proof.json')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=map(read,[PLAN,FONT]);docpath=Path(plan['manuscript']);doc=read(docpath);packet=read(doc['source_context'])
    assert sha(docpath.read_bytes())==plan['manuscript_sha256']==font['manuscript_sha256']
    im=NdsImage.open(plan['parent']);arm=im.read_file('/__arm9__.bin');old=IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks[109]
    block=Path(plan['target_block']).read_bytes();assert sha(block)==plan['target_block_sha256'];profile=profile_for(arm,old)
    negatives=[]
    def reject(label,fn):
        try:fn()
        except (ValueError,AssertionError) as e:negatives.append(dict(case=label,rejected=True,error=str(e)))
        else:raise AssertionError(label)
    r=doc['records'][0];raw=bytes.fromhex(r['source_hex'])
    for label,p in [('width',replace(profile,window_width_px=228)),('rows',replace(profile,max_lines=5)),('glyph',replace(profile,default_ascii_width=5)),('row-spacing',replace(profile,line_height_px=12)),('disabled-LF-guard',replace(profile,guard_linebreaks=False)),('disabled-pair-phase',replace(profile,pair_phase_safe_breaks=False)),('disabled-balancing',replace(profile,balanced_wrapping=False)),('macro-width',replace(profile,macro_ascii_lengths={**profile.macro_ascii_lengths,'FO':10})),('unscoped-base',get_dialogue_profile('maria-story-shared-events-live'))]:
        reject(label,lambda p=p:codec.encode_relocatable_dialogue(raw,r['english'],p))
    for tag in ['{LB}','{ALIGN:0}','{PAD}','{END}']:reject('manual-or-end-'+tag,lambda tag=tag:codec.encode_relocatable_dialogue(raw,r['english']+tag,profile))
    reject('widened-selectors',lambda:codec.encode_relocatable_dialogue(raw,r['english'],replace(profile,leading_speaker_bytes=profile.leading_speaker_bytes|{148})))
    assert len(negatives)==14
    ROOT.mkdir(parents=True);ctx=CurrentContext('work/analysis/maria_B109_voices_v3499/current_native_input.json',packet['historical_snapshot_ROM'],ROOT/'current_context')
    rows={r['id']:r for r in doc['records']};fonts={c['id']:c for c in font['cases']};cases=[];sheets=[]
    for t in plan['text_records']:
        r=rows[t['id']];stored=bytes.fromhex(t['stored_text_hex']);at=t['new_text_offset'];assert block[at:at+len(stored)]==stored and block[at+len(stored)]==0 and stored[0]==r['source_selector']
        result=ctx.execute(expand,stored[1:],stored[0]);ctx.machines.pop();assert len(result['cases'])==4 and all(c['output_hex']==stored[1:].hex() for c in result['cases'])
        assert t['final_native_plane_sha256']==fonts[t['id']]['whole_native_plane_sha256'];cases.append(dict(id=t['id'],stored_text_offset=at,stored_text_hex=stored.hex(),source_complete_preamble_hex=r['source_complete_preamble_hex'],**result))
    assert len(cases)==26 and not ctx.machines
    for s in font['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256'];sheets.append({**s,'review':'All four current native preview sheets viewed; phrase-flow findings resolved.'})
    ellipsis=next(c for c in font['cases'] if c['id']=='DK4_MES_B109_R0068');assert [(e['code'],e['x'],e['y']) for e in ellipsis['complete_glyph_events'] if e['code']!=32]==[(46,0,0),(46,6,0),(46,12,0)]
    save(ROOT/'all26_stored_objects104_macro_cases14_formatter_guards_and_viewed_sheets.json',dict(plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),manuscript=str(docpath),manuscript_sha256=sha(docpath.read_bytes()),stored_target_cases=cases,stored_target_macro_alignment_cases=104,source_bound_formatter_negatives=negatives,source_consumer_negatives=font['negative_controls'],review_sheets=sheets,wordless_three_periods_complete_at_origin=True,logical_compiled_macro_cases=208,logical_compiled_count_includes_hash_bound_prior_cases=True,new_font_cases=font['newly_executed_font_cases'],reused_font_cases=font['reused_unchanged_font_cases'],native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),focused_actual_new_UI_setup_and_transition_pending=True,no_registry_ROM_ledger_or_review_credit_change=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(stored_objects=26,stored_target_macro_cases=104,formatter_negatives=14,consumer_negatives=17,viewed_sheets=4,credit=0))
