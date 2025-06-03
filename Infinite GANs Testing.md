---
title: Infinite GANs Testing
---

# Infinite GANs Testing

_[Link to HackMD](https://hackmd.io/@briankim31415/rkj0MrA-gg/edit)_

### Contents

-   [Overview](#Overview)
-   [Configurations](#Configurations)
-   [Parameter Selection Rationale](#Parameter-Selection-Rationale)
-   [Results](#Results)
-   [Discussion](#Discussion)
-   [Concluding Remarks](#Concluding-Remarks)
-   [Future Testing](#Future-Testing)

## Overview

This testing phase evaluates the **robustness** and **scalability** of the Infinite GANs framework ( [Paper](https://arxiv.org/pdf/2102.03657#page=1.22) | [GitHub](https://github.com/google-research/torchsde/blob/master/examples/sde_gan.py) ) under varying noise conditions. By systematically adjusting key parameters in the configuration space, we aim to understand how sensitive model performance is to different noise regimes.

The primary focus is on:

-   How the model behaves under different noise dimensions
-   The influence of different optimisers
-   Baseline comparisons against the original configuration

> Code for this testing can be found [here](https://github.com/briankim31415/torchsde/tree/master) under the `brian_testing` directory

## Initial Replication

As a starting point, the original results from the paper were replicated locally using the authors' provided codebase. The specific task was to train a Neural SDE generator to match a **time-dependent Ornstein–Uhlenbeck process**, a classic stochastic differential equation used to model mean-reverting behavior.

The generated trajectories and training curves closely resemble those reported in the original publication, suggesting that the replication was successful and faithful to the original design.

![sde_gan_5](https://hackmd.io/_uploads/SJ1ZafIGgg.png|width="40")
![sde_gan_graph](https://hackmd.io/_uploads/HJNZTGUMex.png)

## Configurations

We explored **3 key parameters** in this round of testing:

1. **Optimiser** – Controls the neural network update rule
2. **Initial Noise Size** – Number of latent dimensions sampled at the start of the SDE
3. **Noise Size** – Dimensionality of Brownian motion throughout the SDE trajectory

Since each run is computationally expensive (taking several hours), **8 configurations** were selected, prioritizing **increasing noise size** to observe effects of higher stochasticity.

### Configuration Table

| Config # | Optimiser | Initial noise size | Noise Size |
| -------- | --------- | ------------------ | ---------- |
| 1        | Adadelta  | 5                  | 3          |
| 2        | Adadelta  | 3                  | 1          |
| 3        | Adadelta  | 10                 | 3          |
| 4        | Adadelta  | 10                 | 5          |
| 5        | Adam      | 5                  | 3          |
| 6        | Adam      | 3                  | 1          |
| 7        | Adam      | 10                 | 3          |
| 8        | Adam      | 10                 | 5          |

**Baseline Reference**:
The default configuration from the original code is **Config 1**:

> `Adadelta` optimiser, `Initial Noise Size = 5`, `Noise Size = 3`

## Parameter Selection Rationale

### Optimiser

Two optimisers were selected to balance comparison validity and search efficiency:

-   **Adadelta** - Retained for fidelity to the original paper, which reported strong performance using this optimiser
-   **Adam** - A widely used optimiser known for strong empirical results across generative models. Selection supported by this [optimiser benchmark summary](https://hackmd.io/PduDfE04Qmunohr19Uz1DQ?view)

Currently, both the generator and discriminator use the same optimiser. Future tests may decouple this choice to assess asymmetric optimiser impact.

### Initial Noise Size & Noise Size

These two noise-related parameters govern how much stochasticity is introduced at different stages:

-   **Initial Noise Size** affects the latent input space of the SDE
-   **Noise Size** determines the dimensionality of the Brownian motion injected throughout the trajectory

Both smaller and larger values than the baseline were tested to evaluate Infinite GAN’s performance in lower and higher noise regimes, with an emphasis on higher noise.

## Results

#### Config 1

> **Optimizer**: Adadelta
> **Initial Noise Size**: 5
> **Noise Size**: 3

-   Initially, the generated distribution is slightly wider, indicating some mismatch
-   By t = 31 onward, the overlap between real and generated improves significantly
-   The generated trajectories closely follow the trend and variance of the real trajectories
-   Around step ~5000, the loss stabilizes and flattens out
-   Loss converges to near-zero suggesting the discriminator cannot discern between real and generated distributions

![1_combined_strip](https://hackmd.io/_uploads/SybnJDiMlx.png)
![1_combined_plots](https://hackmd.io/_uploads/Byr2JDizeg.png)

#### Config 2

> **Optimizer**: Adadelta
> **Initial Noise Size**: 3
> **Noise Size**: 1

-   From t = 31 onward, the generated distributions gradually align better with real ones, especially in shape and central tendency
-   Noticably more spread in generated trajectories compared to real trajectories
-   Much slower and noisier loss convergence

![2_combined_strip](https://hackmd.io/_uploads/BkF3kDsMgx.png)
![2_combined_plots](https://hackmd.io/_uploads/ry3n1Djzeg.png)

#### Config 3

> **Optimizer**: Adadelta
> **Initial Noise Size**: 10
> **Noise Size**: 3

-   The generated and real distributions close, but all distributions are slightly offset to the left
-   There are a few outlier trajectories that overshot, which reflects the increased variance due to larger initial noise
-   Eventually all generated trajectories closely mimic real trajectories
-   The unaveraged loss starts very volatile, but gradually stabilizes

![3_combined_strip](https://hackmd.io/_uploads/S1M6JPsMgx.png)
![3_combined_plots](https://hackmd.io/_uploads/S1HaJwszxe.png)

#### Config 4

> **Optimizer**: Adadelta
> **Initial Noise Size**: 10
> **Noise Size**: 5

-   The distribution match is fairly tight, with almost complete overlap in shape and variance in the final steps
-   Generated trajectories accurately track the real trajectories across the entire time span with only a few outliers
-   The loss converges smoothly and gradually, but the it begins to drift slightly upwards after step 8000

![4_combined_strip](https://hackmd.io/_uploads/SyuaJwsfxl.png)
![4_combined_plots](https://hackmd.io/_uploads/S1261Dizgl.png)

#### Config 5

> **Optimizer**: Adam
> **Initial Noise Size**: 5
> **Noise Size**: 3

-   The distributions have relatively similar shapes, but there’s a persistent left shift between the generated and real distributions across time steps
-   The generated trajectories seem to mimic the real trajectories fairly well especially towards the later half
-   Loss is signficantly more volatile with Adam

![5_combined_strip](https://hackmd.io/_uploads/r1kAkDoGlx.png)
![5_combined_plots](https://hackmd.io/_uploads/H1DAyPsGex.png)

#### Config 6

> **Optimizer**: Adam
> **Initial Noise Size**: 3
> **Noise Size**: 1

-   Initial real and generated distributions are significantly different
-   Consistently generates left-skewed distributions
-   Generated trajectories do not mimic the shape of the real trajectories at all
-   Noise is also extrememly volatile and doesn't provide a meaningful convergence

![6_combined_strip](https://hackmd.io/_uploads/rJiRkwjMex.png)
![6_combined_plots](https://hackmd.io/_uploads/r1R0Jvjzgx.png)

#### Config 7

> **Optimizer**: Adam
> **Initial Noise Size**: 10
> **Noise Size**: 3

-   Distribution begins somewhat aligned, but continues to lean left-skew
-   Generated trajectories display more variance and spread than real trajectories
-   Loss is even noisier and volatile

![7_combined_strip](https://hackmd.io/_uploads/rkGkgDjzxl.png)
![7_combined_plots](https://hackmd.io/_uploads/Sk1lxviMex.png)
j

#### Config 8

> **Optimizer**: Adam
> **Initial Noise Size**: 10
> **Noise Size**: 5

-   Distributions are generally similar, but slightly shifted to the left
-   Generated trajectories seem to undershoot towards the later half
-   Loss still noisy and volatile

![8_combined_strip](https://hackmd.io/_uploads/S1weewozge.png)
![8_combined_plots](https://hackmd.io/_uploads/SJ5xgPofgg.png)

## Discussion

#### Optimiser

Between Adadelta and Adam, Adadelta was clearly the better choice. This finding affirms the discovery in the original paper. One caveat is that the optimiser parameters such as learning rate and decay were not tuned specifically for Adam, which could have led to suboptimal performance. But this testing still shows that Adadelta is more resilient to over/undershooting. Adadelta also oscilates to convergence a lot more stably.

#### Initial Noise Size

Lower initial noise size (3,5) resulted in slighltly worse initial distributions and trajectories. Higher noise size (10) is generally able to better mimic the real distributions and trajectories.

#### Noise Size

The degree of impact caused by noise size was sightly different between the 2 optimisers. In Adadelta, higher noise size (3,5) led to smoother oscilations and convergence. It also leads to generated distributions that better align with the real distributions than lower noise size (1).

For Adam, the higher noise size (5) was necessary to introduce proper stochasticity and more accurately mimic the real distribution. Lower noise size (1) remained nearly linear throughout the timesteps.

## Concluding Remarks

Overall, these testings displayed how Infinite GANs performs under different noise conditions. They proved their scalability as adding dimensions of noise increased their robustness. Although there may be a point of diminishing or decreasing returns, there is still promise of improved returns by adding more complex noise. Additionally, Adadelta was able to provide cleaner convergence than Adam which confirms the findings of the original paper as well.

## Future Testing

To further probe the Infinite GAN framework, the following areas are prioritized for future experiments:

-   Increase **Initial Noise Size** and **Noise Size** beyond current upper bounds
-   Vary **Noise Types**: General, Diagonal, Scalar, Additive
-   Compare **Ito vs. Stratonovich** integration
-   Test different **SDE processes** (e.g., Linear, Geometric Brownian Motion, Double-Well Potential)
-   Explore alternative **Optimisers**: SGD, Adagrad, RMSProp, etc.
-   Mix-and-match **Generator/Discriminator configurations** (e.g., different optimisers or noise types)
