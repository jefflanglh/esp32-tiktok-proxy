from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    sec_user_id = request.args.get('sec_user_id', '')
    if not sec_user_id:
        return jsonify({"error": "Missing sec_user_id"}), 400

    # 改用不受 Cloudflare 机房 IP 拦截的 API 接口
    target_url = f"https://www.tikwm.com/api/user/info?unique_id={sec_user_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=10)
        data = res.json()
        
        # 提取粉丝数并按原格式输出，ESP32 可无缝读取
        if data.get("code") == 0 and "data" in data:
            followers = data["data"]["stats"]["followerCount"]
            return jsonify({"followerCount": followers})
        else:
            return jsonify({"error": "Failed to fetch user data", "raw": data}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
