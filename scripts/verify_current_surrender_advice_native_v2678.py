"""Use released2674 bytes and the successor context/parser for the revised line."""
from pathlib import Path
from scripts.current_common_native_context_v2677 import CurrentContext
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.surrender_advice_contextual_v1 import current_entries
from dk4tool.rom.nds import NdsImage

ROOT=Path('work/analysis/current_surrender_advice_native_v2678')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    olddoc=read('translations/aftermath_remaining_contextual_editorial_manuscript_v2.json')
    release=read('work/analysis/surrender_advice_release_v2675/registered_release_verification.json')
    inputpath=ROOT/'current_context_input.json'
    save(inputpath,dict(current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],
        current_ARM9_sha256=release['ARM9_sha256'],current_COMMON_sha256=release['COMMON_sha256'],
        native_context_proof=olddoc['native_context_proof'],full_goal_complete=False))
    ctx=CurrentContext(inputpath,'out/all_routes_combined_v1807_candidate.nds',ROOT/'current_context')
    context=read(olddoc['native_context_proof'])
    rep=next(c for t in context['voice_tables'] if t['table']==0x021177E0 for c in t['all207_original_actor_choices'] if c['message_ID']==2029 and c['actor_ID']!=1)
    result=ctx.speak(0x53F0C,rep['actor_object'],0x021177E0,None)
    owner=int.from_bytes(ctx.arm[0x552A0:0x552A4],'little');loaded=bytes(ctx.machines[-1][0].mem_read(owner+0x2030,512)).split(b'\0')[0]
    assert loaded==ctx.entries[2029].text==b' You cannot win! I suggest you surrender at once!'
    golden=next(c for c in read(olddoc['current_native_font_proof'])['complete_native_planes'] if c['message_ID']==2029)
    assert result['input_hex']==loaded.hex() and result['formatted_hex']==golden['formatted_hex']
    events=[];pixels=bytes(ctx.raster(ctx.arm,bytes.fromhex(result['formatted_hex']),0x01FFCE40-0x02000000,size=(228,64),instruction_limit=2000000,glyph_events=events))
    assert pixels==bytes(independent_font(ctx.arm,ctx.rom.read_file('/GRP/KANJI.FNT'),golden['lines'])) and sha(pixels)==golden['font_plane_sha256']
    assert current_entries(ctx.common,ctx.arm)[2029].text==loaded
    try:current_entries(ctx.common[:-1]+bytes([ctx.common[-1]^1]),ctx.arm)
    except AssertionError:pass
    else:raise AssertionError('Parser accepted modified COMMON')
    save(ROOT/'released_current_native_verification.json',dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],
        ARM9_sha256=sha(ctx.arm),COMMON_sha256=sha(ctx.common),message_ID=2029,
        native_pipeline=result,loaded_template_hex=loaded.hex(),lines=golden['lines'],complete_font_plane_sha256=sha(pixels),
        complete_native_independent_plane_and_prior_reviewed_pixels_equal=True,current_executed_instructions_and_actor_models_exact=True,
        current_parser='dk4tool.patch.surrender_advice_contextual_v1.current_entries',current_context_helper='scripts/current_common_native_context_v2677.py',
        successor_parser_rejects_modified_COMMON=True,context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),
        no_additional_emulator_visit_or_actual2029_activation=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Released2674 revised2029 original pipeline/full font passes;successor current parser/context verified andmodified COMMON rejected. No new actual2029visit.')
