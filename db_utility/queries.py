

def get_resumes(jobid):
	return """
		select HRS_PERSON_ID, HRS_RCMNT_ID from SYSADM.ps_hrs_Rcmnt where hrs_job_opening_id = '{}'
	""".format(jobid)


def get_applicant():
	return """
		select * from SYSADM.ps_hrs_app_profile where hrs_person_id = '243936'  and hrs_profile_seq='1'
	"""

