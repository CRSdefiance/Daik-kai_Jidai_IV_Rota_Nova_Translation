"""Reuse an own-startup native context only for byte-identical current target blocks.

The receipt keeps the older native runtime's identity. Text and command references
are to the current registered target. This never relabels the older snapshot as a
fresh capture, nor allows changed blocks to borrow its current-text proof.
"""
from dk4tool.rom.nds import NdsImage
from scripts import extract_editorial_current_v7 as previous
from scripts.audit_story_glyph_consistency import load
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.source_locked_derivation_v5118 import checked_text


def qualify_scope(ctx,packet,target_release_path):
    release=load(target_release_path)
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert digest(release['candidate'])==release['candidate_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    image=NdsImage.open(release['candidate'])
    # These are the complete bytes supplied to the existing original native
    # machine/catalogue consumer, including font, dispatch and staged payload.
    assert image.read_file('/__arm9__.bin')==ctx.arm
    assert image.read_file('/COMMON/MESFILE.DK4')==ctx.common
    path=packet['file_path']
    before=previous.IlnkContainer.parse(ctx.image.read_file(path)).blocks
    after=previous.IlnkContainer.parse(image.read_file(path)).blocks
    assert len(before)==len(after)
    scope=sorted(g['block'] for g in packet['groups'])
    assert len(scope)==len(set(scope))
    assert all(before[n]==after[n] for n in scope),'Changed source scope cannot reuse the older current-text context'
    receipt=dict(target_release=str(target_release_path),target_release_sha256=digest(target_release_path),
        target_candidate=release['candidate'],target_candidate_sha256=release['candidate_sha256'],
        native_runtime=ctx.receipt(),complete_ARM9_font_payload_andCOMMON_exact=True,
        archive=path,exact_current_blocks=scope,
        exact_current_block_sha256={str(n):previous.sha(after[n]) for n in scope},
        reused_own_snapshot_not_fresh_gameplay=True,original_native_guards_andlookups_still_executed=True,
        no_changed_block_reuse_orhistorical_snapshot_relabeling=True,
        no_editorial_display_orreachability_approval=True,new_credit=0)
    return image,release,receipt


source=checked_text(previous.source,{
    "    ap.add_argument('--captain',type=int,choices=range(4),required=True)":
        "    ap.add_argument('--captain',type=int,choices=range(4),required=True)\n    ap.add_argument('--target-release',type=Path,required=True)",
    '    archive = ctx.image.read_file(path)':
        '    target_image,target_release,scope_reuse=qualify_scope(ctx,packet,args.target_release)\n    archive = target_image.read_file(path)',
    'dict(current_ROM=str(ctx.rompath),':"dict(current_ROM=target_release['candidate'],",
    "current_ROM_sha256=ctx.release['candidate_sha256'], current_archive_sha256=sha(archive),":
        "current_ROM_sha256=target_release['candidate_sha256'], current_archive_sha256=sha(archive),",
    'runtime=ctx.receipt(), all_source_preambles_andcommand_kinds_preserved=True,':
        'runtime=ctx.receipt(), exact_native_context_reuse=scope_reuse, all_source_preambles_andcommand_kinds_preserved=True,',
})
env={**vars(previous),**globals(),'__file__':__file__}
exec(compile(source,__file__+'::original-current-source-controls-native-lookups-with-exact-scope-reuse','exec'),env)

if __name__=='__main__':
    env['main']()
