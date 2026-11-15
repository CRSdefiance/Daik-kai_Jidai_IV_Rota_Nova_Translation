"""Use the source B32 table's first item105 rather than a global item index."""
from scripts.source_locked_derivation_v5118 import derive
from dk4tool.script.common_entry_tables import ITEM_TABLES
if __name__=='__main__':
    assert ITEM_TABLES[32][2]==105
    print(derive('scripts/bind_shachihoko_description_consumers_v6092.py','scripts/bind_shachihoko_description_consumers_v6092b.py',{'B32_TABLE_OFFSET+116*2':'B32_TABLE_OFFSET+(116-105)*2'}))
