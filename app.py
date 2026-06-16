from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/scan', methods=['POST'])
def scan():
    data = request.get_json()

    target = data.get("target")
    cve = data.get("cve")  # opcional

    if not target:
        return jsonify({"error": "No target provided"}), 400

    try:
        # Construir comando
        cmd = ["nuclei", "-u", target]

        if cve:
            cmd += ["-id", cve]

        # EJECUCIÓN CORRECTA (sin check_output, sin PIPE problemático)
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=300,
            bufsize=1
        )

        return jsonify({
            "status": "completed",
            "command": " ".join(cmd),
            "output": result.stdout
        })

    except subprocess.TimeoutExpired:
        return jsonify({
            "error": "Timeout executing nuclei"
        }), 504

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )