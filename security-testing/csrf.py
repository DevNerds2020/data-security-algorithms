import requests
from bs4 import BeautifulSoup

def check_csrf(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    forms = soup.find_all('form')
    
    for form in forms:
        csrf_token = form.find('input', {'name': 'csrf_token'})
        if csrf_token:
            print(f"CSRF token found in form at {url}")
        else:
            print(f"Potential CSRF vulnerability in form at {url}")

def check_headers(url):
    response = requests.get(url)
    
    security_headers = ['X-Content-Type-Options', 'X-Frame-Options', 'Content-Security-Policy']
    
    for header in security_headers:
        if header not in response.headers:
            print(f"Missing security header {header} in response from {url}")

if __name__ == "__main__":
    target_url = 'https://www.digikala.com/_next/static/css/52e27165488ff8a5.css'
    
    print(f"Checking CSRF for {target_url}")
    check_csrf(target_url)
    
    print(f"\nChecking security headers for {target_url}")
    check_headers(target_url)