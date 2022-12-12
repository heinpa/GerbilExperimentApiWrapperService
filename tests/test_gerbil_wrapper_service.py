from app.gerbil_wrapper_service import *
from app import app
from unittest.mock import patch
from unittest import TestCase
from werkzeug.datastructures import FileStorage

class TestService(TestCase):

    logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)

    # TODO: external config
    language = "en"
    gold_standard_file = "results_gold.json"
    test_results_file = "result_test.json"
    test_folder = "./tests/"

    gold_standard = FileStorage(
        stream=open(test_folder+gold_standard_file, "rb"),
        filename="results_gold.json"
    )
    test_results = FileStorage(
        stream=open(test_folder+test_results_file, "rb"),
        filename="result_test.json"
    )
    
#    def test_allowed_file(self):
#        assert False
#
#    def test_upload_file(self):
#        assert False
#
#    def test_start_experiment_with_live_annotator(self):
#        assert False

    def test_start_experiment_with_local_files(self):
        
        data = dict(
            gold_standard = self.gold_standard,
            test_results = self.test_results,
            language="en"
        )

        with app.test_client() as client, \
                patch('app.gerbil_wrapper_service.Gerbil') as mocked_Gerbil:

            # given
            mocked_Gerbil.return_value = None

            # when 
            client.post("/startexperiment", data=data, content_type="multipart/form-data")
            
            # then
            mocked_Gerbil.assert_called_with(language=self.language,
                                              gold_standard_file="./"+self.gold_standard_file,
                                              test_results_file="./"+self.test_results_file)

