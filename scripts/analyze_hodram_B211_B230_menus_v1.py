"""Disambiguate byte-identical menus using exact source keys and ordered surrounding calls."""
from pathlib import Path
from scripts.analyze_native_choice_fixture_samples_v3 import source as previous,menu_scopes
from scripts.audit_story_glyph_consistency import load
from scripts.review_hodram_B221_B230_contextual_v1 import ROOT
from scripts.source_locked_derivation_v5118 import checked_text

BODY=ROOT/'actual_pixels_v1/focused_actual_pixels.json'
source=checked_text(previous,{
    "target=versions[-1]['object_hex'];declared=next(m for m in fixture['menus'] if m['command_hex']==target)":
        "target=versions[-1]['object_hex']",
    "        assert len(source_offsets)==1;source_offset=next(iter(source_offsets))":
        """        assert len(source_offsets)==1;source_offset=next(iter(source_offsets))
        blocks={row['block'] for row in source_rows};assert len(blocks)==1;source_block=next(iter(blocks))
        declared=next(m for m in fixture['menus'] if m['block']==source_block and m['source_command_offset']==source_offset and m['command_hex']==target)
        body=load(BODY);assert body['all_selected_pages_observed_in_exact_fixture_order']
        assert body['evidence'][str(args.fixture)]==sha(args.fixture.read_bytes())
        ordered=body['ordered_selected_source_calls']
        before=max((r for r in fixture['selected_records'] if r['fixture_offset']<declared['fixture_offset']),key=lambda r:r['fixture_offset'])
        after=min((r for r in fixture['selected_records'] if r['fixture_offset']>declared['fixture_offset']),key=lambda r:r['fixture_offset'])
        low=max(r['frame'] for r in ordered if r['id']==before['id'])
        high=min(r['frame'] for r in ordered if r['id']==after['id'])
        assert low<high""",
    "            if cap['frame']<3000:continue":"            if not low<cap['frame']<high:continue",
    "menus.append(dict(block=declared['block'],word=declared['word'],source_command_offset=source_offset,":
        "menus.append(dict(occurrence_window=[low,high],preceding_id=before['id'],following_id=after['id'],block=declared['block'],word=declared['word'],source_command_offset=source_offset,",
    'numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,':
        'byte_identical_menu_occurrences_bound_by_exact_source_keys_andordered_surrounding_calls=True, ordered_body_receipt=str(BODY),ordered_body_receipt_sha256=sha(BODY.read_bytes()), numeric_modal_return_register_original_story_branches_andcancellation_unvisited=True,',
})
if __name__=='__main__':exec(compile(source,__file__+'::strict-source-key-and-ordered-occurrence-windows','exec'),globals())
