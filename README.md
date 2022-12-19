# Instance Space Analysis of Search-Based Software Testing

Search-based software testing (SBST) is now a mature area, with numerous techniques developed to tackle the challenging task of software testing. SBST techniques have shown promising results and have been successfully applied in the industry to automatically generate test cases for large and complex software systems. Their effectiveness, however, has been shown to be problem dependent. In this paper, we revisit the problem of objective performance evaluation of SBST techniques in light of recent methodological advances – in the form of Instance Space Analysis (ISA) – enabling the strengths and weaknesses of SBST techniques to be visualised and assessed across the broadest possible space of problem instances (software classes) from common
benchmark datasets. We identify features of SBST problems that explain why a particular instance is hard for an SBST technique, reveal areas of hard and easy problems in the instance space of existing benchmark datasets, and identify the strengths and weaknesses of state-of-the-art SBST techniques. In addition, we examine the diversity and quality of common benchmark datasets used in experimental evaluations.

This repository contains code and data used in this study. 

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
 
 Metadata: 
 metadata.csv contains the feature vector for each test case along with its coverage. This is the main dataset used in the current study to find impact of each feature on the performance of test generation algorithms. 
 
The evaluation results of our study are available at https://matilda.unimelb.edu.au/matilda/problems/sbse/ast#ast

 
 
 
 
 
 
 
