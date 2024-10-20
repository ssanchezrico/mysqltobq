import json
from mysql_to_bq_loader import MySQLToBigQueryLoader

credentials_path = '.credentials/'
config_path = 'config/'
mysql_config_credentials_file = credentials_path + 'goohtel.json'
bq_credentials_file = credentials_path + 'data-quality-438007-29aa669d743b.json'
config_file = config_path + 'config.json'

with open(mysql_config_credentials_file) as file:
    mysql_config = json.load(file)

with open(config_file) as file:
    config = json.load(file)

project_name = config['project_name']
layer = config['layer']
datasets_file = config['datasets_file']
loader = MySQLToBigQueryLoader(mysql_config, bq_credentials_file, project_name, layer)

with open(datasets_file, 'r') as file:
    datasets = json.load(file)

for dataset in datasets['datasets']:
    dataset_name = dataset['name']
    full_name = f"{project_name}.{layer}.{dataset_name}"
    columns = dataset['columns']
    where = None
    if 'where' in dataset:
        where = dataset['where']
    loader.load_table(dataset_name, full_name, columns, where)

