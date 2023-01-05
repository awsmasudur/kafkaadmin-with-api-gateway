# kafkaadmin-with-api-gateway

## Create a Lambda layer
Follow the below steps to create a Lambda layer with kafka-python client.
1. Create a folder called python
```
mkdir python
cd python
```
2. Run the following command from commandline. This will download all the required packages on the folder you created earlier.
```
pip install -t . kafka-python
```

3. Zip the folder

4. Run below command using [aws cli](https://aws.amazon.com/cli/) to crate the Lambda layer
```
aws lambda publish-layer-version --layer-name kafkaadmin --description "My layer" --zip-file fileb://python.zip --compatible-runtimes python3.6 python3.7 python3.8 
```

5. Note down the LayerARN. Sample:
```
"LayerArn": "arn:aws:lambda:ap-southeast-2:11111111111:layer:kafkaadmin"
```


## Create a Lambda function to connect with your MSK cluster
aws lambda create-function \
--function-name sayemkafkaadmin1 \
--runtime python3.8 \
--role arn:aws:iam::781228881515:role/sayemforklift \
--handler lambda_function.lambda_function \
--zip-file fileb://lambda_function.zip \
--vpc-config SubnetIds=subnet-09d6643161a698bf3,subnet-01f2f547e9f6f8dd3,subnet-0f1b0c5191e0d1863,SecurityGroupIds=sg-0c3fd09fce77c4211 \
--layers arn:aws:lambda:ap-southeast-2:781228881515:layer:kafkaadmin:6
