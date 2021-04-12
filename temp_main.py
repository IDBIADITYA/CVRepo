# Press the green button in the gutter to run the script.
import random
import sys
import os

from flask import Flask, jsonify, request
from flask_cors import CORS

from db_utility.queries import get_applicant
from service import fetch_scores
from util.classifier import cosine_match
from util.helper import *
from db_utility.connect import Oracle

from dotenv import load_dotenv

app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

load_dotenv()


@app.route('/', methods=['GET'])
def index():
	return jsonify(success(result={}))


@app.route('/match-cv', methods=['POST'])
def match_cv():
	"""
	df1 : job_id, JD
	df2 : resume (all the resumes against on JD), applicant_id
	:return:
	"""
	try:
		if request.method == "POST":
			print("----------------------------------------------------------------------------")
			res = "Sample_CVs/sample_12.docx"
			job_description = 'JD_Sample/python_dev_1.docx'
			db_creds = {
				"username": os.getenv("username"),
				"password": os.getenv("password"),
				"database": os.getenv("database"),
				"host": os.getenv("host"),
				"port": os.getenv("port")
			}
			conn = Oracle(db_creds)
			sql = get_applicant()
			data = conn.run_query(sql)
			print(data)
			matchPercentage = fetch_scores(res, job_description)
			# print("Your resume matches about " + str(matchPercentage) + "% of the job description.")
			data = {
				"job_id": random.randint(1, 100000),
				"scores": matchPercentage
			}
			# data.append({
			# 	"job_id": random.randint(1, 100000),
			# 	"applicant_id": random.randint(1, 100000),
			# 	"matching_score": matchPercentage
			# })
			return success(result=data)
		return error(result={}, message="Bad Request!", code=400)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		line_number = exc_tb.tb_lineno
		return error(result={}, message="Bad Request!",
					 errors=["key: Error" + str(e), "File: " + fname, "Line Number: {}".format(line_number)], code=400)


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=5000, threaded=True)

