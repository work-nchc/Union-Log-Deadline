from pymongo import MongoClient
from datetime import timedelta
client = MongoClient('mongodb://deadlinerepo019.gpurender.vdi:27100/')
db = client.deadline10db
collection = db.JobStatistics

with open('log_db.csv', 'w') as output:
    {output.write('\t'.join((
        job['_id'],
        job['User'],
        (job['DateComp'] + timedelta(hours=8)).isoformat(),
        job['TtlRender'],
    )) + '\n') for job in collection.find()}
