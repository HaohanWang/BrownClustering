BrownClustering
===============

This is a python implementation of Brown word clustering algorithm  

USAGE:
------
There are several lines of usage under the class, in the same file.  
It is easy to use, initialize the class with dictionary path and text path.   
    
Dictionary is a file of dinstinct words, one per line.   
text is one sentence per line, should stay consistent with the words dictionary.   

In cluster method, *k* means the number of clusterers of these words   
*m* (only in faster method) means the number of initialize clusters.   

Algorithm:
------
Cluster_naive is the naive implementation of this algorithm, which requires *O(V^5)*, very unrealistic   
Cluster_fast is a faster but approximate algorithm, it first assigns the most frequence *m* words into cluster. This method requires *O(Vm^2+n)*, where *n* is the length of text.  

Reference:
------
1.	Algorithm [Brown et al, 1992](http://dl.acm.org/citation.cfm?id=176316)  
2.	Brief Introduction [PPT from Columbia](www.cs.columbia.edu/~cs4705/lectures/brown.pdf‎)   

