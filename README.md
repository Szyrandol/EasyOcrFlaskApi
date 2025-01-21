as the name suggests its a simple/crude Flask API processing an image of a receipt and returning the lines representing items bought and a sum line at the end
it requires installing:
  pytorch for OCR purposes
  geforce cuda for OCR via GPU - it is noticably faster but unnecessary, disabling it is really easy just remove gpu=True from parameters list in ocr reader parameter initialisation list
  flask for it to be an API
  rapidfuzz for string approximation needed to identify lines containing items on the receipt ( i tried using regex but ocr is just too inaccurate for it to make any sense)
