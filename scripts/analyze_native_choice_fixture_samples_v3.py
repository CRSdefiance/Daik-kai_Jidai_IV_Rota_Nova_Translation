"""Review every complete menu in single-object or grouped native menu receipts."""
from scripts.analyze_native_choice_fixture_samples_v2 import source as previous
from scripts.audit_story_glyph_consistency import load
from scripts.source_locked_derivation_v5118 import checked_text


def menu_scopes(paths):
    for path in paths:
        proof = load(path)
        if 'versions' in proof:
            yield path, proof
            continue
        for menu in proof['menus']:
            key = menu['block'], menu['source_command_offset']
            rows = [row for row in proof['records'] if (row['block'], row['command_offset']) == key]
            assert len(rows) == 2 * len(menu['versions'][-1]['cases'][0]['native_VM']['labels']) * 2
            yield path, {**proof, 'menus': [menu], 'records': rows, 'source_menu_scope': key}


source = checked_text(previous, {
    "    for proofpath in args.proofs:\n        proof=load(proofpath);assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']":
        """    for proofpath,proof in menu_scopes(args.proofs):
        assert proof['complete_caption_glyphs_centering_bounds_guards_andconsumption_pass']""",
    "        source_offsets={r['source_command_offset'] for r in load(manuscript_path)['records']}":
        """        source_rows=load(manuscript_path)['records']
        if 'source_menu_scope' in proof:
            source_rows=[row for row in source_rows if (row['block'],row['source_command_offset'])==proof['source_menu_scope']]
        source_offsets={row['source_command_offset'] for row in source_rows}""",
    "menus.append(dict(word=declared['word'],source_command_offset=source_offset,":
        "menus.append(dict(block=declared['block'],word=declared['word'],source_command_offset=source_offset,",
})


if __name__ == '__main__':
    exec(compile(source, __file__ + '::same-complete-live-menu-pixel-checks-per-source-object', 'exec'), globals())
