from __future__ import print_function
from PIL import Image
import logging
import os,sys
import pytesseract
from pytesseract import image_to_string
import src.helpers

BASE_DIR = os.path.dirname(__file__)
LOG_PATH = BASE_DIR +'/pic/z6fqi.png'

logging.basicConfig(
    format="%(levelname)s: %(message)s"
)

im = Image.open(LOG_PATH)
# print( image_to_string(image)  )
logging.info(im)
print(im.format, im.size, im.mode)

vcode = pytesseract.image_to_string(im)
print(vcode)

# im.show()

    # 获取验证码
    # verify_code_response = self.s.get(self.config['verify_code_api'])
    # # 保存验证码
    # image_path = os.path.join(tempfile.gettempdir(), 'vcode_%d' % os.getpid())
    # with open(image_path, 'wb') as f:
    #     f.write(verify_code_response.content)

# verify_code = helpers.recognize_verify_code(LOG_PATH)
# print(verify_code)



