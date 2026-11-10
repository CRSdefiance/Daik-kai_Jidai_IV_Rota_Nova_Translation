"""Reuse exact visual planes across the fully qualified Emilio-only metadata inverse."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.owned_name_glyph_v1 import plan_arm9_name_glyph
from scripts.source_locked_derivation_v5118 import checked_text

original=Path('scripts/make_unique_editorial_page_sheets.py')
source=checked_text(original.read_text(encoding='utf-8'),{
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--name-change-reuse',type=Path)\n    args=parser.parse_args();assert not args.out.exists()",
    "    assert current['runtime']['ARM9_sha256']==old['runtime']['ARM9_sha256']":
    """    if current['runtime']['ARM9_sha256']!=old['runtime']['ARM9_sha256']:
        assert args.name_change_reuse is not None
        known=load(args.name_change_reuse)
        assert known['current_runtime']==current['runtime'] and known['previous_runtime']==old['runtime']
        before=NdsImage.open(old['runtime']['candidate']).read_file('/__arm9__.bin')
        after=NdsImage.open(current['runtime']['candidate']).read_file('/__arm9__.bin')
        expected,proof=plan_arm9_name_glyph(before,load('work/analysis/Emilio_name_glyph_20261101/owned_field_proposal.json'))
        assert expected==after and proof==known['ARM9_exact_except_source_qualified_exclusive_actor14_name_slot']
        assert known['whole_actual_actor_model_bytes_andCOMMON_andfont_exact']
    else:assert current['runtime']['ARM9_sha256']==old['runtime']['ARM9_sha256']""",
    '        only_pixel_identical_same_consumer_size_runtime_andfont_reuse=True,':
        '        only_pixel_identical_same_consumer_size_code_andfont_reuse=True,qualified_name_inverse=str(args.name_change_reuse) if args.name_change_reuse else None,',
})
exec(compile(source,__file__+'::explicit-eight-byte-name-inverse-only','exec'),globals())
