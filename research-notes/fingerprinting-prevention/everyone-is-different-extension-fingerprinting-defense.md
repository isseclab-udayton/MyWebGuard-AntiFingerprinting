# Everyone is Different: Client-side Diversification for Defending Against Extension Fingerprinting

[PDF](https://www.usenix.org/system/files/sec19-trickel.pdf)

## Overview

Presents CloakX, a client-side anti-fingerprinting tool. Uses diversification techniques to prevent extension detection. CloakX performs static and dynamic analysis and introduces extra information to mask any given extension behaviors or identifiable names.

NOTE: Really good static extension fingerprinting mitigation using WARs

## Motives

"Given that users choose the extensions to install, it is possible to make inferences about a user's thoughts and beliefs based soley on the extensions she keeps. For example, the detection of a coupon-finding extension reveals information about the user's income-level. Additionally, an extension that hides articles about certain political figures reveals the user's political leanings."

## Notes

- Web-accessible resources (WARs): A resource within an extension that the extension identifies as exernally accessible.
  - URL Format: chrome-extension://[extension ID]/[Path to Resource]
  - The extension ID is provided by the google web store
  - Sjosten et al. (2017) demonstrate trivial extension detection using WARs, Just need to request one of it's resources to identify ID
  - Used by 28% of extensions (16,479)
- Dynamic DOM analysis reveals extension behaviors, certain behaviors may reveal extension
- _Anchorprints_: A unique identifier formed to facilitate access and communication between webpages and extensions. An Anchor provides a way to directly access elements and resources available to the webpage. Extensions identified by querying the DOM or sending an XMLHttpRequest.
  - Combo of: WARs, IDs, class names, and custom attributes
  - Ex: Grammarly adds a unique class, if an element of this unique class can be accessed, Grammarly is installed
- _Structureprints_: Based on the structure of changes the extension makes to a webpage. Effectively create a DOM fingerprint that uses the extensions unique behavior to identify the extension.
  - Relies on consistent web page modifications
  - Found that 28.9% of extensions using only the tagName of the DOM elements added or deleted by an extension. Adding attribute names, values, and text of elements increases detection to 73.7%
  - Important subset: behaviorprints, currently limited by targeted attacks on specific extensions/category

## CloakX

- Goal: Diversify each extension's fingerprint from the client-side while maintaining equivalent functionality without making any changes to the browser and without requiring the developers to alter their extension.
- Anchorprint Mitigation: Randomized the names of WARs, IDs, and classes. Does not defeat anchorprint detection using custom attributes, but takes some measures by introducing bogus custom attributes.
