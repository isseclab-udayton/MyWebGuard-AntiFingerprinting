# My Site Knows Where You Are: A Novel Browser Fingerprint to Track User Position

[Paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9500556)
[Github](https://github.com/1362860831/PingLoc)

### Notes on Navigating Github Repo

- ping.js contains the main functionality
- index.html appears to be a home page for testing PingLoc, it references each .html file of which each performs a ping.
- .html files are there to ping specific websites (I believe its the 11 discussed in the paper)
- Note sure what Address.html does...

# Overview

Instead of relying on browser information, this fingerprinting method relies on the time it takes for image requests to be fulfilled. Based on this time it takes for the information to physically travel, they are able to infer a user's geographical position.

# Notes

- Image resource requests does not adhere to the SOP (Same Origin Policy) or CORS (Cross-Origin Resource Sharing)
- Time delay is calculated by capuring the onerror event
- IMPORTANT: Leverages scripts to collect the user's time delay information
- A "Cross-domain resource request scheme to obtain link-state information"
  - Browsers request picture resources to third-party sites, which is not restricted by SOP or CORS
- Timestamp is used as the _relative path_ of the image resources
  - Different paths are generated each time, and there is no such image resource path named by the timestamp
  - Thus, the website always returns an error, and time of delay can be obtained by catching the onerror evernts
- The time delay to 11 well-know websites is collected
- IMPORTANT: The ping() core method is called every 800ms for each webpage. This must be what they refer to as the optimal "window" which
  they fail to clarify as a unit of time or not...

# How it works

1. Browser Sampling: PingLoc uses scripts to collect time delay information, sending it back to a server.

- Time of delay calculated by catching the onerror events.
- Time of delay collected from 11 sites

2. Server Data Processing: Server performs data preprocessing and passes data to learning algorithms.

- Must account for packet loss. They estimate 3% packet loss.
- Must account for extreme values due to network noise.

3. Feature Extraction:

- An appropriate window size must be used to extract features.

4. Model Training:

- Models Used: Support Vector Machine, Decision Tee, Bayes classifier, K-Nearest-Neighbor, and Random Forest

# About the "URL Status Identification Attack" - Another paper but related

- Appears that HTML5 Application Cache allows web apps to cache same-origin and cross-origin resources in the local storage of a browser to enable offline access
  - Possible mitigation apporoach? This seems to be used for attacks... [Link](https://hpc.postech.ac.kr/~hyungsubkim/papers/ndss15_final.pdf) this paper describes the new attack, and also coutnermeasures - "URL status identification attack"
  - Also this new attack opens up "internal web server probing" which allows an attacker to identify networked devices on the user's network.
