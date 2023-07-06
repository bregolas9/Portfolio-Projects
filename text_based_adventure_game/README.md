# Text-based Adventure Game

[![codecov](https://codecov.io/gh/th3oth3rjak3/text_based_adventure_game/branch/main/graph/badge.svg?token=HYTV9F5IRI)](https://codecov.io/gh/th3oth3rjak3/text_based_adventure_game)

Write an adventure-style game, complete with text parser, understanding a number of simple phrases.

In this project, you'll be writing a game modeled from classic text adventures like the original Colossal Cave Adventure, Zork, Anchorhead, and many others. This genre of gaming is sometimes called Interactive Fiction. This project involves text parsing, language processing, and storytelling.

Note: This type of engagement can be expanded fairly easily for a variety of purposes. For instance, imagine a text-based game to drive tourism, introduce a rock band, or for education, etc.

Note: Awesome and original ascii art will probably earn your team extra-credit!

## Objectives

The setting, style, and objective of the game are up to you, but the final project must satisfy the following requirements:

## Game Details

### Rooms

- Your game must have at least 10 "rooms" (beach, basement, dungeon cell, cyberspace virtual reality area, plane of existence, etc.).
- Each room must have at least two "features" that can be examined (a fish on the ground, lightning bolts in the sky, a wooden chair, a smoky smell, etc.).

### Room descriptions

- When you go into a room for the first time, the game must print a long-form description of the room (a paragraph, say).
- When entering the room at a later time, a short-form description should be used instead. This takes up less space then repeating the entire long-form description when you move back to that room.
- You can also have additional explanations after the long or short-form description that talk about something that happens to occur while you're there (e.g. "A train whistle sounds across the lonely field").
- Exits from a room must be described in both the short-form and long-form descriptions, and should include a direction. For example: "There is a dank-smelling staircase, descending into the dark, at the end of the hall on the north wall", or "I can see clouds to the east and west that I think I can jump to from here".

### Objects

- There must be at least 8 objects that you can acquire to your player inventory that have an effect on the game (e.g. a lamp that allows you to proceed safely down a dark corridor, a key that unlocks a car trunk, etc.).
- These objects must be droppable in any room and should stay there, to perhaps be picked up later. Note that this can be overridden fictionally for some areas: lava-filled rooms for example may not allow the player to drop objects, or dropping crumbs of bread in a garden might cause them to be eaten or moved by birds, and thus changed the next time you come through.
- Consider having some verbs (see below) combine or affect features and/or items ("use key on lock", "spread butter on toast", "put gem on staff", etc.).

### Verbs

- Your game must support an action vocabulary space (verbs) of at least ten primary actions (hit, pull, go, eat, etc.). These verbs must allow interaction with each feature in each room (a generic "you can't eat that" type of message is OK to use with some verbs).
- Some verbs must cause the player to move between rooms.
- In addition to the other 10 action verbs, the following verbs and phrases MUST also be supported - no exceptions:
  - look :: repeats the long form explanation of the room.
  - look at :: gives a fictionally interesting explanation of the feature or object. You should be able to "look at" objects in your inventory, as well. If you describe something in your text descriptions, you should be able to "look at" it to examine it.
  - "go north" OR "north" OR "go dank-smelling staircase" OR "dank-smelling staircase" :: proceed through the indicated exit to the next room (note that ALL FOUR of these forms of movement are required, and thus require you to describe the exits appropriately). You might also decide to implement other room-travel verbs such as "jump north" as appropriate.
  - take :: acquire an object, putting it into your inventory.
  - help :: list a set of verbs the game understands. You do not have to list all of the verbs your game understands, in case you want to keep some fictionally hidden ("fly up" [the player didn't realize he had wings the entire time], "think about french fries", "polymorph into toaster", etc.).
  - inventory :: Lists the contents of your inventory.

### Other Considerations

- Spend time coming up with a natural language parser that is able to handle prepositions such as "about", "on", "onto" "above", and "into". Having this kind of extended parser really makes the world come alive, but will require some time.
- You should include aliases for common verbs. For example allow "grab" and "pick up" to do the same thing as "take" (but you still must implement "take").
- You must implement a save system using these two verbs:
  - savegame :: saves the state of the game to a file.
  - loadgame :: confirms with the user that this really is desired, then loads the game state from the file.
- You must submit a step-by-step solution key (a cheat sheet) with the game, which I will use to play your entire game with!
- Feel free to include simple ASCII-only graphical enhancements and embellishments, if you like, but they are not required. If you do, make sure you're completing all other requirements first.

## Technology Requirements

Your project must compile and run on the OSU server flip.engr.oregonstate.edu without any installation of additional software or libraries.
Data about the game must be loaded from individual data files (i.e. you can't just hard code all of the data into the executable); in particular, each room must reside in its own file (consider a json structure).
If your game requires a minimum width and height in characters, inform the user when the game is started; exit the game if the minimums are not met upon game load.

## Making a Better Adventure

Here's a tip that will add depth to your game, making it be something that people will actually want to play with: not all features in a room have to be described in the initial long or short form descriptions. This means that after you look at a feature, you may learn about NEW features you can examine next. For examine, looking at a door may tell you about its keyhole. Looking at the key hole may show you that a sliver of iron is in it. From then on (until you take it), the short form of the room description might change to now list the sliver of iron in it to help remind the player he or she should do something about it. Kicking the door might alternatively shake loose a door hinge pin. Each feature in the room can be its own set-piece mini game. Consider noticeably changing your descriptions as various circumstances occur, and giving hints as appropriate to guide the player. Also, use of ASCII color codes can really make your game pop!
