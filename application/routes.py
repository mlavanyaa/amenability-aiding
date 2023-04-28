from application import app
from flask import render_template, request, json, jsonify
from sklearn import preprocessing
from sklearn.preprocessing import OneHotEncoder
import requests
import numpy
import pandas as pd
import pymysql.cursors

connection = pymysql.connect(host='cvedata.c7q49490bvb2.us-east-1.rds.amazonaws.com',
                             user='admin',
                             password='Reddy#98',
                             database='cve_data',
                             cursorclass=pymysql.cursors.DictCursor)

vendorlis=[]

# with connection:
with connection.cursor() as cursor:
    sql = "select Vendor from my_data_with_ref"
    cursor.execute(sql)
    result = cursor.fetchall()
    for i in result:
        if i['Vendor'] not in vendorlis:
            vendorlis.append(i['Vendor'])
        
    #decorator to access the app
    @app.route("/")
    @app.route("/index", methods=['POST', 'GET'])
    def index():
        return render_template("index.html", vendorlis=vendorlis)

    @app.route('/process_input', methods=['POST'])
    def process_input():
        selected_item = request.form['selected_item']
        with connection.cursor() as cursor:
            sql = "select * from my_data_with_ref where Vendor='"
            sql1=sql+selected_item+"'"
            # print(sql1)
            cursor.execute(sql1)
            # print("query executed")
            result = cursor.fetchall()
            # print(result)
            return render_template("result.html",result=result,selected_item=selected_item)
