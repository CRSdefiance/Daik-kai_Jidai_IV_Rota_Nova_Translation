"""Verify live captions and ordinary A returns at each exact selected menu occurrence."""
from pathlib import Path

from scripts.source_locked_derivation_v5118 import checked_text


PARENT=Path('scripts/analyze_native_choice_fixture_samples_v1.py')
source=checked_text(PARENT.read_text(encoding='utf-8'),{
    "    args=parser.parse_args();assert not args.out.exists()":
        """    parser.add_argument('--body-proof',type=Path,required=True)
    parser.add_argument('--menu-proof',type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()""",
    """    samples=[];menus=[]
    for proofpath in args.proofs:""":
        """    body=load(args.body_proof); exact_menus=load(args.menu_proof)
    assert body['frames']==fixture['frames'] and body['all_selected_pages_observed_in_exact_fixture_order']
    assert body['evidence'][str(args.fixture)]==sha(args.fixture.read_bytes())
    assert body['evidence'][str(args.terminal)]==sha(args.terminal.read_bytes())
    proof_by_key={(m['block'],m['source_command_offset']):m for m in exact_menus['menus']}
    ordered=body['ordered_selected_source_calls']
    speech=fixture['selected_records']
    inputs=load(fixture['inputs'])
    assert sha(Path(fixture['inputs']).read_bytes())==fixture['inputs_sha256']
    samples=[];menus=[]
    for proofpath,declared in zip(args.proofs,fixture['menus'],strict=True):
        exact=proof_by_key[declared['block'],declared['source_command_offset']]
        assert Path(exact['native_receipt'])==proofpath and sha(proofpath.read_bytes())==exact['native_receipt_sha256']
        prev=next(r for r in reversed(speech) if r['fixture_offset']<declared['fixture_offset'])
        follow=next(r for r in speech if r['fixture_offset']>declared['fixture_offset'])
        left=max(r['frame'] for r in ordered if r['id']==prev['id'])
        right=next(r['frame'] for r in ordered if r['id']==follow['id'] and r['page']==1)
        assert right>left""",
    """        target=versions[-1]['object_hex'];declared=next(m for m in fixture['menus'] if m['command_hex']==target)""":
        """        target=versions[-1]['object_hex']
        assert declared['command_hex']==target==exact['target_object_hex']""",
    "            if cap['frame']<3000:continue": "            if not left<cap['frame']<right:continue",
    """                    assert not cyan or cyan==blank
                    if cyan:selected.append(option)
                    else:assert all(im.getpixel(point)==(205,198,180) for point in blank)""":
        """                    if cyan:
                        lo=min(pt[1] for pt in cyan);hi=max(pt[1] for pt in cyan)
                        assert cyan=={pt for pt in blank if lo<=pt[1]<=hi}
                        selected.append(option)
                    assert all(im.getpixel(point)==(205,198,180) for point in blank-cyan)""",
    """        samples.extend(found);menus.append(dict(word=declared['word'],source_command_offset=declared['stored_command_offset'],count=count,""":
        """        selected_samples=[r for r in found if r['visible_selected_option'] is not None]
        assert selected_samples,('no observed cursor',declared)
        final_menu_frame=selected_samples[-1]['frame']
        presses=[r['start'] for r in inputs if r['buttons']==['A'] and final_menu_frame<r['start']<=right]
        assert len(presses)==1,('A return not isolated between menu and next dialogue',final_menu_frame,right,presses)
        samples.extend(found);menus.append(dict(word=declared['word'],source_command_offset=declared['stored_command_offset'],count=count,
            clean_source_command_offset=declared['source_command_offset'],block=declared['block'],
            preceding_speech=prev['id'],following_speech=follow['id'],following_speech_frame=right,observed_default_return_A_input=presses[0],""",
    "        all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches=True,":
        """        all_declared_native_menus_have_complete_pixel_centering_bounds_andbackground_matches=True,
        observed_each_menu_between_its_own_exact_preceding_and_following_speech=True,
        complete_contiguous_cursor_band_and_remaining_paper_background_checked=True,
        ordinary_A_return_to_next_fixture_speech_observed=True,
        body_proof=str(args.body_proof),body_proof_sha256=sha(args.body_proof.read_bytes()),""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::complete-ordered-menu-occurrences-and-ordinary-return','exec'),globals())

