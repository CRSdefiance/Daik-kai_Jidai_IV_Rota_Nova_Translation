"""Reuse the verified Rafael successor's exact reviewed RGB chain and own fresh RAM."""
from scripts.verify_registered_rafael_startup_v1 import source as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous,{
    "    approval_path=Path(args.parent_startup).parent/'direct_visual_andcontext_approval_v1.json'\n    approval=load(approval_path)\n    assert approval['context_sha256']==sha(args.parent_startup.read_bytes())\n    assert Path(approval['context'])==args.parent_startup\n    assert approval['all_six_key_frames_directly_viewed'] and len(parent['captures'])==6":
        "    approval_path=Path(parent['parent_visual_approval'])\n    assert sha(approval_path.read_bytes())==parent['parent_visual_approval_sha256']\n    approval=load(approval_path)\n    assert approval['all_six_key_frames_directly_viewed'] and parent['six_key_frames_directly_viewed']\n    assert len(parent['exact_own_RGB_reuse_of_prior_direct_visual_review'])==10\n    assert all(r['byte_identical_to_prior_reviewed_RGB'] for r in parent['exact_own_RGB_reuse_of_prior_direct_visual_review'])",
})
exec(compile(source,__file__+'::same-native-startup-proof-exact-reviewed-Rafael-parent-RGB-chain','exec'),globals())
