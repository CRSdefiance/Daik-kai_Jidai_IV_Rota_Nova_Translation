# Maria route Action Replay bypass

Target: Japanese Nintendo DS release, game ID `ADKJ 404387D8`.

```text
0209F068 03A00004
```

Enable the code before selecting **New Game**. The fourth entry on **Choose Captain**
will remain available, allowing Maria to be selected without completing another
route. The code changes only the in-memory selection-screen limit and does not set
or save a false completion flag.

## Reverse-engineering notes

The character-selection initializer at `0x0209F05C` calls `0x02046DFC` with the
persistent-progress structure at `0x02279824`. The callee tests bits 0 through 3 of
the halfword at structure offset `0x38` (`0x0227985C`) and returns true if any bit is
set.

When the test returns false, the original instructions are:

```text
0209F064  cmp    r0, #0
0209F068  moveq  r0, #3
0209F06C  streq  r0, [r10, #0x930]
```

The store changes the already-created four-entry captain list to three entries.
The Action Replay code changes `moveq r0, #3` (`03A00003`) to `moveq r0, #4`
(`03A00004`), so the locked path explicitly retains all four entries.

The instruction address and original bytes were verified against both the clean
ARM9 image and `out/all_routes_unified_v2.nds`.
