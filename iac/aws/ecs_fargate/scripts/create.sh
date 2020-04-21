aws cloudformation create-stack \
    --stack-name refget-insdc \
    --template-body file://template.yaml \
    --parameters file://scripts/private-parameters.json