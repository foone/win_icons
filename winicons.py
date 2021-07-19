import tweepy,os,time,sys
from shuffled_list import ShuffledList
from PIL import Image

CONSUMER_KEY='INSERT_CONSUMER_KEY_HERE'
CONSUMER_SECRET='INSERT_CONSUMER_SECRET_HERE'
ACCESS_KEY,ACCESS_SECRET = (u'INSERT_KEY_HERE', u'INSERT_SECRET_HERE')
AUTHORIZING=False

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
if AUTHORIZING:
	print auth.get_authorization_url()
	verifier = raw_input('Verifier:')
	print auth.get_access_token(verifier)
	sys.exit()
else:
	auth.set_access_token(ACCESS_KEY,ACCESS_SECRET)


api = tweepy.API(auth)
sl=ShuffledList('winicons','source/*.png')
if len(sys.argv)==1:
    while True:
        path=sl.pop()
        # loop until the path exists, so we skip deleted files
        if os.path.exists(path):
            break
else:
    path=sys.argv[1]

OUT_FILE='out.png'

def generate_image(filename, outpath=None):
	im=Image.open(filename).convert('RGBA')
	template=Image.open('template.png')
	template.paste(im, (47,37), im)
	scaled2x = im.resize((64,64), Image.NEAREST)
	scaled4x = im.resize((128,128), Image.NEAREST)
	template.paste(scaled2x, (31,102), scaled2x)
	template.paste(scaled4x, (200,39), scaled4x)
	if outpath is None:
		outpath= OUT_FILE
	template.save(outpath)
	return outpath

outpath = generate_image(path)

name=os.path.splitext(os.path.basename(path))[0]
print time.time()
print path,name
print api.update_with_media(outpath,name)
