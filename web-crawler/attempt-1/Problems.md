

1. A lot of href links only had "/mapping". So I had to add the root domain.
2. In Qualibar's case, it had .html pages as identifier. Like 'careers.html'
   Example
<a href="career.html">Careers</a>

3. Discard external urls

4. Big Website Issues - There can be thousands of links in hospitals websites. 
   We should have a limit to how many pages should the crawler discover and generate java class files.
   
5. Sometimes there are urls which do not follow standard and due to that we are not able to parse it properly and get an error.
UnboundLocalError: local variable 'match' referenced before assignment
   8365 link
   "https://www.tgh.org/"

We will have to test this crawler on several websites.
Websites made on React, Angular, SPAs


domain_to_crawl = "https://ufhealth.org"

This website has over 2K links

https://mintmobile.com

This website was not working with our code.


Ask Kunal

The java files the site crawler creates. should it be blank files? Or do you want some content.


Sandip - Questions to Ask

1. We want to store the crawler's site map links in a log file or a DB.
2. There some big websites with more than 1000 links. Should we put a limit on the number of links the crawler will fetch.

Inaccuracies
1. It does not work for mintmobile.com
2. It does not work for large websites with thousands of links
3. How to give names to the java classes? Extract the last word from the url?
   3.1 What is the name has -. Ex = contact-us. This file name will not work for Java classes
   


table = company_site_map
level col