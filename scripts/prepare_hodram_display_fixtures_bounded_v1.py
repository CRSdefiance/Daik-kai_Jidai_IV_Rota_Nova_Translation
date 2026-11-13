"""Reject oversized QA blocks before writing a ROM; preserve native opening cleanup."""
from scripts import prepare_hodram_display_fixtures_with_opening_exit_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    args = parser.parse_args()':
        "    parser.add_argument('--capacity',type=Path,required=True)\n    args = parser.parse_args()",
    "    arm = image.read_file('/__arm9__.bin')":
        """    arm = image.read_file('/__arm9__.bin')
    capacity=load(args.capacity)
    assert capacity['registered_ARM9_sha256']==sha(arm)
    assert capacity['source_current_consumer_code_exact'] and capacity['native_saved_LR_overwritten_by_fixture_text']
    assert capacity['all_ten_production_blocks_inside_conservative_bound']
    assert capacity['safe_QA_block_limit']==9216""",
    '        block = bytes(logical)+bytes(-len(logical) % 4)':
        "        block = bytes(logical)+bytes(-len(logical) % 4)\n        assert len(block)<=capacity['safe_QA_block_limit'],('Oversized synthetic QA block',spec['name'],len(block),capacity['safe_QA_block_limit'])",
    "            source_bound_QA_host_opening_exit=host_exit,source_bound_QA_host_exit_hex=host_exit_bytes.hex(),":
        """            source_bound_QA_host_opening_exit=host_exit,source_bound_QA_host_exit_hex=host_exit_bytes.hex(),
            native_host_capacity_proof=str(args.capacity),native_host_capacity_proof_sha256=sha(args.capacity.read_bytes()),
            padded_QA_block_bytes=len(block),source_bound_QA_block_limit=capacity['safe_QA_block_limit'],
            QA_block_inside_original_stack_buffer=True,""",
    'ORDINARY,args.roles,Path(__file__)]':'ORDINARY,args.roles,args.capacity,Path(__file__)]',
})
exec(compile(source,__file__+'::same-display-fixtures-enforced-original-native-stack-bound','exec'),globals())
