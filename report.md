# Course and Instructor information

- Course: CPS 574 - Language Based Security
- Instructor: Dr. Phu Phung
- TA: Ruthvik Kolli

## Team Project: MyWebGuard

Trello Workspace: [MyWebGuard Trello](https://trello.com/b/ItvCIIq7/mywebguard)

Bitbucket Repository: [MyWebGuard Bitbucket](https://bitbucket.org/ss-lbs-f22-team8/mywebguard/src/master/)

### Team Members

- Nathan Joslin - <joslinn1@udayton.edu>
- Justen Stall - <stallj2@udayton.edu>

## Project Summary

(Expected length: 0.5 page)

Browser fingerprinting is the technique of collecting attributes associated with a device. These attributes are combined to form a unique identifier, a fingerprint, which may be used for tracking or identification. A fingerprint of one device will differ from another as a result of software and hardware configurations. Fingerprinting methods have been shown to be used in industry as an additional layer of fraud protection. When logging in, user provided login credentials are verified as well as the device being used. As an unrecognized device is an indicator of suspicous activity, extra verification measures can be enforced to validate the user request. However, fingerprinting methods could just as easily be used by malicious actors. A third-party can collect device fingerprints to track user activity across the web without the user being aware of it. We consider this involuntary tracking and collection of private data to violate user privacy. By using MyWebGuard's enforcement technology we are able to successfully mitigate the ability for malicious actors to track user activity across the web. More specifically, we mitigate the possibility of canvas fingerprinting by taking a "hide in the crowd" approach. This approach is similar to methods used by the Tor browser, which is known for protecting user privacy.

## Introduction

(Expected length: 1-1.5 pages)

Although device fingerprinting is used positively in the wild and in research, it is possible for device fingerprinting to be used maliciously. In _An Empirical Evaluation of Web-Based Fingerprinting_ Khademi et al. outline a scenario where device fingerprinting may be used in conjunction with social media to unveil the person using the device.

1. A user logs onto website A using facebook credentials.
   - Website A has access to their _public_ information.
   
2. Website A fingerprints the user's device, linking their facebook profile to the device fingerprint.
   - This fingerprint:profile link is stored in a database.
   
3. Website A then shares the fingerprint database with Website B.

4. Website B uses the same fingerprinting algorithm as Website A.
   - The same fingerprint should be generated.
   
5. Website B identifies the user by querying the database.
   - User's public facebook profile information is revealed.

Using this method, the ability for a user to be tracked is dependent on the number of websites sharing the database. Scenarios such as the one provided by Khademi et al. are the motivation for our work.

In order to mitigate malicious fingerprinting activities we first needed a concrete understanding of browser/device fingerprinting, how it is used, how effective it is, and how common is its use. We collected and examined research papers that surveyed the prevalence of fingerprinting in the wild as well as the methods used. In sum, it is known that some of the Alexa top 1M websites use browser or device fingerprinting. The specific number of websites is hard to determine as it is often difficult to differentiate between functional use of API's and using API's for fingerprinting. This is the main research question as currently many anti fingerprinting technologies result in frequent major or minor website breakage. Furthermore, many of these studies examined the effectiveness of fingerprinting methods. It can be seen that some fingerprinting methods are more effective than others. For example it appears that the User-agent, Canvas, List of Plugins, and List of Fonts attributes of a device provide the most unique fingerprints. Combining multiple high entropy attributes to form a single fingerprint yields an increasingly unique fingerprint. Laperdrix et al. provide a table demonstrating the entropies for device attributes determiend by three other research papers: </br>

![AttributeEntropyTable](https://i.ibb.co/qyLQdgM/Fingerprinting-Methods-Entropy-Table.png)
</br>

Due to time constraints it was necessary to reduce the scope of our research project. Due to its prevalence and high entropy, we decided to narrow down our research to canvas fingerprinting. We researched fingerprinting methods that primarily focused on using canvas elements to uniquely identify users. From these methods we were able to design a policy enforced by MyWebGuard that successfully mitigates the ability for a canvas fingerprinter to consistently identify a user over time. We achieved this by implementing a method called "Canvas Poisoning". If our policy flags a canvas element as suspicious, i.e. the canvas element is being created by the fingerprinting algorithm itself, we "poison" the canvas image. Canvas poisoning slightly changes a canvas image so that is is similar to the original image but the data for the element is different from the original image.Adding a watermark to a canvas element would be considered canvas poisioning. Because the image data is changed from the original data, the resulting fingerprint is also different. As a fingerprinter relies on a consistent fingerprint over time to track a given device or user, slightly changing a devices fingerprint each time it is collected significantly limits the effectivness of the fingerprinting algorithm.

## Background & Research

(Expected length: 1.5-2 pages)
Phung et. al implement an Inline Reference Monitor (IRM) as a browser extension which monitors the JavaScript operations carried out on webpages. Three types of JavaScript operations are monitored:
method calls, object creation and access, and property access. When these operations are are executed the IRM intercepts them, which allows for a policy to be enforced. Furthermore, Phung et. al propose
a new approach to the same-origin policy in which they call code-origin. Their code-origin policy traces the callstack in the JavaScript language to determine the true origin of JavaScript code within a web page.

Browser fingerprinting is the technique of collecting attributes associated with a device. These attributes are combined to form a unique identifier, a fingerprint, which may be used for tracking or
identification. Fingerprinting methods have been used as a secondary form of identifitation. This is used by transaction companies as a layer of fraud protection. Fingerprinting methods are also used maliciously.
Fingerprinting reveals device and browser information. By nature, fingerprinting reveals software versions and configuratations which a malicious attacker might use to their advantage. A malicous attacker may use
this knowledge to target specific users and exploit known software vulnerabilities. The danger behind this lies in its silent approach. Fingerprinting can be done without the user having knowledge of it. It is nearly
impossible for users to opt-out or block fingerprinting.

FP-Inspector was designed to detect fingerprinting behaviors as well as mitigate them. They surveyed the Alexa top 100k, determining that 10% of websites use some form of fingerprinting.

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
