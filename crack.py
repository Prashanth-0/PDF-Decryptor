import os
import pikepdf
from tqdm import tqdm
from pyfiglet import Figlet
from termcolor import colored



def find_file(file_name):
    # Search for the file in the current directory
    for root, _, files in os.walk(os.getcwd()):
        if file_name in files:
            return os.path.join(root, file_name)
    return None

def is_complex(password):
    # Basic implementation for password complexity check
    length_check = len(password) >= 8
    uppercase_check = any(char.isupper() for char in password)
    lowercase_check = any(char.islower() for char in password)
    digit_check = any(char.isdigit() for char in password)
    special_char_check = any(char in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for char in password)

    return all([length_check, uppercase_check, lowercase_check, digit_check, special_char_check])

def display_pdf_metadata(pdf_file):
    try:
        with pikepdf.open(pdf_file) as pdf:
            info = pdf.docinfo
            print("\nPDF Metadata:")
            for key, value in info.items():
                print(f"{key}: {value}")
    except Exception as e:
        print(colored(f"\nError reading PDF metadata: {e}", 'red'))

# Function to decrypt PDF using a wordlist
def decrypt_pdf(pdf_file, wordlist_file):
    total_passwords = 0
    with open(wordlist_file, 'r') as file:
        for line in tqdm(file, "Decrypting PDF"):
            password = line.strip()
            if not password:
                continue
            total_passwords += 1
            try:
                with pikepdf.open(pdf_file, password=password) as pdf:
                    print(colored("[+] Password found:", 'green'), colored(password, 'red'))
                    print(f"\nTotal passwords attempted: {total_passwords}")
                    return
            except Exception as e:
                continue

if __name__ == "__main__":
    try:
        custom_fig = Figlet(font='slant')
        banner_text = "PDF Cracker"
        banner = custom_fig.renderText(banner_text)
        colored_banner = colored(banner, 'yellow')
        print(colored_banner)
     
        developer_name = colored("Developed by Prashanth",'red')
        padding = " " * ((len(colored_banner) - len(developer_name)) // 1)
        print(padding + developer_name)

        while True:
            print(colored("\nOptions:", 'red'))
            print(colored("1. Decrypt PDF", 'green'))
            print(colored("2. Password Complexity Checker", 'green'))
            print(colored("3. Display PDF Metadata", 'green'))
            print(colored("4. Exit", 'green'))

            choice = input(colored("Enter your choice (1-4): ", 'green'))

            if choice == '1':
                pdf_file_name = input(colored("Enter the name of the PDF file: ", 'green'))
                wordlist_file_path = input(colored("Enter the path to the wordlist file: ", 'green'))
                pdf_file_path = find_file(pdf_file_name)
                if pdf_file_path:
                    decrypt_pdf(pdf_file_path, wordlist_file_path)
                else:
                    print(colored("\nError: PDF file not found in the current directory.", 'red'))
                break
               
            elif choice == '2':
                password_input = input(colored("Enter a password to check its complexity: ", 'green'))
                if is_complex(password_input):
                    print(colored("Password is complex!", 'red'))
                else:
                    print(colored("Password is not complex. Consider choosing a stronger password.", 'red'))
                break
    
            elif choice == '3':
                pdf_file_name = input(colored("Enter the name of the PDF file: ", 'green'))
                pdf_file_path = find_file(pdf_file_name)
                if pdf_file_path:
                    display_pdf_metadata(pdf_file_path)
                else:
                    print(colored("\nError: PDF file not found in the current directory.", 'red'))
                break

            elif choice == '4':
                print(colored("\nExiting PDF Decryptor. Goodbye!", 'yellow'))
                break

            else:
                print(colored("Invalid choice. Please enter a number between 1 and 4.", 'red'))
                break
    except KeyboardInterrupt:
        print(colored("\n\n[-] Operation interrupted by user. Exiting...", 'yellow'))
