import os
from datetime import datetime
import csv
import webbrowser

# Ruta al archivo export.html
html_file = 'C:\\Users\\Gabriel\\Desktop\\Software_I\\POO\\Condominio\\export.html'

# Abre el archivo HTML en el navegador predeterminado
webbrowser.open(f'file:///{html_file}')

from py2flowchart import pyfile2flowchart
pyfile2flowchart('C:\\Users\\Gabriel\\Desktop\\Software_I\\POO\\Condominio\\CondominioSystem.py', 'export.html')

try:
    pyfile2flowchart('condominiosystem.py', 'export.html')
    print("El diagrama de flujo se ha generado exitosamente en 'export.html'.")
except Exception as e:
    print(f"Error al generar el diagrama de flujo: {e}")

class CondominioSystem:
    def __init__(self):
        self.current_user = None
        self.residents = {}
        self.users = {
            "admin": {"password": "admin123", "role": "admin"},
            "staff": {"password": "staff123", "role": "staff"}
        }
        self.initialize_csv_files()
        self.load_data()

    def initialize_csv_files(self):
        """Initialize CSV files if they don't exist"""
        # Residents file
        if not os.path.exists('residents.csv'):
            with open('residents.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['unit_number', 'owner_name', 'contact_number', 'monthly_fee', 'outstanding_balance'])

        # Payments file
        if not os.path.exists('payments.csv'):
            with open('payments.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['unit_number', 'payment_date', 'amount'])

    def load_data(self):
        """Load data from CSV files"""
        try:
            # Load residents data
            with open('residents.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    unit_number = row['unit_number']
                    self.residents[unit_number] = {
                        'owner_name': row['owner_name'],
                        'contact_number': row['contact_number'],
                        'monthly_fee': float(row['monthly_fee']),
                        'outstanding_balance': float(row['outstanding_balance']),
                        'payment_history': []
                    }

            # Load payment history
            with open('payments.csv', 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    unit_number = row['unit_number']
                    if unit_number in self.residents:
                        self.residents[unit_number]['payment_history'].append({
                            'date': row['payment_date'],
                            'amount': float(row['amount'])
                        })
        except Exception as e:
            print(f"Note: Starting with empty data. {str(e)}")

    def save_data(self):
        """Save data to CSV files"""
        # Save residents data
        with open('residents.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['unit_number', 'owner_name', 'contact_number', 'monthly_fee', 'outstanding_balance'])
            writer.writeheader()
            for unit_number, data in self.residents.items():
                writer.writerow({
                    'unit_number': unit_number,
                    'owner_name': data['owner_name'],
                    'contact_number': data['contact_number'],
                    'monthly_fee': data['monthly_fee'],
                    'outstanding_balance': data['outstanding_balance']
                })

        # Save payments data
        with open('payments.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['unit_number', 'payment_date', 'amount'])
            writer.writeheader()
            for unit_number, data in self.residents.items():
                for payment in data['payment_history']:
                    writer.writerow({
                        'unit_number': unit_number,
                        'payment_date': payment['date'],
                        'amount': payment['amount']
                    })

    def generate_report_file(self, data, filename, headers):
        """Generic method to generate CSV report files"""
        with open(filename, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            for row in data:
                writer.writerow(row)

    def login(self):
        """ User login"""
        print("\n=== Condominio Management System Login ===")
        attempts = 3
        while attempts > 0:
            username = input("Username: ")
            password = input("Password: ")

            if username in self.users and self.users[username]["password"] == password:
                self.current_user = username
                print(f"\Bienvenido al Condominio Management System, {username}!")
                return True
            
            attempts -= 1
            print(f"Credencialas no validas. {attempts} intentos.")
        
        print("Muchos intentos fallidos. Sistema bloqueado.")
        return False

    def add_resident(self):
        """Add a new condominium resident"""
        print("\n=== Add New Condominio Resident ===")
        unit_number = input("Enter Unit Number: ")
        owner_name = input("Enter Owner Name: ")
        contact_number = input("Enter Contact Number: ")
        monthly_fee = float(input("Enter Monthly Condominium Fee: "))

        self.residents[unit_number] = {
            "owner_name": owner_name,
            "contact_number": contact_number,
            "monthly_fee": monthly_fee,
            "payment_history": [],
            "outstanding_balance": monthly_fee
        }
        self.save_data()
        print("Condominium resident added successfully!")

    def record_payment(self):
        """Pago de cuota de condominio"""
        print("\n=== Record Pago ===")
        unit_number = input("Ingrese el numero: ")
        
        if unit_number in self.residents:
            amount = float(input("Ingrese la cantidad: "))
            payment_date = datetime.now().strftime("%Y-%m-%d")
            
            self.residents[unit_number]["payment_history"].append({
                "date": payment_date,
                "amount": amount
            })
            
            self.residents[unit_number]["balance"] -= amount
            self.save_data()
            print("Pago exitoso!")
        else:
            print("Numero no encontrado!")

    def view_resident(self):
        """View condominium resident details"""
        print("\n=== View Condominio Resident Details ===")
        unit_number = input("Enter Unit Number: ")
        
        if unit_number in self.residents:
            resident = self.residents[unit_number]
            print(f"\nUnit Number: {unit_number}")
            print(f"Owner Name: {resident['owner_name']}")
            print(f"Contact Number: {resident['contact_number']}")
            print(f"Monthly Fee: ${resident['monthly_fee']:.2f}")
            print(f"Outstanding Balance: ${resident['outstanding_balance']:.2f}")
            
            if resident['payment_history']:
                print("\nPayment History:")
                for payment in resident['payment_history']:
                    print(f"Date: {payment['date']}, Amount: ${payment['amount']:.2f}")
        else:
            print("Unit not found!")

    def generate_outstanding_payments_report(self):
        """Generate report of units with outstanding condominium fees"""
        print("\n=== Outstanding Condominium Fees Report ===")
        report_data = []
        headers = ['Unit Number', 'Owner Name', 'Outstanding Balance']
        
        for unit_number, data in self.residents.items():
            if data['outstanding_balance'] > 0:
                report_data.append({
                    'Unit Number': unit_number,
                    'Owner Name': data['owner_name'],
                    'Outstanding Balance': f"${data['outstanding_balance']:.2f}"
                })
                print(f"\nUnit Number: {unit_number}")
                print(f"Owner Name: {data['owner_name']}")
                print(f"Outstanding Balance: ${data['outstanding_balance']:.2f}")
        
        if report_data:
            self.generate_report_file(report_data, 'outstanding_payments_report.csv', headers)
            print("\nReport saved to 'outstanding_payments_report.csv'")
        else:
            print("No outstanding payments found.")

    def generate_payment_report(self):
        """Generate complete condominium fee payment history"""
        print("\n=== Condominio Payment History Report ===")
        report_data = []
        headers = ['Unit Number', 'Owner Name', 'Total Paid', 'Outstanding Balance']
        
        for unit_number, data in self.residents.items():
            total_paid = sum(payment['amount'] for payment in data['payment_history'])
            report_data.append({
                'Unit Number': unit_number,
                'Owner Name': data['owner_name'],
                'Total Paid': f"${total_paid:.2f}",
                'Outstanding Balance': f"${data['outstanding_balance']:.2f}"
            })
            print(f"\nUnit Number: {unit_number}")
            print(f"Owner Name: {data['owner_name']}")
            print(f"Total Paid: ${total_paid:.2f}")
            print(f"Outstanding Balance: ${data['outstanding_balance']:.2f}")
        
        if report_data:
            self.generate_report_file(report_data, 'payment_history_report.csv', headers)
            print("\nReport saved to 'payment_history_report.csv'")
        else:
            print("No payment history found.")
    def generate_payment_report(self):
    """Generar el historial completo de pagos de la cuota del condominio"""
    print("\n=== Reporte del Historial de Pagos del Condominio ===")
    report_data = []
    headers = ['Número de Unidad', 'Nombre del Propietario', 'Total Pagado', 'Saldo Pendiente']
    
    for unit_number, data in self.residents.items():
        total_paid = sum(payment['amount'] for payment in data['payment_history'])
        report_data.append({
            'Número de Unidad': unit_number,
            'Nombre del Propietario': data['owner_name'],
            'Total Pagado': f"${total_paid:.2f}",
            'Saldo Pendiente': f"${data['outstanding_balance']:.2f}"
        })
        print(f"\nNúmero de Unidad: {unit_number}")
        print(f"Nombre del Propietario: {data['owner_name']}")
        print(f"Total Pagado: ${total_paid:.2f}")
        print(f"Saldo Pendiente: ${data['outstanding_balance']:.2f}")
    
    if report_data:
        self.generate_report_file(report_data, 'payment_history_report.csv', headers)
        print("\nReporte guardado en 'payment_history_report.csv'")
    else:
        print("No se encontró historial de pagos.")

    def display_menu(self):
        """Display the main menu"""
        while True:
            print("\n=== Condominio Management System ===")
            print("1. Agregar Residente")
            print("2. Registrar Pago de Cuota de Condominio")
            print("3. Mirar Detalles de Residente")
            print("4. Generar informe de pagos pendientes")
            print("5. Generar informe de pago completo")
            print("6. Salir")
            
            choice = input("\nEnter your choice (1-6): ")
            
            if choice == '1':
                self.add_resident()
            elif choice == '2':
                self.record_payment()
            elif choice == '3':
                self.view_resident()
            elif choice == '4':
                self.generate_outstanding_payments_report()
            elif choice == '5':
                self.generate_payment_report()
            elif choice == '6':
                print("Salienddo del Sistema")
                break
            else:
                print("Opcion invalida. Intente de nuevo.")

def main():
    system = CondominioSystem()
    if system.login():
        system.display_menu()

if __name__ == "__main__":
    main()