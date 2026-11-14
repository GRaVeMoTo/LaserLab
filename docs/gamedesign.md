3D table arena with wall, starting size 3 rows x 5 columns
one laser entry point on left and one endpoint on right side.

*goals*
    put items on table to route laser beam from left to right point.
    finish as many levels as possible before the time limit runs out.

*run*
    setup before the start:
        start seed: a number from 1 to 999.
        time limit: 1 to 60 minutes, 5 by default.
        both can be set with a slider or typed as a number.
    one countdown timer runs through the whole run, it does not reset between levels.
    the levels of a run are generated from the start seed, the same seed gives the same series of levels.
    the first level has a 3 rows x 5 columns table, later levels grow by the difficulty curve.
    a finished level is followed by the next level right away.
    the run ends when the countdown timer runs out.

*rules*
    mirrors:
        fixed direction by default, the player can not rotate them.
        deflect the laser beam by 90 deg by default.
        one-sided mirror: 4 types, one for each orientation.
            the front side deflects the beam, the back side stops it like a block.
        two-sided mirror: 2 types, one for each diagonal.
            both sides deflect the beam.
    placing:
        a placed item can not be picked up again.
        exception: pick-up ability, removes one placed item from the table.
        the player has only 0-3 pick-up abilities per round.
    item queue:
        only the top item of the queue can be placed.
        not all items have to be placed, a successful test finishes the level.
        on later difficulty levels only the next few items are visible.
    laser:
        the laser is off by default, it is not shown continuously.
        test button: fires the laser to check the current route, at any time.
        automatic test: when the last item of the queue is placed, the test starts by itself.
        test button presses are counted, automatic tests are not.
        failed test: the level continues.
    undo and restart:
        undo button: takes back the last move, 3 undos per level.
        each undo takes 5 seconds off the countdown timer.
        undo is separate from the pick-up ability, both are available.
        restart button: restarts the level, the countdown timer keeps running.
    win condition:
        a test where the laser beam reaches the endpoint, even if not all items are placed.
        with colored lasers: every endpoint must be reached by a beam of its own color.
    stuck level:
        no more possible moves and the laser beam does not reach the endpoint.
        the laser beam hits a bomb / forbidden field.
        the player has to restart the level, the countdown timer keeps running.
    run result:
        the number of levels finished before the countdown timer runs out.
        shown at the end of the run with the start seed, the time limit, the test button presses and the used undos.
    quit menu:
        Esc opens a "Quit the game?" dialog with Yes and No, at any time.
        while it is open the countdown timer stops and the table takes no input.
        Yes quits the game; No or Esc again closes the dialog and the run continues.

*items*
    empty block.
    block item: block laser beam.
    mirror item: change laser direction to 90 deg, one-sided or two-sided.
    not movable mirror item.

*items for later levels*
    beam splitter: splits one beam into two, used with more than one endpoint.
    prism / color filter: changes the laser color, endpoints can require a given color.
    colored lasers: a level can have more colored endpoints and more colored entry points.
    checkpoint: the beam must pass through it before reaching the endpoint.
    teleport pair: the beam enters one and continues from the other.
    rotating or moving mirror: changes direction or position during the level.
    glass block: lets the beam through, but no item can be placed on it.
    bomb / forbidden field: if the beam hits it, the level is lost immediately and the whole level must be restarted.

*levels*
    items queue on right side of the table
    1. level 3x5 table with a few blocking blocks, random different entry and target block, use 2 mirror item
    2. level same as before, with one more blocking block.
    3. increase table size on level, two mirrors are already fixed on the table.
    later levels: keep growing by the difficulty curve until the time runs out.

*level generation*
    seed:
        every level is generated from a seed, derived from the start seed and the level number.
        the same seed always gives the same level, so a level can be replayed and shared.
    solvability:
        the generator can only output solvable levels.
    variety:
        the mirrors of a level are a random mix of one-sided and two-sided mirrors.
        the mirrors in the queue are never all the same kind, at least two kinds are present.
        the entry row and the exit row are both different from the rows of the previous level.
    blocking blocks:
        about one sixth of the cells, plus one more with every level, at most one third of the cells.
        blocks never stand on the route of the solution.
    difficulty curve, what grows level by level:
        table size.
        number of blocking blocks.
        number of mirrors needed.

*controls and camera*
    input: mouse.
    actions: place the top item of the queue, use pick-up ability, undo, restart, test.
    camera: tilted 3D view, with limited camera movement up-down and sideways.
    the grid cell under the cursor is highlighted before placing.

*feedback and style*
    visual style: can change level by level, neon, sci-fi or lab.
    colors: dark lab look, only the laser and the important items glow.
        background near-black navy #0B1020, panels and table dark slate #1A2338, text off-white #E6EDF7.
        cyan #22D3EE for the interface: buttons, sliders, highlighted cell.
        red #FF2D2D only for the laser beam.
        amber #FBBF24 entry point, green #34D399 endpoint.
        mirrors cold silver #C8D3E0, no glow; one-sided and two-sided mirrors differ by shape.
    countdown: shown in 3D as mm:ss on the five middle cubes of the far wall, one character per cube.
    laser look: bloom, particles where the beam hits something.
    sounds: placing an item, laser hum on test, reaching the endpoint.
    end of level: a 5 second animation, then the next level.
        the beam turns green, after a second the items shrink and sink into the floor.
        the countdown timer stops during the animation.
    start of level: the blocks and fixed items rise out of the floor.
    end of run: the run result screen.

*progression*
    best run result per start seed and time limit.
    level select screen, saved progress, unlocks.
    tutorial: the first levels teach the items one by one.
    hint system for players who get stuck.

*technical*
    engine: Unreal Engine, made with Blueprint.
    target platform: PC desktop.
    data model: the table is a grid, the laser route is traced cell by cell on test.
    first playable version (MVP):
        rules, run setup, level generation and the levels above.
        items: empty block, block item, mirror item, not movable mirror item.
    later: items for later levels, visual styles, progression.