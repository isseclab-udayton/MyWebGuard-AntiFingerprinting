# CPS 474/574 Software/Language-based Security

Fall 2022

Instructor: Dr. Phu Phung

## Team 8: Fingerprinting Prevention with MyWebGuard

Trello Workspace: [MyWebGuard Trello](https://trello.com/b/ItvCIIq7/mywebguard)

Bitbucket Repository: [MyWebGuard Bitbucket](https://bitbucket.org/ss-lbs-f22-team8/mywebguard/src/master/)

### Team Members

* Nathan Joslin - <joslinn1@udayton.edu>
* Justen Stall - <stallj2@udayton.edu>

## Background Summary

Phung et. al implement an Inline Reference Monitor (IRM) as a browser extension which monitors the JavaScript operations carried out on webpages. Three types of JavaScript operations are monitored: method calls, object creation and access, and property access. When these operations are are executed the IRM intercepts them, which allows for a policy to be enforced. Furthermore, Phung et. al propose a new approach to the same-origin policy in which they call *code-origin*. Their code-origin policy traces the callstack in the JavaScript language to determine the true origin
of JavaScript code within a web page.

Browser fingerprinting is the technique of collecting attributes associated with a device. These attributes are combined to form a unique identifier, a fingerprint, which may be used for tracking or identification. Fingerprinting methods have been used as a secondary form of identifitation. This is used by transaction companies as a layer of fraud protection. Fingerprinting methods are also used maliciously. Fingerprinting reveals device and browser information. By nature, fingerprinting reveals software versions and configuratations which a malicious attacker might use to their advantage. A malicous attacker may use this knowledge to target specific users and exploit known software vulnerabilities. The danger behind this lies in its silent approach. Fingerprinting can be done without the user having knowledge of it. It is nearly impossible for users
to opt-out or block fingerprinting.

## Glossary

* DF: Digital Fingerprinting
  * A way to identify a client machine across the web by unique attributes
* IRM: Inline Reference Monitor
  * Observes execution of a program and can intervene in the execution
* MyWebGuard
  * Browser extension created by Dr. Phung's lab implementing an IRM to monitor Javascript operations for policy enforcement
* ML: Machine Learning
* Static Policy
  * A security policy that is pre-defined
  * Ex: a blocklist of known ad-serving domains
* Dynamic Policy
  * A security policy that is dynamically enforced
  * Ex: an ML model that is trained to identify if a site is malicious

## Project Objectives

<!-- Tried to order these in the order we will accomplish them, 
and commented out some that are not in our scope anymore or are specific to MyWebGuard -->

* Understanding of Digital Fingerprinting Methods.
* Deep Understanding of IRMs and policy enforcement mechanisms.
* Implement a policy to prevent Digital Fingerprinting.
* Prevent Digital Fingerprinting by Monitoring Web Pages.
* Preserve Web Page Functionality while Enforcing Policies.
* Research dynamic policies with Machine Learning.
* Create an implementation plan for a Machine Learning model for dynamic policies.
<!-- * Understanding of Malicious JavaScript Mitigation Techniques. -->
<!-- * Understanding of Information Flow -->
<!-- * Web Page Monitoring with a fine grained policy -->

## Expected contributions and relevance to the course topics

<!-- * Lab 2 - Inline Reference Monitors

Implement a more fine grained policy from which users may customize from a variety of security options. Enforce policies while maintaining web functionality. -->

* Digital Fingerprinting Research

Research how online tracking uses Digital Fingerprinting to identify your internet usage. These Digital Fingerprinting Methods are relevant to Language-Based Security because of the novel ways they use the client information accessible through the web to build up an identifying profile of a machine. Since these methods are within the expected use of the browser, they are not preventable by things like firewalls or even adblockers.

* Implement a policy to prevent Digital Fingerprinting Method

We plan to implement a policy in the MyWebGuard extension that prevents a Digital Fingerprinting method. We will make the policy fine-grained and configurable, and it should not affect normal use of web pages. The MyWebGuard extension acts as an Inline Reference Monitor for web page Javascript code, which is a main theme of our Language-Based Security Course.

* Research Applications of Machine Learning for Dynamic Policy Creation

We will research existing applications of Machine Learning to dynamically enforce policies, such as the ad-blocking research project "AdGraph". Our goal is to understand the features they identify and the data they were trained on.

## Your team plan

Each of us will implement static and dynamic policies which aim to protect user data. First, we plan on researching
prior measurement studies done of the effectiveness of fingerprinting methods. Then, we plan to research current fingerprinting mitigation techniques.
Using this background research, we hope to develop dynamic policies to prevent the collection of fingerprinting data.

## Timeline

### Week 1 (09/19 - 09/25)

* Create & Format README
* Upload Source Code to Repository
* Read Research Paper
* Submit Project Proposal

### Week 2 (09/26 - 10/02)

* Read Relevant Research
* Continue to Update README
* Brainstorm Policy Objectives

### Week 3 (10/03 - 10/09)

* Read Relevant Research - Dynamic Policies, Information Flow
* Continue to Update README
* Create List of Known Fingerprinting Methods
* Practice enforcement methods for document.getElementById

### Week 4 (10/10 - 10/16)

* Read Relevant Research
* Continue to Update README
* Practice enforcement methods for document.getcookie
* Create List of known fingerprinting methods and determine effectiveness

### Week 5 (10/17 - 10/23)

* Read Relevant Research
* Continue to Update README
* Begin brainstorming for project ideas

### Week 6 (10/24 - 10/30)

* Read Relevant Research - Digital Fingerprinting, AdGraph Dynamic Adblocker
* Continue to Update README
* Outline project plan
  * Ideas for a static DF prevention policy
  * Look at existing dynamic policy research to see if there is an opportunity for dynamic DF prevention policies
* Re-evaluate project objectives
* Plan out project timeline (Trello)

### Week 7 (10/31 - 11/06)

* Research dynamic policies with Machine Learning.

### Week 8 (11/07 - 11/13)

* Research dynamic policies with Machine Learning.
* Create an implementation plan for a Machine Learning model for dynamic policies.

### Week 9 (11/14 - 11/20)

* Create an implementation plan for a Machine Learning model for dynamic policies.

### Week 10 (11/21 - 11/27)

* Create an implementation plan for a Machine Learning model for dynamic policies.
* Begin implementation.

### Week 11 (11/28 - 12/04)

* Continue implementation.

### Week 12 (12/05 - 12/11)

* Deadline Week
