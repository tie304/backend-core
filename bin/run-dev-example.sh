export database_name=test
export database_user=test
export database_password=1234
export database_host=localhost
export jwt_key=qwer
export sendgrid_api_key=
export sendgrid_sender=tylerhanson921@gmail.com
export product_name="test-product"
export product_ingress_host=http://localhost:8000
export aws_access_key=
export aws_secret_key=
export aws_bucket_name=test-bucket-84823vj44in4
uvicorn main:app --port 8000 --reload
