"""Qualify explicitly selected fresh blocks against a previous loader proof in the same batch."""
from scripts import check_reviewed_scene_loaders_v2 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args = parser.parse_args()':
        "    parser.add_argument('--fresh-blocks',type=int,nargs='+',required=True)\n    args = parser.parse_args()",
    "    assert changed==set(rebuilt['changed_blocks'])":
        "    assert changed==set(args.fresh_blocks) and changed<=set(rebuilt['changed_blocks'])",
    'fresh_whole_archive_loads_andcache_hits=325,':
        'fresh_whole_archive_loads_andcache_hits=325, incremental_fresh_blocks=sorted(changed),',
})
exec(compile(source,__file__+'::same-exact-block-hashes-current-loads-andnative-parent-guards','exec'),globals())
