# Gerbil Experiment Api Wrapper Service

This web service aims to automate the generation of benchmark results with Gerbil for QA 
using [GerbilExperimentApiWrapper](https://pypi.org/project/gerbil-api-wrapper/).

Public DockerHub image: https://hub.docker.com/r/heipa/gerbil-wrapper-service


## Building and Running the Service

This repository includes a `docker-compose.yml` file for easy deployment using Docker.

Use the 'environment' section to define configuration parameters like the port to be used. 

Build the docker image with `docker-compose build`,
then start the service with `docker-compose up`


## Endpoints

- `/health`: GET -- returns "alive" if the service is running
- `/about`: GET -- returns a short description of the service
- `/startexperiment`: POST -- starts an experiment with the specified datasets
- `/resultjsonld`: GET (with argument) -- returns experiment results in JSON-LD format


## Parameters

The web service expects the same parameters as the GerbilExperimentApiWrapper.
Besides the required gold standard dataset you need to specify either 
a local file with test results **or** 
a live annotator.

Parameters are passed as form-data.

- language: (required) The question language
- gold_standard_file: (required) The path to a gold standard dataset
- gold_standard_name: (optional) The name of the gold standard dataset
- test_results_file: (optional) The path to a test result dataset to be used *instead* of a live annotator
- test_results_name: (optional) The name of the test results dataset
- live_annotator_name: (optional) The name of a live annotator to be used *instead* of local test results; requires a value for 'live_annotator_url'
- live_annotator_url: (optional) The URL for a live annotator; requires a value for 'live_annotator_name'


## Examples

To start an experiment with local files only (with custom dataset names):
```bash
curl -X POST \
-F gold_standard=@results_gold.json \
-F gold_standard_name='GoldStandard' \
-F test_results=@result_test.json \
-F test_results_name='TestResults' \
-F language=en  \
'localhost:8080/startexperiment' \
-H 'Content-Type:multipart/form-data'
```

To start an experiment using a live annotator:
```bash
curl -X POST \
-F gold_standard=@results_gold.json \
-F live_annotator_url='http://porque.cs.upb.de:40123/qanswer/gerbil' \
-F live_annotator_name='QAnswer' \
-F language=en  \
'localhost:8080/startexperiment' \
-H 'Content-Type:multipart/form-data'
```


## Viewing Results

A successful POST request to `/startexperiment` will return a url with results for the started
experiment, including the experiment ID. 
This id can be passed as argument in a GET request to the `/resultjsonld` endpoint
to retrieve the results in JSON-LD format. 

**Note**: It might take some time for the results to be computed and displayed. 

```bash
curl localhost:8080/resultjsonld?experimentId=<experimentId>
```
