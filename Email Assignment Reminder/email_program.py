import smtplib
import csv
import datetime
from email.message import EmailMessage

from dotenv import load_dotenv
load_dotenv()
import os

# List the assignment file
assignments_file = "testing_assignments.csv"

# Define the sender and recipient email addresses.
sender_email = os.environ.get("sender_email")

# Define the SMTP server settings.
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = os.environ.get("smtp_username")
smtp_password = os.environ.get("smtp_password")

# Define the expected order of the assignments.
expected_order = ["Assignment 1", "Assignment 2", "Assignment 3"]

def getSundayDates():
    # Get the current date and time.
    now = datetime.datetime.now()

    # Calculate the date of the next Sunday.
    next_sunday = now.date() + datetime.timedelta((6 - now.weekday()) % 7)

    # Calculate the date of the Sunday after the next Sunday.
    next_sunday_after = next_sunday + datetime.timedelta(7)

    # Return the next sunday and next sunday after dates
    return next_sunday, next_sunday_after

# Define the main function.
def main():
    # Define the recipient_emails and assignments variables.
    recipient_emails = []
    recipient_names = {}
    assignments = {}
    assignments_for_order = {}
    next_assignments_for_order = {}

    next_sunday, next_sunday_after = getSundayDates()

    # Open the file with the assignments data.
    with open(assignments_file) as file:
        # Read the data from the file using the csv module.
        reader = csv.reader(file)

        # Loop over the rows in the file.
        for row in reader:
            # Check if the row has at least one element.
            if row:
                # Get the recipient's email address from the second column of the row.
                email = row[1]

                # Get the recipient's name from the first column of the row.
                name = row[0]

                # Add the recipient's email address to the recipient_emails list.
                recipient_emails.append(email)
                recipient_names[email] = name

                # Get the recipient's assignments from the remaining columns of the row.
                recipient_assignments = row[2:]

                # Add the recipient's assignments to the assignments dictionary.
                assignments[email] = recipient_assignments

    # Define the body of the email.
    body = "Hello,<br><br>Here are the assignments for this Sunday {}:<br><br>".format(next_sunday)

    # Define the subject of the email.
    subject = "Email Subject"

    # Loop over the recipients and add their assignments to the email body.
    for recipient in recipient_emails:
        # Get the recipient's assignments from the assignments dictionary.
        recipient_assignments = assignments[recipient]

        # Get the recipient's current assignment.
        last_assignment = recipient_assignments[0]

        # Get the next assignment in the rotation schedule.
        next_assignment = recipient_assignments[1]

        # Remove the current assignment from the list of assignments.
        recipient_assignments.remove(last_assignment)

        # Append the current assignment to the end of the list.
        recipient_assignments.append(last_assignment)

        # Update the recipient's assignments in the assignments dictionary.
        assignments[recipient] = recipient_assignments

        # Add the assignment to a dictionary to be ordered.
        if last_assignment != "None":
            assignments_for_order[last_assignment] = recipient_names[recipient]

        if next_assignment != "None":
            next_assignments_for_order[next_assignment] = recipient_names[recipient]

    for one_assignment in expected_order:
        body += "- {}: {}<br>".format(assignments_for_order[one_assignment], one_assignment)

    body += "<br><br>Next week's assignments {}:<br><br>".format(next_sunday_after)

    for one_assignment in expected_order:
        body += "- {}: {}<br>".format(next_assignments_for_order[one_assignment], one_assignment)

    # Create a new email message.
    body += "<br><br>Thank you!<br>Your Name"
    msg = EmailMessage()
    msg.set_content(body)
    msg.add_alternative(body, subtype="html")
    msg['Subject'] = subject
    msg.from_address = sender_email
    msg['To'] = ', '.join(recipient_emails)

    # Open the file with the assignments data.
    with open(assignments_file, "w", newline="") as file:
        # Create a writer object using the csv module.
        writer = csv.writer(file)

        # Loop over the recipients and their assignments.
        for recipient, recipient_assignments in assignments.items():
            # Write the recipient's email address and assignments to the file.
            writer.writerow([recipient_names[recipient]] + [recipient] + recipient_assignments)

    # Connect to the SMTP server and send the email.
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(msg)

    # Print a success message.
    print("Email sent successfully to {} recipients.".format(len(recipient_emails)))

# Run the main function.
if __name__ == "__main__":
    main()
