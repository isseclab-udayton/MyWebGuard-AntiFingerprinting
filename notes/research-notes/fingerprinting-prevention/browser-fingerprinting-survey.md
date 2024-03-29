# Browser Fingerprinting: A Survey

<https://dl.acm.org/doi/pdf/10.1145/3386040>

Analyzes current fingerprinting techniques being used and categorize defense solutions, considers some challenges

Focuses on information given by a web browser, nothing else

## Outline

Section 2: Evolution of web pages

Section 3: Work done in domain (survey)

Section 4: Different mitigation approaches

Section 5: Usage of technique and challenges in research/industry

## Section 3

- Canvas, WebGL, AudioContext: differences in hardware and software configurations present differences in the processing, which results in a unique fingerprint.
- Discusses entropy which is used to measure the effectiveness of a fingerprinting method
- Challenges:
  - Very difficult to classify scripts correctly as the goal of two scripts can vastly vary even if they present very similar content
  - Cross-browser fingerprinting is possible by collecting enough data from the OS and hardware layers
  - Telltale signs that indicate possible fingerprinting activities:
    - Accessing specific functions: those that return device specific information
    - Collecting a large quantity of device-specific information
    - Performing numerous access to the same object or value
    - Storing values in a single object
    - Hashing values: used to ease processing
    - Creating an ID: does the script appear to make an id and store it for later access?
    - Sending info to a remote server?
    - Minification and obfuscation?
- Defense Techniques:
  - Spoofing leads to problems, you have to change all values to properly spoof (no mismatched values), some spoofed values may just not make sense.
  - Introducing noise:
    - Most attributes are collected as strings, which is easy to spoof/replace
    - Canvas and AudioContext yield more complex data structures
      - Og image is shown to user, when the image is read then it is modified. This means that only the call to read the image gets the spoofed stuff.
  - Homogenization works in practice, however slightly deviating from these “normal values” then you will be easily fingerprintable maybe more than normal.
  - Firefox and Tor work together. Currently they:
    - Block canvas api, normalize user-agent, timezone and screen resolution
- Challenges & Implications of Fingerprinting:
  - Because of the hardware and software information fingerprinting provides, they can be used to identify potential security vulnerabilities. Ex. Known to be running an outdated plugin.
