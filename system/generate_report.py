import csv
from io import StringIO
from system.model import Appointment

def generate_report():
    # Query the Appointment model to get all appointments
    appointments = Appointment.query.all()

    # Prepare the data for the CSV file
    data = [
        ['Appointment Date', 'Appointment Time', 
         'Doctor Name', 'Doctor Email', 'Department', 'Patient Name', 'Patient Email',
         'Patient Contact No.', 'Appointment Location',
         'Appointment Status'],
    ]

    for appointment in appointments:
        patient_name = "{} {}".format(appointment.user.first_name, appointment.user.last_name)
        data.append([
            appointment.appointment_date,
            appointment.appointment_time,
            appointment.doctor.name,
            appointment.doctor.email,
            appointment.doctor.department,
            patient_name,
            appointment.user.email,
            appointment.user.phone,
            appointment.location,
            'Cancelled' if appointment.status else 'Confirmed',
        ])

    output = StringIO()
    writer = csv.writer(output)
    writer.writerows(data)
    output.seek(0)
    # Convert the StringIO object to bytes
    output_bytes = output.getvalue().encode('utf-8')
    return output_bytes
