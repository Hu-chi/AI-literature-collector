# Introduction 

I make a tool for searching literature about some topic in my area.

Common NLP Conferences:

* ACL: https://aclanthology.org/venues/acl/
* EMNLP: https://aclanthology.org/venues/emnlp/
* NAACL: https://aclanthology.org/venues/naacl/
* COLING: https://aclanthology.org/venues/coling/

Common AI Conferences:

* IJCAI: https://www.ijcai.org/past_proceedings
* AAAI: https://aaai.org/Conferences/AAAI/aaai.php
* ....



I organized the collected papers into the following format and saved them in a `year*.json` format file

```json
{
	"url": "https://ojs.aaai.org/index.php/AAAI/article/view/8117", 
	"abstract": "With the exponential increase in the number of documents available online, e.g., news articles, weblogs, scientific documents, the development of effective and efficient classification methods is needed. The performance of document classifiers critically depends, among other things, on the choice of the feature representation. The commonly used \"bag of words\" and n-gram representations can result in prohibitively high dimensional input spaces. Data mining algorithms applied to these input spaces may be intractable due to the large number of dimensions. Thus, dimensionality reduction algorithms that can process data into features fast at runtime, ideally in  constant time per feature, are greatly needed in high throughput applications, where the number of features and data points can be in the order of millions. One promising line of research to dimensionality reduction is feature clustering. We propose to combine two types of feature clustering, namely hashing and abstraction based on hierarchical agglomerative clustering, in order to take advantage of the strengths of both techniques. Experimental results on two text data sets show that the combined approach uses significantly smaller number of features and gives similar performance when compared with the \"bag of words\" and n-gram approaches.", 
	"title": "Combining Hashing and Abstraction in Sparse High Dimensional Feature Spaces"
}
```

If the abstract is not collected, it will be stored as a null value.