from flask import Flask, request, jsonify
from selenium import webdriver
import pickle
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import os
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

PASSWORD_SECRET = os.environ["PASSWORD_SECRET"]

MONGO_URI = os.environ['MONGODB']
client = MongoClient(MONGO_URI)
db = client['KPW']

resultCrawl = []

@app.route("/check-password", methods=["POST"])
def check_password():
    # Lấy dữ liệu từ yêu cầu JSON
    data = request.get_json()
    password = data.get("password")

    # Kiểm tra mật khẩu
    if password == PASSWORD_SECRET:
        return jsonify(success=True, message="Đúng mật khẩu!")
    else:
        return jsonify(success=False, message="Sai mật khẩu!"), 401

@app.route("/")
def index():
    return "Hello, world!"

@app.route("/check-password", methods=["POST"])
def check_password():
    data = request.get_json()
    password = data.get("password")

    if password == PASSWORD_SECRET:
        return jsonify(success=True, message="Đúng mật khẩu!")
    else:
        return jsonify(success=False, message="Sai mật khẩu!"), 401

@app.route("/crawl", methods=["POST"])
def crawl():
    request_url = data.get("group_url")
    num_of_post = data.get("num_of_post")
    typeCrawl = data.get("type_crawl")
    date_time = data.get("date_time")

    # Khởi chạy worker.py với các tham số
    result = subprocess.run(
        ["python", "worker.py", request_url, str(num_of_post), typeCrawl, date_time],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify(success=False, message="Đã xảy ra lỗi khi chạy worker.py"), 500

    resultCrawl = result.stdout
    return jsonify(success=True, resultCrawl=resultCrawl)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
