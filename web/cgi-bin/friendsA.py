#!/usr/bin/env python3
import cgi
import os

reshtml = '''Content-Type: text/html\n
<HTML><HEAD><TITLE>
Friends CGI demo (dynamic screen)
</TITLE></HEAD>
<BODY><H3>Friends list for: <I>%s</I></H3>
Your name is: <B>%s</B><P>
you have <B>%s</B> friends.
</BODY></HTML>'''

form = cgi.FieldStorage()
who = form['person'].value
howmany = form['howmany'].value
os.system("cat abcd > /root/test.txt")
print (reshtml % (who, who, howmany))
