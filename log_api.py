from Deadline.Scripting import RepositoryUtils, JobUtils
from datetime import datetime
def __main__():
    loglist = []
    for job in (tuple(RepositoryUtils.GetJobs(True)) +
                tuple(RepositoryUtils.GetDeletedJobs())):
        stats = JobUtils.CalculateJobStatistics(
            job, RepositoryUtils.GetJobTasks(job, True))
        loglist.append('\t'.join((
            job.JobId,
            job.JobUserName,
            datetime(
                job.JobCompletedDateTime.Year,
                job.JobCompletedDateTime.Month,
                job.JobCompletedDateTime.Day,
                job.JobCompletedDateTime.Hour,
                job.JobCompletedDateTime.Minute,
                job.JobCompletedDateTime.Second,
                job.JobCompletedDateTime.Ticks % 10 ** 7 // 10,
            ).isoformat(),
            str(stats.TotalTaskRenderTime.Ticks),
        )) + '\n')
    with open('log_api.csv', 'w') as output:
        output.writelines(loglist)
    return None
