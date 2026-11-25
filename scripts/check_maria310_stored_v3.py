"""Bind the unchanged compound helper in the journaled stored-check environment."""
from scripts import check_maria310_stored_v2 as previous
source=previous.source
if __name__=='__main__':
    env={**vars(previous.previous.previous),**vars(previous.previous),**vars(previous),**globals()}
    exec(compile(source,__file__+'::same-complete-stored-guards-journal-and-declared-compound-helper','exec'),env)
