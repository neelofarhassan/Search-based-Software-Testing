# Identifying the Strengths and Weaknesses of Automated Software Testing Techniques (supplementary material)
Automated software testing has become an active research topic in software engineering in recent years, with a variety of techniques developed by academics and industry practitioners. Although there are several comparative studies which report the effectiveness of these techniques in terms of their average performance, we still lack precise knowledge of what makes a particular testing technique effective on a given piece of software. A recent methodology called Instance Space Analysis uncovers insights into the relationship between algorithm performance and instance features, through a visual representation of the space occupied by the instances, in this case representing software programs. This paper presents an Instance Space Analysis for six widely used automated software testing techniques, on a set of 1088 Classes Under Test (CUT). To construct the instance space, we collect 78 measurable features of each CUT. Then, through feature selection and projection, we construct a two-dimensional visualization of the strengths and weaknesses of each testing technique, in the context of the instance features. Moreover, we identify similarities and differences between CUTs, providing an understanding of the level of difficulty, bias and diversity of the commonly used automated testing benchmarks. This repository contains metadata, instances and feature extraction code for the generated Instance Space.

Feature Generation:
Features are extracted using various tools and scripts
<ul>
  <li> <a href="http://gromit.iiar.pwr.wroc.pl/p_inf/ckjm/">CKJM: Object Oriented Features</a></li>
  <li> <a href="https://github.com/mauricioaniche/ck"> CK: Object Oriented and Code Features</a></li>
  <li> <a href="https://networkx.org/">Networkx: Graph Features</a>. cfgs.py (in the current repository) can be used to extract graph features using Networkx and save them in a CSV file.</li>
  <li> <a href="https://javaparser.org/">Javaparser: Class Features showing information about class modifiers, variables, operators,expressions etc. </a> </li>
 </ul>
 
 Test Suite Generation: 
 We used evosuite to generate test suite and MAJOR mutation tool for mutation testing. The script RunTestGenerationAndMutation.sh can be used for the generation of test suite using the configuration we used in our study. 
 
 
 
 
 
 
 
