from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

def base_10_to_any_base(number, base, convert_base):
    try:
        number = int(number)
        answer = ""
        if base != 10:
            raise ValueError("This function only supports base 10 conversion.")  

        while number > 0:
            remainder = number % convert_base 
            if remainder < 10:
                answer += str(remainder)
            else:
                answer += chr(ord('A') + remainder - 10)
            number //= convert_base

        return answer[::-1] if answer else "0"
    except ValueError as e:
        print(f"Error: {e}")
        return None

def any_base_to_base_10(number, base):
    try:
        if not (2 <= base <= 16):
            raise ValueError("Base must be between 2 and 16.")

        number = number.upper()
        answer = 0
        b = len(number)

        for i in range(b):
            char = number[i]
            if char.isdigit():
                digit = int(char)
            elif 'A' <= char <= 'F':
                digit = ord(char) - ord('A') + 10
            else:
                raise ValueError(f"Invalid character '{char}' for base {base}.")

            if digit >= base:
                raise ValueError(f"Digit '{char}' is not valid for base {base}.")

            answer += digit * (base ** (b - i - 1))

        return answer
    except ValueError as e:
        print(f"Error: {e}")
        return None

@app.route('/convert', methods=['POST'])
def convert():
    print(f"Headers: {request.headers}")
    print(f"Content-Type: {request.content_type}")
    print(f"Body: {request.data}")

    if request.content_type != 'application/json':
        return jsonify({"error": "Content-Type must be 'application/json'"}), 415

    try:
        data = request.get_json()
        if data is None:
            return jsonify({"error": "Invalid JSON data"}), 400

        number = data.get('number')
        base = int(data.get('base'))
        convert_base = int(data.get('convertBase'))

        if not number or base is None or convert_base is None:
            return jsonify({"error": "Missing required fields: number, base, or convertBase"}), 400

        if base == 10:
            result = base_10_to_any_base(number, base, convert_base)
        else:
            decimal = any_base_to_base_10(number, base)
            if decimal is None:
                return jsonify({"error": "Invalid number for base"}), 400
            result = base_10_to_any_base(decimal, 10, convert_base)

        if result is None:
            return jsonify({"error": "Conversion failed"}), 400

        return jsonify({"result": result})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
