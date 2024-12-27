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
from celeryapp import perform_crawl

app = Flask(__name__)
CORS(app)

PASSWORD_SECRET = os.environ["PASSWORD_SECRET"]

@app.route("/")
def index():
    return "Hello, world!"

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

@app.route("/task_status/<task_id>", methods=["GET"])
def task_status(task_id):
    task = perform_crawl.AsyncResult(task_id)
    if task.ready():
        return jsonify({
            'task_id': task_id,
            'status': task.status,
            'result': task.result
        })
    else:
        return jsonify({
            'task_id': task_id,
            'status': task.status,
            'result': None
        })

@app.route("/crawl", methods=["POST"])
def crawl():
    # Lấy thông tin từ request
    request_url = request.form.get('group_url')
    num_of_post = int(request.form.get('num_of_post'))
    typeCrawl = request.form.get('type_crawl')
    date_time = request.form.get('date_time')

    # Gửi tác vụ đến Celery
    task = perform_crawl.apply_async(args=[request_url, num_of_post, typeCrawl, date_time])

    # Trả về ID của tác vụ cho client
    return jsonify({"task_id": task.id}), 202

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
