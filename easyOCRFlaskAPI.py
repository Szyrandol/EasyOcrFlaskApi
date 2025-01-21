from flask import Flask, request, jsonify
import easyocr
import numpy as np
from PIL import Image  # For processing image bytes
import io
from rapidfuzz import fuzz
#import torch

app = Flask(__name__)
reader = easyocr.Reader(['pl'], gpu=True)  # Initialize EasyOCR for English // Polish

@app.route('/ocr', methods=['POST'])
def ocr():

    print('processing')# + '\n' + torch.cuda.is_available())

    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    file = request.files['image']
    image_bytes = file.read()  # Read the image as bytes

    try:
        # Convert bytes to a PIL Image
        image = Image.open(io.BytesIO(image_bytes)) #.convert('RGB')
        width = image.width
        # Convert PIL Image to a NumPy array
        image_np = np.array(image)

        # Perform OCR using EasyOCR
        raw_result = reader.readtext(image_np,width_ths=width)

        rawList = [
            item[1]
            for item in raw_result
        ]

        isLineAnItem = False
        listLength = len(rawList)
        result = []
        n = 0

        for x in range(listLength):
            print(rawList[x])# + ' ' + str(fuzz.partial_ratio('paragon fiskalny', rawList[x].lower())))
            if(isLineAnItem):
                result.append(rawList[x])
                n += 1
                if fuzz.partial_ratio('sprzedaż opodatkowana', rawList[x + 1].lower()) > 85: #exit clause
                    print(fuzz.partial_ratio('sprzedaż opodatkowana', rawList[x + 1].lower()))
                    isLineAnItem = False
            elif fuzz.partial_ratio('paragon fiskalny', rawList[x].lower()) > 70: #entry clause
                print(fuzz.partial_ratio('paragon fiskalny', rawList[x].lower()))
                isLineAnItem = True
            elif fuzz.partial_ratio('suma pln', rawList[x].lower()) > 75: 
                print(fuzz.partial_ratio('suma pln', rawList[x].lower()))
                result.append(rawList[x])
                break
        
        ResultLoD = [
            {'newline': item}
            for item in result
        ]
#
        return jsonify(ResultLoD)  # Return the result as JSON

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on all interfaces at port 5000


'''
regex:
        for x in range(listLength):
            if(isLineAnItem):
                result.append({f'item{n}': x})
                n += 1
                if re.search(r"", processed_result[x+1]['newline']) != 0: #exit clause
                    isLineAnItem = False
            elif re.search(r"^NIP", processed_result[x]['newline']) > 0: #entry clause
                isLineAnItem = True

list of dict:
        processed_result = [
            {   
                'newline': item[1]
            }
            for item in raw_result

        processed_result = [
            {
                'bounding_box': [tuple(map(float, coord)) for coord in item[0]],  # Convert bounding box to floats
                'text': item[1],  # Extract detected text
                'confidence': float(item[2]),  # Convert confidence to float
                '\\n': ''
            }
            for item in raw_result
        ]

        formatted_result = []
        for idx, item in enumerate(raw_result):
            formatted_text = f"\n{item[1]}" if idx > 0 else item[1]  # Add newline before all but the first text
            formatted_result.append({
                'bounding_box': [tuple(map(float, coord)) for coord in item[0]],  # Convert bounding box to floats
                'text': formatted_text,  # Include formatted text
                'confidence': float(item[2])  # Convert confidence to float
            })


        formatted_result = []
        for idx, item in enumerate(raw_result):
            formatted_text = f"\\n{item[1]}" if idx > 0 else item[1]  # Add newline before all but the first text
            formatted_result.append({
                'text': formatted_text,  # Include formatted text
            })
'''
