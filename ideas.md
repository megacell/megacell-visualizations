Visualization Ideas
-------------------

* Without solver output
    1. Link flow map
    2. Cell voronoi diagram
    3. True route flows
        - Between OD pairs (not very good for interaction since some OD pairs
          have very few routes)
        - From a single origin
    4. Cellpath flows (select cells and find routes that passes through it)
* With Solver output
    1. Inferred route flows
    2. Route flow errors (|x - x_true|)
    3. Link flow errors (|Ax - b|)
    4. Link closure: close off a link and see percentage of commuters in each
       TAZ affected (this can be done without solver output too)


Feedback
--------
Display UE and inference.
delta maps (link flows from matsim/solver/UE inference)


1. First visualization shown for routes between two cells
-> have revised geometry for the TAZ

2. Second visualization shown: all routes emerging from an Origin
- generate quantitative plots containing (color coding, why is there only 40 ODs? etc.)

3. Work with Alexei and Andrew to generate a movie for agents in L.A. based on MATSIM
