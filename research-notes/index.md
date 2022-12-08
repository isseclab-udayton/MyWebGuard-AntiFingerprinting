# Index of Research

## Paper Links

- Browser Fingerprinting from Course Traffic Summaries: Techniques and Implications <https://link.springer.com/content/pdf/10.1007/978-3-642-02918-9_10.pdf>
- An Empirical Evaluation of Web-Based Fingerprinting: <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7106402>
  A. F. Khademi, M. Zulkernine and K. Weldemariam, "An Empirical Evaluation of Web-Based Fingerprinting," in IEEE Software, vol. 32, no. 4, pp. 46-52, July-Aug. 2015, doi: 10.1109/MS.2015.77.
- Pixel Perfect: Fingerprinting Canvas in HTML5 <https://hovav.net/ucsd/dist/canvas.pdf>
- Mitigating browser fingerprint tracking: multi-level reconfiguration and diversification <https://hal.inria.fr/hal-01121108/document>
- Evaluating Anti-Fingerprinting Privacy Enhancing Technologies <https://dl.acm.org/doi/pdf/10.1145/3308558.3313703> a hybrid between observational and experimental data collection- uses FPInspector and another
- Fingerprinting the Fingerprinters: Learning to Detect Browser Fingerprinting Behaviors <https://ieeexplore.ieee.org/document/9519502>
- Browser fingerprinting: A survey <https://dl.acm.org/doi/pdf/10.1145/3386040>
- A Defense against JavaScript Object-Based Fingerprinting and Passive Fingerprinting <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9885716>
- FPDetective: Dusting the Web for Fingerprinters <https://dl.acm.org/doi/pdf/10.1145/2508859.2516674>
- How Unique Is Your Web Browser? <https://coveryourtracks.eff.org/static/browser-uniqueness.pdf> Referenced by many, seems to have an outdated data on effectiveness of fingerprinters
- AdGraph: A Graph-Based Approach to Ad and Tracker Blocking <https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9152669&tag=1>
- JStrong: Malicious JavaScript detection based on code semantic representation and graph neural network <https://doi.org/10.1016/j.cose.2022.102715>
- Deobfuscation, unpacking, and decoding of obfuscated malicious JavaScript for machine learning models detection performance improvement <https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/trit.2020.0026>
- JaSt: Fully Syntactic Detection of Malicious (Obfuscated) JavaScript <https://link.springer.com/content/pdf/10.1007/978-3-319-93411-2_14.pdf>
- JStap: a static pre-filter for malicious JavaScript detection <https://dl.acm.org/doi/10.1145/3359789.3359813>
- Morellian Analysis for Browsers (canvas fingerprinting done ethically) <https://link.springer.com/content/pdf/10.1007/978-3-030-22038-9_3.pdf>

## Testing Tools

Should use these to test implementation

- <https://coveryourtracks.eff.org/>
- <https://amiunique.org/>

## General Thoughts

- Should test effectiveness with testing tools and test site breakage as well
- Concept: users collectively identify unsafe data elements and report them to server. Server then considers all values from all users and if its all the same then it is considered safe.
  - Maybe dynamically create policies based on the values of many users?
- Idea: build a whitelist
  - Start by approving the original domain i.e. newyorktimes itself
  - Observe how other third party domains behave and if its not suspicious, then approve it.
  - Allows for strict rules for newer, not seen api’s but relaxed on well known ones
  - Perhaps a server to compare to other users stuff
- Option to pause blocking as banking/transaction companies use fingerprints in a good way
- Since balancing between security and usability can be difficult, perhaps there could be a “whats wrong with this web page” button where you can say “pictures not working” or “animations not working”.
