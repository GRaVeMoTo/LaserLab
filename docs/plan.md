# Plan: working level demo

## Demo scope

Level 1, playable from start to finish:

- 5x9 table with walls
- laser entry point on the left, endpoint on the right (in a different row)
- 2 mirrors in the queue
- placing with the mouse
- Test button
- win feedback

Left out (needed for the MVP, not for the demo): scoring, countdown timer, undo, pick-up ability, seeded generator, levels 2–3, sounds, effects.

## Implementation approach

Blueprint, built through the running editor over MCP (`unreal-mcp`, `127.0.0.1:8424`). Python only for editor automation where it speeds things up (for example placing level elements); it cannot be used for game logic.

## Steps

- [x] **1. Grid and table**: a `BP_Board` actor that lays out 5x9 cells from simple cubes, with walls and markers for the entry point and the endpoint. Cell state is stored in an array (empty, block, 4 mirror types).
- [x] **2. Camera and mouse**: fixed tilted camera, highlight on the cell under the cursor.
- [x] **3. Queue and placing**: the 2 mirrors on the right side; a click places the top one on the cell; an occupied cell cannot be used.
- [x] **4. Laser trace**: on Test, the route is computed cell by cell (a mirror turns the beam 90 degrees, a block or a wall stops it) and the beam is drawn for a few seconds.
- [x] **5. Win**: if all items are placed and the beam reaches the endpoint, show "Level complete"; Restart button.
- [x] **6. Manual playthrough** in the editor, checked with a screenshot.

# Plan: MVP

## MVP scope

From the design doc: the rules, level generation and levels 1–3, with the items empty block, block item, mirror item and not movable mirror item.

## Decision: mirror types

The game has both one-sided and two-sided mirrors.

- **One-sided mirror**: 4 types, one for each orientation. The front side deflects the beam by 90 degrees, the back side stops it like a block.
- **Two-sided mirror**: 2 types, one for each diagonal. Both sides deflect the beam by 90 degrees.

The demo only has two-sided behaviour: its 4 mirror states act as 2 pairs (NE = SW, NW = SE). The MVP splits these into 4 one-sided states and 2 two-sided states.

## Steps

- [x] **1. Mirror types**: extend the cell state with 4 one-sided and 2 two-sided mirrors, update the laser trace (back side of a one-sided mirror stops the beam) and give the two kinds a visibly different shape.
- [x] **2. Level data and generator**: a level (table size, entry point, endpoint, blocks, queue) is generated from a seed instead of the hardcoded values. The generator only outputs solvable levels, and the same seed always gives the same level.
- [x] **3. Missing items**: block item on the table and not movable mirror item.
- [x] **4. Levels 2 and 3, level flow**: level 2 adds blocking blocks, level 3 has a bigger table; after a win the next level starts.
- [x] **5. Rules**: undo (3 per level), pick-up ability (0–3 per round), test press counter, countdown timer, lose conditions (timer runs out, no more possible moves). Replace the 3D buttons and labels with a screen UI first, because the counters and the timer need it.
- [x] **6. Scoring and level result screen**: remaining seconds as base score, minus 5 per test press, plus 10 per unused pick-up ability, minus 15 per used undo.
- [ ] **7. Playthrough of levels 1–3** in the editor, checked with screenshots.

# Plan: jam submission

Deadline: November 15, 2026. Requirements are in `submit.md`.

## Scope

A packaged Windows build on itch.io with sounds and a basic look. Left out: items for later levels, level select, saved progress, tutorial, hint system.

## Steps

- [ ] **1. First package**: Windows development build, started outside the editor, levels 1–3 playable. Done first, so packaging problems show up early.
- [x] **2. Sounds**: placing an item, laser hum on test, reaching the endpoint; menu music on the setup screen, two tracks that take turns during the run.
- [x] **3. Look**: models and materials for the table, walls, mirrors, blocks, entry point and endpoint, in place of the simple cubes.
- [ ] **4. Laser effects**: bloom on the beam, particles where the beam hits something.
- [ ] **5. End of level animation** before the level result screen.
- [ ] **6. Final package**: rebuild, play through levels 1–3 in the build, zip as `TeamName_GameName`, under 1 GB.
- [ ] **7. Gameplay video**: 30–60 seconds, uploaded, link ready.
- [ ] **8. itch.io page and submission**: upload the zip to the own itch.io account and submit to the jam with the team name, each member's name and Epic Games account email, the game name, the video link and the list of tools used (needed for partner prizes).

# Plan: timed run

Design change: the game is a timed run. The player sets a start seed and a time limit, and finishes as many levels as possible before the time runs out.

## Steps

- [x] **1. Run setup screen**: start seed (1–999) and time limit (1–60 minutes, default 5) on a panel before the start, each with a slider and a number field that can be typed into; the Start button begins the run.
- [x] **2. Run timer**: one countdown through the whole run instead of a timer per level; when it runs out, the run ends.
- [x] **3. Level series**: level seed derived from the start seed and the level number; the table starts at 3x5 and grows every two levels (5x7, 5x9, 7x11), with more blocks on later levels; no last level.
- [x] **4. Tests and win**: automatic test when the last item is placed (not counted); a successful test finishes the level even with items left in the queue; the next level starts after a short pause.
- [x] **5. Undo cost**: each undo takes 5 seconds off the timer.
- [x] **6. Stuck level and run result**: a stuck level shows a restart message instead of ending the game; the run result screen shows seed, time limit, tests, undos and finished levels, with a New run button.
- [ ] **7. Manual playthrough with the mouse**: seed and time fields, Start and New run buttons clicked by hand.
