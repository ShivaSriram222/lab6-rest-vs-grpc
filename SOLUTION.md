# Lab 6 Results – REST vs gRPC

# SOLUTION — REST vs gRPC

Fill the table with average milliseconds per operation (from your runs).

| Method            | Local (us-west1-a) | Same-Zone (2 VMs) | Different Region (us-west1-a to europe-west3-a) |
|-------------------|-------------------:|-------------------:|-----------------------------------------------:|
| REST add          |        3.387 ms    |     3.964 ms       |            300.354 ms                         |
| gRPC add          |        0.725 ms    |     0.973 ms       |            150.823 ms                         |
| REST rawimg       |        8.245 ms    |     12.973 ms      |            1194.406 ms                        |
| gRPC rawimg       |        14.188 ms   |     10.422 ms      |            567.176 ms                         |
| REST dotproduct   |        4.214 ms    |     7.319 ms       |            301.793 ms                         |
| gRPC dotproduct   |        0.900 ms    |     1.140 ms       |            154.009 ms                         |
| REST jsonimg      |        47.382 ms   |     43.348 ms      |            1353.158 ms                        |
| gRPC jsonimg      |        34.566 ms   |     26.067 ms      |            628.636 ms                         |
| PING (ms rtt)     |            _       |     0.710 ms       |            142.598 ms                         |

Observations:

From my tests, gRPC consistently ran faster than REST, especially for smaller requests like add and dotproduct. That makes sense because gRPC uses HTTP/2 and Protocol Buffers, which send compact binary data instead of the heavier JSON format that REST uses. With REST, every request and response has more text and headers to process, so it naturally takes longer per call. For larger data like images, gRPC still came out ahead, but the difference wasn’t as big. The biggest slowdown happened with the jsonimage endpoint, since base64 encoding makes the image about one-third larger than its raw version. This extra size means more data has to travel over the network.

When I tested across regions (between Oregon and Frankfurt), the delay jumped from just a few milliseconds to hundreds of milliseconds. At that point, network distance dominates — it doesn’t really matter whether you’re using gRPC or REST; the time it takes for data to cross continents overshadows the software overhead. Overall, gRPC is the better choice when speed and efficiency matter, like in systems that make frequent or small API calls. REST is still simpler to work with and debug, but it adds more communication overhead, especially noticeable when handling many lightweight requests.


