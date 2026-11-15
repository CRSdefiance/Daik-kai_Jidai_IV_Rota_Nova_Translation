"""Reuse complete stored glyph/parity/branch checks on exact pending block payloads."""
from scripts import check_rafael_early_tutorial_stored as previous
from scripts.source_locked_derivation_v5118 import checked_text

check_FE_rows=previous.check_FE_rows
progressive_expand=previous.progressive_expand
FE_expand=previous.FE_expand
source=checked_text(previous.source,{
    "    image=NdsImage.open(rebuilt['research_ROM'])\n    assert sha(Path(rebuilt['research_ROM']).read_bytes())==rebuilt['research_ROM_sha256']":
        "    assert rebuilt['no_ROM_orwhole_archive_created']\n    image=ctx.image",
    "    blocks=IlnkContainer.parse(image.read_file(load(rebuilt['manuscript'])['file_path'])).blocks":
        """    archive=image.read_file(load(rebuilt['manuscript'])['file_path'])
    assert sha(archive)==rebuilt['source_archive_sha256']
    blocks=list(IlnkContainer.parse(archive).blocks)
    for group in rebuilt['groups']:
        assert sha(blocks[group['block']])==group['current_sha256']
        payload=Path(group['target_block']).read_bytes();assert sha(payload)==group['target_sha256']
        blocks[group['block']]=payload""",
    "replace(b'FO',b'Castor Co.')":"replace(b'FO',b'Castor Co.').replace(b'FU',b'Rafael Castor')",
})
exec(compile(source,__file__+'::same-stored-native-checks-block-only-composition-pending','exec'),globals())
