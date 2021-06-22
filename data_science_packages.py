from urllib import parse
import requests
import sys
import json
from datetime import datetime
import os
from github import Github

repos_url = [
    'https://github.com/pandas-dev/pandas'
    ,'https://github.com/dask/dask'
    ,'https://github.com/h2oai/datatable'
    ,'https://github.com/man-group/dtale'
    ,'https://github.com/EpistasisLab/tpot'
    ,'https://github.com/microsoft/nni'
    ,'https://github.com/automl/auto-sklearn'
    ,'https://github.com/ClimbsRocks/auto_ml'
    ,'https://github.com/HDI-Project/ATM'
    ,'https://github.com/automl/SMAC3'
    ,'https://github.com/HDI-Project/BTB'
    ,'https://github.com/keras-team/keras'
    ,'https://github.com/pytorch/pytorch'
    ,'https://github.com/BVLC/caffe'
    ,'https://github.com/fastai/fastai'
    ,'https://github.com/microsoft/CNTK'
    ,'https://github.com/dmlc/xgboost'
    ,'https://github.com/microsoft/LightGBM'
    ,'https://github.com/catboost/catboost'
    ,'https://github.com/RGF-team/rgf'
    ,'https://github.com/scikit-garden/scikit-garden'
    ,'https://github.com/manifoldai/merf'
    ,'https://github.com/jundongl/scikit-feature'
    ,'https://github.com/EpistasisLab/ReBATE'
    ,'https://github.com/tensorflow/tensorflow'
    ,'https://github.com/scikit-learn/scikit-learn'
    ,'https://github.com/scikit-learn-contrib/imbalanced-learn'
    ,'https://github.com/rasbt/mlxtend'
    ,'https://github.com/biolab/orange3'
    ,'https://github.com/hmmlearn/hmmlearn'
    ,'https://github.com/amueller/dabl'
    ,'https://github.com/TeamHG-Memex/eli5'
    ,'https://github.com/marcotcr/lime'
    ,'https://github.com/DistrictDataLabs/yellowbrick/'
    ,'https://github.com/reiinakano/scikit-plot'
    ,'https://github.com/cortexlabs/cortex'
    ,'https://github.com/huggingface/transformers'
    ,'https://github.com/explosion/spaCy'
    ,'https://github.com/RaRe-Technologies/gensim'
    ,'https://github.com/nltk/nltk'
    ,'https://github.com/allenai/allennlp'
    ,'https://github.com/sloria/TextBlob'
    ,'https://github.com/stanfordnlp/stanfordnlp'
    ,'https://github.com/PKSHATechnology-Research/camphr'
    ,'https://github.com/numpy/numpy'
    ,'https://github.com/scipy/scipy/'
    ,'https://github.com/pymc-devs/pymc3'
    ,'https://github.com/statsmodels/statsmodels'
    ,'https://github.com/bokeh/bokeh'
    ,'https://github.com/matplotlib/matplotlib'
    ,'https://github.com/mwaskom/seaborn'
    ,'https://github.com/plotly/plotly.py'
    ,'https://github.com/altair-viz/altair'
    ,'https://github.com/pyviz/holoviews'
    ,'https://github.com/stanfordnlp/stanza'
    ,'https://github.com/firmai/deltapy'
    ,'https://github.com/ResidentMario/missingno'
    ,'https://github.com/pycaret/pycaret'
    ,'https://github.com/pandas-profiling/pandas-profiling'
    ,'https://github.com/spotify/chartify'
    ,'https://github.com/PrefectHQ/prefect'
    ,'https://github.com/Netflix/metaflow'
    ,'https://github.com/plotly/dash'
	]

def query_repo(g, author, repo):
	qry_string = author + "/" + repo
	repo = g.get_repo(qry_string)
	# github.PaginatedList.PaginatedList of github.GitRelease.GitRelease
	releases = repo.get_releases()
	last_release = datetime(1900,1,1)

	for rel in releases:
		rel_pub_dt = rel.published_at
		if rel_pub_dt > last_release:
			last_release = rel_pub_dt
	lr_str = last_release.strftime('%Y-%m-%d')
	return repo.created_at.strftime('%Y-%m-%d'), lr_str , repo.stargazers_count, repo.forks_count



def parse_repo(repo_url):
	parsed_url = parse.urlparse(repo_url)
	url_path = parsed_url[2]
	path_split = url_path.split("/")
	author = path_split[1]
	repo = path_split[2]
	return author, repo


def parse_github_response(gh_response):
	json_data = json.loads(gh_response.text)
	create_date_str = json_data['created_at']
	create_date_str = datetime.strptime(create_date_str, '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d')

	repo_watchers = json_data['watchers']
	repo_forks = json_data['forks']
	return create_date_str, repo_watchers, repo_forks


if __name__ == "__main__":
	g = Github(os.environ['GITHUB_PERSONAL_ACCESS_TOKEN'])

	for r in repos_url:
		author, repo = parse_repo(r)
		created_at, latest_rel_at, stars, forks = query_repo(g, author, repo)
		print(r, author, repo, created_at, latest_rel_at, stars, forks)
