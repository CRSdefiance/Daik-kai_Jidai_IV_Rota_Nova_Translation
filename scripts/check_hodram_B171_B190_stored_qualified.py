"""Qualify one exact terminal zero-ink flush while preserving every real glyph check."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts import check_hodram_B171_B190_stored as previous
from scripts.check_editorial_compiled_pages_v6 import check_FE_rows as strict_FE_rows
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text

DIAGNOSTIC = Path('work/analysis/Hodram_B171_B190_stored_FE_diagnostic_20261104/diagnostic.json')
diagnostic = load(DIAGNOSTIC)
assert sha(Path(diagnostic['reconstruction']).read_bytes()) == diagnostic['reconstruction_sha256']
exceptions = [r for r in diagnostic['records'] if r['extra_events']]
assert len(exceptions) == 1 and exceptions[0]['id'] == 'DK4_MES_B179_R0047'
case = exceptions[0]
assert case['source_alignment_flag'] and case['complete_plane_equal'] and case['complete_visible_rows_match']
assert case['extra_events'] == [dict(kind='ascii', code=32, style=15, x=x, y=24) for x in [0, 6]]


def check_FE_rows(expected, rendered):
    if expected.hex() != case['expanded_hex']:
        return strict_FE_rows(expected, rendered)
    assert expected == bytes.fromhex(case['original_expanded_hex']) + b' '
    assert rendered['events'] == case['native_events']
    assert sha(rendered['physical']) == case['native_plane_sha256']
    target = [line.strip(b' ') for line in expected.split(b'\n')]
    events = rendered['events']
    assert all(e['kind'] == 'ascii' and 0 <= e['code'] < 128 for e in events)
    actual = [bytes(e['code'] for e in events if e['y'] == 12 * i).strip(b' ') for i in range(len(target))]
    extra = [e for e in events if e['y'] not in range(0, 12 * len(target), 12)]
    assert actual == target and extra == case['extra_events']
    return dict(planned_rows=[v.decode('ascii') for v in target], actual_rows=[v.decode('ascii') for v in actual],
        complete_glyph_row_membership_exact=True, guard_spaces_ignored_for_membership_only=True,
        exact_owned_terminal_alignment_space_andzeroink_flush_row_qualified=True,
        qualified_id=case['id'], qualified_events=extra, complete_reviewed_pixel_plane_exact=True,
        diagnostic=str(DIAGNOSTIC), diagnostic_sha256=sha(DIAGNOSTIC.read_bytes()))


compound_storage = previous.compound_storage
source = checked_text(previous.source, {
    "        print('Stored block',group['block'],'checked',flush=True)":
    """        save(args.out/('B'+str(group['block'])+'_checked.json'),dict(
            reconstruction=str(args.reconstruction),reconstruction_sha256=sha(args.reconstruction.read_bytes()),
            native=str(args.native),native_sha256=sha(args.native.read_bytes()),runtime=runtime,
            records=[r for r in rows if r['block']==group['block']],
            relative_cases=[r for r in relatives if r['block']==group['block']],
            typed_objects=[r for r in typed if r['block']==group['block']],
            all_checks_through_this_block_pass=True,new_credit=0))
        print('Stored block',group['block'],'checked',flush=True)""",
})
exec(compile(source, __file__ + '::same-stored-checks-one-exact-zeroink-terminal-case', 'exec'), globals())
