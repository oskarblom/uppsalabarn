from BeautifulSoup import BeautifulSoup
import re

#with open("destinationuppsaladump.html") as f:
#    doc = "".join(f)
#
#soup = BeautifulSoup(doc, fromEncoding="utf-8")
#
#header = soup.find("font", "head1").find(text=True)
#description = soup.find("span", id=re.compile("Description$")).find(text=True)
#phone = soup.find("span", id=re.compile("Phone$"))
#print phone.text.replace("Tfn:", "")
with open("untguidendump.html") as f:
    doc = "".join(f)

soup = BeautifulSoup(doc)

header = soup.find("h1")

h1 = header.find(text=True)
desc = header.parent.text

print h1
print desc

print re.sub(r"^%s" % h1, "", desc, count=1)
print header.parent.text
print header.parent.find(text=True)
print header.find(text=True)

web = soup.find("strong", text="Webb")

email = soup.find("strong", text="E-post")

phone = soup.find("strong", text="Kontakt")
print phone.parent.text
#print email.parent.findNextSibling("a").find(text=True)
