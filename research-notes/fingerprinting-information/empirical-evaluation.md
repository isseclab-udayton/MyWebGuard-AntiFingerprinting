# An Empirical Evaluation of Web-Based Fingerprinting

<https://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=7106402>

Good at explaining fingerprinting methods and metrics to identify its happening

- “Fingerprinting lets trackers create identifiers for browsers, not individuals
- Low-level system properties (look into)
- Three challenges of fingerprinting
  - Fingerprinting is silent
  - Users might observe it happening but can’t do anything about it
  - Many websites can be integrated with social-networking services to increase their popularity and attract traffic. So, integrating fingerprinting with such services can link the fingerprints to easily reveal users’ identity and compromise their security and privacy
- Fingerprinting methods they analyze:
  - JS object fingerprinting – identifies 32 features
  - JS font detection
  - Canvas fingerprinting
  - Flash-based fingerprinting
- 9 Methods for Characterizing fingerprinting attempts
  - Number of accesses to the navigator and  screen objects’ properties
  - Number of accesses to the Plugin and MimeType objects’ properties
  - Number of fonts loaded using JS
  - Number of accesses to the offset properties of HTML elements
  - The presence of writes and reads to a canvas element
  - If a canvas element is hidden or created dynamically
  - The presence of methods for enumerating system fonts and accessing system-related info in a flash file’s source code
  - The presence of methods for transferring or storing info using Flash
  - IF a flash file is small or hidden or if its added dynamically
- Canvas fingerprinting – helpful for fingerprinting when used in conjunction with other methods, not alone
  - Canvas element draws graphical content on the fly using JS
  - First draw an arbitrary context (pangram) on a canvas element
  - Next, collect the canvas element’s image data (pixels), which depends on software and hardware config (font libraries, graphics hardware, OS). As a result, image data can be unique depending on configuration.
  - Metric for identifying:
    - Writes and reads to a canvas element
- Flash-Based Fingerprinting
  - Acquire system info through Capabilities and Font
  - Capabilities
    - Info about underlying system (ex. OS name), running application (flash plugin version)
  - Font
    - Apis for managing embedded fonts in flash files
  - Metrics for identifying:
    - If flash file contains methods for enumerating system fonts or accessing system-related info
    - The presence of methods for transferring or storing info using flash
    - If the flash file is small or hidden or if its added dynamically
- How fingerprinting could be used in conjunction with social media to identify people instead of just browsers:
  - A user logs onto website A using facebook credentials, website A has access to their public information
  - Website A fingerprints the users browser, links facebook profile to the fingerprint, stores this in database
  - Website A shares fingerprint database with website B, a third-party web tracker
  - Web B uses the same fingerprinting algorithm so the same fingerprints can be generated
  - Web B identifies the user using Website A’s database.
