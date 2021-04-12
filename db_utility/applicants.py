
class Applicant:
	def __init__(self, applicant_table):
		self.applicant_profile = None
		self.applicant = None
		self.applicant_exp = None
		self.resumes = None
		self.jobs = None

	def get_applicant_experience(self):
		return True

	def get_applicant_academics(self):
		return True

	def get_cvs_against_single_job(self, job_id):
		return True

	def get_single_applicant_info(self):
		return True

	def get_notice_period(self):
		return True
