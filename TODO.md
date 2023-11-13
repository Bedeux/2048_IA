# TODO 

These are the tasks I plan to continue if I return to the project in the future.

## Different reward strategies as the game and states progresses

* Explore different reward strategies based on the game's early stages. Should the approach differ at the beginning of the game or if, for instance, the largest tile is in the middle ? 
* Optimize best weights in function of parameter (largest tile > 1024, empty cells number,...)

## Reward Ideas

* When the first row is complete, encourage cells to converge to the other side of the row.
* Negative reward : Count the number of dead cells (impossible to displace) in a corner surrounded by much larger cells.

## Communication

* Create videos of the AI on the 2048 (-> add to README.md)
* Next step : Create a website to show videos of AI playing the game (1v1 against human ?)