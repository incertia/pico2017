# TW1

We need to pick up the flag with `check == 64`, so we look at the script that
generates flags to figure out which one has `idx == check == 64`.

# TW2

If an enemy is within 3 units, it will always move in a direction. If there is
no better move, it will move to the right.

# TW3

Item IDs are generated per floor with respect to how many items are currently on
the floor. Item pickup picks up all items with the same ID on the current floor.
Resort items will renumber the item IDs you currently have with respect to the
order in the script. We pick up items one by one and renumber them so that `id =
0`. This allows us to pick up more than eight items at a time. Once we have more
than thirteen items in our inventory, we can resort again to make something with
`id == 12`, allowing us to pick up our flag remotely.

# TW4

socket.io event handlers run asynchronously. If we launch multiple
`socket.on("action")` handlers and travel onto the stairs, it will increment our
floor number multiple times and hopefully set our game state to floor 5. We can
spam movements via some simple javascript.

    for (i = 0; i < 10; i++) {
        socket.emit("action", {type: "move", direction: 4});
    }
