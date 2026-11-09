# 3D Chess (4×4×4)

A two-player chess variant played on four stacked 4×4 boards, written in Python with
[pygame](https://www.pygame.org/). It started as a university homework project ("Nagyházi").

![Pieces](babuk.png)

## Running

```bash
pip install -r requirements.txt
python main.py
```

Needs Python 3.8+ and pygame 2.5+.

## How to play

- White moves first. Players take turns.
- Click one of your pieces to select it. The squares it can move to light up red,
  and the selected piece lights up green.
- Click a highlighted square to move there. Click anywhere else to cancel the selection.
- Moves that would leave your own king in check aren't allowed.
- The button in the top-right corner starts a new game.
- The game is saved to `mentes.txt` when you close the window and loaded on the next start.

## Files

| File | What it does |
| --- | --- |
| `main.py` | Entry point |
| `fuggvenyek.py` | Drawing, mouse input and the main game loop |
| `osztalyok.py` | `Babu` (piece) and `Palya` (board) classes, movement rules |
| `fajlkezeles.py` | Saving and loading the game |
| `Kepek/` | Piece images |
| `Extra/` | Original user and developer documentation (Hungarian) |
