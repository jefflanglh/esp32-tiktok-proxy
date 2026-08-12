from flask import Flask, request, jsonify
from curl_cffi import requests

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    sec_user_id = request.args.get('sec_user_id', '')
    if not sec_user_id:
        return jsonify({"error": "Missing sec_user_id"}), 400
        
    target_url = f"https://countik.com/api/userinfo?sec_user_id={sec_user_id}"
    
    try:
        # impersonate="chrome120" 会伪造真实 Chrome 的 TLS 握手特征与 Header 结构
        res = requests.get(
            target_url,
            impersonate="chrome120",
            headers={
                "Referer": "https://countik.com/",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept-Language": "en-US,en;q=0.9"
            },
            timeout=10
        )
        return (res.text, res.status_code, {'Content-Type': 'application/json'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
