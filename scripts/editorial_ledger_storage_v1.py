"""Deterministic, readable current-ledger storage without dropping provenance."""
import json


def encode_ledger(value):
    if not isinstance(value,dict):
        raise TypeError('The current editorial ledger must remain a complete JSON object')
    return (json.dumps(value,ensure_ascii=False,indent=1)+'\n').replace('\n','\r\n').encode('utf-8')
