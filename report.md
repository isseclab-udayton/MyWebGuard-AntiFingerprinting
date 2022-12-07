# Course and Instructor information

* Course: CPS 574 - Language Based Security
* Instructor: Dr. Phu Phung
* TA: Ruthvik Kolli

## Team Project: MyWebGuard

Trello Workspace: [MyWebGuard Trello](https://trello.com/b/ItvCIIq7/mywebguard)

Bitbucket Repository: [MyWebGuard Bitbucket](https://bitbucket.org/ss-lbs-f22-team8/mywebguard/src/master/)

### Team Members

* Nathan Joslin - <joslinn1@udayton.edu>
* Justen Stall - <stallj2@udayton.edu>

## Project Summary

(Expected length: 0.5 page)

Summary of the problem, motivation, your work, and the results.

## Introduction

(Expected length: 1-1.5 pages)

In this section, you will introduce to the problem and the motivation of your work. Summarize your work and your results.

## Background

(Expected length: 1.5-2 pages)
Phung et. al implement an Inline Reference Monitor (IRM) as a browser extension which monitors the JavaScript operations carried out on webpages. Three types of JavaScript operations are monitored:
method calls, object creation and access, and property access. When these operations are are executed the IRM intercepts them, which allows for a policy to be enforced. Furthermore, Phung et. al propose
a new approach to the same-origin policy in which they call code-origin. Their code-origin policy traces the callstack in the JavaScript language to determine the true origin of JavaScript code within a web page.

Browser fingerprinting is the technique of collecting attributes associated with a device. These attributes are combined to form a unique identifier, a fingerprint, which may be used for tracking or
identification. Fingerprinting methods have been used as a secondary form of identifitation. This is used by transaction companies as a layer of fraud protection. Fingerprinting methods are also used maliciously.
Fingerprinting reveals device and browser information. By nature, fingerprinting reveals software versions and configuratations which a malicious attacker might use to their advantage. A malicous attacker may use
this knowledge to target specific users and exploit known software vulnerabilities. The danger behind this lies in its silent approach. Fingerprinting can be done without the user having knowledge of it. It is nearly
impossible for users to opt-out or block fingerprinting.

## Project Description

(Expected length: 2-4 pages)

If this is a survey project, you need to describe how your work has been done, including a detailed summary of the work you have surveyed.

If this work has implementation and/or experiments, you need to present your design in one part and your code/experiment structure in the other. Instructions how to run your code/experiments also must be presented.  

## Results

(Expected length: 1-2 pages)

You will present the results of your work in this part. Clearly specify what are the contributions of your work. In a subsection, you need to clarify how each of you has contributed to the project.

## Project Prototype

Include the README.md file and the link to the latest commit of your bitbucket repository

## Appendix

Unlimited appendix pages to show e.g., screenshots of your demo.
