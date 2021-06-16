from ckip_transformers import __version__
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker
import re
def replace_all_blank(value):
   """
   去除value中的所有非字母內容，包括標點符號、空格、換行、下劃線等
   :param value: 需要處理的內容
   :return: 返回處理後的內容
   """
   # \W 表示匹配非數字字母下劃線
   result = re.sub('\W+', '', value).replace("_", '')
   return result

def Word_Segmentation(text):

   # Show version
   print(__version__)

   # Initialize drivers
   print('Initializing drivers ... WS')
   ws_driver  = CkipWordSegmenter(level=3)

   # Input text
#    text = []

   # print(text)
   # Run pipeline
   print('Running pipeline ... WS')
   ws  = ws_driver(text)

   return ws
   # with open('./dataset/article.txt', 'w', encoding='utf-8') as f:
   #    for list in ws:
   #       for item in list:
   #          # print('item:', item)
   #          f.write(item)
   #          f.write(' ')
