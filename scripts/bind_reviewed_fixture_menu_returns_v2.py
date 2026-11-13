"""Accept the scoped approved-menu proof keys with unchanged live interval guards."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import checked_text
source = checked_text(Path('scripts/bind_reviewed_fixture_menu_returns_v1.py').read_text(encoding='utf-8'), {
    "exact['native_receipt']": "exact['proof']",
    "exact['native_receipt_sha256']": "exact['proof_sha256']",
})
if __name__ == '__main__':
    exec(compile(source,__file__+'::same-own-menu-interval-andordinary-A-return-guards','exec'),globals())
