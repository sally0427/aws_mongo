from ckip_transformers import __version__
from ckip_transformers.nlp import CkipWordSegmenter, CkipPosTagger, CkipNerChunker

def Word_Segmentation(text):

   # Show version
   print(__version__)

   # Initialize drivers
   print('Initializing drivers ... WS')
   ws_driver  = CkipWordSegmenter(level=3)

   # Input text
#    text = [
#       '傅達仁今將執行安樂死，卻突然爆出自己20年前遭緯來體育台封殺，他不懂自己哪裡得罪到電視台。',
#       '美國參議院針對今天總統布什所提名的勞工部長趙小蘭展開認可聽證會，預料她將會很順利通過參議院支持，成為該國有史以來第一位的華裔女性內閣成員。',
#       '空白 也是可以的～',
#       '已經退讓了，環團詐騙集團還是會繼續亂吧!尤其是姓潘的，他也使接受日月光模式的協議',
#    ]

   print(text)
   # Run pipeline
   print('Running pipeline ... WS')
   ws  = ws_driver(text)

   # Show results
   for sentence, sentence_ws in zip(text, ws):
      print(sentence)
      print('------------------------------------------')
      print(sentence_ws)
      print()
