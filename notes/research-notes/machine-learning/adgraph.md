# ADGraph: A graph-Based Approach to Ad and Tracker Blocking

<https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9152669&tag=1>

- A graph-based machine learning approach for detecting advertising and tracking resources
  - Builds a graph representation of HTML structure, network requests, and JS behavior
  - Considers the context a network request takes place in
- Domain Based Blocking
  - Prevent advertising and tracking by identifying suspect domains, and blocking all requests to resources on such domains
  - Countermeasures:
    - Fails as a result of Domain Generation Algorithms that randomize domains
    - Also circumvented by proxying the malicious resource through the first-party domain.
- JavaScript Code Unit Classification
  - Identify undesirable code based on the structure or behavior of JS code units
    - Take a single code unit as an input, train ML classifiers for identifying
  - Countermeasures:
    - Does not consider the interactions between code units, easily circumvented by dividing up code units to the smallest susceptible behavior
    - If looking at static features, such as names of cookie values, are vulnerable to obfuscation techniques
- JavaScript Attribution Approaches
  - Need to associate code units to DOM modifications. Without knowing the source of the modification, how can you block it?
  - JS Stack Walking
    - Most common
    - Interpose on the prototype chain of the methods observed, throw an exception, walk the resulting stack object to determine what code unit called the modified method.
    - Allows for runtime policy decisions
    - Faults in this Design:
      - Many cases where calling code can mask its identity from the stack, making attribution impossible
        - Eval’ed code and inlined functions by JS runtime
      - Requires that code be able to modify prototype objects, which requires the attributing code to run before any other code on the page.

## ADGraph Design

- Take the DOM tree, contextualize it by including information about execution and communication of the page
  - Edges to captures JS interactions with HTML elements, or which code unit triggered a given network request
  - Edges turn the tree into a graph
- The graph representation of a webpage tracks changes in the websites HTML structure, network requests, and JS behavior
- This Graph approach brings some benefits:
  - Cause & Content of network requests & DOM modification: the graph allows for tracing the origin of any change or behavior back to the responsible JS code unit.
  - Allows for extraction of context-rich features, which is used to identify tracking related network requests
    - Ex. Determinations of the source script sending an AJAX request, the position/depth/location of an image request, and if a subdocument was injected into a page from JS code

### Graph representation

- Nodes: All elements are 1 of 4 types of nodes
  - Parser – attributes document changes and network requests to the HTML parser, instead of script execution. Each graph has one parser node.
  - HTML – HTML elements in the page. Ex. Image tags, anchor tags, paragraph tags. Annotated with info about tag type and HTML attributes (src, class, value). Text nodes do not have a type.
  - Network – Remote resources. Annotated with type of resource being requested (subdocuments/iframes, images, XMLHTTPRequest fetches, etc.)
  - Script – Each compiled and executed body of JS code.
- Edges (Directed): The relationship between any two nodes. 3 types.
  - May have cycles
  - Structural – Relationship between two HTML elements (nodes). Inserted to represent parent-child node relationships and order of siblings.
    - HTML -> HTML
  - Modification – Creation, insertion, removal, deletion, and attribute modification of each HTML node. Notes the type of event and other info such as the attribute modified, new values, etc.
    - Script -> HTML
  - Network – Browser making request for a remote resource (network node). Annotated with the URL being requested
    - Script/HTML -> Network
- Examples:
  - Image src represented as HTML node – (Network Edge)🡪 Network node depicting the image
  - Script modifying the value of a form element
    - Script node –(Modification Edge)🡪 HTML node
    - Requires different approach to determine which script unite “owned” any given execution.

## Feature Extraction

Features that ADGraph extracts to distinguish ads and trackers from functional resources

### Structural – Features that consider the relationship between nodes and edges

Ex. Graph size, Modifications by scripts, etc.

- Whether a node’s parents have ad-related values for the class attribute, the tag names of node’s siblings, or how deeply nested in the DOM a given node is
- Also considers the interactions between JS code and the resource requested
  - Relies on chromium’s Blink and V8

### Content - Features that depend on the values and attributes of nodes in isolation from their connections

Ex. Request type, length of URL, Domain party, etc.

- Most significant value is the URL of resource requested

### Classification

Uses random forest, a well known ensemble supervised ML classification algorithm

- Combines decisions from multiple decision trees by choosing the mode of the predicted class distribution

3 categories of network requests

- Initiated by the HTML
- Initiated by a node’s attribute change
- Initiated directly by JS code

#### Most useful features in distinguishing between malicious and benign content

Structural Features

- Node’s average degree of connectivity
  - AD nodes are expected to have lower average degree of connectivity
  - Non-AD nodes are expected to have higher average degree of connectivity
  - This was found to be true ^
- Parents’ attributes
  - AD nodes are expected to be more likely to follow common practices, such as asynchronous attribute methods for ads
  - AD nodes did indeed have more async scripts

Content Features

- Domain Party
  - Expect AD nodes to be more likely to come from third-party domains than Non-AD nodes. Yes more than 90% came from third-party
- URL Length
  - Expect AD nodes to have a large number of query parameters in URLs. True on average.

### Implementation

ADGraph was implemented inside the browser, not an extension.

Implemented as an extension, using JS stack walking. This method takes a serious hit in recall.

- Blink instrumentation:
  - Instrument Blink to capture anytime a:
    - Network request is about to be sent
    - HTML node is created/modified
    - Control about to be passed to V8
  - Modified each page’s execution environment to bind the graph representation of the page to each page’s document object.
    - Allows to distinguish between scripts executing in different frames/sub-documents (difficult in prior works Section II-C)
  - Add instrumentation to allow to map between V8’s identifiers for script unites and the sources of script in the executing site (script tags, eval’ed scripts, script by extensions)
- V8 Instrumentation:
  - Add points to allow to track anytime a script is compiled, anytime control changes between script units.
    - Done by associating every function and global scope to the script they’re compiled from. Then can note every time a new scope is entered and attribute any document modifications or network requests to that script until scope is exited.
