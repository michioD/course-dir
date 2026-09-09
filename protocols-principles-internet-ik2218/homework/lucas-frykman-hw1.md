## 1. IPv4 Addressing

a) Best-fit netmask for 25 hosts and 2 routers
A network with 25 hosts and 2 routers requires 27 IP addresses. 
The number of usable IPs in a subnet is `2^{32 - prefix} - 2`.
A /27 subnet provides `2^5 - 2 = 30` IP addresses.
- Best-fit netmask: `255.255.255.224` or /27
- Unused IP addresses: `30 - 27 = 3` unused addresses.

b) Division of `10.20.0.0/22` into equal-sized subnets (min 50 IPs each)
Each subnet must support at least 50 usable IP addresses.
The smallest subnet size that supports 50 usable IPs is a /26, which provides `2^6 - 2 = 62` usable addresses.
The original network is a /22.
- Maximum number of subnets: `2^{26 - 22} = 2^4 = 16` subnets.
- Total number of usable IP addresses: `16 \times 62 = 992` IP addresses available for hosts and routers across all subnets.

<!-- c) Subnetting 172.16.40.0/24
The requirements are for 96, 60, 28, and 20 usable IP addresses.
The required block sizes (including network and broadcast) are 128, 64, 32, and 32 respectively.
Assigning in ascending order of size:

| Subnet Size | Usable IPs | Network Address (Binary) | Netmask (Binary) | CIDR Notation |
| :--- | :--- | :--- | :--- | :--- |
| **32** | 20 | `10101100.00010000.00101000.00000000` | `11111111.11111111.11111111.11100000` | 172.16.40.0/27 |
| **32** | 28 | `10101100.00010000.00101000.00100000` | `11111111.11111111.11111111.11100000` | 172.16.40.32/27 |
| **64** | 60 | `10101100.00010000.00101000.01000000` | `11111111.11111111.11111111.11000000` | 172.16.40.64/26 |
| **128** | 96 | `10101100.00010000.00101000.10000000` | `11111111.11111111.11111111.10000000` | 172.16.40.128/25 |

d) Directed broadcast address of 172.20.4.160/27
The prefix /27 implies a block size of 32. 160 is a multiple of 32 ($160 = 5 \times 32$), so 172.20.4.160 is the network address.
The broadcast address is the last address in this block: $160 + 31 = 191$.
- Directed broadcast address:`172.20.4.191`

e) Subnets for 172.16.75.142 with broadcast 172.16.75.255
The IP is `172.16.75.142` (142 in binary is `10001110`).
The broadcast is `172.16.75.255` (255 in binary is `11111111`).
For a subnet to have .255 as its broadcast address, all host bits must be 1. The subnet mask determines how many bits belong to the host part.
- Smallest possible subnet: The host portion must be large enough to encompass the difference between 142 and 255. Comparing `10001110` and `11111111`, they only share the first bit (`1`). Therefore, the host part must be at least 7 bits long. A 7-bit host part means a /25 prefix. Network: `172.16.75.128/25`
- Largest possible subnet: We can decrease the prefix length as long as the broadcast address remains 172.16.75.255.
  - /24: Broadcast is 172.16.75.255 (Valid)
  - /23: Broadcast is 172.16.75.255 (Valid, network is 172.16.74.0/23)
  - /22: Broadcast is 172.16.75.255 (Valid, network is 172.16.72.0/22)
  - /21: Broadcast is 172.16.79.255 (Invalid)
- Results:
  - Largest subnet: `172.16.72.0/22`
  - Smallest subnet: `172.16.75.128/25` -->

f) IANA and RIR for `194.71.64.0/22`
- **RIR:** RIPE NCC
- **Organization:** Forsakringskassan
- **AS Number:** AS197942



<!-- 
afsawefawefaw
---

## 2. Address Allocation (30/100)

**a) Possible values of prefix length $x$ for 10.88.0.0/$x$**
First, calculate the required number of IP addresses for each network:
- **A:** 300 hosts + 1 router = 301 IPs $\rightarrow$ Requires a /23 (512 block)
- **B:** 126 hosts + 1 router = 127 IPs $\rightarrow$ Requires a /24 (256 block). (Note: A /25 gives 126 usable IPs, which is not enough for 127 interfaces).
- **C:** 500 hosts + 1 router = 501 IPs $\rightarrow$ Requires a /23 (512 block)
- **D:** 510 hosts + 1 router = 511 IPs $\rightarrow$ Requires a /22 (1024 block). (Note: A /23 gives 510 usable IPs, which is not enough for 511 interfaces).
- **E:** R1, R2, R3, H1 = 4 IPs $\rightarrow$ Requires a /29 (8 block)
- **F:** R1, R4, R5, H2, H3 = 5 IPs $\rightarrow$ Requires a /29 (8 block)

Total required IP addresses = $1024 + 512 + 512 + 256 + 8 + 8 = 2320$.
To fit 2320 addresses, the block size must be at least 4096 (a /20 prefix). Therefore, $x \le 20$.
Also, `10.88.0.0` must be a valid network address for prefix $x$. The address `10.88.0.0` in binary is `00001010.01011000.00000000.00000000`. The first 1 bit from the right is the 14th bit from the right (or the 19th bit from the left). A valid network address requires all bits in the host portion to be 0. Thus, the prefix length $x$ can be at most $32 - 19 = 13$ bits long if we consider trailing zeros, meaning $x$ can range down to 13.
- **Possible values of $x$:** `13, 14, 15, 16, 17, 18, 19, 20`

**b) Address allocation for maximum $x$ ($x = 20$)**
We use the block `10.88.0.0/20`. To minimize unassigned IPs and aggregate where possible, we allocate them in adjacent contiguous blocks, keeping in mind that D must be assigned the lowest address.

- **Network D:** `10.88.0.0/22` (Assign lowest address first)
- **Network C:** `10.88.4.0/23` 
- **Network A:** `10.88.6.0/23`
- **Network B:** `10.88.8.0/24`
- **Network E:** `10.88.9.0/29`
- **Network F:** `10.88.9.8/29`

*Reasoning Sketch:* We need 2320 addresses. The available space is 4096 addresses. We assign the largest required block (Network D, /22) to the lowest part of the address space `10.88.0.0/22` to satisfy the lowest address requirement. Then, we consecutively assign the remaining networks starting from `10.88.4.0` downwards by size (/23, /23, /24, /29, /29). This prevents fragmentation, minimizes unassigned IPs between the allocated subnets, and leaves the upper half of the /20 block completely unassigned for future use.

**c) Forwarding table of router R1**
Router R1 connects directly to Networks E and F.
Let's assign IPs to the router interfaces on the respective subnets:
- **E (10.88.9.0/29):** R1 = 10.88.9.1, R2 = 10.88.9.2, R3 = 10.88.9.3
- **F (10.88.9.8/29):** R1 = 10.88.9.9, R4 = 10.88.9.10, R5 = 10.88.9.11

| Destination | Next hop | Interface |
| :--- | :--- | :--- |
| `10.88.0.0/22` (D) | 10.88.9.11 (R5) | Eth_F |
| `10.88.4.0/23` (C) | 10.88.9.10 (R4) | Eth_F |
| `10.88.6.0/23` (A) | 10.88.9.2 (R2) | Eth_E |
| `10.88.8.0/24` (B) | 10.88.9.3 (R3) | Eth_E |
| `10.88.9.0/29` (E) | - | Eth_E |
| `10.88.9.8/29` (F) | - | Eth_F |

---

## 3. IPv4 Forwarding (20/100)

Because Eth2 is down, the default route (`0.0.0.0/0`) cannot be used. The successful datagrams must have matched specific entries in the table.

- **b) 10.64.2.1** must match `10.X.0.0/16`.
  Since the prefix is /16, the network address is exactly the first two octets. Thus, `X = 64`.
- **a) 193.147.1.31** must match `193.147.1.0/T`.
  For `193.147.1.31` to be contained in this subnet, the host portion must cover up to 31 (binary `00011111`), which requires at least 5 host bits. This means $T \le 27$. For `193.147.1.0` to be a valid network address, the 1 in the 3rd octet must not be part of the host bits, so $T \ge 24$. Thus, `T` can be any integer from **24 to 27** (inclusive).
- **c) 190.1.45.129** must match `190.1.45.Z/29`.
  A /29 subnet has a block size of 8. The address `129` falls into the block `190.1.45.128/29` (which spans from 128 to 135). Therefore, `Z = 128`.
- **d) 144.127.32.211** must match `144.Y.0.0/5`.
  A /5 mask indicates that only the first 5 bits of the first octet define the network. For a valid network address, all bits following the 5th bit (including the entire second octet Y) must be zero. Therefore, `Y = 0`.

**Values:** `X = 64`, `Y = 0`, `Z = 128`, `T \in [24, 27]`

---

## 4. IPv4 and IPv6 Datagram Formats (20/100)

Given header: `45 00 00 3C 1C 46 20 B9 40 06 51 86 C0 00 02 01 C6 33 64 02`

**a. Protocol version and Type of Service?**
- **Protocol version:** IPv4 (first nibble `4` in `45`).
- **Type of service (DS field):** `0x00` (second byte).

**b. Is this IP datagram a fragment? Why?**
- **Yes.** The 7th and 8th bytes are `20 B9` (binary `0010 0000 1011 1001`). The top 3 bits are the flags: `0` (Reserved), `0` (Don't Fragment), and `1` (More Fragments). Since the More Fragments (MF) bit is set to 1, and the fragment offset is non-zero (`0x0B9` or 185), this is a fragment.

**c. What is the size of the IP payload?**
- The Total Length is `0x003C` (60 bytes). The header length (IHL) is 5 words ($5 \times 4 = 20$ bytes). 
- **Payload size:** $60 - 20 = 40$ bytes.

**d. Do we know if the IP header was corrupted during transmission? What would happen if the checksum does not match?**
- Yes, we can determine this by computing the header checksum. Summing the 16-bit words of the header and performing one's complement gives `0x0000`, which means it was **not corrupted**. If the checksum did not match, the router/receiver would silently discard (drop) the datagram.

**e. How many routers has the packet traversed?**
- The Time to Live (TTL) is `0x40` (64). The default TTL for Ubuntu Linux is 64. Since $64 - 64 = 0$, the packet has traversed **0 routers** (it originated from a host on the local network).

**f. What is the identification number of the datagram? What is it used for?**
- **Identification number:** `0x1C46` (7238 in decimal). It is used to identify fragments of the same original IP datagram so that the receiving host can correctly reassemble them.

**g. What is the source address in dotted decimal format? Is it routable?**
- **Source address:** `192.0.2.1` (`C0 00 02 01`). 
- **Is it routable?** No. It belongs to the `192.0.2.0/24` (TEST-NET-1) block, which is reserved for documentation and examples and is not routable on the public internet.

**h. What is the destination address in dotted decimal format? Is it routable?**
- **Destination address:** `198.51.100.2` (`C6 33 64 02`). 
- **Is it routable?** No. It belongs to the `198.51.100.0/24` (TEST-NET-2) block, which is also reserved for documentation and examples.

**i. Which transport layer protocol is used, and how can you tell? Is the transport layer header included in the payload?**
- **Protocol:** TCP. We can tell because the Protocol field (10th byte) is `0x06`, which corresponds to TCP.
- **Is the header included?** No. The fragment offset is 185 (which means this fragment starts at byte offset $185 \times 8 = 1480$ of the original payload). The transport layer header is only present in the first fragment (offset 0).

**j. Are there any IPv4 options used?**
- **No.** The Internet Header Length (IHL) is 5 ($5 \times 4 = 20$ bytes). Because 20 bytes is the minimum size of an IPv4 header, there is no room for options. -->
