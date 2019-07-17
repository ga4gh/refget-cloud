cd layer
pip freeze > python/requirements.txt
pip install --upgrade -r python/requirements.txt -t python
zip -r refget-serverless.zip python
aws s3 cp refget-serverless.zip s3://ga4gh-dependencies