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
