# only run when refget-serverless virtual environment is active
cd layer
mkdir -p python
pip install --upgrade -r requirements.txt -t python
zip -r refget-serverless.zip python
aws s3 cp refget-serverless.zip s3://ga4gh-dependencies
