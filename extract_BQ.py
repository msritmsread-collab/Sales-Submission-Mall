import os
from google.cloud import bigquery
from google.oauth2 import service_account

class BigQueryHandler:
    def __init__(self,key_path):
        self.credentials = service_account.Credentials.from_service_account_file(key_path)
        self.client = bigquery.Client(credentials=self.credentials)


    def run_query(self, sql_query):
        try:
            query_job = self.client.query(sql_query)
            query_job.result()  # Wait for the query to finish
            data = query_job.to_dataframe()
            return data
        except Exception as e:
            print(f"Error running query: {e}")
            return None