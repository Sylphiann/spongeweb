# Load Testing Documentation

## Project Overview

- **Project Name**: Spongeweb
- **Repository URL**: [Spongeweb Github](https://github.com/Sylphiann/spongeweb)

## Objective

The objective of this load testing activity is to evaluate the system's performance under high concurrent user traffic, ensuring it is scalable, reliable, and capable of handling the expected load.

## Test Environment

- **Tool Used**: Apache JMeter
- **Environment Setup**:
  - **Server**: Cloud Instance with IP 104.154.136.222
  - **Network Conditions**: Stable internet connection
  - **Operating System**: macOS
  - **Dependencies**: JMeter v5.6.3 installed via Homebrew

## Test Scenarios

### Scenario 1: Concurrent User Load on /result endpoint

- **Description**: This scenario tests the system's performance by simulating 100 concurrent users accessing the /result endpoint over a short ramp-up period.
- **Expected User Count**: 100 users
- **Load Profile**:
  - **Ramp-Up Period**: 5 seconds
  - **Sustained Load**: 100 users for multiple iterations
  - **Ramp-Down Period**: Immediate stop after test execution
- **Metrics to Monitor**:
  - **Average Response Time**
  - **Error Rate**
  - **Throughput (requests/sec)**
  - **Received and Sent KB/sec**
  - **Standard Deviation (response time)**

### Scenario 2: Increased Concurrent User Load on `/detail`

- **Description**: This scenario tests the system's performance under higher load conditions by simulating 200 concurrent users accessing the `/detail` endpoint with a longer ramp-up period.
- **Expected User Count**: 200 users
- **Load Profile**:
  - **Ramp-Up Period**: 10 seconds
  - **Sustained Load**: 200 users for multiple iterations
  - **Ramp-Down Period**: Immediate stop after test execution
- **Metrics to Monitor**:
  - **Average Response Time**
  - **Error Rate**
  - **Throughput** (requests/sec)
  - **Data Transferred**:
    - **Received KB/sec**
    - **Sent KB/sec**
  - **Standard Deviation** (response time)


## Execution Details

### Scenario 1 Details

- **Date of Execution**: December 10, 2024
- **Load Testing Tool Configuration**:
  - Number of Threads (Users): 100
  - Ramp-Up Period: 5 seconds
  - Loop Count: Infinite (100 iterations tested for this run)
  - Sampler Configuration:
    - Protocol: HTTP
    - Server Name or IP: 104.154.136.222
    - Port: 8000
    - Endpoint Path: /result

### Scenario 2 Details

- **Date of Execution**: December 10, 2024
- **Load Testing Tool Configuration**:
  - Number of Threads (Users): 200
  - Ramp-Up Period: 10 seconds
  - Loop Count: Infinite (100 iterations tested for this run)
  - Sampler Configuration:
    - Protocol: HTTP
    - Server Name or IP: 104.154.136.222
    - Port: 8000
    - Endpoint Path: /detail

## Results

### Scenario 1

#### Summary of Metrics

- **Total Requests**: 10,000
- **Average Response Time**: 459 ms
- **Peak Response Time**: 712 ms
- **Minimum Response Time**: 447 ms
- **Error Rate**: 0.00%
- **Throughput**: 195.4 requests/second
- **Data Transferred**:
  - **Received**: 202.88 KB/sec
  - **Sent**: 24.43 KB/sec
- **Standard Deviation**: 23.51 ms

#### Graph Results

- The system maintained stable response times with no significant deviations over the test duration.
- No errors were observed, indicating high reliability.

#### Scenario 1 Observations

- The response time remained within acceptable limits (below 500 ms on average).
- The system demonstrated a consistent throughput of ~195 requests/second, handling the simulated load effectively.

### Scenario 2

#### Metrics Summary

- **Total Requests**: 20,000
- **Average Response Time**: 607 ms
- **Peak Response Time**: 1,939 ms
- **Minimum Response Time**: 448 ms
- **Error Rate**: 0.00%
- **Throughput**: 282.5 requests/second
- **Data Transferred**:
  - **Received**: 293.27 KB/sec
  - **Sent**: 35.31 KB/sec
- **Standard Deviation**: 96.26 ms

#### Scenario 2 Observations

- The system successfully handled 200 concurrent users with zero errors.
- The average response time (607 ms) is slightly higher than Scenario 1, indicating an expected increase due to higher concurrency.
- The peak response time (1,939 ms) suggests occasional latency spikes under high load.
- Throughput remained consistent at ~282.5 requests/second, demonstrating the system's ability to manage sustained high traffic.
- The standard deviation (96.26 ms) indicates a minor variability in response times, which is acceptable under the tested conditions.


## Analysis Based on All Scenario

- **Bottlenecks Identified**:
  - **Scenario 1**: No critical bottlenecks identified. The system handled the load effectively with minimal variance in response times.
  - **Scenario 2**: Higher concurrency led to increased peak response times, indicating potential areas for optimization in request handling.
- **System Performance Under Load**: 
  - **Scenario 1**: Excellent performance with low response times, zero errors, and stable throughput.
  - **Scenario 2**: Good performance under higher load, though peak response times suggest possible room for backend optimization to maintain consistency and performance.

- **My Recommendations**:
  - **Scalability Testing**: Increase the user count to evaluate system performance under higher loads.
  - **Stress Testing**: Push beyond expected load levels to identify breaking points.
  - **Optimization**: Ensure backend optimizations are in place to maintain low response times as load increases.


## Conclusion

The system successfully handled both scenarios with zero errors, showcasing its ability to manage concurrent users effectively. While Scenario 1 demonstrated optimal performance, Scenario 2 revealed slight increases in peak response times under higher concurrency, providing opportunities for further optimization.

## References

- [JMeter User Manual Guide](https://jmeter.apache.org/usermanual/index.html)

## Appendix

- [Load Testing Scripts](./load-testing/pmpl-mini-project-rafi.jmx)
