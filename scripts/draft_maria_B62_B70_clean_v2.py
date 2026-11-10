"""Keep Maria's repeated tomato acknowledgment neutral rather than affirming an apple identity."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/draft_maria_B62_B70_clean_v1.py').read_text(encoding='utf-8'),{
    'B62_B70_independent_drafts_v1.json':'B62_B70_independent_drafts_v2.json',
    "7:'Yes, they are.',":"7:'Mm-hmm.',",
    "14:'Yes, they are.',":"14:'Mm-hmm.',",
    'Repeat Maria\'s distracted automatic agreement even though Emilio now mentions apples;the slight mismatch is the exchange\'s deadpan humor.':
        'Repeat the same neutral acknowledgment as R7. This preserves distracted agreement without adding a predicate that could imply tomatoes are apples.',
    '[path,Path(__file__)]':"[path,Path('scripts/draft_maria_B62_B70_clean_v1.py'),Path(__file__)]",
})
if __name__=='__main__':exec(compile(source,__file__+'::same-source-bound-independent-drafts-faithful-neutral-tomato-responses','exec'),globals())
