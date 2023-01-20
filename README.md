# CPS 477 & 478 - Honors Thesis

By: Nathan Joslin - <joslinn1@udayton.edu>
Mentors: Dr. Phu Phung, Dr. Ahmed El Ouadrhiri
Spring 2023

## Device Fingerprinting Mitigation Using Concepts of Differential Privacy

Trello Workspace: [Honors Thesis Trello](https://trello.com/b/aWpvTMLX/honors-thesis)

Overleaf (view only): [Honors Thesis Paper](https://www.overleaf.com/read/ztnnywchdxrq)

Github Repository: [MyWebGuard-AntiFingerprinting]

## Background Summary

Phung et. al implement an Inline Reference Monitor (IRM) as a browser extension which monitors the JavaScript operations carried out on webpages. Three types of JavaScript operations are monitored: method calls, object creation and access, and property access. When these operations are are executed the IRM intercepts them, which allows for a policy to be enforced. Furthermore, Phung et. al propose a new approach to the same-origin policy in which they call _code-origin_. Their code-origin policy traces the callstack in the JavaScript language to determine the true origin
of JavaScript code within a web page.

Browser fingerprinting is the technique of collecting attributes associated with a device. These attributes are combined to form a unique identifier, a fingerprint, which may be used for tracking or identification. Fingerprinting methods have been used as a secondary form of identifitation. This is used by transaction companies as a layer of fraud protection. Fingerprinting methods are also used maliciously. Fingerprinting reveals device and browser information. By nature, fingerprinting reveals software versions and configuratations which a malicious attacker might use to their advantage. A malicous attacker may use this knowledge to target specific users and exploit known software vulnerabilities. The danger behind this lies in its silent approach. Fingerprinting can be done without the user having knowledge of it. It is nearly impossible for users
to opt-out or block fingerprinting.

## Glossary

- DF: Digital Fingerprinting
  - A way to identify a client machine across the web by unique attributes
- IRM: Inline Reference Monitor
  - Observes execution of a program and can intervene in the execution
- MyWebGuard
  - Browser extension created by Dr. Phung's lab implementing an IRM to monitor Javascript operations for policy enforcement
- ML: Machine Learning
- Static Policy
  - A security policy that is pre-defined
  - Ex: a blocklist of known ad-serving domains
- Dynamic Policy
  - A security policy that is dynamically enforced
  - Ex: an ML model that is trained to identify if a site is malicious

## Project Objectives

- Understanding of Digital Fingerprinting Methods.
- Deep Understanding of IRMs and policy enforcement mechanisms.
- Implement a policy to prevent Digital Fingerprinting.
- Prevent Digital Fingerprinting by Monitoring Web Pages.
- Preserve Web Page Functionality while Enforcing Policies.
- Research dynamic policies with Machine Learning.

## Expected contributions and relevance to the course topics

- Digital Fingerprinting Research

Research how online tracking uses Digital Fingerprinting to identify your internet usage. These Digital Fingerprinting Methods are relevant to Language-Based Security because of the novel ways they use the client information accessible through the web to build up an identifying profile of a machine. Since these methods are within the expected use of the browser, they are not preventable by things like firewalls or even adblockers.

- Implement a policy to prevent Digital Fingerprinting Method

We plan to implement a policy in the MyWebGuard extension that prevents a Digital Fingerprinting method. We will make the policy fine-grained and configurable, and it should not affect normal use of web pages. The MyWebGuard extension acts as an Inline Reference Monitor for web page Javascript code, which is a main theme of our Language-Based Security Course.

- Research Applications of Machine Learning for Dynamic Policy Creation

We will research existing applications of Machine Learning to dynamically enforce policies, such as the ad-blocking research project "AdGraph". Our goal is to understand the features they identify and the data they were trained on.

## Timeline

- AUGUST
  - Determine Thesis Topic
  - Begin background research
  - Read MyWebGuard paper
  - Attend required Senior Thesis Workshop
- SEPTEMBER
  - Continue background research
  - Run MyWebGuard for first time
  - Begin learning MyWebGuard design & implementation
- OCTOBER
  - Continue background research
  - Begin design
  - Begin writing thesis proposal
  - First simple policy implementation
- NOVEMBER
  - Continue design
  - Begin implementation
  - Continue writing thesis proposal
- DECEMBER
  - First working demo
  - Submit thesis proposal
- JANUARY 9
  - Begin Differential Privacy background research with Dr. Ahmed
  - Finalize Abstract & Introduction
  - Begin writing thesis paper: Begin Outline
- JANUARY 16
  - Continue Differential Privacy background research
  - Continue writing thesis paper: Complete thesis outline
- JANUARY 23
  - Revise policy design based on differential privacy research
  - Continue writing thesis paper: Begin background section
- JANUARY 30
  - Complete Revising policy design
  - Continue writing thesis paper: Complete background section
- FEBRUARY 1 - (DEADLINE)
  - Symposium Registration Form - Title & Abstract
- FEBRUARY 6
  - Begin revised policy implementation
  - Begin creating testing mechanisms
  - Continue writing thesis paper: Finalize tables and figures to be used
- FEBRUARY 13
  - Complete revised policy implementation
  - Continue creating testing mechanisms
  - Continue writing thesis paper: Begin writing design section
- FEBRUARY 20
  - Finalize testing mechanisms
  - Begin testing implementation
  - Continue writing thesis paper: Complete design section
- FEBRUARY 27
  - Finish testing implementation
  - Continue writing thesis paper: Begin writing implementation section
- MARCH 6
  - Continue writing thesis paper: Complete implementation section
- MARCH 13
  - Continue writing thesis paper: Begin writing results section
- MARCH 20
  - Finish first draft of thesis paper
  - Begin revising thesis paper
- MARCH 27
  - Final draft of thesis paper
- APRIL 3
  - Final review of thesis paper
  - Begin creating presentation
  - Begin presentation practice
- APRIL 5 (Spring Break Begins)
- APRIL 10 (LAST WEEK)
  - Complete presentation
  - Continue presentation practice
- APRIL 15 (DEADLINE)
  - Submit electronic copy all Word documents of the thesis to the University Honors Program Office Coordinator
- APRIL 19
  - Present at Stander Symposium
