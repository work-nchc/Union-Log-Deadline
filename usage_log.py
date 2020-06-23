from datetime import datetime, timedelta

logname_filtered = input('filtered log: ')
filename_accounts = input('accounts file: ')
filename_usage = input('usage output: ')
month_init = datetime.strptime(input('initial month YYYY-mm: '), '%Y-%m')

usage = {}
with open(logname_filtered) as input_log:
    for job in input_log:
        data = job.strip().split('\t')
        stamp = datetime.strptime(data[0], '%Y-%m-%dT%H:%M:%S')
        name = data[1]
        ticks = int(data[2])
        key = (stamp.year, stamp.month)
        if key not in usage:
            usage[key] = {}
        if name not in usage[key]:
            usage[key][name] = 0
        usage[key][name] += ticks * 32

with open(filename_accounts) as input_accounts:
    accounts = [username.strip() for username in input_accounts]

def col_key(k):
    return (k[0] - month_init.year) * 12 + k[1] - month_init.month

table = [[''] * len(usage) for username in accounts]
for key in usage:
    col = col_key(key)
    if col >= 0:
        for name in usage[key]:
            table[accounts.index(name)][col] = str(round(
                usage[key][name] / (36 * 10 ** 9), 2))

with open(filename_usage, 'w') as output_usage:
    output_usage.write('\n'.join(map('\t'.join, table)))
