import re
import urllib
import json
import praw

print "||===============================Starting betterLinks.py===============================||"

SUBREDDIT = "jailbreak"
USER_AGENT = ""


def main():
    global USERNAME
    global USER_AGENT
    r = praw.Reddit('betterLinks', user_agent=USER_AGENT)
    USERNAME = r.user.me().name

    print "Getting top 50 submissions on " + SUBREDDIT
    subreddit = r.subreddit(SUBREDDIT)

    for thread in subreddit.new(limit=50):
        link = thread.url

        if (bool(re.search("(moreinfo\.thebigboss.org/moreinfo/depiction.php\?file=)", link)) or
                bool(re.search("(modmyi\.com\/info\/)", link))):
            title = thread.title
            print title + ": " + link
            if checkCommentExists(thread):
                print "Comment already exists"
                continue
            else:
                name = parseName(link)
                jr = getJSON(name)
                # print jr['results'][0]['display'] = BreadcrumbsAway
                # print jr['results'][0]['name'] = org.thebigboss.breadcrumbsaway
                # print jr['results'][0]['section'] = Tweaks
                # print jr['results'][0]['summary'] = dismiss iOS 9's back-to-app link
                # print jr['results'][0]['version'] = 1.1
                goodName = jr['results'][0]['display']
                # goodSummary = jr['results'][0]['summary']
                goodURL = "http://cydia.saurik.com/package/" + jr['results'][0]['name']

                thread.reply("Hey there!\n\nIt's better to use the link below when linking to" +
                             "packages. This way, mobile users can install the package from the " +
                             "link displayed at the top of the page.\n\n" + goodURL +
                             "\n\n###How To:\n\nThere's two ways to do this. \n\n**1.** If " +
                             "you're already in cydia, open the package and scroll all the way " +
                             "to the bottom. You'll see the bundle id which looks like `" +
                             jr['results'][0]['name'] + "`. Just put this at the end of " +
                             "`http://cydia.saurik.com/package/`. \n\n**2.** If you don't have " +
                             "your phone on you, you can lookup the bundle id. Use the following " +
                             "URL:\n\nhttp://cydia.saurik.com/api/macciti?query=\n\nAfter " +
                             "`query=` enter the name of the package. For example, if you wanted " +
                             "to find the bundle id for Cydia Substrate, you would use " +
                             "`http://cydia.saurik.com/api/macciti?query=" + goodName +
                             "`. Then just copy the `name` which is the bundle id (" +
                             jr['results'][0]['name'] + ") and put it at the end of " +
                             "`http://cydia.saurik.com/package/`.")
    return


def parseName(name):
    if bool(re.search("(moreinfo\.thebigboss.org/moreinfo/depiction.php\?file=)", name)):
        name = name.replace("http://moreinfo.thebigboss.org/moreinfo/depiction.php?file=", "")
        name = name[:-3]
    elif bool(re.search("(modmyi\.com\/info\/)", name)):
        name = name.replace("http://modmyi.com/info/", "")
        name = name[:-5]
    return name


def checkCommentExists(sub):
    global USERNAME
    response = False
    comments = sub.comments
    for com in comments:
        if str(com.author) == USERNAME:
            response = True
            break
    return response


def getJSON(name):
    url = "https://cydia.saurik.com/api/macciti?query=" + name
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data


if __name__ == '__main__':
    main()
