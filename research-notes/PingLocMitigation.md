# Design Ideas for Mitigating the PingLoc Attack

- Image elements may use the crossorigin attribute to limit how cross origin resources are accessed. Possibly set the crossorigin attribute for each image?
- Don't prevent all img.onerrors, just detect that theres alot from this place and stop the rest?
- Parse the image src links?

# How it works

- PingLoc calls ping every 800ms for each site it attempts to load a non-existant image from
  - ping creates a new image each time it pings. This is because the img.src = website + time, thus the beginning of each image object reference is the same, but the ends are different
- The authors of the paper set PingLoc to ping every 800ms. This number may have to be adjusted if a server response takes longer.
  - For example, pining cs.ucla.edu takes longer than 800ms. With the default settings each ping will respond with an 800ms time. However by increasing this ceiling to 2200ms you can correctly time each ping.
  - NOTE: You must change the MAX_LIMIT in the ping.js file (my case testping.js) as well as the timeout for the generatePing function ran on the "malicious" webpage (my case index.html)

```
var img = new Image();
start = new Date().getTime();
img.src = 'http://' + ip + '/' + start;
```
