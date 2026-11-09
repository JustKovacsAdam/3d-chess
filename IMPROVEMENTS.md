# Code analysis and possible improvements

This is a review of the code on `main` (after the modernization pass). Items are grouped by
type and roughly ordered by impact. Line references point to the `main` branch versions of the files.

The bugs already fixed on `main` (pawns never marked as moved, recursive flood fill, images
reloaded every frame, bare `except`, and so on) aren't repeated here.

---

## 1. Gameplay bugs and missing rules

### 1.1 The game never ends: no checkmate or stalemate detection
`nincsMatt` (`osztalyok.py:187`) stops a player from moving into check, but nothing checks
whether the side to move has **any** legal move left. When a player is checkmated, their pieces
simply show no highlighted squares and the game stalls. The user documentation says the game
ends with checkmate, but that isn't implemented.

**Fix:** after every move, collect the legal moves for the side to move (`hovaLephet` for each of
their pieces). No moves while in check means checkmate. No moves while not in check means stalemate.
Show the result on screen.

### 1.2 Whose turn it is isn't saved
`fajlkezeles.mentes` only writes the board. On load `kor` is always reset to `"feher"`
(`fuggvenyek.py:175`). If you close the game after White's move, White moves again on the next start.

**Fix:** write the side to move as an extra line in `mentes.txt` (for example `kor:fekete`) and read
it back in `betoltes`. The `web-version` branch already stores it in `localStorage`.

### 1.3 No pawn promotion
A pawn that reaches the last row (`z == 0` for White, `z == 3` for Black) stays a pawn. It can
then only slide between levels. Promote it (automatically to a queen, or with a small picker).

### 1.4 Can't switch selection by clicking another of your own pieces
If a piece is selected and you click a different piece of yours, the selection is cleared
(`fuggvenyek.py:194-202`) and you have to click again. Selecting the new piece directly is what
players expect.

### 1.5 No visual feedback on game state
There's no indication of whose turn it is, whether a king is in check, or what the last move was.
A small text line at the top ("White to move", "Check!") and highlighting the last move's squares
would make the game a lot easier to follow.

### 1.6 Features described in the documentation that are missing
`Extra/Felhasznaloi Dokumentacio.pdf` describes a main menu (Quit / Continue / New game) and a
help button that shows each piece's move set. Only the restart button exists. Either implement them
or update the documentation.

### 1.7 Rule design questions (worth deciding on deliberately)
These aren't necessarily bugs, but they're inconsistent and should be choices, not accidents:

- **No space-diagonal (triagonal) moves.** Bishop and queen only move diagonally within a plane
  (`osztalyok.py:36-52`). The king also can't step to `(±1, ±1, ±1)` because of the
  `abs(rX)+abs(rY)+abs(rZ) <= 2` check. Classic 3D variants such as Raumschach either allow these
  or add a separate piece (the unicorn) for them.
- **Pawns move between levels but can't capture between levels.** A pawn may step one level up or
  down (`abs(rY) == 1`), in either direction and at any time, but it can only capture diagonally in
  the x–z plane.
- **The starting setups aren't mirror images.** `feherSorrend` and `feketeSorrend`
  (`osztalyok.py:104-105`) swap king and queen. Check that this is the intended setup.

---

## 2. Robustness

- **Missing king crashes the check test.** If the save file has no king of a colour (hand-edited
  or corrupted), `kiralyPoz` stays `None` in `nincsMatt` (`osztalyok.py:199`) and indexing it raises a
  `TypeError`. Validate the loaded position (exactly one king per side) and fall back to a new game.
- **Unknown piece codes become pawns.** In `fajlkezeles._beolvas` anything that isn't
  `f`, `kn`, `k`, `l` or `b` silently turns into a pawn, and any colour code except `fh` becomes black.
  Reject unknown codes instead.
- **The game is only saved on a clean exit.** If the program crashes or is killed, the game is
  lost. Saving after every move is cheap at this board size (the web branch already does this).
- **Board size is hard-coded in many places.** `Palya(x, y, z)` takes a size, but
  `Palya(4,4,4)` (`osztalyok.py:191`), `range(4)` in the file functions, `len(sakktabla.tabla)` used
  for all three axes (`fuggvenyek.py:151-153`), the `x+y*4` indexing in `reset`, and every
  screen coordinate all assume 4×4×4. Use one `MERET = 4` constant, or read the size from the board.

---

## 3. Code structure

### 3.1 Separate game logic from drawing and input
`fuggvenyek.py` mixes rendering, hit-testing, move generation (`hovaLephet`, `lepes`) and the main
loop. All game state (`kor`, `kivalasztott`, `specialis`, ...) lives in local variables of the
70-line `kirajzol` function with deeply nested `if`s.

Suggested split:

| Module | Responsibility |
| --- | --- |
| `jatek.py` / `game.py` | `Jatek` class: board, side to move, selection, `valaszt(xyz)`, `lep(honnan, hova)`, game-over state |
| `szabalyok.py` / `rules.py` | Move generation, check, checkmate, promotion. No pygame import |
| `megjelenites.py` / `render.py` | Everything that draws, plus screen ↔ board coordinate conversion |
| `main.py` | Event loop: turns pygame events into `Jatek` calls, redraws |

This makes the rules unit-testable without a window and the event loop short.

### 3.2 One coordinate conversion instead of magic numbers
The isometric projection is written out by hand in four places: `korvonalak`, `szinezesek`,
`babukMegjelenitese` (`121+z*25+x*50, 610-z*25-y*150`) and the hand-written range checks in
`kattintas` (`fuggvenyek.py:93-140`). A single function such as

```python
def mezo_sarok(x, y, z):
    return 100 + 50*x + 25*z, 650 - 150*y - 25*z
```

plus the four cell corners derived from it would drive drawing, piece placement and click
detection (point-in-polygon, or invert the projection). Changing the board's size or position
would then be a one-line change.

### 3.3 Use enums or constants instead of strings
Colours (`"feher"`, `"fekete"`) and piece names (`"kiraly"`, `"paraszt"`, ...) are compared as
string literals all over the code. A typo fails silently. `enum.Enum` (or at least module-level
constants) would catch typos and allow a lookup table for images and save-file codes instead of
the `if/elif` chains in `Babu.__str__` and `fajlkezeles._beolvas`.

### 3.4 Data-driven move rules
`Babu.lephetE` is a long `if/elif` chain. Describing pieces as direction vectors plus a "slides"
flag is shorter, easier to verify, and generates moves directly instead of testing all 64 squares:

```python
BASTYA = [(1,0,0), (-1,0,0), (0,1,0), (0,-1,0), (0,0,1), (0,0,-1)]
FUTO   = [v for v in itertools.product((-1,0,1), repeat=3) if sorted(map(abs, v)) == [0,1,1]]
LOVAS  = [v for v in itertools.permutations((0,1,2)) ...]  # all (±2, ±1, 0) permutations
```

Sliding pieces walk each direction until they hit something, which also removes the need for a
separate `szabadUt` path check for them.

### 3.5 Cheaper check test
`nincsMatt` builds a full new `Palya` and copies 64 cells for every candidate move, then scans the
whole board. That's fine at 4×4×4, but a make/unmake approach (move the piece, test, move it back)
is simpler and faster. It'll matter if you add checkmate detection or a computer opponent, since
both need every legal move each turn.

### 3.6 Smaller things
- Load the save **before** the main loop instead of using the `toltsdBe` flag on the first frame
  (`fuggvenyek.py:178`, `225`).
- `pygame.display.update()` runs 30 times a second even when nothing changed. Only call it after a
  redraw.
- Fill board squares with `pygame.draw.polygon` instead of a pixel flood fill: it's pixel-identical
  and far faster (already done on `web-version`).
- `Palya`'s methods are indented 8 spaces instead of 4.
- Add docstrings and type hints to the public functions.

---

## 4. Code hygiene

- **Encoding mix-up in comments.** Comments contain `õ` where `ő` was meant (for example
  "Kitöltõ", "Királynõ"). The files were saved in a Windows code page and later converted with the
  wrong mapping. A search-and-replace of `õ` → `ő` (and `û` → `ű`, if any) fixes it.
- **CRLF line endings.** The `.py` files use Windows line endings. Add a `.gitattributes` with
  `* text=auto` and normalize them so diffs stay clean on every OS.
- **Naming.** Hungarian identifiers are fine for a university project. If the repo is meant for a
  wider audience, consider English names, or at least avoid mixing the two (`click`, `fut`, `kor`).
- **Linting/formatting.** Add `ruff` (lint + format) and fix what it reports (spacing after commas,
  unused variables, line length).

---

## 5. Testing and tooling

- **No tests.** The rules are the part most worth testing, and they don't need pygame:
  - every piece's moves from the centre and from a corner on an empty board
  - blocking and capturing for sliding pieces
  - pinned pieces and "can't move into check"
  - the pawn double step works only once
  - save → load round trip, and rejection of broken save files
  - checkmate and stalemate positions, once implemented
- **CI:** a GitHub Actions workflow running `ruff check` and `pytest` on every push and pull request.
- **Packaging:** a `pyproject.toml` with the pygame dependency and a `3d-chess` entry point would
  make `pip install .` work.

---

## 6. Feature ideas

Roughly in order of effort:

1. Turn indicator, check warning and last-move highlight (see 1.5)
2. Game-over screen for checkmate or stalemate (see 1.1)
3. Undo (keep a move history list) and a move log
4. Help screen showing each piece's move pattern, as described in the original documentation
5. Different highlight colours for quiet moves and captures
6. Hover highlight under the mouse cursor
7. Scalable or resizable window and HiDPI support
8. A simple computer opponent (minimax with alpha-beta pruning; feasible on a 4×4×4 board once
   move generation is vector-based)
9. Online two-player mode for the browser version

---

## Suggested order of work

1. Extract rules into a pygame-free module and add tests (3.1, 5)
2. Fix the gameplay gaps: checkmate/stalemate, saving the turn, promotion, reselection (1.1–1.4)
3. Add on-screen state: turn, check, game over (1.5)
4. Refactor coordinates and enums (3.2, 3.3), then data-driven moves (3.4)
5. Hygiene and CI (4, 5)
6. Features (6)
