---
title: Patient-specific computational models predict prognosis in B cell
  lymphoma by quantifying pro-proliferative and anti-apoptotic signatures from
  genetic sequencing data
publication_types:
  - "2"
authors:
  - Richard Norris
  - John Jones
  - Erika Mancini
  - Timothy Chevassut
  - Fabio A. Simoes
  - Chris Pepper
  - Andrea Pepper
  - Simon Mitchell
doi: https://doi.org/10.1038/s41408-024-01090-y
publication: Blood Cancer Journal
publication_short: Blood Cancer Jnl
abstract: Genetic heterogeneity and co-occurring driver mutations impact
  clinical outcomes in blood cancers, but predicting the emergent effect of
  co-occurring mutations that impact multiple complex and interacting signalling
  networks is challenging. Here, we used mathematical models to predict the
  impact of co-occurring mutations on cellular signalling and cell fates in
  diffuse large B cell lymphoma and multiple myeloma. Simulations predicted
  adverse impact on clinical prognosis when combinations of mutations induced
  both anti-apoptotic (AA) and pro-proliferative (PP) signalling. We integrated
  patient-specific mutational profiles into personalised lymphoma models, and
  identified patients characterised by simultaneous upregulation of
  anti-apoptotic and pro-proliferative (AAPP) signalling in all genomic and
  cell-of-origin classifications (8-25% of patients). In a discovery cohort and
  two validation cohorts, patients with upregulation of neither, one (AA or PP),
  or both (AAPP) signalling states had good, intermediate and poor prognosis
  respectively. Combining AAPP signalling with genetic or clinical prognostic
  predictors reliably stratified patients into striking prognostic categories.
  AAPP patients in poor prognosis genetic clusters had 7.8 months median overall
  survival, while patients lacking both features had 90% overall survival at 120
  months in a validation cohort. Personalised computational models enable
  identification of novel risk-stratified patient subgroups, providing a
  valuable tool for future risk-adapted clinical trials.
draft: false
featured: true
projects:
  - primary-DLBCL
  - RR-DLBCL
image:
  filename: featured.png
  focal_point: Smart
  preview_only: false
date: 2024-07-07T09:55:38.443Z
---
In this study, led by [Richard Norris](/authors/Richard/) we asked: If you take a simulation of healthy cells, and add patient-specific mutations, can you predict patient outcome?

This journey started with the last Figure of [the Immunity paper](/publication/roy-2019-regulatory/) published with Alex Hoffmann and Koushik roy back in 2019. The simulations we were using to understand healthy B-cells looked a bit like lymphoma if we changed the right numbers. So, can we simulate lymphoma?

We first looked at double hit lymphoma (DHL), with mutations in MYC and BCL2/BCL6. These patients have poor prognosis.  The model predicts lots of cells when MYC+BCL2 are mutated but not MYC+BCL6 are mutated. Excitingly, this aligns with prognosis in recent trials!

![](twitterdh.png)

Does this work with any other patient archetypes?

Yes! Gain1q multiple myeloma is a very poor prognosis B-cell cancer, and if we simulate increasing copies of some key genes involved in the disease the simulation predicts more and more cells with more and more copies of chromosome 1q. This again, aligns with recent clinical trial results, building faith in the model's ability to predict outcome from mutations.

![](twittermm.png)

Question: What do the previous combinations of mutations have in common?
A: They are both combinations of mutations that increase cell division and decrease cell death (MYC+BCL2, CKS1B+MCL1). These combination of mutations map to the apoptotic and cell division networks in the mode. Therefore we asked: can we use our simulations to find more lymphoma patients with reduced cell death, and increased cell division?

![](twitterpipeline.png)

We took mutational data (WES/WGS/targeted), and created personalised simulations.
Simulating individual patients from Chapuy et al. 2018 revealed patients predicted to have pro-proliferative signaling, anti-apoptotic signaling, neither and both.

How do these patients do? What is their prognosis?

![](twitterkm.png)

In a discovery cohort and 2 validation cohorts patients predicted to have both anti-apoptotic and pro-prolfierative signalling do much worse.
This is particularly interesting because we only simulate 6 hours of cell signalling, and can predict >10 years of patient outcomes!

![](twitterothermetrics.png)

Simulations finds poor prognosis patients within all patient groups (cell of origin, genetic clusters, IPI etc).
This means when we combine the model stratification with other metrics we get striking predictions.
The model lets us find patients that won't benefit from R-CHOP.

So to recap: 

* Simulations can reveal when mutations combine in unexpected ways.
* By simulating patients, we can predict when mutations will combine to create "double hit"-like signalling.
* If we want to design clinical trials that succeed should we target these patients?
* Perhaps we can give kinder/reduced treatments to the good prognosis patients?

What's next?

* Now that we can identify patients that need new approaches, can we use these virtual patients to find targeted therapies that will work?
* Could this work in other diseases? Myeloma? CLL? or even breast cancer?

Thank you to [Leukaemia UK ](/project/primary-dlbcl/)and the [UKRI](/project/rr-dlbcl/) for funding this work.
