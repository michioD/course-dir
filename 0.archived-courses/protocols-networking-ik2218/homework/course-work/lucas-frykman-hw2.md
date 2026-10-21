# 1. ARP 

a)
- `H1 cache: 10.0.10.1 to MAC c` Because H1 first targets router R1 because H4 is on a another /24 subnet
- `H2 cache: 10.0.10.11 to MAC a` Because ARP snooping is enabled, H2 learns this from H1's broadcasted ARP request
- `R1 cache: 10.0.10.11 to MAC a, 10.0.20.44 to MAC f` Because R1 learns H1's mapping from the request of the ARP on LAN 1 and H4's mapping from the reply of the ARP on LAN 2
- `H3 cache: 10.0.20.1 to MAC d` because ARP snooping is enabled, H3 learns this from R1's broadcasted ARP request
- `H4 cache: 10.0.20.1 to MAC d` because H4 learns this since its the target of R1's request 

b) 
- `B1: Port N to MAC a, PORT E to MAC c` because B1 learns MAC a when H1 does ARP request  and MAC c when R1 sends its ARP reply
- `B2: Port W to MAC d, Port S to MAC f` because B2 learns MAC d when R1 sends its ARP request and MAC f when H4 sends its reply. 


c)
- `H1 cache: 10.0.10.1 to MAC c`
- `H2 cache: nothing` because passive snooping is disabled so H2 drops H1's request since its not the target
- `R1 cache: 10.0.10.11 to MAC a, 10.0.20.44 to MAC f` 
- `H3: nothing`
- `H4 cache: 10.0.20.1 to MAC d`  

# 2. UDP and fragmentation

IP fragment offsets are written in 8-byte blocks. The byte size of every non-final fragment must be a multiple of 8.
$\lfloor 1260 / 8 \rfloor \times 8 = 157 \times 8 = 1256$

a)

We simply divide the application data size by the size of the fragment and we get 
$\lceil 5408/ 1256\rceil = 5$. So `5 fragments` are transmitted 

b) 


| Fragment ID | Payload | Total Length | MF bit | Fragment offset
| - | - | - | - | - |
| Frag 1| Bytes 0-1255 | 1276 bytes | 1 |  0 (0/8)
| Frag 2 | Bytes 1256-2511 | 1276 bytes | 1 | 157 (1256/8)
| Frag 3 | Bytes 2512-3767 | 1276 bytes | 1 | 314 (2512/8)
| Frag 4 | Bytes 3768-5023 | 1276 bytes | 1 | 471 (3768/8)
| Frag 5 | Bytes 5024-5407 | 404 bytes | 0 | 628 (5024/8)

# 3. Routing

a)

| Destination | Metric | Next hop(s) |
| :--- | :--- | :--- |
| 192.168.1.0/24 | 2 | 192.168.2.1, 192.168.3.1 |
| 192.168.2.0/24 | 1 | -|
| 192.168.3.0/24 | 1 | -|
| 192.168.4.0/24 | 1 | - |
| 192.168.5.0/24 | 2 | 192.168.3.1 |

b)

- (i) 
  - For the packet to `192.168.1.88` (net1) Router C is allowed to use `192.168.2.1` and `192.168.3.1`
  - For the packet to `192.168.5.140` (net5) Router C is only allowed to use `192.168.3.1`
  - Why?: Router C supports equal-cost mutli-path (ECMP) routing. It splits traffic for network 1 because it has two equally good paths with a metric of 2, but it cannot split traffic at net5 because the path via Router A (metric 2) is better than the alternative path via Router B (metric 3)
- (ii) It gives the network load balancing which improves network throughput and reduces congestion


# 4. ICMP

IPs (from the figure): H1=10.0.1.2; R1: 10.0.1.1/10.0.2.2; R2: 10.0.2.1/10.0.3.2; R3: 10.0.3.1/10.0.4.2; H2=10.0.4.1.

a) 

Traceroute (TTL 1→4), datagrams received by H1 and H2, in order** (convention: an ICMP error's source address = the interface that received the errored packet, i.e., the interface facing back toward H1):

| # | Received by | Src IP | Dst IP | ICMP Type/Code |
|---|---|---|---|---|
| 1 | H1 | 10.0.1.1 (R1) | 10.0.1.2 | 11/0 Time Exceeded |
| 2 | H1 | 10.0.2.1 (R2) | 10.0.1.2 | 11/0 Time Exceeded |
| 3 | H1 | 10.0.3.1 (R3) | 10.0.1.2 | 11/0 Time Exceeded |
| 4 | H2 | 10.0.1.2 (H1) | 10.0.4.1 | 8/0 Echo Request (TTL=4 survives all 3 hops) |
| 5 | H1 | 10.0.4.1 (H2) | 10.0.1.2 | 0/0 Echo Reply |

b) 

H2 → H1 UDP, 1000 B data, DF=1:** IP datagram = 20(IP)+8(UDP)+1000 = 1028 B. It crosses net4 (MTU 1500, fine) but net3 has MTU **620**, which is smaller than 1028 and DF forbids fragmentation. **Yes**, H2 receives an ICMP error:
**Type 3, Code 4** (Destination Unreachable — Fragmentation Needed and DF Set), source = R3's interface facing H2 (10.0.4.2), destination = H2 (10.0.4.1).

c) 

Header `03 03 A2 1C 00 00 00 00`:**
- Type = 3, Code = 3 → **Destination Unreachable — Port Unreachable**.
- Meaning: the destination host received a datagram (typically UDP) for a port with no process listening, and no application could accept it, so it returns this to tell the sender delivery isn't possible.
- Checksum verification: **not possible** from the 8 bytes shown — the ICMP checksum covers the whole message, including the original IP header + first 8 bytes of the offending datagram that must follow this fixed header, which isn't given here.


# 5. TCP

Parameters of the network:

`transmission_time: (1200 Bytes / 960,000 bps) = 10ms`

`propagation_time: one way propogation time is 50ms`

`segment_arrival_time: sent_time + transmission_time + propagation_time = sent_time + 10ms + 50ms = sent_time + 60ms`

`MSS: Path MTU (1240 bytes), IPV4 Header (20 bytes), TCP Header (20 bytes)`

`Total segments: (13200 bytes / 1200 bytes per segment) = 11 segments total`

a) 

1. RTT
- `host A` sends `seg 1` at $t=0$. Transmission ends at $t=10$
- `seg 1` arrives at `Host B` at $t=60$ ms
- `Host B` delays ACK for 300ms because only one was recieved 
- ACK 2200 arrives at A at $360+50= 410$ ms
so from the start of the transmission the first RTT is 410 ms

2.  RTO Calculation (RFC 6298):
- SRTT = 410 ms.
- RTTVAR = R / 2 = 205 ms.
- The clock granularity G is 250 ms (0.25 seconds).
- RTO = SRTT + max(G, 4 * RTTVAR) = 410 + max(250, 4 * 205) = 410 + 820 = 1230 ms.

3.  t1 = 410 ms + 1230 ms = 1640 ms.


<!-- 3.  Timeout Event: At t = 410 ms, A receives the first ACK, updates CWND to 2 MSS, and sends Segment 2 (Seq=2200) and Segment 3 (Seq=3400). A starts the retransmission timer for Segment 2 at t = 410 ms. 
1.  Since the second ACK sent by the receiver is lost, the timer expires exactly 1230 ms later.  -->


<!-- ### b) 
Sequence of segments sent by Host A
Following the timeout at t1 = 1640 ms, A's `ssthresh` drops to 2 MSS `(max(FlightSize/2, 2 * MSS))` and `cwnd` drops to 1 MSS. The receiver will immediately generate duplicate ACKs for out-of-order data, restoring A's window. Assuming standard Congestion Avoidance increments (where `cwnd` strictly tracks bytes after hitting `ssthresh`) and a hard cap at RWND (3 MSS):

| Segment ID | Time Sent (ms) | Sequence Number | Notes |
| :--- | :--- | :--- | :--- |
| Seg 1 | 0 | 1000 | Initial send. |
| Seg 2 | 410 | 2200 | CWND = 2 MSS. |
| Seg 3 | 420 | 3400 | CWND = 2 MSS. |
| Seg 2 (Retransmit) | 1640 | 2200 | Timeout triggers retransmission; CWND = 1 MSS. |
| Seg 4 | 1750 | 4600 | Duplicate ACK 4600 arrives, acknowledging Segs 2 & 3. CWND increases to 2 MSS. |
| Seg 5 | 1760 | 5800 | CWND = 2 MSS. |
| Seg 6 | 1870 | 7000 | ACK 7000 arrives. CWND hits `ssthresh`. (Assuming Slow Start at equality). CWND = 3 MSS. |
| Seg 7 | 1880 | 8200 | CWND = 3 MSS. |
| Seg 8 | 1890 | 9400 | CWND = 3 MSS. |
| Seg 9 | 1990 | 10600 | ACK 9400 arrives. RWND caps in-flight data at 3 MSS. |
| Seg 10 | 2000 | 11800 | RWND limit applied. |
| Seg 11 | 2100 | 13000 | ACK 11800 arrives. Last segment sent. | -->

<!-- *(Note: Depending on whether the textbook strictly applies Slow Start or Congestion Avoidance when `cwnd == ssthresh`, Segments 6-11 may shift slightly in their grouping, but the total flight limits are ultimately constrained by the 3 MSS receiver window).* -->

<!-- ### c) 
Final Acknowledgement Arrival Time
*   Segment 11 (Seq=13000) is sent at t = 2100 ms and finishes transmission at t = 2110 ms.
*   It arrives at Host B at t = 2160 ms (2110 + 50). 
*   Since Host B received Segment 10 previously (arriving at t = 2060 ms), Segment 11 is the *second* full-sized segment received since the last ACK. 
*   This immediately triggers ACK 14200 (bypassing the 300 ms delay).
*   The ACK propagates back to A, taking 50 ms.
*   Host A receives the final ACK at `t = 2210 ms`. -->