from rembg import remove
import requests
from PIL import Image
from io import BytesIO
import os

os.makedirs('original', exist_ok=True)
os.makedirs('masked', exist_ok=True)

img_url = "https://m.media-amazon.com/images/I/71SiF721KOL.jpg"

img_name = img_url.split('/')[-1]

img = Image.open(BytesIO(requests.get(img_url).content))

img.save('original/' + img_name, format = 'jpeg')

output_path = 'masked/'+img_name

with open(output_path, 'wb') as f:
    input = open('original/'+img_name, 'rb').read()
    subject = remove(input, alpha_matting=True)
    f.write(subject)
    
    

background_img = 'https://colibriwp.com/blog/wp-content/uploads/2019/06/pawel-czerwinski-vI5XwPbGvmY-unsplash.jpg'

background_img = Image.open(BytesIO(requests.get(background_img).content))

background_img = background_img.resize((img.width, img.height))

foreground_img = Image.open(output_path)

background_img.paste(foreground_img, (0,0), foreground_img)

background_img.save('masked/background.jpg', format='jpeg')