

1. When using the login crawler, one of the links will be logout and that will make you leave the page. This is what is happening in Qaits.

2. Logout link issue. If there are 5 links and the logout link the 3rd one. When the 3rd link is executed, it will make the login end. 
   Then when the 4th and 5th link are called you will get not found error.
   
3. The web scraping library BeautifulSoup is not able to pick up achor tags in AllState code.

variations in Anchor tag

Blocked
The web scraping library BeautifulSoup is not able to pick up anchor tags in AllState website code.  
It finds body as 1 tag and does not pick up any of its child tags.  
It finds a total of 17 tags. All the tags under <body> is considered 1 tag. I am not sure why.
I have tried a different parser as well (lxml). We used html.parser before. 

In Qaits website it recognizes all tags and we get total of 110 tags. Then we filter for <a> tags and get 3 tags.  

If there are any other login websites which you would like to be scrapped, pls let me know.


<a href="page1.html">Page 1</a>
<a onclick="location.href='page2.html'">Page 2</a>
<a data-href="page3.html">Page 3</a>