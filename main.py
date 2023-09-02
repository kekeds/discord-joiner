import concurrent.futures
import random
import string

import tls_client
from colorama import Fore, Style

import dtypes


class Joiner:
    def __init__(self, data: dtypes.Instance) -> None:
        self.session = data.client
        self.session.headers = data.headers
        self.get_cookies()
        self.instance = data

    def rand_str(self, length: int) -> str:
        return ''.join(random.sample(string.ascii_lowercase + string.digits, length))

    def get_cookies(self) -> None:
        site = self.session.get("https://discord.com")
        self.session.cookies = site.cookies

    def join(self) -> None:
        self.session.headers.update({"Authorization": self.instance.token})
        result = self.session.post(f"https://discord.com/api/v9/invites/{self.instance.invite}", json={
            'session_id': self.rand_str(32),
        })

        if result.status_code == 200:
            logger.printk(logger.color('green', f'Joined server: {result.status_code}'))

        else:
            logger.printk(logger.color('red', result.text))

class logger:
    colors_table = dtypes.OtherInfo.colortable

    @staticmethod
    def printk(text) -> None:
        print(f"[>] {text}")

    @staticmethod
    def convert(color):
        return color if color.__contains__("#") else logger.colors_table[color]

    @staticmethod
    def color(opt, obj):
        return f"{logger.convert(opt)}{obj}{Style.RESET_ALL}"

class intilize:
    @staticmethod
    def start(i):
        Joiner(i).join()
        
if __name__ == '__main__':
    with open("tokens.txt") as file:
        tokens = [line.strip() for line in file]

    instances = []
    max_threads = 5
    invite = input("Discord invite: ")
    
    try:
        invite=invite.split("/")[-1]
    except:
        pass

    for token_ in tokens:
        header = dtypes.OtherInfo.headers
        instances.append(
            dtypes.Instance(
                client=tls_client.Session(
                    client_identifier=f"chrome_{random.randint(110, 115)}",
                    random_tls_extension_order=True,
                ),
                token=token_,
                headers=header,
                invite=invite,
            )
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        for i in instances:
            executor.submit(intilize.start, i)
