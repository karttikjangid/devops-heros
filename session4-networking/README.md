# Networking Commands

## ifconfig

```
$ ifconfig en0
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
	ether 5e:36:62:77:5b:f1
	inet6 fe80::c44:3938:9bab:435c%en0 prefixlen 64 secured scopeid 0xc
	inet 100.129.161.186 netmask 0xfffff000 broadcast 100.129.175.255
	status: active
```

shows the network interface details, like the ip address, mac address and if the interface is up or not. on linux the equivalent is `ip a`.

## ping

```
$ ping -c 4 google.com
PING google.com (142.250.206.110): 56 data bytes
64 bytes from 142.250.206.110: icmp_seq=0 ttl=117 time=26.869 ms
64 bytes from 142.250.206.110: icmp_seq=1 ttl=117 time=27.556 ms
64 bytes from 142.250.206.110: icmp_seq=2 ttl=117 time=24.833 ms
64 bytes from 142.250.206.110: icmp_seq=3 ttl=117 time=24.826 ms

--- google.com ping statistics ---
4 packets transmitted, 4 packets received, 0.0% packet loss
round-trip min/avg/max/stddev = 24.826/26.021/27.556/1.216 ms
```

checks if a host is reachable and how long it takes for a packet to go there and back. 0% packet loss means the connection is fine.

## traceroute

```
$ traceroute -m 8 google.com
traceroute to google.com (142.250.206.110), 8 hops max, 40 byte packets
 1  wifi.height8tech.com (100.129.160.1)  9.096 ms  6.724 ms  5.677 ms
 2  202.131.133.5.convergentindia.com (202.131.133.5)  7.742 ms  9.501 ms  9.393 ms
 3  115.117.125.189.static-mumbai.vsnl.net.in (115.117.125.189)  14.582 ms  18.994 ms  8.628 ms
 4  * 172.28.117.90 (172.28.117.90)  11.501 ms  11.608 ms
 5  115.112.15.114.static-chennai.vsnl.net.in (115.112.15.114)  13.125 ms  13.005 ms  11.185 ms
 6  * * *
 7  216.239.59.170 (216.239.59.170)  30.134 ms
 8  172.253.70.166 (172.253.70.166)  14.830 ms
```

shows every hop (router) the packet passes through to reach the destination. the `*` means that hop didnt reply in time, still moves on to the next one.

## dig

```
$ dig google.com +short
142.250.206.110
```

does a dns lookup, basically asks "what ip does this domain point to". `+short` just trims the output to the answer only instead of the full response.

## curl

```
$ curl -sI https://google.com
HTTP/2 301
location: https://www.google.com/
content-type: text/html; charset=UTF-8
date: Fri, 04 Sep 2026 16:31:04 GMT
cache-control: public, max-age=2592000
server: gws
```

`-I` fetches only the response headers, no body. useful for checking status codes and redirects without downloading the whole page.

## netstat

```
$ netstat -an
Active Internet connections (including servers)
Proto Recv-Q Send-Q  Local Address            Foreign Address        (state)
tcp4       0      0  100.129.161.186.54470    13.107.213.48.443      ESTABLISHED
tcp4       0      0  100.129.161.186.54468    172.217.119.4.443      ESTABLISHED
tcp4       0      0  100.129.161.186.54466    142.250.66.1.443       ESTABLISHED
```

lists active network connections on the machine. each row is one connection, showing local and remote address plus its state (ESTABLISHED = currently connected).

## whois

```
$ whois -h whois.verisign-grs.com google.com
Domain Name: GOOGLE.COM
Registry Domain ID: 2138514_DOMAIN_COM-VRSN
Registrar: MarkMonitor Inc.
Creation Date: 1997-09-15T04:00:00Z
Registry Expiry Date: 2028-09-14T04:00:00Z
Name Server: NS1.GOOGLE.COM
Name Server: NS2.GOOGLE.COM
```

looks up who owns a domain and when it was registered. had to point it at `whois.verisign-grs.com` directly since the default server just gave a referral instead of the actual record.
