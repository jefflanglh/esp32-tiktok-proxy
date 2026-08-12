from flask import Flask, request, jsonify
import cloudscraper

app = Flask(__name__)

@app.route('/api/userinfo', methods=['GET'])
def get_user_info():
    sec_user_id = request.args.get('sec_user_id', '')
    if not sec_user_id:
        return jsonify({"error": "Missing sec_user_id"}), 400
        
    target_url = f"https://countik.com/api/userinfo?sec_user_id={sec_user_id}"
    
    try:
        # 创建可绕过 Cloudflare 盾的 scraper 实例
        scraper = cloudscraper.create_scraper(
            browser={
                'browser': 'chrome',
                'platform': 'windows',
                'desktop': True
            }
        )
        res = scraper.get(target_url, timeout=10)
        return (res.text, res.status_code, {'Content-Type': 'application/json'})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()
