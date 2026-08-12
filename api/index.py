from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    # 优先读取 username 参数，若没有则读取 sec_user_id
    user_id = request.args.get('username') or request.args.get('sec_user_id', '')
    if not user_id:
        return jsonify({"error": "Missing user identifier"}), 400

    # TikWM API 使用用户名查询
    target_url = f"https://www.tikwm.com/api/user/info?unique_id={user_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://www.tikwm.com/"
    }

    try:
        res = requests.get(target_url, headers=headers, timeout=10)
        
        # 增加防护，防止非 JSON 返回导致后端崩溃
        if res.status_code != 200 or not res.text.strip():
            return jsonify({"error": f"Target API status {res.status_code}", "body": res.text}), 502

        data = res.json()
        
        # 提取粉丝数，保持 ESP32 适配格式
        if data.get("code") == 0 and "data" in data:
            followers = data["data"]["stats"]["followerCount"]
            return jsonify({"followerCount": followers})
        else:
            return jsonify({"error": "User not found or TikWM API error", "details": data}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
