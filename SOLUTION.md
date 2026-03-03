# Lab 6 Results – REST vs gRPC

## Benchmark Results

| Method | Local | Same-Zone | Different Region |
|--------|--------|------------|------------------|
| REST add | 5.10 ms | 5.36 ms | TBD |
| gRPC add | 2.30 ms | 1.20 ms | TBD |
| REST rawimg | 15.43 ms | 13.98 ms | TBD |
| gRPC rawimg | 27.47 ms | 18.28 ms | TBD |
| REST dotproduct | ~6 ms | 6.38 ms | TBD |
| gRPC dotproduct | ~2 ms | 1.36 ms | TBD |
| REST jsonimg | ~15 ms | 50.64 ms | TBD |
| gRPC jsonimg | ~41 ms | 40.24 ms | TBD |
| PING | ~0.4 ms | ~0.46 ms | TBD |

## Observations

- gRPC is significantly faster than REST for small computational calls (add, dotproduct).
- REST and gRPC performance is similar for large image operations where serialization dominates.
- Same-zone latency is very low (~0.4 ms ping), so network delay is minimal.
- gRPC benefits from persistent HTTP/2 connections, while REST creates new connections.
