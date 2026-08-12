from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    sec_user_id = request.args.get('sec_user_id', '')
    if not sec_user_id:
        return jsonify({"error": "Missing sec_user_id"}), 400
        
    target_url = f"https://countik.com/api/userinfo?sec_user_id={sec_user_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Referer": "https://countik.com/"
    }
    
    try:
        res = requests.get(target_url, headers=headers, timeout=8)
        return (res.text, res.status_code, {'Content-Type': 'application/json'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
