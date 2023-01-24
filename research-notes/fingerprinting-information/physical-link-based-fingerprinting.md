# My Site Knows Where You Are: A Novel Browser Fingerprint to Track User Position

[Paper](https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=9500556)
[Github](https://github.com/1362860831/PingLoc)

# Overview

Instead of relying on browser information, this fingerprinting method relies on the time it takes for image requests to be fulfilled. Based on this time it takes for the information to physically travel, they are able to infer a user's geographical position.

# Notes

- Image resource requests does not adhere to the SOP (Same Origin Policy) or CORS (Cross-Origin Resource Sharing)
- Time delay is calculated by capuring the onerror event
- IMPORTANT: Leverages scripts to collect the user's time delay information

# How it works

- Timestamp is used as the _relative path_ of the image resources
  - Different paths are generated each time, and there is no such image resource path named by the timestamp
  - Thus, the website always returns an error, and time of delay can be obtained by catching the onerror evernts
- The time delay to 11 well-know websites is collected

# Side Notes - Regarding info not in paper

- Appears that HTML5 Application Cache allows web apps to cache same-origin and cross-origin resources in the local storage of a browser to enable offline access
  - Possible mitigation apporoach? This seems to be used for attacks... [Link](https://hpc.postech.ac.kr/~hyungsubkim/papers/ndss15_final.pdf) this paper describes the new attack, and also coutnermeasures - "URL status identification attack"
  - Also this new attack opens up "internal web server probing" which allows an attacker to identify networked devices on the user's network.
