from pymongo import MongoClient
from datetime import timedelta
client = MongoClient('mongodb://deadlinerepo019.gpurender.vdi:27100/')
db = client.deadline10db
collection = db.JobStatistics
for job in collection.find():
    print('\t'.join((
        job['_id'],
        job['User'],
        (job['DateComp'] + timedelta(hours=8)).isoformat(),
        job['TtlRender'],
    )))
