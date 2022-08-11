# Single-Agent-Search

This repository implements 6 single-agent search algorithms. 
The program will be called with python3.9 using:

 `python3 main.py <search-type> <init-file>`

where `<search-type>` might be one of the following:
<ul>
  <li>DFS</li>
  <li>BFS</li>
  <li>UCS</li>
  <li>GS</li>
  <li>A*1</li>
  <li>A*2</li>
</ul>

`<init-file>` will be a text file gives all details related to the initial environment.
An example environment can be found in init.txt.

## Introduction to the Environment:

The environment is as follows:
<ul>
  <li>The environment is NxM grid world</li>
  <li>Each grid in the environment might contain</li>
  <ul>
    <li>Vacuum cleaner (our agent)</li>
    <li>Obstacles that avoid entering to that grid. There is not dirt in the obstacle with grid</li>
    <li>Jumper” which moves the agent that moves an incoming agent to the next grid (if the next grid does not
contain an obstacle). For example, an agent coming from left to a jumper grid is transformed to the grid on the
right. An agent coming from up is transformed to the grid down.</li>
  </ul>
  <li> The vacuum cleaner has five actions:
  <ul>
    <li>left, right, up, down moves the cleaner one grid, unless that grid is an obstacle</li>
    <li>suck action that sucks one dirt. (in order to clean n dirts in a grid, suck action should be executed n times)</li>
  </ul>
  <li>Costs of the actions:
  <ul>
  <li>Left and right: 1</li>
  <li>Up and down: 2</li>
  <li>Suck: 5</li>
</ul>
</ul>

The Environment will be represented as textfile, where
<ul>
  <li>x corresponds to obstacles</li>
  <li>c corresponds to the vacuum-cleaner</li>
  <li>digits corresponds to the number of dirts in the corresponding grid</li>
 <li>j corresponds to the jumper
</ul>


