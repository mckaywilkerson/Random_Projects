# Email Assignment Reminder Program

This program goes through an assignment list, and sends assignment reminders to users every week. It sends a reminder for this current week, as well as the future assignments for next week. It can be automated further with your operating system to run automatically once a week or however often you need it to run.

Rundown of files:
 - .env - variables needed to run the code, specifically smtp information.
 - testing_assignments.csv - A list that needs to be in the following order for each person/line: email,name, assignment1, assignment2, ...etc.
 - email_program - The actual program that you will run.

Just a note, this program will also do the following:
 - Skip displaying a person's assignment if their assignment is "None"
 - Order the assignments in the email based on the expected_order variable (aka. will display the assignments in a certain order instead of being based on their order in the assignment sheet)

Feel free to play around with it, and let me know if you have any questions or requests.

Thanks!