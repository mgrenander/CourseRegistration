
An easy-to-use script that logs in to McGill's Minerva service and registers for courses.
You need to go into the python script and change lines 38 - 41. These need to change to reflect the POST request that is sent when you attempt to register.
Then go to lines 107 - 108 and change the function calls to the specific courses you are looking to register in.

To start the script running, download the repository on a Linux server that has cron jobs enabled. Use the following line to give permission to the course_register_wrapper script to execute:

chmod 744 course_register_wrapper

To start the script, use the following:
./course_register_wrapper <McGill email> <password>

And voilà, the cron job will run the Python script every 15 minutes. If it is successful, it will send an email notifying you. If it is unsuccessful, every two days it will
send a single email notifying you that it is still running and waiting for an open spot.