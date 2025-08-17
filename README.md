# Chaos Testing for Microservice Resilience  

## Problem Statement  

The shift from monoliths to microservices improved fault isolationbut independence alone isn’t enough. Systems must survive **extreme, sudden load spikes** to avoid cascading failures.  

### Real-World Challenges  
- **E-commerce**: Amazon’s "Big Billion Days" sees millions of simultaneous users. Unprepared systems risk slowdowns or crashes during checkout surges.  
- **Live Streaming**: Hotstar experiences **millions of instant viewers** when cricket stars like Kohli or Dhoni batdemand spikes in *seconds*, not gradually.  
- **APIs & Data**: Sudden bursts of API calls (1000s/sec) or storage floods (S3 ingestions, file uploads) can overwhelm backends silently.  

### Why Chaos Testing?  
Simulating failures in **controlled environments** reveals weaknesses *before* production:  
- Intentional stress on CPU, memory, and network to match real-world spikes.  
- Validates auto-scaling, fallbacks, and recovery under duress.  
- Prevents costly outages (e.g., Hotstar’s risk of losing **17M viewers**).  

**Goal**: Ensure zero downtime and smooth user experiences even at peak demand.  

## Project Overview
I built a large-scale, complex infrastructure composed of multiple microservices to replicate a real-world enterprise environment. The goal? To conduct realistic chaos testing by targeting individual services, measuring their resilience under heavy traffic, and validating failure recovery.

Unlike typical DevOps projects that rely on simplified setups, this one stands out—it's a Netflix Chaos Monkey-inspired implementation but designed from scratch. Every component was carefully planned and executed, making it a truly unique endeavor. Very few projects simulate such a detailed infrastructure purely for testing, proving this isn't a "copy-paste" solution but a thoughtfully engineered system.

*(Bonus brag: I'm proud of how distinct this turned out!)*

## Chaos Testing Execution
Now that the entire infrastructure is built, it's time to begin the attack phase—the chaos testing itself.

Based on my knowledge and expertise, every company has different systems and services powering their infrastructure. Testing 100+ or even 1000+ possible failure scenarios isn't practical—it requires precise and exact knowledge of their current setup. Instead, the right approach is identifying which specific services need testing, then strengthening those weak points.

After careful analysis, I found that most cloud-based companies rely on a few critical services that, if disrupted, can cause major failures. So, I've narrowed it down to the top 6 most vulnerable areas to target:

1. **CPU-only stress behavior** – Overloading CPU to test throttling and auto-scaling
2. **RAM-only stress behavior** – Exhausting memory to check crash recovery
3. **Pod Kill** – Randomly terminating Kubernetes pods to verify self-healing
4. **Service Kill** – Force-stopping core services to test redundancy
5. **Node Drain** – Simulating node failures in multi-node clusters

These tests cover the most likely failure points in modern cloud environments.

## Testing Methodology: Default vs Stress vs Final Values
Before approaching the chaos testing, we need to understand three key states - what I call the default value, stress value, and final value.

The **default value** means when everything is in idle state - no sudden strong traffic, like what big companies experience during normal days when users are sleeping or late at night between 3 AM to 9 AM. This is our baseline.

The **stress value** is what we see during extreme conditions - like when Amazon starts their big sale or when Virat Kohli comes to bat in an IPL match. These are the values we record during maximum stress.

The **final value** shows what happens after my protection mechanisms take action - what kind of response times and system behavior we get after implementing safeguards.

Now for the actual testing - I specifically target each of those 6 critical services one at a time in a controlled environment. I do this when the server is just casually working (producing default values) and then suddenly hit it with stress to see:
- How that service behaves under pressure
- What other services get affected
- What happens to my overall platform

**Important note:** We do all this in a completely controlled environment where we can rollback and undo everything. Since we're testing when there are very few users on our platform, we're very safe to perform these experiments.
# CPU-Only Stress Testing

## Goal
Show how the system behaves when the CPU is maxed out while memory stays normal.



# Test Setup

- **Stress Tool:** `stress-ng` with CPU workers only (no memory stress via `--vm`).  
- **Kubernetes Requests/Limits:**  
  - CPU request: `300m`  
  - CPU limit: `3 cores` per container  

**Monitored in Grafana:**  
- CPU utilisation  
- Minimum CPU guaranteed  
- Maximum CPU allowed  

---

# Baseline: CPU Usage at Idle

<p align="center">
  <img src="https://github.com/user-attachments/assets/f199f2ef-6f21-419e-ad42-8bf2cb582e88" width="70%" />
</p>
<p align="center"><strong>Grafana CPU panel at idle load</strong></p>

---

# Stress Applied: CPU Pressure Only

<p align="center">
  <img src="https://github.com/user-attachments/assets/d9f7e250-0c97-42d8-8282-e26e611896bf" width="70%" />
</p>
<p align="center"><strong>CPU usage spiking under stress-ng load</strong></p>

**Why meters turned red:**  
The Grafana panels turned red because CPU usage crossed the alert threshold (80%+), indicating saturation and risk of throttling.

---

# Actions Taken

- Applied **Kubernetes CPU limits** per container to prevent a single pod from consuming all available cores.  

<p align="center">
  <img src="https://github.com/user-attachments/assets/c6ba4a02-85e9-4b61-9987-682abc790f96" width="70%" />
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/363172b3-e43b-4b1e-9dbf-5b1c949f14fc" width="70%" />
</p>

- Configured **limits:** CPU `250m` / Memory `256Mi` per container.  
- Configured **Horizontal Pod Autoscaler (HPA):**  
  - Scale when CPU usage > 75% for 15s  
  - Minimum pods: 1  
  - Maximum pods: 5  

<p align="center">
  <img src="https://github.com/user-attachments/assets/fcf06b77-32c4-4d05-9fd2-897a0cb1ad04" width="70%" />
</p>
<p align="center">
  <img src="https://github.com/user-attachments/assets/9cc91a50-8537-4383-b224-cf3c2c2e669b" width="70%" />
</p>

---

# Result After Mitigation

<p align="center">
  <img src="https://github.com/user-attachments/assets/31d5b7ee-2799-4fe8-8e34-a07ba44d7931" width="70%" />
</p>
<p align="center"><strong>CPU utilization stabilized after applying limits and HPA</strong></p>

- CPU utilization stabilized around **48%** despite same load.  

**Why Grafana Gauge Shows 92% Red:**  
- Gauges are relative to pod CPU limit, not absolute node capacity.  
- Even if node CPU is ~48%, the pod may appear at 92% of its allocated quota, triggering the red zone.  

- API latency reduced compared to stress phase, confirming load distribution via HPA.

---

# Conclusion

This test demonstrates:  
- How CPU saturation impacts performance.  
- The importance of **realistic CPU limits** and **autoscaling**.  
- Grafana gauge readings can appear “red” due to **limit-relative scaling**, not absolute CPU usage.

## RAM-Only Stress Test

### Goal
Demonstrate how the system behaves when memory utilization increases, while keeping CPU load normal.

### Test Setup
- Used `stress-ng` with only memory workers: `--vm N --vm-bytes <size>`.
- Started small at 25% memory allocation, then gradually increased to observe behavior.
- No CPU workers used (`--cpu` omitted).

### Kubernetes Setup
- Memory requests and limits set to ensure scheduler can allocate memory safely:
  - Requests: 2 GiB
  - Limits: 4 GiB
- Pod runs once (`restartPolicy: Never`) to monitor effects.
- Pod Disruption Budget (PDB) recommended for critical pods to prevent eviction during node stress.

### Monitoring
- Grafana panels used:
  - `container_memory_usage_bytes`
  - `container_memory_rss`
  - `container_memory_limits`
- Observed OOMKill events via:
```bash
kubectl describe pod ram-stress
```
### create pod 
```bash
kubectl apply -f ram-stress.yaml
```
### Monotring the pod in terminal that it created succefully or not 
```bash
kubectl get pods ram-stress
kubectl describe pod ram-stress
kubectl logs ram-stress
```
> ⚠️ **Note for Reviewers:** This README is a living document and being updated regularly. The content, proofs, and formatting are in progress please refer to the commit history to see the latest changes.
