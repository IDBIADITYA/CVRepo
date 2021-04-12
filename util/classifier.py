#!/usr/bin/env python
# coding: utf-8
import sys

import docx2txt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from util.preprocessing import PreProcessing
import numpy as np
from util.cosine_simi import find_similarity
import pandas as pd
import glob
import random
from util.helper import *
import os

from util.resume_parser import get_document_content, get_txt_from_pdf


removable = [
	"JOB DESCRIPTION",
	"PURPOSE OF THE JOB",
	"Job Context",
	"Challenges",
	"DETAILS OF THE JOB",
	"Designation & Job",
	"Level",
	"Business Unit",
	"Function",
	"Country",
	"Work Location",
	"Reporting Manager",
	"Manager’s Manager",
	"Matrix Manager",
	"Team Size",
	"Direct Reportees",
	"KEY ACCOUNTABILITIES",
	"Training & Development",
	"KEY INTERFACES",
	"EDUCATION & EXPERIENCE",
	"Desired Certifications",
	"Experience Range",
	"Desirable experience",
	"SKILLS REQUIRED",
	"Skills",
	"Description",
	"Behavioral Skills"
]


def levenshtein_matching(s, t, ratio_calc=True):
	# Initialize matrix of zeros
	rows = len(s) + 1
	cols = len(t) + 1
	distance = np.zeros((rows, cols), dtype=int)

	# Populate matrix of zeros with the indices of each character of both strings
	for i in range(1, rows):
		for k in range(1, cols):
			distance[i][0] = i
			distance[0][k] = k

	# Iterate over the matrix to compute the cost of deletions,insertions and/or substitutions
	for col in range(1, cols):
		for row in range(1, rows):
			if s[row - 1] == t[col - 1]:
				# If the characters are the same in the two strings in a given position [i,j] then the cost is 0
				cost = 0  #
			else:
				# In order to align the results with those of the Python Levenshtein package, if we choose to calculate the ratio
				# the cost of a substitution is 2. If we calculate just distance, then the cost of a substitution is 1.
				if ratio_calc:
					cost = 2
				else:
					cost = 1
			distance[row][col] = min(distance[row - 1][col] + 1,  # Cost of deletions
									 distance[row][col - 1] + 1,  # Cost of insertions
									 distance[row - 1][col - 1] + cost)  # Cost of substitutions
	if ratio_calc:
		# Computation of the Levenshtein Distance Ratio
		Ratio = ((len(s) + len(t)) - distance[row][col]) / (len(s) + len(t))
		return Ratio * 100
	else:
		# insertions and/or substitutions
		# This is the minimum number of edits needed to convert string a to string b
		return False


# Cosine Similarity Algo
def cosine_match(resume, job_desc, filename=None):
	final_result = []
	try:
		preprocess = PreProcessing()

		# Cleaning up resumes
		resume = preprocess.clean_text(resume)
		res_temp = resume
		resume = " ".join(resume)

		# Store the job description into a variable
		job_desc = preprocess.clean_text(job_desc)
		# temp_jd = job_desc

		# Cleaning up JD
		# job_desc = job_desc.split(" ")
		# for words in removable:
		# 	if words in job_desc:
		# 		job_desc.remove(words)

		job_desc = " ".join(job_desc)

		resume_temp = [i for i in res_temp if i in job_desc]
		resume_temp = " ".join(resume_temp)

		# A list of text
		text = [resume, job_desc]

		# Temporary Arrangement
		resume = [resume_temp]
		job_desc = [text[1]]
		job_id = [123]

		try:
			df_results = find_similarity(resume, job_desc, job_id)
			results = df_results.to_dict('records')
			for res in results:
				temp = {
					"filename": filename,
					"applicant_id": random.randint(1, 100000), #res["resume_id"],
					"score": round(res["similarity"]*100, 2)
				}
				final_result.append(temp)
		except Exception as e:
			print(str(e))

		return final_result

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		line_number = exc_tb.tb_lineno
		return error(result={}, message="Bad Request!",
					 errors=["key: Error" + str(e), "File: " + fname, "Line Number: {}".format(line_number)], code=400)

