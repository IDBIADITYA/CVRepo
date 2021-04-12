#!/usr/bin/env python
# coding: utf-8
import os
import sys

import docx2txt

from util.classifier import cosine_match
from util.helper import *
from util.resume_parser import get_document_content, get_txt_from_pdf


def fetch_scores(resume, job_description):
	try:
		file_path = "sample_jll/PSADMIN/"
		ps_ad = os.listdir(file_path)
		job_description = "sample_jll/JD_for_psadmin.docx"

		# file_path = "sample_jll/PSDEVELOPER/"
		# ps_ad = os.listdir("sample_jll/PSDEVELOPER/")
		# job_description = "sample_jll/JD_for_ps_developer.docx"

		# file_path = "sample_jll/Head-Quality/"
		# ps_ad = os.listdir(file_path)
		# job_description = "sample_jll/JD_Head-Quality_Generics.docx"

		# file_path = "sample_jll/Manager_Design_n_Engineering/"
		# # os.system("lowriter --convert-to docx "+file_path+"/*.doc")
		# ps_ad = os.listdir(file_path)
		# job_description = "sample_jll/Manager_Design_n_Engineering.docx"

		final_res = []
		for resume in ps_ad:
			resume = "{}{}".format(file_path, resume)
			filename = resume
			temp = filename.split(".")[-1]
			try:
				# Reading the CV
				if temp.lower() == "pdf":
					resume = get_txt_from_pdf(resume)
				elif temp.lower() == "docx":
					# if filename.endswith(".doc") or filename.endswith(".DOC"):
					# 	doc_file = file_path + filename
					# 	resume = doc_file + 'x'
					# 	os.system('mv ' + doc_file + ' ' + resume)

					resume = docx2txt.process(resume)
				elif temp.lower() == "pptx":
					resume = get_document_content(resume)
			except:
				continue

			# Store the job description into a variable
			job_desc = docx2txt.process(job_description)

			result = cosine_match(resume, job_desc, filename=filename)
			temp = [res for res in result]
			if temp:
				final_res.extend(temp)

		return sorted(final_res, key=lambda i: i["score"], reverse=True)
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
		line_number = exc_tb.tb_lineno
		return error(result={}, message="Bad Request!",
					 errors=["key: Error" + str(e), "File: " + fname, "Line Number: {}".format(line_number)], code=400)

