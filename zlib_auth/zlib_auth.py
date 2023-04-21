import base64
from io import BytesIO

import click
from PIL import Image
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Playwright


class ZlibAuthException(Exception):
    pass


class ZlibAuth:
    def __init__(self, playwright: Playwright) -> None:
        self.url = "https://singlelogin.me"
        self.browser = playwright.firefox.launch(headless=True)
        self.context = self.browser.new_context()
        self.current_page = self.context.new_page()
        self.captcha_image = None

    def init_registration_page(self):
        self.current_page.goto(self.url + "/registration.php")
        self.captcha_image = self.current_page.locator(
            "div[class='captcha']").locator("img").get_attribute("src").split(",")[1]

    def login(self, email: str, password: str) -> dict:
        self.current_page.goto(self.url + "/login.php")

        self.current_page.locator("input[name='email']").fill(email)
        self.current_page.locator("input[name='password']").fill(password)
        with self.current_page.expect_response(self.url + "/rpc.php") as response_info:
            self.current_page.locator("button[name='submit']").click()
        response = response_info.value.json()

        if response.get("errors"):
            raise ZlibAuthException(f"Failed to login. {response}")
        return {
            "remix_userid": self.get_cookie(self.context.cookies(), "remix_userid"),
            "remix_userkey": self.get_cookie(self.context.cookies(), "remix_userkey"),
        }

    def send_verification_email(self, email: str, password: str, username: str, captcha: str) -> dict:
        self.current_page.locator("input[name='email']").fill(email)
        self.current_page.locator("input[name='password']").fill(password)
        self.current_page.locator("input[name='name']").fill(username)
        self.current_page.locator("input[name='captcha']").fill(captcha)

        with self.current_page.expect_response(self.url + "/rpc.php") as response_info:
            self.current_page.locator("button[type='submit']").click()
        response = response_info.value.json()

        if response.get("errors"):
            raise ZlibAuthException(f"Failed to send verification email. {response}")
        return response

    def show_captcha(self):
        image_bytes = base64.b64decode(self.captcha_image)
        image = Image.open(BytesIO(image_bytes))
        image.show()

    @staticmethod
    def get_cookie(cookies: list, name: str):
        for cookie in cookies:
            if cookie["name"] == name:
                return cookie["value"]
        return None

    def confirm_verification_email(self, confirmation_url: str) -> tuple[str, str]:
        self.current_page.goto(confirmation_url, wait_until="networkidle")

        return {
            "remix_userid": self.get_cookie(self.context.cookies(), "remix_userid"),
            "remix_userkey": self.get_cookie(self.context.cookies(), "remix_userkey"),
        }


@click.command()
@click.option("--register", is_flag=True, help="Init registration")
@click.option("--login", is_flag=True, help="Init login")
def cli(register, login):
    with sync_playwright() as playwright:
        zlib_auth = ZlibAuth(playwright)
        if register:
            zlib_auth.init_registration_page()

            click.echo("Please fill the form below")
            email = click.prompt("Email", type=str)
            password = click.prompt("Password", type=str)
            username = click.prompt("Username", type=str)

            zlib_auth.show_captcha()
            captcha = click.prompt("Captcha", type=str)

            click.echo("Sending verification email...")
            try:
                zlib_auth.send_verification_email(email, password, username, captcha)
            except ZlibAuthException as e:
                click.echo(e)
            else:
                confirmation_url = click.prompt("Enter confirmation url sent to your email", type=str)
                cookies = zlib_auth.confirm_verification_email(confirmation_url)
                click.echo(cookies)

        elif login:
            click.echo("Please fill the form below")
            email = click.prompt("Email", type=str)
            password = click.prompt("Password", type=str)

            click.echo("Logging in...")
            try:
                cookies = zlib_auth.login(email, password)
            except ZlibAuthException as e:
                click.echo(e)
            else:
                click.echo(f"Succesfully logged in : {cookies}")


if __name__ == "__main__":
    cli()
