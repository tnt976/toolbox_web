from flask import Flask, render_template, request, jsonify
from datetime import datetime, timezone, timedelta
import base64
import urllib.parse
import html
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tools/time')
def time_tools():
    return render_template('time.html')

@app.route('/tools/encode')
def encode_tools():
    return render_template('encode.html')

@app.route('/tools/url')
def url_tools():
    return render_template('url.html')

@app.route('/tools/aes')
def aes_tools():
    return render_template('aes.html')

@app.route('/api/time/current', methods=['GET'])
def get_current_time():
    now = datetime.now()
    timestamp = int(now.timestamp())
    return jsonify({
        'timestamp': timestamp,
        'datetime': now.strftime('%Y-%m-%d %H:%M:%S')
    })

@app.route('/api/time/to_datetime', methods=['POST'])
def timestamp_to_datetime():
    data = request.get_json()
    timestamp = data.get('timestamp')

    try:
        timestamp = int(timestamp)
        dt = datetime.fromtimestamp(timestamp)
        return jsonify({
            'success': True,
            'datetime': dt.strftime('%Y-%m-%d %H:%M:%S'),
            'timestamp': timestamp
        })
    except (ValueError, OSError, OverflowError):
        return jsonify({
            'success': False,
            'error': '无效的时间戳'
        }), 400

@app.route('/api/time/to_timestamp', methods=['POST'])
def datetime_to_timestamp():
    data = request.get_json()
    datetime_str = data.get('datetime')

    try:
        dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M')
        timestamp = int(dt.timestamp())
        return jsonify({
            'success': True,
            'timestamp': timestamp,
            'datetime': datetime_str
        })
    except ValueError:
        return jsonify({
            'success': False,
            'error': '无效的日期时间格式'
        }), 400

@app.route('/api/encode/base64', methods=['POST'])
def encode_base64():
    data = request.get_json()
    text = data.get('text', '')

    try:
        encoded = base64.b64encode(text.encode('utf-8')).decode('utf-8')
        return jsonify({
            'success': True,
            'result': encoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/decode/base64', methods=['POST'])
def decode_base64():
    data = request.get_json()
    text = data.get('text', '')

    try:
        decoded = base64.b64decode(text.encode('utf-8')).decode('utf-8')
        return jsonify({
            'success': True,
            'result': decoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Base64解码失败，请检查输入是否正确'
        }), 400

@app.route('/api/encode/url', methods=['POST'])
def encode_url():
    data = request.get_json()
    text = data.get('text', '')

    try:
        encoded = urllib.parse.quote(text)
        return jsonify({
            'success': True,
            'result': encoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/decode/url', methods=['POST'])
def decode_url():
    data = request.get_json()
    text = data.get('text', '')

    try:
        decoded = urllib.parse.unquote(text)
        return jsonify({
            'success': True,
            'result': decoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/encode/html', methods=['POST'])
def encode_html():
    data = request.get_json()
    text = data.get('text', '')

    try:
        encoded = html.escape(text)
        return jsonify({
            'success': True,
            'result': encoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/decode/html', methods=['POST'])
def decode_html():
    data = request.get_json()
    text = data.get('text', '')

    try:
        decoded = html.unescape(text)
        return jsonify({
            'success': True,
            'result': decoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/url/encode', methods=['POST'])
def encode_full_url():
    data = request.get_json()
    url = data.get('url', '')

    try:
        encoded = urllib.parse.quote(url, safe='')
        return jsonify({
            'success': True,
            'result': encoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/url/decode', methods=['POST'])
def decode_full_url():
    data = request.get_json()
    url = data.get('url', '')

    try:
        decoded = urllib.parse.unquote(url)
        return jsonify({
            'success': True,
            'result': decoded
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/url/parse', methods=['POST'])
def parse_url():
    data = request.get_json()
    url = data.get('url', '')

    try:
        parsed = urllib.parse.urlparse(url)
        params = urllib.parse.parse_qs(parsed.query)

        result_params = {}
        for key, values in params.items():
            result_params[key] = values[0] if len(values) == 1 else values

        return jsonify({
            'success': True,
            'scheme': parsed.scheme,
            'netloc': parsed.netloc,
            'path': parsed.path,
            'params': result_params,
            'fragment': parsed.fragment
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/aes/encrypt', methods=['POST'])
def aes_encrypt():
    data = request.get_json()
    plaintext = data.get('text', '')
    key_str = data.get('key', '')
    mode = data.get('mode', 'ECB')
    padding_mode = data.get('padding', 'PKCS7')
    key_size = int(data.get('key_size', 128))
    encoding = data.get('encoding', 'UTF-8')
    output_format = data.get('output_format', 'Base64')
    key_type = data.get('key_type', 'Text')

    try:
        # Process key
        key_length = key_size // 8
        if key_type == 'Hex':
            key_bytes = bytes.fromhex(key_str)
        else:
            key_bytes = key_str.encode(encoding)
        
        if len(key_bytes) < key_length:
            key_bytes = key_bytes.ljust(key_length, b'\x00')
        elif len(key_bytes) > key_length:
            key_bytes = key_bytes[:key_length]

        # Process plaintext
        plaintext_bytes = plaintext.encode(encoding)

        # Padding
        if padding_mode == 'ZeroPadding':
            pad_length = key_length - (len(plaintext_bytes) % key_length)
            if pad_length != key_length:
                plaintext_bytes += b'\x00' * pad_length
        else:
            padder = padding.PKCS7(128).padder()
            plaintext_bytes = padder.update(plaintext_bytes) + padder.finalize()

        # Create cipher
        if mode == 'ECB':
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB())
        else:
            iv = os.urandom(16)
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
        
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(plaintext_bytes) + encryptor.finalize()

        # Output format
        if mode == 'CBC':
            ciphertext = iv + ciphertext
        
        if output_format == 'Base64':
            result = base64.b64encode(ciphertext).decode('utf-8')
        else:
            result = ciphertext.hex()

        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/aes/decrypt', methods=['POST'])
def aes_decrypt():
    data = request.get_json()
    ciphertext_str = data.get('text', '')
    key_str = data.get('key', '')
    mode = data.get('mode', 'ECB')
    padding_mode = data.get('padding', 'PKCS7')
    key_size = int(data.get('key_size', 128))
    encoding = data.get('encoding', 'UTF-8')
    input_format = data.get('input_format', 'Base64')
    key_type = data.get('key_type', 'Text')

    try:
        # Process key
        key_length = key_size // 8
        if key_type == 'Hex':
            key_bytes = bytes.fromhex(key_str)
        else:
            key_bytes = key_str.encode(encoding)
        
        if len(key_bytes) < key_length:
            key_bytes = key_bytes.ljust(key_length, b'\x00')
        elif len(key_bytes) > key_length:
            key_bytes = key_bytes[:key_length]

        # Process ciphertext
        if input_format == 'Base64':
            ciphertext = base64.b64decode(ciphertext_str)
        else:
            ciphertext = bytes.fromhex(ciphertext_str)

        iv = None
        if mode == 'CBC' and len(ciphertext) >= 16:
            iv = ciphertext[:16]
            ciphertext = ciphertext[16:]

        # Create cipher
        if mode == 'ECB':
            cipher = Cipher(algorithms.AES(key_bytes), modes.ECB())
        else:
            cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(iv))
        
        decryptor = cipher.decryptor()
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()

        # Unpadding
        if padding_mode == 'ZeroPadding':
            plaintext_bytes = padded_data.rstrip(b'\x00')
        else:
            unpadder = padding.PKCS7(128).unpadder()
            plaintext_bytes = unpadder.update(padded_data) + unpadder.finalize()

        result = plaintext_bytes.decode(encoding)

        return jsonify({
            'success': True,
            'result': result
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
