"""Accept ordered meaning/draft triples with the same source and timestamp guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source=checked_text(Path('scripts/seal_clean_editorial_parts_v1.py').read_text(encoding='utf-8'), {
    "authored=load(d['authored']);assert authored['source_gloss_precedes_independent_draft_in_each_entry']":
        """authored=load(d['authored'])
        assert authored['whole_clean_exchanges_read_before_drafting'] and authored['current_English_not_consulted']
        assert all(isinstance(row,list) and len(row)==3 and isinstance(row[1],str) and row[1].strip() and isinstance(row[2],str) and row[2].strip() for row in authored['records'])
        assert [(row['id'],row['source_meaning'],row['independent_English_draft']) for row in d['records']]==[tuple(row) for row in authored['records']]""",
})
if __name__=='__main__':
    exec(compile(source,__file__+'::same-ordered-meanings-before-drafts-andno-current-exposure-contract','exec'),globals())
