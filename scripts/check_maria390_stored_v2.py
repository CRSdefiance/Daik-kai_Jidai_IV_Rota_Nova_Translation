"""Preserve all stored checks and journal each completed record before later assertions."""
from scripts import check_maria390_stored_v1 as previous
from scripts.source_locked_derivation_v5118 import checked_text

source=checked_text(previous.source,{
    '    rows,relatives=[],[];fresh_pages=reused_pages=0;typed=[];style_records=[]':
        """    class JournalRows(list):
        def append(self,row):
            super().append(row)
            save(args.out/('record_'+row['id']+'.json'),dict(record=row,reconstruction=str(args.reconstruction),
                reconstruction_sha256=sha(args.reconstruction.read_bytes()),native=str(args.native),
                native_sha256=sha(args.native.read_bytes()),producer=str(Path(__file__)),producer_sha256=sha(Path(__file__).read_bytes()),
                complete_individual_stored_checks_pass=True,whole_batch_branches_andrelease_not_inferred=True,new_credit=0))
    rows,relatives=JournalRows(),[];fresh_pages=reused_pages=0;typed=[];style_records=[]""",
})
if __name__=='__main__':
    env={**vars(previous),**globals()}
    exec(compile(source,__file__+'::same-full-stored-assertions-with-durable-successful-record-receipts','exec'),env)
