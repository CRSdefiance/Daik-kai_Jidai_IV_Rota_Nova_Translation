"""Accept explicit contextual speakers for FE drafts without approving their native layout."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text

source = checked_text(Path('scripts/save_source_first_editorial_drafts.py').read_text(encoding='utf-8'), {
    "    for ident, english, note in authored['records']:":
    """    for authored_row in authored['records']:
        assert len(authored_row) in [3, 4]
        ident, english, note = authored_row[:3]""",
    "        exposed = [r for r in bindings.get('incidental_legacy_dialogue_exposure', []) if r['id'] == ident]":
    """        if len(authored_row) == 4:
            assert actor == 254 and authored_row[3].strip()
            speaker = authored_row[3]
        elif actor == 254:
            raise ValueError('FE draft needs its individual contextual speaker')
        exposed = [r for r in bindings.get('incidental_legacy_dialogue_exposure', []) if r['id'] == ident]""",
    "                         incidental_legacy_line_exposure=exposed,":
    """                         incidental_legacy_line_exposure=exposed,
                         contextual_FE_speaker_not_native_geometry_approval=actor == 254,""",
})
exec(compile(source, __file__ + '::logical-drafts-with-contextual-FE-speaker', 'exec'), globals())
