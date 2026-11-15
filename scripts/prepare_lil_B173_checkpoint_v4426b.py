"""Repair the encoding literal caught before any checkpoint writes;retain original."""
from scripts.prepare_lil_B156_layout_v3705 import derive

if __name__=='__main__':
    derive('scripts/checkpoint_lil_B173_v4426.py','scripts/checkpoint_lil_B173_v4426b.py',{'utf-3':'utf-8'})
    print('Restored UTF-8 literal;first producer failed before directory/ledger/document mutation and remains preserved.')
