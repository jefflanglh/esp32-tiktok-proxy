from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    sec_user_id = request.args.get('sec_user_id', '')
    if not sec_user_id:
        return jsonify({"error": "Missing sec_user_id"}), 400

    # 1. 优先尝试访问 Countik API
    countik_url = f"https://countik.com/api/userinfo?sec_user_id={sec_user_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Referer": "https://countik.com/"
    }

    try:
        res = requests.get(countik_url, headers=headers, timeout=5)
        if res.status_code == 200 and "followerCount" in res.text:
            data = res.json()
            return jsonify({"followerCount": data.get("followerCount", 0)})
    except:
        pass  # 若被 Cloudflare 拦截则自动切换备用数据源

    # 2. 备用方案：直接请求 TikTok 官方 Web 接口 (同样接收 secUid)
    try:
        tt_url = f"https://www.tiktok.com/api/user/detail/?secUid={sec_user_id}"
        tt_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://www.tiktok.com/"
        }
        res = requests.get(tt_url, headers=tt_headers, timeout=8)
        data = res.json()
        followers = data["userInfo"]["stats"]["followerCount"]
        return jsonify({"followerCount": followers})
    except Exception as e:
        return jsonify({"error": "Failed to fetch follower count", "details": str(e)}), 500

if __name__ == '__main__':
    app.run()
