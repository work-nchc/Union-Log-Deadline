from datetime import datetime

logname_db = input('db log: ')
logname_api = input('api log: ')
logname_filtered = input('filtered log output: ')
logname_err = input('error output: ')
maxlim_time = datetime.strptime(
    input('max limit of date YYYY-mm-dd (excluded): '), '%Y-%m-%d')
empty_time = datetime(1, 1, 1)

with open(logname_db) as log_db:
    jobs_db = {job.split()[0]: job.split()[1:] + [job] for job in log_db}
with open(logname_api) as log_api:
    jobs_api = {job.split()[0]: job.split()[1:] + [job] for job in log_api}

all_id = set(jobs_db) | set(jobs_api)
log_filtered = []

# error types
miss_api = []
empty_db = []
empty_api = []
neg_db = []
neg_api = []
diff_name = []
diff_time = []
diff_usage = []

for id_job in all_id:
    username = ''

    date_db = empty_time
    ticks_db = 0
    if id_job in jobs_db:
        username = jobs_db[id_job][0]
        date_db = datetime.strptime(
            jobs_db[id_job][1].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        
        hours, minutes, seconds = jobs_db[id_job][2].split(':')
        if '-' in hours:
            hours = hours.replace('-', '')
        if '.' in hours:
            days, hours = map(int, hours.split('.'))
        else:
            days = 0
            hours = int(hours)
        minutes = int(minutes)
        if '.' in seconds:
            seconds, ticks = map(int, seconds.split('.'))
        else:
            seconds = int(seconds)
            ticks = 0
        ticks_db = ticks + 10 ** 7 * (
            seconds + 60 * (minutes + 60 * (hours + 24 * days)))
        if '-' in jobs_db[id_job][2]:
            ticks_db *= -1
    
    date_api = empty_time
    ticks_api = 0
    if id_job in jobs_api:
        username = jobs_api[id_job][0]
        date_api = datetime.strptime(
            jobs_api[id_job][1].split('.')[0], '%Y-%m-%dT%H:%M:%S')
        
        ticks_api = int(jobs_api[id_job][2])
    
    if id_job in jobs_db and date_db >= maxlim_time:
        continue
    if id_job in jobs_api and date_api >= maxlim_time:
        continue
    
    if id_job in jobs_db:
        if ticks_db and date_db == empty_time:
            empty_db.append('empty_db\t' + jobs_db[id_job][-1])
        if ticks_db < 0:
            neg_db.append('neg_db\t' + jobs_db[id_job][-1])
    if id_job in jobs_api:
        if ticks_api and date_api == empty_time:
            empty_api.append('empty_api\t' + jobs_api[id_job][-1])
        if ticks_api < 0:
            neg_api.append('neg_api\t' + jobs_api[id_job][-1])
    else:
        miss_api.append('miss_api\t' + jobs_db[id_job][-1])

    if id_job in jobs_db and id_job in jobs_api:
        if jobs_db[id_job][1] != jobs_api[id_job][1]:
            diff_time.append('diff_time\t' + jobs_db[id_job][-1])
            diff_time.append('         \t' + jobs_api[id_job][-1])
        if ticks_db != ticks_api:
            diff_usage.append('diff_usage\t' + jobs_db[id_job][-1])
            diff_usage.append('          \t' + jobs_api[id_job][-1])
        if jobs_db[id_job][0] != jobs_api[id_job][0]:
            diff_name.append('diff_name\t' + jobs_db[id_job][-1])
            diff_name.append('         \t' + jobs_api[id_job][-1])
            continue
    
    ticks = max(ticks_db, ticks_api, 0)
    if ticks:
        log_filtered.append((max(date_db, date_api), username, ticks))

with open(logname_filtered, 'w') as output_filtered:
    [output_filtered.write(
        job[0].isoformat() + '\t' + job[1] + '\t' + str(job[2]) + '\n'
    ) for job in sorted(log_filtered)]

with open(logname_err, 'w') as output_err:
    output_err.writelines(miss_api)
    output_err.writelines(empty_db)
    output_err.writelines(empty_api)
    output_err.writelines(neg_db)
    output_err.writelines(neg_api)
    output_err.writelines(diff_name)
    output_err.writelines(diff_time)
    output_err.writelines(diff_usage)
