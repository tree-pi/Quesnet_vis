a short phrase, "label" appears in the visusalization. The question label should end with "?" while the answer label with ".". The followed detailed explaination won't appear as label.

**new update** 04/15/2018
1. parallel structure: between several leaf nodes from the same root and same link. This structure allows 1) "group-based" follow-ups and 2) structured expansion by combination.

To mark the parallel structure, use "_edge..." to start, "..." to mark the specific leaf nodes, and "_end" to mark the finish of the parallels.

2. "group-based" follow-ups: after the "_end", the next level question will be considered as following up the whole group of parallel nodes instead of following up the last node (should be written before "_end"). Examples include "what are the differences between the xx?".

3. a "meta-network" to express higher level logic between major types questions: in a seperate file "thesamename_meta.txt", describe the relations between major edge labels. A usual relation is "A x B", meaning every answer to quesiton A can be combined with every answer to question B.