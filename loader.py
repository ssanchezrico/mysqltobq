import json
from mysql_to_bq_loader import MySQLToBigQueryLoader
class Loader:
    def __init__(self):
        credentials_path = '.credentials/'
        config_path = 'config/'
        
        mysql_config_credentials_file = credentials_path + 'goohtel.json'
        bq_credentials_file = credentials_path + 'data-quality-438007-29aa669d743b.json'
        config_file = config_path + 'config.json'

        with open(mysql_config_credentials_file) as file:
            mysql_config = json.load(file)

        with open(config_file) as file:
            config = json.load(file)

        self.project_name = config['project_name']
        self.layer = config['layer']
        self.datasets_file = config['datasets_file']
        self.mtq_loader = MySQLToBigQueryLoader(mysql_config, bq_credentials_file, self.project_name, self.layer)

    def __main__(self):
        with open(self.datasets_file, 'r') as file:
            datasets = json.load(file)

        for dataset in datasets['datasets']:
            dataset_name = dataset['name']
            full_name = f"{self.project_name}.{self.layer}.{dataset_name}"
            columns = dataset['columns']
            where = None
            if 'where' in dataset:
                where = dataset['where']
            self.mtq_loader.load_table(dataset_name, full_name, columns, where)

if __name__ == "__main__":
    loader = Loader()
    loader.__main__()