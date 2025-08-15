from Crypto.Cipher import PKCS1_v1_5
from Crypto.PublicKey import RSA
import re
import math

CHAR_ENCODE_ARR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

HEX_ENCODE_STR = "0123456789abcdef"

BASE_64_STR = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="

def EncodeProtoBuff(proto_buffer):
    buffer_len = len(proto_buffer)
    encode_blocks = []
    buffer_mod = buffer_len % 3
    loop_step = 16383
    loop_limit = buffer_len - buffer_mod
    i = 0

    while i < loop_limit:
        encode_blocks.append(EncodeProtoSection(proto_buffer, i, loop_limit if i + loop_step > loop_limit else i + loop_step))
        i += loop_step

    match buffer_mod:
        case 1:
            char_value = proto_buffer[-1]
            encode_blocks.append(CHAR_ENCODE_ARR[char_value >> 2] + CHAR_ENCODE_ARR[char_value << 4 & 63] + "==")
        case 2:
            char_value = (proto_buffer[-2] << 8) + proto_buffer[-1]
            encode_blocks.append(CHAR_ENCODE_ARR[char_value >> 10] + CHAR_ENCODE_ARR[char_value >> 4 & 63] + CHAR_ENCODE_ARR[char_value << 2 & 63] + "=")
        case _:
            pass
    return "".join(encode_blocks)

def EncodeProtoSection(proto_buffer, start_index, end_index):
    encode_blocks = []
    for index in range(start_index, end_index, 3):
        aggregate_val = ((proto_buffer[index] << 16) & 16711680) + ((proto_buffer[index + 1] << 8) & 65280) + (proto_buffer[index + 2] & 255)
        encode_blocks.append(CHAR_ENCODE_ARR[aggregate_val >> 18 & 63] + CHAR_ENCODE_ARR[aggregate_val >> 12 & 63] + CHAR_ENCODE_ARR[aggregate_val >> 6 & 63] + CHAR_ENCODE_ARR[aggregate_val & 63])
    
    return "".join(encode_blocks)

def EncryptPassword(password, rsa_key):
    key_mod = int(rsa_key.publickey_mod, 16)
    key_exponent = int(rsa_key.publickey_exp, 16)
	
	
    key = RSA.construct((key_mod, key_exponent))
    cipher = PKCS1_v1_5.new(key)
    ciphertext = cipher.encrypt(password.encode())
    decode_hex_str = decodeHexString(ciphertext.hex())
    encode_hex_str = encodeHexString(decode_hex_str)
    return encode_hex_str

def decodeHexString(hex_value):
    if not hex_value:
        return 0
    hex_value_clean = re.sub(r"/[^0-9abcdef]/g", "", hex_value)
    hex_string_arr = []
    index = 0

    while index < len(hex_value_clean):
        temp_val = HEX_ENCODE_STR.index(hex_value_clean[index]) << 4 & 240
        index += 1
        temp_val |= 15 & HEX_ENCODE_STR.index(hex_value_clean[index])
        index += 1
        hex_string_arr.append(chr(temp_val))
    hex_string = "".join(hex_string_arr)

    return hex_string

def encodeHexString(hex_string):
    if not hex_string:
        return 0
    
    index = 0
    encode_string_arr = []

    while index < len(hex_string):
        t = ord(hex_string[index])
        n = t >> 2
        index += 1

        try:
            s = (3 & t) << 4
            r = ord(hex_string[index])
            s |= r >> 4
        except:
            r = float("nan")
            
        index += 1
        
        try:
            i = ord(hex_string[index])
            a = (15 & r) << 2 | i >> 6
            o = 63 & i
        except:
            i = float("nan")
            a = 0
            o = 0

        index += 1

        if math.isnan(r):
            o = 64
            a = o
        elif math.isnan(i):
            o = 64
    
        encode_string_arr.append(f"{BASE_64_STR[n]}{BASE_64_STR[s]}{BASE_64_STR[a]}{BASE_64_STR[o]}")
    
    encode_string = "".join(encode_string_arr)
    return encode_string


