from aoc_utils import hex2bin
from math import prod


def parse_packet(bits, start):
    V = int(bits[start:start+3], 2)
    T = int(bits[start+3:start+6], 2)
    i = start + 6

    if T == 4: # Literal
        R = None
        num = ''
        while True:
            num += bits[i + 1:i + 5]
            last = (int(bits[i]) == 0)
            i += 5
            if last:
                break
        R = int(num, 2)
        return V, T, R, i

    # Operators
    S = []
    LTID = int(bits[i])
    if LTID == 0:
        total = int(bits[i+1:i+16], 2)
        i += 16
        end = total + i
        while i < end:
            pck = parse_packet(bits, i)
            i = pck[-1]
            S.append(pck)
    else:
        number = int(bits[i+1:i+12], 2)
        i += 12
        for _ in range(number):
            pck = parse_packet(bits, i)
            i = pck[-1]
            S.append(pck)

    return V, T, S, i


def ver_sum(pck):
    V = pck[0]
    if isinstance(pck[2], list):
        V += sum(map(ver_sum, pck[2]))
    return V


def evaluate(pck):
    if pck[1] == 4:  # Value literal
        return pck[2]

    if pck[1] == 0:  # Sum
        return sum(map(evaluate, pck[2]))
    if pck[1] == 1:  # Product
        return prod(map(evaluate, pck[2]))
    if pck[1] == 2:  # Min
        return min(map(evaluate, pck[2]))
    if pck[1] == 3:  # Max
        return max(map(evaluate, pck[2]))

    if pck[1] == 5:  # Greater than
        return 1 if evaluate(pck[2][0]) > evaluate(pck[2][1]) else 0
    if pck[1] == 6:  # Less than
        return 1 if evaluate(pck[2][0]) < evaluate(pck[2][1]) else 0
    if pck[1] == 7:  # Equal to
        return 1 if evaluate(pck[2][0]) == evaluate(pck[2][1]) else 0

    assert False, "Unknown packet type!"


################################################################################
message = "C20D7900A012FB9DA43BA00B080310CE3643A0004362BC1B856E0144D234F43590698FF31D249F87B8BF1AD402389D29BA6ED6DCDEE59E6515880258E0040A7136712672454401A84CE65023D004E6A35E914BF744E4026BF006AA0008742985717440188AD0CE334D7700A4012D4D3AE002532F2349469100708010E8AD1020A10021B0623144A20042E18C5D88E6009CF42D972B004A633A6398CE9848039893F0650048D231EFE71E09CB4B4D4A00643E200816507A48D244A2659880C3F602E2080ADA700340099D0023AC400C30038C00C50025C00C6015AD004B95002C400A10038C00A30039C0086002B256294E0124FC47A0FC88ACE953802F2936C965D3005AC01792A2A4AC69C8C8CA49625B92B1D980553EE5287B3C9338D13C74402770803D06216C2A100760944D8200008545C8FB1EC80185945D9868913097CAB90010D382CA00E4739EDF7A2935FEB68802525D1794299199E100647253CE53A8017C9CF6B8573AB24008148804BB8100AA760088803F04E244480004323BC5C88F29C96318A2EA00829319856AD328C5394F599E7612789BC1DB000B90A480371993EA0090A4E35D45F24E35D45E8402E9D87FFE0D9C97ED2AF6C0D281F2CAF22F60014CC9F7B71098DFD025A3059200C8F801F094AB74D72FD870DE616A2E9802F800FACACA68B270A7F01F2B8A6FD6035004E054B1310064F28F1C00F9CFC775E87CF52ADC600AE003E32965D98A52969AF48F9E0C0179C8FE25D40149CC46C4F2FB97BF5A62ECE6008D0066A200D4538D911C401A87304E0B4E321005033A77800AB4EC1227609508A5F188691E3047830053401600043E2044E8AE0008443F84F1CE6B3F133005300101924B924899D1C0804B3B61D9AB479387651209AA7F3BC4A77DA6C519B9F2D75100017E1AB803F257895CBE3E2F3FDE014ABC"
binary = hex2bin(message)
packets = []
index = 0
while index < len(binary):
    pck = parse_packet(binary, index)
    packets.append(pck)
    index = pck[-1]
    if all(map(lambda x: x == '0', binary[index:])):
        break

print("Version sum:", sum(map(ver_sum, packets)))
print("Packet result:", evaluate(packets[0]))