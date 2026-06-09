"""
Free Fire Bot Web Dashboard
Flask-based web interface for controlling the bot and managing features
Runs on port 4040
"""

import os

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from flask import Flask, render_template, request, jsonify, session
    from flask_cors import CORS
except ImportError:
    print("[ERROR] Flask not installed. Installing now...")
    import subprocess
    subprocess.run(['pip', 'install', 'flask', 'flask-cors'])
    from flask import Flask, render_template, request, jsonify, session
    from flask_cors import CORS

import asyncio
import json
from datetime import datetime
from like_utils import (search_player, send_like_to_player, get_like_count,
                        get_player_level, get_player_nickname,
                        check_player_exists, get_all_regions, send_bulk_likes)
from like_bot_accounts import LIKE_BOT_ACCOUNTS

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

# Global stats
stats = {
    "total_likes_sent": 0,
    "total_searches": 0,
    "total_players_found": 0,
    "server_start_time": datetime.now()
}


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html',
                           total_bots=len(LIKE_BOT_ACCOUNTS),
                           stats=stats)


@app.route('/api/search', methods=['POST'])
def api_search():
    """Search for a player - Returns COMPLETE player data with stats"""
    try:
        data = request.json
        uid = data.get('uid')
        region = data.get('region', 'BD')

        if not uid:
            return jsonify({"error": "UID is required"}), 400

        # Run async function in sync context
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        player_data = loop.run_until_complete(
            search_player(uid, region.lower()))
        loop.close()

        stats["total_searches"] += 1

        if player_data and "basicInfo" in player_data:
            stats["total_players_found"] += 1
            basic = player_data["basicInfo"]
            
            # Return comprehensive data
            return jsonify({
                "success": True,
                "data": player_data,
                "summary": {
                    "nickname": basic.get("nickname", "Unknown"),
                    "level": basic.get("level", 0),
                    "likes": basic.get("liked", 0),
                    "exp": basic.get("exp", 0),
                    "region": region.upper(),
                    "uid": uid
                }
            })
        else:
            return jsonify({
                "success": False,
                "error": "Player not found"
            }), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/like', methods=['POST'])
def api_like():
    """Send likes to a player"""
    try:
        data = request.json
        target_uid = data.get('uid')
        region = data.get('region', 'BD')
        num_likes = int(data.get('num_likes', 100))

        if not target_uid:
            return jsonify({"error": "UID is required"}), 400

        # Limit to prevent abuse
        num_likes = min(num_likes, 100)

        # Select random bot accounts
        import random
        selected_bots = random.sample(LIKE_BOT_ACCOUNTS,
                                      min(num_likes, len(LIKE_BOT_ACCOUNTS)))

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        results = {"total": len(selected_bots), "success": 0, "failed": 0}

        for bot_uid, bot_password in selected_bots:
            try:
                success = loop.run_until_complete(
                    send_like_to_player(target_uid, bot_uid, bot_password,
                                        region.lower()))
                if success:
                    results["success"] += 1
                    stats["total_likes_sent"] += 1
                else:
                    results["failed"] += 1
            except:
                results["failed"] += 1

        loop.close()

        return jsonify({"success": True, "results": results})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/likecount', methods=['POST'])
def api_likecount():
    """Get ONLY like count - Fast and minimal response"""
    try:
        data = request.json
        uid = data.get('uid')
        region = data.get('region', 'BD')

        if not uid:
            return jsonify({"error": "UID is required"}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Only fetch like count - faster than full player search
        like_count = loop.run_until_complete(
            get_like_count(uid, region.lower()))
        
        loop.close()

        if like_count is not None:
            return jsonify({
                "success": True,
                "uid": uid,
                "likes": like_count,
                "region": region.upper(),
                "formatted_likes": f"{like_count:,}"  # Formatted with commas
            })
        else:
            return jsonify({
                "success": False,
                "error": "Failed to get like count or player not found"
            }), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/regions', methods=['GET'])
def api_regions():
    """Get list of supported regions"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        regions = loop.run_until_complete(get_all_regions())
        loop.close()

        return jsonify({"success": True, "regions": regions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """Get bot statistics"""
    uptime = (datetime.now() - stats["server_start_time"]).total_seconds()
    hours = int(uptime // 3600)
    minutes = int((uptime % 3600) // 60)

    return jsonify({
        "success": True,
        "stats": {
            **stats, "total_bots":
            len(LIKE_BOT_ACCOUNTS),
            "uptime":
            f"{hours}h {minutes}m",
            "server_start_time":
            stats["server_start_time"].strftime("%Y-%m-%d %H:%M:%S")
        }
    })


@app.route('/api/bot/status', methods=['GET'])
def api_bot_status():
    """Check if main bot is running"""
    return jsonify({
        "success": True,
        "bot_running": True,
        "total_bots": len(LIKE_BOT_ACCOUNTS)
    })


@app.route('/api/bulk_like', methods=['POST'])
def api_bulk_like():
    """Send bulk likes using advanced system with detailed stats"""
    try:
        import time
        start_time = time.time()
        
        data = request.json
        target_uid = data.get('uid')
        region = data.get('region', 'BD')
        num_likes = int(data.get('num_likes', 100))
        # Always use Advanced Procur Mode
        use_future = True

        if not target_uid:
            return jsonify({"error": "UID is required"}), 400

        # Limit to prevent abuse
        num_likes = min(num_likes, len(LIKE_BOT_ACCOUNTS))

        # Select bot accounts
        import random
        selected_bots = random.sample(LIKE_BOT_ACCOUNTS, num_likes)

        print(f"\n{'='*60}")
        print(f"🚀 LIKE SENDING OPERATION INITIATED")
        print(f"{'='*60}")
        print(f"🎯 Target UID: {target_uid}")
        print(f"🌍 Region: {region.upper()}")
        print(f"📊 Total Likes: {num_likes}")
        print(f"🔮 Advanced Procur Mode: ENABLED")
        print(f"{'='*60}\n")

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        results = loop.run_until_complete(
            send_bulk_likes(target_uid,
                            selected_bots,
                            region.lower(),
                            use_future=use_future))

        loop.close()

        elapsed_time = time.time() - start_time
        stats["total_likes_sent"] += results["success"]

        print(f"\n{'='*60}")
        print(f"✅ OPERATION COMPLETED")
        print(f"{'='*60}")
        print(f"✅ Successful: {results['success']}")
        print(f"❌ Failed: {results['failed']}")
        print(f"📊 Total: {results['total']}")
        print(f"⏱️  Time: {elapsed_time:.2f}s")
        print(f"⚡ Rate: {results['success']/elapsed_time:.1f} likes/sec")
        print(f"{'='*60}\n")

        return jsonify({
            "success": True, 
            "results": {
                **results,
                "elapsed_time": round(elapsed_time, 2),
                "rate": round(results['success']/elapsed_time, 1) if elapsed_time > 0 else 0
            }
        })

    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}\n")
        return jsonify({"error": str(e)}), 500


@app.route('/api/player_info', methods=['POST'])
def api_player_info():
    """Get BASIC player profile - Name, Level, UID only (lightweight)"""
    try:
        data = request.json
        uid = data.get('uid')
        region = data.get('region', 'BD')

        if not uid:
            return jsonify({"error": "UID is required"}), 400

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Get only basic info - nickname and level
        nickname = loop.run_until_complete(
            get_player_nickname(uid, region.lower()))
        level = loop.run_until_complete(
            get_player_level(uid, region.lower()))

        loop.close()

        if nickname and level is not None:
            return jsonify({
                "success": True,
                "uid": uid,
                "nickname": nickname,
                "level": level,
                "region": region.upper(),
                "profile_url": f"https://ff.garena.com/player/{uid}"
            })
        else:
            return jsonify({
                "success": False,
                "error": "Player not found or data unavailable"
            }), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    print("\n" + "=" * 50)
    print("🚀 FREE FIRE BOT WEB DASHBOARD")
    print("=" * 50)
    print(f"📊 Total Bot Accounts: {len(LIKE_BOT_ACCOUNTS)}")
    print(f"🌐 Server: http://0.0.0.0:5000")
    print(f"⚡ Status: Running")
    print(f"🔥 Advanced Features: Enabled")
    print("=" * 50 + "\n")

    # Bind to 0.0.0.0 so it's accessible externally on Replit
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
