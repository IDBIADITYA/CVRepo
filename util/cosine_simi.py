import numpy as np
import pandas as pd
import sparse_dot_topn.sparse_dot_topn as ct
from scipy.sparse import csr_matrix


def tf_idv_vec(train_i, actual_i):
	# count vectorizer
	from sklearn.feature_extraction.text import CountVectorizer
	count_vect = CountVectorizer()
	train_i = count_vect.fit_transform(train_i)
	actual_i = count_vect.transform(actual_i)

	# tf-idf score
	from sklearn.feature_extraction.text import TfidfTransformer
	tfidf_transformer = TfidfTransformer()
	train_i = tfidf_transformer.fit_transform(train_i)
	actual_i = tfidf_transformer.transform(actual_i)
	
	return train_i, actual_i


def awesome_cossim_top(A, B, ntop, lower_bound=0):
	# force A and B as a CSR matrix.
	# If they have already been CSR, there is no overhead
	A = A.tocsr()
	B = B.tocsr()
	M, _ = A.shape
	_, N = B.shape

	idx_dtype = np.int32
	nnz_max = M*ntop

	indptr = np.zeros(M+1, dtype=idx_dtype)
	indices = np.zeros(nnz_max, dtype=idx_dtype)
	data = np.zeros(nnz_max, dtype=A.dtype)

	ct.sparse_dot_topn(
		M, N, np.asarray(A.indptr, dtype=idx_dtype),
		np.asarray(A.indices, dtype=idx_dtype),
		A.data,
		np.asarray(B.indptr, dtype=idx_dtype),
		np.asarray(B.indices, dtype=idx_dtype),
		B.data,
		ntop,
		lower_bound,
		indptr, indices, data)

	return csr_matrix((data,indices,indptr),shape=(M,N))


def get_matches_df(sparse_matrix, name_vectorQ, name_vectorR, resume_id_list, top=100):
	non_zeros = sparse_matrix.nonzero()
	
	sparserows = non_zeros[0]
	sparsecols = non_zeros[1]
	
	if top<sparsecols.size:
		nr_matches = top
	else:
		nr_matchesQ = sparserows.size
		nr_matchesR =sparsecols.size
	
	# resume = np.empty([nr_matchesQ], dtype=object)
	# left_side = np.empty([nr_matchesQ], dtype=object)
	resume = np.empty([nr_matchesQ], dtype=object)
	right_side = np.empty([nr_matchesQ], dtype=object)
	resume_id = np.empty([nr_matchesQ], dtype=object)
	similarity = np.zeros(nr_matchesQ)
	
	for index in range(0, nr_matchesQ):
		# print(index, sparserows[index], name_vector[sparserows[index]])
		# left_row[index] = sparserows[index]
		# right_row[index] = sparsecols[index]

		resume_id[index] = resume_id_list[sparserows[index]]  # append this value in below dataframe
		
		resume[index] = name_vectorQ[sparserows[index]]
		right_side[index] = name_vectorR[sparsecols[index]]
		similarity[index] = sparse_matrix.data[index]
	
	return pd.DataFrame(
			{
				'resume_id': resume_id,
				'resume': resume,
				'job_description': right_side,
				'similarity': similarity
			}
		)


# either send me dataframe or list object  this is assume that it is list
def find_similarity(resumes, job_des, resume_id):
	# these are list eg: df.resumes.tolist() and df.job_des.tolist()
	resumes_t, job_des_t =  tf_idv_vec(resumes, job_des)
	
	# if job_des.getnnz() > 0:
	matches = awesome_cossim_top(resumes_t, job_des_t.transpose(), 10, 0.1)
	matches_df = get_matches_df(matches, resumes, job_des, resume_id, top=matches.size)

	return matches_df.sort_values(['similarity'], ascending=False)

