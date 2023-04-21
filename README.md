# zlibrary-auth

Just a simple script to authenticate to the Z-Library.

## Installation

You can install this package using pip
    
```bash
pip install --upgrade git+https://github.com/krishna2206/zlibrary-auth.git
```

## Usage
### CLI
You can use the `zlib-auth` command to authenticate to the Z-Library.

#### Login
```bash
zlib-auth --login
```

#### Register
```bash
zlib-auth --register
```

### Module
You can also use this package as a module. To do so, import the `ZlibAuth` class and instantiate it.

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as playwright:
    zlib_auth = ZlibAuth(playwright)
    # All the code goes here
```

#### Login
```python
print("Please fill the form below")
email = input("Email : ")
password = input("Password : ")

print("Logging in...")
try:
    cookies = zlib_auth.login(email, password)
except ZlibAuthException as e:
    print(e)
else:
    print(f"Succesfully logged in : {cookies}")
```

#### Register
```python
zlib_auth.init_registration_page()

print("Please fill the form below")
email = input("Email : ")
password = input("Password : ")
username = input("Username : ")

zlib_auth.show_captcha()
captcha = input("Captcha : ")

print("Sending verification email...")
try:
    zlib_auth.send_verification_email(email, password, username, captcha)
except ZlibAuthException as e:
    print(e)
else:
    confirmation_url = input("Enter confirmation url sent to your email : ")
    cookies = zlib_auth.confirm_verification_email(confirmation_url)
    print(cookies)
```

The script will send a verification url to your email. 
Enter the verification url when prompted, and the script will authenticate to Z-Library and display the session token.

## License

MIT License

Copyright (c) 2023 Fitiavana Anhy Krishna

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
