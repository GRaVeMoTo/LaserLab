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
- [ ] **2. Camera and mouse**: fixed tilted camera, highlight on the cell under the cursor.
- [ ] **3. Queue and placing**: the 2 mirrors on the right side; a click places the top one on the cell; an occupied cell cannot be used.
- [ ] **4. Laser trace**: on Test, the route is computed cell by cell (a mirror turns the beam 90 degrees, a block or a wall stops it) and the beam is drawn for a few seconds.
- [ ] **5. Win**: if all items are placed and the beam reaches the endpoint, show "Level complete"; Restart button.
- [ ] **6. Manual playthrough** in the editor, checked with a screenshot.
