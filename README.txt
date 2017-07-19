An easy-to-use script that logs in to McGill's Minerva service and registers for courses.
Note that the script is currently hard-coded to register for the two courses I am interested in, but I am working to generalize the script.

Note also that the script is built for a cron job, set at a 15 minute interval.
If you wish to use the script with cron job, you must change the username and password fields to your own McGill email and password (lines 79 and 80)
If you do not wish to use the script with cron job, please keep in mind that the script will only send a failure email every other day between noon and quater past noon.
To change that, remove line 74 (and fix the resulting indentation errors).