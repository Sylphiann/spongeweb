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

### Scenario 2: [Name of Scenario]

- **Description**: [Provide a brief description of the scenario]
- **Expected User Count**: [Number of users]
- **Load Profile**:
  - **Ramp-Up Period**: [e.g., 5 users every 30 seconds]
  - **Sustained Load**: [e.g., 100 users for 20 minutes]
  - **Ramp-Down Period**: [e.g., 5 users per minute]
- **Metrics to Monitor**:
  - **Response Time**
  - **Error Rate**
  - **Database Load**

## Execution Details

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

#### Observations

- The response time remained within acceptable limits (below 500 ms on average).
- The system demonstrated a consistent throughput of ~195 requests/second, handling the simulated load effectively.


### Scenario 2

- **Average Response Time**: [Insert value]
- **Peak Response Time**: [Insert value]
- **Error Rate**: [Insert percentage]
- **Memory Usage**: [Insert value]
- **Observations**: [Any observations noted during this scenario]

## Analysis Based on All Scenario

- **Bottlenecks Identified**: No critical bottlenecks were identified during this test. The response times and throughput metrics suggest the system can handle the load scenario tested.
- **System Performance Under Load**: 
  - The system performed reliably with zero errors, low standard deviation, and a stable throughput rate.
  - Response times remained consistent and within acceptable ranges even at high concurrency levels.

- **Recommendations**:
  - **Scalability Testing**: Increase the user count to evaluate system performance under higher loads.
  - **Stress Testing**: Push beyond expected load levels to identify breaking points.
  - **Infrastructure Monitoring**: Use server-side monitoring tools to validate CPU, memory, and database usage during these tests.
  - **Optimization**: Ensure backend optimizations are in place to maintain low response times as load increases.


## Conclusion

- **Summary of Findings**: [Summarize the key findings from the load test]
- **Next Steps**: [Outline what actions are planned based on the load test results, such as code optimizations, additional testing, etc.]

## References

- [Documentation/Guides used for Load Testing]
- [Link to Load Testing Tool Documentation]

## Appendix

- **Test Logs**: [Attach or link test logs if available]
- **Load Testing Scripts**: [Attach or link load testing scripts if applicable]
