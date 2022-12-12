import logging
from flask import Blueprint, jsonify, request, redirect 
from gerbil_api_wrapper.gerbil import Gerbil
from bs4 import BeautifulSoup
import requests
import json
from werkzeug.utils import secure_filename
import os


logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)
wrapper_service_bp = Blueprint('wrapper_service_bp', __name__, template_folder="templates")

get_experiment_url  = "http://gerbil-qa.aksw.org/gerbil/experiment?id="

upload_folder = "./"


## /startexperiment
#

def allowed_file(filename):
    return True


def upload_file(file):
    logging.info(f"called UPLOAD_FILE with file {file}")

    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_path = os.path.join(upload_folder, filename)
            file.save(upload_path)
            logging.info(f"saved file {filename} to {upload_path}")
            return upload_path


def delete_saved_files(files):
    for file in files:
        filename = files[file]
        logging.info(f"removed file: {filename}")
        os.remove(filename)


@wrapper_service_bp.route("/startexperiment", methods=['POST'])
def start_experiment():

    saved_files = dict()

    logging.info(f"files: {request.files}")

    # check file parts 
    if 'gold_standard' not in request.files and not('test_results' in request.files or 'live_annotator_name' in request.form):
        logging.info("incomplete")
        return redirect(request.url)

    # required
    gold_standard_upload = request.files['gold_standard']
    # optional
    test_results_upload = request.files.get('test_results')

    language = request.form["language"] 

    upload_path = upload_file(gold_standard_upload)
    saved_files["gold_standard"] = upload_path

    # optional 
    live_annotator_name = request.form.get("live_annotator_name")
    live_annotator_url =  request.form.get("live_annotator_url")

    gerbil = None

    # setup experiment with local files
    logging.info("setting up Gerbil experiment ...")
    if test_results_upload:
        upload_path = upload_file(test_results_upload)
        saved_files["test_results"] = upload_path 
        try: 
            gerbil = Gerbil(language=language, gold_standard_file=saved_files["gold_standard"], 
                            test_results_file=saved_files["test_results"])
            logging.info("setup experiment with local files")
            delete_saved_files(saved_files)
        except:
            # TODO: handle
            pass
    elif live_annotator_url:
        try:
            gerbil = Gerbil(language=language, gold_standard_file=saved_files["gold_standard"], 
                            live_annotator_name=live_annotator_name, 
                            live_annotator_url=live_annotator_url)
            logging.info("setup experiment with live annotator")
            delete_saved_files(saved_files)
        except:
            # TODO: handle
            pass
    else:
        raise Exception(f"Could not initialize GerbilBenchmarkService!"
                        + "Missing results file or live annotator.")

    if gerbil: 
        logging.info(f"experiment created: {gerbil.get_results_url()}")
        return jsonify(gerbil.get_results_url())
    else: 
        return redirect(request.url)


wrapper_service_bp.route("/getresultsjsonld", methods=["GET"])
def get_experiment_results_as_json_ld():
    args = request.args
    experiment_id = args.get("experimentId", "")

    query_url = get_experiment_url + experiment_id
    # extract json-ld from response content
    soup = BeautifulSoup(requests.get(query_url).text, "html.parser")
    data = [
        json.loads(x.string) for x in soup.find_all("script", type="application/ld+json")
    ]
    return data[0]



