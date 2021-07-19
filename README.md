# win_icons
 A twitter bot to post windows 3.x icons

This is a bot, intended to be invoked by cron, which takes an image from the source folder and posts it to an affiliated twitter account. It applies some simple resizing and templating to it, to make it a better image for twitter than just posting a raw 32x32 image which wouldn't work terribly well. 

I run it by wrapping bash script around it, and set that to run every hour using a crontab:

    0 * * * * /home/foone/projects/winicons/do.sh

do.sh is inclued in extra, but will require modification to run on your system, unless your username is also foone:

    #!/bin/bash
    cd /home/foone/projects/winicons
    venv/bin/python winicons.py >> winicons.log

# Requirements

The code uses python 2.x and the tweepy library. I know this isn't the latest and best twitter library, but it works, and I've not bothered to rewrite it.
It also uses Pillow to do the image modifications, but PIL would work just as well if that's easier to install. I run it inside a virtualenv which you can create by doing:

    virtualenv venv
    venv/bin/pip install -r requirements.txt 

but this is not required. You can install the packages globally if you want, I'm not your real dad. 

For the shuffled_list functionality, it uses redis. shuffled_list serves to do a better job of randomly selecting images than picking one item each time would. It basically gets a lot of files from the source folder, randomizes their order, then stuffs it into an ordered redis list. Entries in the list are posted one by one until no more items are available, then the query-files-and-shuffle-them step is repeated. This ensures that item X won't reappear until every other item has been posted at least once. If you want to run the bot without requiring redis, I provided a simple_shuffled_list.py file in extra, which just picks a random file each time it's called. 


# Actually using this on a Twitter account

This is slightly tricky because of how tweepy works.
So what you want to do is get access to the twitter API: How you do this has changed since I did it for win_icons, so I can't help you there. 
https://developer.twitter.com/en is probably where you want to start. 

From there, you'll need to get your consumer key and consumer secret. This is the key that lets you access the API, but you can't tweet yet: for that you need an access token.

Edit winicons.py and set AUTHORIZING to True. Then run it, and it'll give you a URL to visit.
Visit that URL while logged into the twitter account you want to tweet to, and click the accept button to give access to this key/secret.
winicons.py will then print out a tuple that looks like:

    (u'gibberish_letters',u'more_gibberish_letters')

You need to edit that back into winicons.py, in the line starting with ACCESS_KEY, so it looks like:

    ACCESS_KEY,ACCESS_SECRET = (u'dQw4w9WgXcQ',u'oHg5SJYRHA0')

(but obviously different as your keys/secret will be different).

Then set AUTHORIZING back to False, and you should now be able to run winicons.py and have it post for you.

While running it'll need the template.png file as the background, and it'll create a temporary file named out.png before posting it. It doesn't ever clean up out.png, I'm lazy. 

There's no checking on if the twitter API call succeeded or failed, right now the error is just printed out, and will end up in the log (if you're running it with the do.sh suggested above). You may want to change this if you require High Resilience in your twitter shitposting.  

I have only tested this on ubuntu, but the python code should be pretty portable and run on basically anything with a hard drive and internet access. 

# Reuse for other bots

This is like 90% the same script I use to run another bot, [@gayocats](https://twitter.com/gayocats). Basically to turn this into a bot that just posts images from a folder and doesn't do any special image editing on them, you just need to replace this line:

    outpath = generate_image(path)

with

    outpath = path


Then it'll just post the image as-is. 

# Downsides and caveats

1. As mentioned before, there's no real error checking. It tries to post to twitter and it'll print out an error if it can't, but it won't retry or sent alerts or anything. If twitter is having a momentary hiccup, you'll get nothing. 
2. Tweepy is an older library and I'm using an old version of it. There may be better libraries to use, I don't know. This works for me
3. I'm maybe not using the latest twitter API? Twitter has changed a lot of stuff since this bot was written. Possibly this can and should be updated for a newer API: I don't know. I'll let you know if I ever do that, but for now, this works.
4. New images can't appear until the existing queue is used up. Because of how the shuffling works, you won't see anything new that quickly. This could possibly be fixed, at the cost of making the randomization worse, but in the meantime you can always manually log into redis and delete the list. (that's just DEL winicons)
5. The redis list name isn't namespaced. Yeah I just thought of this one: You can always change it if you want to run more than one copy of the bot on a server, or if you're already using "winicons" for something. 
6. simple_shuffled_list.py in extra hasn't been tested. It's some very simple python code so I don't think it'll break, but I haven't even run it.
7. It assumes all the input files are 32x32, and does not check this. The resizing and pasting onto the temple will work very weirdly or break if your input files are the wrong size. 

# Not actually downsides and caveats, even if you think they might be:
1. It's written in python 2.7: You are welcome to eat my entire ass if you think this is a downside. I'm a retrocomputerist, you're lucky I didn't write this in QBasic for MS-DOS 6.22.
2. I've already easter-egg rickrolled you (twice) in this readme.

# License
This is licensed under the GPL, version 3. This basically just means that if you modify this script and republish those modifications, you need to also license it under the GPL3. It doesn't mean you need to share any modifications if you just install it in your server and use it (even if you modify it to do weird things to the images or something like that)

You do NOT have to agree to the GPL to use this software. You never have to agree to the GPL: It's not a EULA, you don't need to agree to it!