"""Use the qualified menu pixel/occurrence checker with an explicit body receipt."""
from scripts.analyze_hodram_B301_B310_menus_v1 import source as previous,menu_scopes,background_band
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    '    args=parser.parse_args();assert not args.out.exists()':
        "    parser.add_argument('--body',type=Path,required=True)\n    args=parser.parse_args();assert not args.out.exists()\n    BODY=args.body",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-key-and-native-caption-cursor-checks-explicit-body','exec'),globals())
