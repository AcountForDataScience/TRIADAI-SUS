import re #regular expression
import requests #http requests
# to do: replace with httpx when making async version
from Crypto.Cipher import AES



def send_to_php(message, url = "https://aiproducts.xo.je/TriadSusAI/ExpressOverveiwFirstStage.php"):
    # url = "https://aiproducts.xo.je/TriadSusAI/ExpressOverveiwFirstStage.php"
    # moved to default variable instead in case we want to use some other site later

    params = {
        "message": message
    }

    session = requests.Session()

    headers = {
        "User-Agent": "Mozilla/5.0",
        "Connection": "close"
    }

    r1 = session.get(url, params=params, headers=headers, timeout=30)
    html = r1.text

    # this checks for encryption, I assume? 
    values = re.findall(r'toNumbers\("([a-f0-9]+)"\)', html)

    # and if encrypted, we decrypt.
    if len(values) >= 3:
        # print("is_encrypted")
        key = bytes.fromhex(values[0])
        iv = bytes.fromhex(values[1])
        ciphertext = bytes.fromhex(values[2])

        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(ciphertext)

        test_cookie = decrypted.hex()

        session.cookies.set("__test", test_cookie, domain="aiproducts.xo.je", path="/")

        params["i"] = "1"

        r2 = session.get(url, params=params, headers=headers, timeout=30)
        return r2.text

    return html

def AR_format(params:dict[str,float|str|object], max_length=42): # type: ignore
    message : str = ""
    lines: list[str] = []
    for key, value in params.items():
        match value:
            case str():
                fvalue = f"{key}: {value}"
            case float()|int():
                fvalue = f"{key}: {value:.2f}"
            case None:
                fvalue = f"{key}: N/A"
            case _:
                fvalue = f"{key}: {value.display_name}"  # this assumes custom ENUM type # type: ignore
        lines.append(fvalue)
    # print(lines)
    length = 0
    for line in lines:
        length += len(line)
        if length > max_length:
            message += "\n" + line
            length = 0
        elif message:
            message += "| " + line
        else:
            message = line
    return (message)

params = {
    "Intel Confidence": .9,
    "Volatility": "High",
    "Time Pressure": "Strategic",
    "Decision Risk Index": 12,
    "Hope": "Gone",
    "smartness": .23456789,
}

# print(AR_format(params))

# hello = "hello"
# world = "world"
# print(len(hello + world))
