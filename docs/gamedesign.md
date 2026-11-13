3D table arena with wall, basic size 5x9
one laser entry point on left and one endpoint on right side.

*goals*
    put items on table to route laser beam from left to right point.

*rules*
    mirrors:
        fixed direction by default, the player can not rotate them.
        deflect the laser beam by 90 deg by default.
        4 types, one for each orientation.
    placing:
        a placed item can not be picked up again.
        exception: pick-up ability, removes one placed item from the table.
        the player has only 0-3 pick-up abilities per round.
        unused pick-up abilities give a bonus in the level result.
    item queue:
        only the top item of the queue can be placed.
        all items must be placed to finish the level.
        on later difficulty levels only the next few items are visible.
    laser:
        the laser is off by default, it is not shown continuously.
        test button: fires the laser to check the current route.
        test button presses are counted.
        failed test: the level continues, only the press counter increases.
    undo and restart:
        undo button: takes back the last move, 3 undos per level.
        undo is separate from the pick-up ability, both are available.
        restart button: restarts the level, it does not affect the level result.
    win condition:
        all items are placed and the laser beam reaches the endpoint.
        with colored lasers: every endpoint must be reached by a beam of its own color.
    lose condition:
        no more possible moves and the laser beam does not reach the endpoint.
        the laser beam hits a bomb / forbidden field.
        the countdown timer runs out.
    level result:
        base score: a countdown timer, it depends on the level and starts from 300 seconds.
        bigger levels get more time.
        the remaining seconds at the end of the level are the base score.
        each test button press costs 5 points.
        each remaining pick-up ability gives 10 points.
        each used undo costs 15 points.

*items*
    empty block.
    block item: block laser beam.
    mirror item: change laser direction to 90 deg.
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
    1. level clean table, random different entry and target block, use 2 mirror item
    2. level same as before, just add blocking block on table.
    3. increase table size on level.

*level generation*
    seed:
        every level is generated from a seed.
        the same seed always gives the same level, so a level can be replayed and shared.
    solvability:
        the generator can only output solvable levels.
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
    laser look: bloom, particles where the beam hits something.
    sounds: placing an item, laser hum on test, reaching the endpoint.
    end of level: animation and the level result screen.

*progression*
    score or stars at the end of the level, based on the level result rules.
    level select screen, saved progress, unlocks.
    tutorial: the first levels teach the items one by one.
    hint system for players who get stuck.

*technical*
    engine: Unreal Engine, made with Blueprint.
    target platform: PC desktop.
    data model: the table is a grid, the laser route is traced cell by cell on test.
    first playable version (MVP):
        rules, level generation and the 3 levels above.
        items: empty block, block item, mirror item, not movable mirror item.
    later: items for later levels, visual styles, progression.