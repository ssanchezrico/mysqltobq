import mysql.connector
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

class MySQLToBigQueryLoader:
    def __init__(self, mysql_config, bq_credentials_path, project_name, layer):
        self.mysql_config = mysql_config
        self.bq_credentials = service_account.Credentials.from_service_account_file(bq_credentials_path)
        self.bq_client = bigquery.Client(credentials=self.bq_credentials, project=self.bq_credentials.project_id)
        self.project_name = project_name
        self.layer = layer
        self.cursor = None
        self.connection = None

    def load_table(self, mysql_table, bq_table_id, columns, where_clause=None, limit=None):
        self._connect()
        rows = self._get_origin_data(columns, mysql_table, where_clause, limit)
        self._close_connection()
        # Crear DataFrame de pandas
        data_frame = pd.DataFrame(rows, columns=columns.keys())
        # Configurar el esquema de BigQuery
        schema = [bigquery.SchemaField(name, dtype, mode="NULLABLE") for name, dtype in columns.items()]
        # Cargar los datos a BigQuery
        self._create_dataset(self.layer)
        self._load_data_in_big_query(schema, data_frame, bq_table_id)
        print(f"Datos cargados correctamente en {bq_table_id}")

    def _create_dataset(self, dataset_name):
        dataset = bigquery.Dataset(self.bq_client.dataset(dataset_name))
        dataset.location = "EU"
        dataset = self.bq_client.create_dataset(dataset, exists_ok=True)

    def _connect(self):
        self.connection = mysql.connector.connect(**self.mysql_config)
        self.cursor = self.connection.cursor()
    
    def _close_connection(self):
        self.cursor.close()
        self.connection.close()

    def _get_origin_data(self, columns, mysql_table, where_clause, limit):
        sql_query = f"SELECT {', '.join(columns.keys())} FROM {mysql_table}"
        if where_clause:
            sql_query += f" WHERE {where_clause}"
        if limit:
            sql_query += f" LIMIT {limit}"        
        self.cursor.execute(sql_query)
        rows = self.cursor.fetchall()
        return rows
    
    def _load_data_in_big_query(self, schema, data_frame, bq_table_id):
        job_config = bigquery.LoadJobConfig(schema=schema)
        job_config.write_disposition = bigquery.WriteDisposition.WRITE_TRUNCATE
        load_job = self.bq_client.load_table_from_dataframe(data_frame, bq_table_id, job_config=job_config)
        load_job.result()  # Esperar a que el trabajo termine

