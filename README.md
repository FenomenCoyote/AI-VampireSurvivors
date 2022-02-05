# AI-VampireSurvivors

Finite-State-Machine Based AI created for "Vampire Survivors" Steam game. The AI takes screenshots of the game, and by changing the game sprites, it's able to know where the enemies are, choose the correct items, and go towards experience. It interprets the data by making "pie slices" around the player and counting the pixels color. (You need to replace some game resources with the AI, single color assets)

It currently runs at 18 frames per second, taking the most of the frame time the screenshot. Most of the times the AI sleeps for 10% of the frame, but sometimes it drops and lags a frame. 

This AI can be easily improved, perhaps by including pathfinding to the safest / more rewarding area instead of doing a pie-slice observations, perhaps by emulating player's input by making a case base reasoning (cbr) sort of AI. Enemies are still all the same to the AI, not differencing elites from normal or their movement speed to try predicting the next state.

It all would be much easier if the AI had access to the game itself and all the enemies positions. The game would of course look much prettier, but at the same time its always kind of stimulating to create an AI which only input is a visual input and perhaps the game sound stream. Now to do all of that in 16 - 50 ms is pretty hardcore.

This AI-project was created for fun and perhaps some day I take the challenge again, perhaps in a faster environment than python.
