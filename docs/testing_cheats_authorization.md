# Authorized testing shortcuts

The user explicitly permits isolated location fixtures and testing cheats for
crew health, money, ship repairs, inventory and other useful test setup. On
2026-10-13 they additionally confirmed that travel-route unlock cheats may be
used for testing when available. No further approval is needed for these tests.

Use copied saves or isolated test runs. Preserve original donor saves and keep
cheats out of the production ROM and reconstructable translation patch. Record
each change and identify captures as fixtures. Synthetic discovery or unlock
does not establish ordinary travel, earned progression or normal acquisition.

Before using a travel-route code, verify its DS target and actual fields against
the current build. The previously verified Maria selection code exposes the
fourth captain; it does not unlock travel routes. See
[Maria code](maria_unlock_action_replay.md).

No DS travel-route unlock code has been confirmed by this checkpoint. The initial
published-code search produced a [PSP code author's reference](https://oretic.lsv.jp/DrEazyCool_Room-005.html);
its PSP addresses must not be applied to the DS build. Continue with original
DS discovery/route consumers if a published DS code cannot be verified.


## Supported Historic Sites fixtures

Use `scripts/prepare_supported_sites_v529.py` for normal Gallery image testing.
Original21 metadata slots include null image entries1/4, with placeholder
descriptions. Unlocking them produces invalid test selections. The supported
fixture selects19 real Iseki images, verifies source ownership and checksum,
and its declared supported-image preflight rejects null selections. Historical
all21/single1/4 copies are retained only as explicitly failed diagnostic tests.
No production-code repair or global-unused-name claim follows from these flags.
