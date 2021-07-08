export database_name=test
export database_user=test
export database_password=1234
export database_host=localhost
export jwt_key=qwer
export sendgrid_api_key=
export sendgrid_sender=tylerhanson921@gmail.com

uvicorn main:app --port 8000 --reload
