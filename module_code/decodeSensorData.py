from Crypto.Cipher import AES
import base64
import binascii

key = b'sF2t@L8q9!yP$azx'


def decode_sensordata(encoded_payload):
    # decode the changes the sender made
    decoded_payload = base64.b64decode(encoded_payload).decode('utf-8')
    # decode making is a hex
    msg = binascii.unhexlify(decoded_payload.encode("utf-8"))

    # decode the AES encoding
    cipher = AES.new(key, AES.MODE_CFB, msg[:16])
    # clean original data
    originalbyte = cipher.decrypt(msg[16:])
    original = originalbyte.decode('utf-8')
    cleaned_string = original[0:-1]

    # Split the string by '-' to separate the values
    values = cleaned_string.split('-')

    # Extract the individual values and assign them to variables
    a = float(values[0])
    b = float(values[1])
    c = tuple(map(int, values[2][1:-1].split(',')))

    return a, b, c


if __name__ == '__main__':

    encoded_payload = "OWIwM2VlM2Y4NTY3YmM3MjlmMWU5MWU1M2E1MDM0NGFjMDQ2MDRjNzU0YjhkYzE0YTVlZTJjZmNhNzdlYTlmYTcwZjY2ZjIyZmE2OWVhOGY1MzAyZTNhYg=="
    temperature, humidity, light = decode_sensordata(encoded_payload)


    print("temperature =", temperature)
    print("humidity =", humidity)
    print("light =", light)



