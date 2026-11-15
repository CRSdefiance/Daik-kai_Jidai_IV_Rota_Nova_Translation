"""Initialize the backing-image height required by the current bounded native painter."""
from scripts.source_locked_derivation_v5118 import derive
if __name__=='__main__':
    print(derive('scripts/current_item_detail_machine_v6102b.py','scripts/current_item_detail_machine_v6102c.py',{
        "SOURCE=checked_text(inspect.getsource(original),{":"SOURCE=checked_text(inspect.getsource(original),{\n    '    put(IMAGE, mode, pitch)':'    put(IMAGE, mode, pitch, surface_size[1])',",
    }))
    print(derive('scripts/prove_shachihoko_detail_fonts_v6101c.py','scripts/prove_shachihoko_detail_fonts_v6101d.py',{
        'scripts.current_item_detail_machine_v6102b import':'scripts.current_item_detail_machine_v6102c import',
        "Path('scripts/current_item_detail_machine_v6102b.py')":"Path('scripts/current_item_detail_machine_v6102c.py')",
    }))
