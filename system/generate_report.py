import csv
from io import BytesIO
from system.model import Appointment

def generate_report():
    # Query the Appointment model to get all appointments
    appointments = Appointment.query.all()

    # Prepare the data for the CSV file
    data = [
        ['Appointment Date', 'Appointment Time', 'Doctor Name', 'Department', 'Patient Name', 'Patient Contact No.', 'Appointment Location', 'Appointment Status'],
    ]

    for appointment in appointments:
        data.append([
            appointment.appointment_date,
            appointment.appointment_time,
            appointment.doctor.name,
            appointment.doctor.department,
            appointment.user.first_name,
            appointment.user.phone,
            appointment.location,
            'Cancelled' if appointment.status else 'Confirmed',
        ])

    output = BytesIO()
    writer = csv.writer(output)
    writer.writerows([map(lambda x: x.encode('utf-8'), row) for row in data])
    output.seek(0)
    return output
