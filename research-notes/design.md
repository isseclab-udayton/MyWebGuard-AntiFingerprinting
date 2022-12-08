# Our Design Ideas

## Static Analysis

Abstract Search Trees (ASTs) are commonly used to classify JavaScript as malicious or benign. ASTs encode
scripts as a tree of syntax primitives. A static analysis of present JavaScript code has been proven to be
effective to identify the presence of fingerprinting with a high degree of accuracy.

![AbstractSyntaxTree-Wikipedia](https://i.ibb.co/0GJK7B8/1200px-Abstract-syntax-tree-for-Euclidean-algorithm-svg.png)

- Generate Abstract Search Trees
  - How...?
  - Must unpack packed scripts by embedding them in an empty HTML page using instrumented browser, allows to extract scripts as they're parsed
- Consider parent-child pairs that are indicative of Fingerprinting
  - Intuitively, fingerprinting script vectors have combinations of parent:child pairs that are specific to an API access pattern indicative of fingerprinting that are unlikely to occur in functional script
  - Only considers parent-child pairs if theres a keyword that matches a name, method, or property from one of the JS APIs (reduced AST nodes to evaluate)

## Dynamic Analysis

Obfuscation techniques are commonly used on malicious JavaScript as a concealment method. Static analysis
methods are often ineffective for classifying obfuscated JavaScript. Dynamic analysis helps overcome this
weakness of Static analysis. Here dynamic features are extracted by monitoring the execution of scripts.

- Monitor the presence and count of the number of times a script accesses each individual API method or property
  - Use MyWebGuard
- Build features from APIs that are passed arguments or return values (FPInspector)
  - Need clarification here...
  
### System Design Flow Chart
![FlowChartPolicy](https://i.ibb.co/DMvYFVR/mywebguard-Flow-Chart.png)

## Classification

Combine static and dynamic analysis results. Use Random Forest a decision tree classifier.

## Mitigation

Targeted API restriction has the least major website breakage. Idea is to restrict access to fingerprinting
APIs (canvas, webGL, etc.) from domains detected to use fingerprinting scripts.

# Next Steps
- Whitelist trusted sites to avoid site breakage from canvas poisoning
- orginAllowed could be included to strengthen policy - check the orgin of the code including the canvas element
