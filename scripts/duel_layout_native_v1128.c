/* Research implementation: complete-word 24x3 layout after macro expansion.
 * The original caller owns 1024 bytes before its private font context.
 * Workspace starts at byte128 and ends by byte1000. No heap or global state.
 */
typedef unsigned char u8;
typedef signed short i16;
typedef signed int i32;
typedef unsigned int u32;

enum { WORDS = 32, COLS = 24, ROWS = 3, INF = 0x3fffffff };
typedef struct {
    u8 start[WORDS + 1], end[WORDS], last_db[WORDS];
    i16 boundary[WORDS];
    i32 cost[ROWS + 1][WORDS + 1];
    u8 next[ROWS][WORDS + 1];
    u8 output[80];
} Workspace;
typedef char workspace_must_fit[(sizeof(Workspace) <= 896) ? 1 : -1];

static const u32 weak[] = {
    0x61, 0x616e, 0x746865, 0x746f, 0x6f66, 0x77697468, 0x666f72,
    0x66726f6d, 0x6f6e, 0x696e, 0x6173, 0x6174, 0x616e64
};

static int punctuation(u32 c) {
    return c >= 32 && c < 64 && ((0x8c005002u >> (c - 32)) & 1);
}

static u32 lower(u32 c) {
    return c >= 'A' && c <= 'Z' ? c + 32 : c;
}

/* A complete normalized word, never a suffix hash of a longer name. */
static u32 word_hash(const u8 *text, u32 a, u32 b) {
    u32 length, hash = 0;
    while (a < b && punctuation(text[a])) ++a;
    while (b > a && punctuation(text[b - 1])) --b;
    length = b - a;
    if (length > 5) return 0;
    while (a < b) hash = (hash << 8) | lower(text[a++]);
    if (length == 5) return hash == 0x65742773 ? hash : 0;
    return hash;
}

int duel_layout(u8 *text) {
    Workspace *work = (Workspace *)(text + 128);
    u32 n = 0, pos = 0, db = 0, i, j, r, best_rows = 0;
    i32 best = INF;
    if (!text[0] || text[0] == ' ') return 0;
    while (text[pos]) {
        u32 c;
        if (n == WORDS || pos >= 128) return 0;
        work->start[n] = (u8)pos;
        while ((c = text[pos]) && c != ' ') {
            if (c < 32 || pos >= 127) return 0;
            if (c >= 128) {
                u32 trail = text[pos + 1];
                if (!((c >= 0x81 && c <= 0x9f) || (c >= 0xe0 && c <= 0xfc))) return 0;
                if (!((trail >= 0x40 && trail <= 0x7e) || (trail >= 0x80 && trail <= 0xfc))) return 0;
                pos += 2;
                db = pos;
            } else ++pos;
        }
        work->end[n] = (u8)pos;
        work->last_db[n] = (u8)db;
        if (pos - work->start[n] > COLS) return 0;
        ++n;
        if (text[pos] == ' ') {
            ++pos;
            if (!text[pos] || text[pos] == ' ') return 0;
        }
    }
    for (i = 0; i < n; ++i) {
        u32 hash = word_hash(text, work->start[i], work->end[i]);
        u32 next = i + 1 < n ? word_hash(text, work->start[i + 1], work->end[i + 1]) : 0;
        u32 final = text[work->end[i] - 1];
        i32 cost = 0;
        if (final != '.' && final != '!' && final != '?' && final != ';' && final != ':') {
            for (j = 0; j < sizeof(weak) / sizeof(weak[0]); ++j)
                if (hash == weak[j]) cost += 2000;
        }
        if ((next == 0x6475656c && (hash == 0x61 || hash == 0x66616972 || hash == 0x65742773)) ||
            (hash == 0x6f6e65 && next == 0x6f6e) ||
            (hash == 0x6f6e && next == 0x6f6e65) ||
            (hash == 0x6c6574 && next == 0x7573)) cost += 3000;
        if (final == '.' || final == '!' || final == '?') cost -= 200;
        else if (final == ',' || final == ';' || final == ':') cost -= 100;
        work->boundary[i] = (i16)cost;
    }
    for (r = 0; r <= ROWS; ++r)
        for (i = 0; i <= n; ++i) work->cost[r][i] = INF;
    work->cost[0][n] = 0;
    for (r = 1; r <= ROWS; ++r) {
        for (i = n; i-- > 0;) {
            for (j = i; j < n; ++j) {
                u32 width = work->end[j] - work->start[i];
                u32 reset = work->last_db[j];
                i32 cost, tail, gap;
                if (width > COLS) break;
                if (reset < work->start[i]) reset = work->start[i];
                /* A pending ASCII pair needs its invisible blank inside the view. */
                if (width + ((work->end[j] - reset) & 1) > COLS) continue;
                tail = work->cost[r - 1][j + 1];
                if (tail == INF) continue;
                gap = COLS - width;
                cost = gap * gap + tail;
                if (j + 1 < n) cost += work->boundary[j];
                else if (i) {
                    if (j == i) cost += 8000;
                    if (width < 9) cost += 1000;
                }
                /* Ascending ends preserve the reference's shorter-prefix tie rule. */
                if (cost < work->cost[r][i]) {
                    work->cost[r][i] = cost;
                    work->next[r - 1][i] = (u8)(j + 1);
                }
            }
        }
        if (work->cost[r][0] != INF) {
            i32 cost = work->cost[r][0] + 160 * (r - 1);
            if (cost < best) { best = cost; best_rows = r; }
        }
    }
    if (!best_rows) return 0;
    pos = 0;
    i = 0;
    for (r = best_rows; r; --r) {
        u32 end = work->next[r - 1][i];
        u32 a = work->start[i], b = work->end[end - 1], phase = 0;
        while (a < b) {
            u32 c = text[a++];
            work->output[pos++] = (u8)c;
            if (c >= 128) { work->output[pos++] = text[a++]; phase = 0; }
            else phase ^= 1;
        }
        if (r > 1) {
            if (phase) work->output[pos++] = ' ';
            work->output[pos++] = '\n';
        }
        i = end;
    }
    work->output[pos] = 0;
    for (i = 0; i <= pos; ++i) text[i] = work->output[i];
    return (int)best_rows;
}
