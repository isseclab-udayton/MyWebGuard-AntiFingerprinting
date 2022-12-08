# FP-Inspector (Fingerprinting the fingerprinters)

<https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9519502>

- Machine Learning Syntactic-semantic approach to detect browser fingerprinting behaviors
  - “Static analysis helps FP-Inspector overcome the coverage issues of dynamic analysis, while dynamic analysis overcomes the inability of static analysis to handle obfuscation
  - 99% accuracy, less site breakage than other technologies
  - Find that fingerprinting has increased in recent years (written in 2021), now 10% of alexa top 100k use it
- General Thoughts while reading:
  - Machine Learning approaches often mention that their tool has unveiled new fingerprinting APIs not previously known
  - This paper and many others mention faults in prior papers evaluation/analysis strategies as their testing user base was biased
  - Seems to be known that browser fingerprints change quite frequently. But, it is also known that new fingerprints can often be linked back to others. One study found that they could track repeat visitors for up to 74 days. Persistent fingerprint tracking is necessary for it to be even worth it.
  - **Research OpenWPM, Abstract Syntax Trees for classifying malicious javascript, Supervise vs Unsupervised ML, RandomForest algorithm**
- Discovered that many fingerprinting scripts use Permissions and Performance APIs more
- Talks about prevalence of fingerprinting and what not quite well in background section
- Also define active vs passive fingerprinting
  - Active: scripts that probe for device properties such as the installed fonts
  - Passive: servers that collect information that’s readily included in web requests such as the User-Agent header.

## Design

- Detection component: extracts syntactic and semantic features from scripts and trains a machine learning classifier to detect fingerprinting scripts
- Mitigation component: applies a layered set of restrictions to the detected fingerprinting scripts to counter passive and/or active fingerprinting in the browser

### Detection

- Trains separate supervised machine learning models for static and dynamic representations and combines their output to accurately classify a script as fingerprinting or non-fingerprinting
- *Collects script contents* by extending OpenWPM’s network monitoring instrumentation. Allows them to capture both inline and external JS
- *Collects script execution* traces by extending the APIs covered by OpenWPM to include as many fingerprinting APIs as possible

### Static Analysis

- using **Abstract Syntax Trees** (ASTs) to encode scripts as a tree of syntax primitives (Variable Declaration and For Statement)
  - Nodes are keywords, identifiers, literals
  - Edges are the relationship between them
- Unpacks scripts containing eval or Function by embedding them in an empty HTML page and open in an instrumented browser allowing them to extract scripts as they are parsed
  - These are used instead of packed versions when building ASTs
- *Now generates static features using ASTs similar to how prior research uses ASTs to classify malicious JavaScript*
  - Parents represent context (if, for, try, etc.)
  - Children represent the function inside the context
  - Only considers parent-child pairs if theres a keyword that matches a name, method, or property from one of the JS APIs (reduced AST nodes to evaluate)
- Intuitively, fingerprinting script vectors have combinations of parent:child pairs that are specific to an API access pattern indicative of fingerprinting that are unlikely to occur in functional scripts
- Apply unsupervised and supervised feature selection methods to reduce number of features
  - Prune features that do no vary much
  - Short list top 1k features so those APIs that are typically used for fingerprinting are used to train a supervised machine learning model
  - Essentially reducing the number of features to examine
- Information gain can be used in decision trees to evaluate the quality of a decision split – decision trees using in supervised ML model

### Dynamic Analysis

- Helps assist where static analysis fails - obfuscation
- Extract dynamic features by monitoring the execution of scripts
  - Provides the semantic relationship between scripts
- Two approaches to extract features from execution traces
  - Presence and count of the number of times a script accesses each individual API method or property and use that as a feature
  - Build features from APIs that are passed arguments or return values
    - Don’t use arguments or return values directly
    - Instead, they use derived values to captures a higher-level semantic that is more likely to be generalized during classifications
    - Ex. Compute length and complexity of string rather than the text itself
    - Ex. Calculate the area of canvas element, text size, presence on screen when processing execution logs related to `CanvasRenderingContext2D.fillText()`
    - Idea is to not train classifier with overly specific features

### Classifying Fingerprinting Scripts

- Uses a decision tree classifier for training a machine learning model
  - Passed feature vectors of scripts for classification
- While constructing the tree, at each node the decision tree chooses the feature that most effectively splits the data, the attribute with the highest information gain is chosen

## Mitigation

Utilizes one method at a time to evaluate each methods effectiveness and usability

- **Blanket API restriction** – restrict access for all scripts to the JS APIs known to be used by fingerprinting scripts, does not rely on FP-Inspector detection
- **Targeted API restriction** – restrict access to fingerprinting APIs only from domains that are detected by FP-Inspector to deploy fingerprinting scripts
- **Request Blocking** – Block requests to download scripts served from domains that are detected to deploy fingerprinting scripts
- **Hybrid** – does not block for first-party or inline scripts. Restrict access to fingerprinting APIs for first-party and inline scripts on detected domains.

## Findings

- High site breakage >= 25% major breakage for all mitigation methods
- Found that fingerprinting is often used on news sites
