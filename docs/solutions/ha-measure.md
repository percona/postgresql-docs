# Measuring high availability

The need for high availability is determined by the business requirements, potential risks, and operational limitations. For example, the more components you add to your infrastructure, the more complex and time-consuming it is to maintain. Moreover, it may introduce extra failure points. The recommendation is to follow the principle "The simpler the better".

The level of high availability depends on the following:

* how frequently you may encounter an outage or a downtime.
* how much downtime you can bear without negatively impacting your users for every outage, and
* how much data loss you can tolerate during the outage.


When you evaluate high-availability, consider these two aspects:

* Expected level of availability. 
* Actual availability level of your infrastructure.

### Expected level of availability

It is measured by establishing a measurement time frame and dividing it by the time that it was available. This ratio will rarely be one, which is equal to 100% availability. At Percona, we don't consider a solution to be highly available if it is not at least 99% or two nines available.
    
The following table shows the amount of downtime for each level of availability from two to five nines.
    
| Availability %           | Downtime per year | Downtime per month | Downtime per week | Downtime per day  |
|--------------------------|-------------------|--------------------|-------------------|-------------------|
| 99% (“two nines”)        | 3.65 days         | 7.31 hours         | 1.68 hours        | 14.40 minutes     |
| 99.5% (“two nines five”) | 1.83 days         | 3.65 hours         | 50.40 minutes     | 7.20 minutes      |
| 99.9% (“three nines”)    | 8.77 hours        | 43.83 minutes      | 10.08 minutes     | 1.44 minutes      |
| 99.95% (“three nines five”) | 4.38 hours        | 21.92 minutes      | 5.04 minutes      | 43.20 seconds     |
| 99.99% (“four nines”)    | 52.60 minutes     | 4.38 minutes       | 1.01 minutes      | 8.64 seconds      |
| 99.995% (“four nines five”) | 26.30 minutes     | 2.19 minutes       | 30.24 seconds     | 4.32 seconds      |
| 99.999% (“five nines”)   | 5.26 minutes      | 26.30 seconds      | 6.05 seconds      | 864.00 milliseconds |

### Actual level of availability

Measuring the real level of high availability (HA) in your system is key to making sure your investment in HA infrastructure pays off. Instead of relying on assumptions or expectations, you should base your availability insights on incident management data. This is the information collected during service disruptions, failures, or outages that affect the normal functioning of the setup. With this data, you can track metrics like uptime, Mean Time to Recovery (MTTR), and Mean Time Between Failures (MTBF).

MTBF gives you a picture of how reliable your infrastructure really is. In well-designed high-availability environment, the incidents should be rare, typically occurring no more than once every 2 to 4 years. This assumes a robust infrastructure, as not all systems equally suit for handling database load.

Recovery speed matters too. For example, a typical Patroni-based cluster can fail over to a new primary node within 30 to 50 seconds. However, note that database availability metrics typically don't consider the application's ability to detect the failover and reconnect. Some applications recover seamlessly, while others may require a restart. 

