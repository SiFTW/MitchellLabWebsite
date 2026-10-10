---
title: Applying computational modelling to a high-risk multiple myeloma data set to
  create novel risk stratification groupings
authors:
- Orthi Shahzad
- Richard Norris
- Niels Weinhold
- Charlotte Pawlyn
- Brian Walker
- Cody Ashby
- Christopher Wardell
- David Cairns
- Martin Kaiser
- Gordon Cook
- Faith Davies
- Mark Drayson
- Roger Owen
- Graham Jackson
- Gareth Morgan
- Simon Mitchell
- John Jones
date: '2025-11-01'
doi: https://doi.org/10.1182/blood-2025-5790
publication: Conference Abstract (Blood (Supplement 1))
publication_types:
- '1'
abstract: "**Abstract**\n\n \n \n Introduction:\n\n Multiple Myeloma (MM) is a heterogeneous\
  \ disease making it difficult to accurately predict the disease course in individual\
  \ patients. Staging systems in MM have evolved, firstly the International Staging\
  \ System (ISS), then incorporation of genomic aberrations with revised-ISS. Recently,\
  \ the IMWG agreed on consensus genomic staging of high-risk MM. However, no scoring\
  \ system captures the nuances of the genetic landscape of each MM patient. In the\
  \ era of genomic profiling, this information should be utilised to predict disease\
  \ behaviour, which can be achieved through computational modelling.\n\n We recently\
  \ developed and validated a model signalling network within B cells, which predicts\
  \ pathway activation and protein abundance in B cells. We hypothesised that inclusion\
  \ of genetic mutations from MM as parameter changes in this model could enable the\
  \ creation of patient specific virtual cells that could improve disease stratification.\n\
  \n Methods:\n\n Genetic data for 53 newly diagnosed MM patients, enrolled to the\
  \ NCRI Myeloma XI was collected. The cohort were phenotypically high risk, relapsing\
  \ within 30 months of maintenance randomisation. All patients achieved at least\
  \ a partial response prior to relapse. Whole exome sequencing was conducted at presentation\
  \ and relapse. All genetic mutations (SNPs, copy number variants, translocations)\
  \ were verified for their oncogenic potential with OncoKB.\n\n Each mutation in\
  \ each patient was mapped to a model parameter to create a set of 53 unique patient\
  \ models in silico (e.g. gain of one copy of BCL2 increased the parameter representing\
  \ BCL2 expression by 50%). To determine the apoptotic, and proliferative signalling\
  \ state of the patient models 6-hour simulation was performed and the predicted\
  \ abundance of cytoplasmic Smac, cytochrome C and cadherin-1 was stored. Patients\
  \ were grouped according to their predicted signalling state, namely anti-apoptotic\
  \ (AA, n=16), pro-proliferative (PP, n=11), anti-apoptotic and pro-proliferative\
  \ (AAPP, n=15) and non-proliferative or apoptotic (NAP, n=11). We compared progression-free\
  \ survival (PFS) in days between different groups using Cox regression for Hazard\
  \ ratios (HR) and Log-Rank test for p-values.\n\n Results:\n\n As a benchmark we\
  \ first evaluated the ISS in our cohort. ISS II versus ISS I was associated with\
  \ a significantly worse PFS (HR 2.27 95% CI 1.07-4.8, p=0.032) as well as ISS III\
  \ (HR 2.45 CI 1.13-5.31 p=0.024). However, ISS II was not significantly different\
  \ from ISS III, likely due to the phenotypic high-risk cohort assessed.\n\n High-risk\
  \ lesions del(17p), gain(1q), del(1p), (t(4;14), t(14;16), t(14;20) and neutral\
  \ lesions, del(13q), HRD, t(6;14), t(11;14) and t(MYC), were all non-significant\
  \ predictors of progression (p&gt;0.05). Maintenance strategy (lenalidomide vs observation)\
  \ was also not a significant predictor of outcome, consistent with the phenotypic\
  \ behaviour.\n\n We then applied the model-driven signalling state stratification\
  \ (AA, PP, AAPP, NAP) and found model stratification alone significantly predicted\
  \ PFS (p=0.047). The PP group was associated with the longest PFS and the NAP group\
  \ had the shortest (HR 3.33 CI 1.37-8.11, p=0.008). No HR genetic lesions were noted\
  \ in the PP group, compared to 2/11 (18%), 4/16 (25%) and 7/15 (47%) for the NAP,\
  \ AA and AAPP groups respectively.\n\n To incorporate modelling with existing prognostic\
  \ tools we combined all good prognosis patient groups (ISS I [n=13], and PP patients\
  \ [n=11]) into one group and compared it to the rest. This stratification method\
  \ identified 9/53 (17%) patients with high ISS (II/III), but good prognosis predicted\
  \ through modelling, and assigned them to the low-risk group. The remaining high\
  \ risk patients (n=29) had a significantly higher HR of 2.21 for shorter PFS (CI\
  \ 1.24-3.94, p=0.007).\n\n Conclusion:We show that computational modelling can be\
  \ utilised to stratify MM patients into both good and poor prognostic groups in\
  \ ways that improve on previous staging systems. Furthermore, this has been illustrated\
  \ within a phenotypical high-risk cohort, emphasising its ability to uncover distinct\
  \ subgroups in previously hard to classify patients. This approach provides the\
  \ foundation for a novel approach to improving treatment decisions, developing personalised\
  \ approaches such as treatment intensification based on the full genetic profile\
  \ of an individual patient. Characterising the signalling state in a larger cohort\
  \ and predicting response to treatment is underway."
---
