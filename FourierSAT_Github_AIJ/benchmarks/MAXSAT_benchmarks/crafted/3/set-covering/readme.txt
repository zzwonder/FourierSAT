Here you may find Unicost Set Covering instances converted into maxSAT. The original instances from which the conversion was performed can be found in Beasley's OR library [1]: http://people.brunel.ac.uk/~mastjjb/jeb/orlib/scpinfo.html

For the unicost set covering problem, the usage of hard clauses can be avoided and therefore we chose to model them as ordinary maxsat rather than partial maxsat (although partial maxsat can also be used). 

A solution to a maxsat instance with cost X can be directly converted to a solution for the set covering problem at hand with cost X.

There are many papers that consider these instances, both unicost and nonunicost set covering. As an example, see [2]. 

If you have any questions of comments, do not hesitate to contact us:

Emir Demirović - demirovic@dbai.tuwien.ac.at
Nysret Musliu - musliu@dbai.tuwien.ac.at

[1] Beasley, John E. "OR-Library: distributing test problems by electronic mail." Journal of the operational research society (1990): 1069-1072.

[2] Naji-Azimi, Zahra, Paolo Toth, and Laura Galli. "An electromagnetism metaheuristic for the unicost set covering problem." European Journal of Operational Research 205.2 (2010): 290-300.