acc_used = set()
logname_input = input('filtered log: ')
filename_output = input('used accouts output: ')
with open(logname_input) as input_log:
    for data in input_log:
        acc_used.add(data.split()[1])
with open(filename_output, 'w') as output_acc:
    output_acc.write('\n'.join(sorted(acc_used)))
