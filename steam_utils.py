
CHAR_ENCODE_ARR = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

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
            encode_blocks.append(CHAR_ENCODE_ARR[char_value >> 10] + CHAR_ENCODE_ARR[char_value >> 4 & 63] + "-")
        case _:
            pass
    return "".join(encode_blocks)

#    for (var t, n = e.length, o = n % 3, i = [], s = 16383, a = 0, l = n - o; a < l; a += s)
#        i.push(u(e, a, a + s > l ? l : a + s));
#    1 === o ? (t = e[n - 1],
#    i.push(r[t >> 2] + r[t << 4 & 63] + "==")) : 2 === o && (t = (e[n - 2] << 8) + e[n - 1],
#    i.push(r[t >> 10] + r[t >> 4 & 63] + r[t << 2 & 63] + "="));
#    return i.join("")
    
def EncodeProtoSection(proto_buffer, start_index, end_index):
    encode_blocks = []
    for index in range(start_index, end_index, 3):
        aggregate_val = ((proto_buffer[index] << 16) & 16711680) + ((proto_buffer[index + 1] << 8) & 65280) + (proto_buffer[index + 2] & 255)
        encode_blocks.append(CHAR_ENCODE_ARR[aggregate_val >> 18 & 63] + CHAR_ENCODE_ARR[aggregate_val >> 12 & 63] + CHAR_ENCODE_ARR[aggregate_val >> 6 & 63] + CHAR_ENCODE_ARR[aggregate_val & 63])
    
    return "".join(encode_blocks)
#        function u(e, t, n) {
#            for (var o, i, s = [], a = t; a < n; a += 3)
#                o = (e[a] << 16 & 16711680) + (e[a + 1] << 8 & 65280) + (255 & e[a + 2]),
#                s.push(r[(i = o) >> 18 & 63] + r[i >> 12 & 63] + r[i >> 6 & 63] + r[63 & i]);
#            return s.join("")
#        }
