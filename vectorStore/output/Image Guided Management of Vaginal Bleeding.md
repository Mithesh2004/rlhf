```markdown
# Standard Treatment Workflow (STW)
IMAGE GUIDED MANAGEMENT OF VAGINAL BLEEDING
ICD-10-H90.5, 072,D25

July/2024
सत्यमेव जयते
Department of Health Research
Ministry of Health and Family Welfare, Government of India
icma
INDIAN COUNCIL OF
MEDICAL RESEARCH
Serving
*   **HEAVY MENSTRUAL BLEEDING**
    Losing 80ml or more in each period, having periods that last longer than 7 days, or both
*   Uterus preserving treatment for two important causes of vaginal bleeding in women of reproductive age group
*   **POST PARTUM HAEMORRHAGE**
    500ml after vaginal delivery or 1000ml after Cesarean section

## SIGNS AND SYMPTOMS

|                |                                                                                                                              |                                                                                                                                                                                  |
| :------------- | :--------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Look for anaemia | Primary **PPH** is within the first 24 hour of delivery and secondary **PPH** is more than 24 hour after delivery           | Hypotension to haemorrhagic shock and multi-organ failure depending on the quantum of bleeding                                                                                |
|                | Prophylactic IR on patients with an increased risk of massive bleeding at delivery                                            | Check for uterine contractility, retained placenta Abnormal placenta on imaging                                                                                                    |

## INVESTIGATIONS

|                |                                           |                                                                                                                                                   |
| :------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
|                | **ESSENTIAL**                             | **OPTIONAL**                                                                                                                                    |
| **HEMATOLOGICAL** | **Hb, PT, INR, APTT and Platelet count**  | Thrombo-elastogram (TEG) or Rotational Thromboelastometry (ROTEM)                                                                               |
| **IMAGING**    | **USG**                                   | **MRI**                                                                                                                                         |

## MANAGEMENT

### FIBROID MANAGEMENT
*   Medical: **NSAIDS**, **Tranexamic acid**, combined oral contraceptive pills, progestogens
*   Interventional Radiology: **Uterine Artery Embolisation**
*   Surgical: **Myomectomy** or **Hysterectomy**

#### FIBROID: IR MANAGEMENT

*   Indications
    *   Fibroids with heavy menstrual cycles pain, pressure, and urinary symptoms
*   Contraindication:
    *   Suspected infection
    *   Approximate days of required hospitalisation: 1-3 days

#### PROCEDURAL DETAILS

*   Under conscious sedation or anaesthesia
*   Arterial access (femoral/radial)
*   Selective internal iliac arterial angiograms and cannulation of hypertrophied (uterine) arteries
*   Embolisaton with appropriate agent - **PVA** particles
*   Check angiogram
*   Expected outcomes: At 12 months, menorrhagia control in 90%-92% of patients and improvement in bulk symptoms in 88%-96%
*   Associated adverse events/complications
    *   Fibroid expulsion 5%
    *   Ovarian failure with amenorrhoea 7.5% of patients, overwhelming majority in women > 45 years of age
    *   Uterine sepsis requiring hysterectomy 0.1%
*   After care
    *   Pain management: **NSAIDS** and if required intravenous narcotics (Morphine sulfate 30 mg SC/IM/IV), hypogastric nerve block
    *   Follow up: after 3 months; clinical, Hb, USG
*   Other image guided minimally invasive treatment for fibroid include **HIFU** and ablation
*   Other gynaecological conditions like adenomyosis also can be managed similarly by **UAE**

### PPH MANAGEMENT
*   Medical: Intensive Care Support
    *   Uterotonic drugs - Oxytocin infusion: 20 IU in 500 ml RL/NS @ 40-60 drops/ minute
    *   Transfusion of blood products
    *   Inotropes, ventilation and other organ support
*   Interventional Radiology: Uterine Artery Embolisation
*   Surgical: Bilateral internal iliac artery ligation or Hysterectomy

#### PPH: IR MANAGEMENT
*   Indications
    *   Uterine atony despite medical treatment
    *   Vaginal or cervical tear after failed surgical repair
    *   Persistent hemorrhage after arterial ligation or hysterectomy
    *   Placenta accreta - including prophylactic treatment
*   Contraindication:
    *   Nil; but risk of acute kidney injury to be considered
    *   Approximate days of required hospitalisation: 2 to 7 days

#### Procedural details

*   Under conscious sedation or anaesthesia
*   Arterial access (femoral/radial)
*   Selective internal iliac arterial angiograms and cannulation of hypertrophied (uterine) arteries
*   Embolisaton with appropriate agents - **PVA** particles, gel foam, histoacryl etc.
*   Check angiogram
*   Expected outcomes: successful haemostasis > 95%
*   Associated adverse events/complications: ovarian failure, uterine sepsis, uterine infarctions (rare; less than 2%)
*   After care
    *   Medical: ICU care till bleeding arrests and organ failures are reversed
    *   Investigation: USG
    *   Criteria and timing for safe discharge: 3 days after the procedure if uneventful
    *   Follow up: after two weeks; Clinical, Hb, USG
*   Other obstetric conditions like post-abortive haemorrhage secondary to uterine artery pseudoaneurysm, complications of molar regnancy, uterine arteriovenous malformation (AVM) can also be treated similarly

```mermaid
graph TD
    A[VAGINAL BLEEDING] --> B{CLINICAL ASSESSMENT};
    B -- Haemodynamically unstable --> C1[PPH];
    B -- Symptomatic --> C2[HMB];
    C1 --> D1{Look for retained placenta, AVF (uterine)};
    D1 -- Yes --> E1[ICU care, blood products, Oxytocin infusion];
    E1 --> F1{Continued Bleed};
    F1 --> G1[Surgery];
    G1 --> H1[Hysterectomy];
    C2 --> D2{Assess anemia};
    D2 --> E2{Look for fibroids};
    E2 -- No --> F2[Gynaecology referral];
    E2 -- Yes --> F3[NSAIDS, Tranexamic acid, combined OCPS];
    F3 --> G2{No relief};
    G2 -- Submucosal fibroid --> H2[Hysteroscopic removal];
    G2 -- Intramural fibroids can be treated by UAE with preservation of the uterus --> H3[UAE];
    H3 --> I1{No Relief};
    I1 --> J1[Myomectomy];
    J1 --> K1[Hysterectomy];
    C1 --> L1[3 months Follow up];
     C2 --> L2[2 weeks Follow up];
     style A fill:#f9f,stroke:#333,stroke-width:2px
     style C1 fill:#f9f,stroke:#333,stroke-width:2px
     style C2 fill:#f9f,stroke:#333,stroke-width:2px
    
     style E1 fill:#f9f,stroke:#333,stroke-width:2px
     style E2 fill:#f9f,stroke:#333,stroke-width:2px
    
     style F1 fill:#f9f,stroke:#333,stroke-width:2px
     style F2 fill:#f9f,stroke:#333,stroke-width:2px
     style F3 fill:#f9f,stroke:#333,stroke-width:2px
    
     style G1 fill:#f9f,stroke:#333,stroke-width:2px
     style G2 fill:#f9f,stroke:#333,stroke-width:2px
    
     style H1 fill:#f9f,stroke:#333,stroke-width:2px
     style H2 fill:#f9f,stroke:#333,stroke-width:2px
     style H3 fill:#f9f,stroke:#333,stroke-width:2px
    
     style I1 fill:#f9f,stroke:#333,stroke-width:2px
     style J1 fill:#f9f,stroke:#333,stroke-width:2px
     style K1 fill:#f9f,stroke:#333,stroke-width:2px
     style L1 fill:#f9f,stroke:#333,stroke-width:2px
     style L2 fill:#f9f,stroke:#333,stroke-width:2px
    
    
```

GREEN FLAG SIGN
Symptomatic intramural fibroids
can be treated by **UAE**
with preservation of the uterus

RED FLAG SIGN
PR > 120/min
Systolic BP < 100 Mm Hg
Tachypnoea >20 breaths
per minute
SpO2 < 95%
Deterioration of sensorium
Refer to uterine fibroids and polyps ICD-10-D25 & N84
Refer to Postpartum hemorrhage ICD-72
Timely referral to a higher centre must be considered where facilities for ICU, surgical and IR are available

## CONCLUSION
*   Uterine artery embolization is a minimally invasive image guided procedure which has an important role in management of select cases of obstetric and gynecological conditions
*   It is a uterus preserving procedure
*   It has evolving role in case of uterine malignancies

## ABBREVIATIONS
APTT: Activated Partial Thromboplastin Time
AVF: Arteriovenous Fistula (uterine)
CECT: Contrast Enhanced Computed Tomography
Hb: Haemoglobin
HIFU: High Frequency Focussed Ultrasound
HMB: Heavy Menstrual Bleeding
ICU: Intensive Care Unit
INR: International Normalized Ratio
IR: Interventional Radiology
MRI: Magnetic Resonance Imaging
NSAIDs: Non-steroidal anti-inflammatory Drugs
OCPs: Oral Contraceptive Pills
PPH: Postpartum Haemorrhage
PT: Prothrombin Time
PVA: Poly Vinyl Alcohol
UAE: Uterine Arterial Embolization
USG: Ultrasonography
VB: Vaginal Bleeding

## REFERENCES
1.  Heavy periods, overview. NHS, UK. https://www.nhs.uk/conditions/heavy-periods/.
2.  Bulman JC, Ascher SM, Spies JB. Current concepts in uterine fibroid embolization. Radiographics. 2012 Oct;32(6):1735-50. doi: 10.1148/rg.326125514. PMID: 23065167.
3.  Newsome J, Martin JG, Bercu Z, Shah J, Shekhani H, Peters G. Postpartum Hemorrhage. Tech Vasc Interv Radiol. 2017 Dec;20(4):266-273. doi: 10.1053/j.tvir.2017.10.007. Epub 2017 Oct 10. PMID: 29224660.
4.  Mahankali, Subramanyam S.. Interventional Radiology: A Disruptive Innovation Which is Transforming Management of Post-Partum Haemorrhage. Journal of Obstetric Anaesthesia and Critical Care 7(2):p 65-68, Jul-Dec 2017. |
    DOI: 10.4103/joacc.JOACC_47_17
5.  Reiko Woodhams, The role of interventional radiology in primary postpartum hemorrhage, Hypertension Research in Pregnancy, 2016, Volume 4, Issue 2, Pages 53-64, Released on J-STAGE May 11, 2017, Advance online publication
    February 23, 2017, Online ISSN 2187-9931, Print ISSN 2187-5987, https://doi.org/10.14390/jsshp.HRP2015-016, https://www.jstage.jst.go.jp/article/jsshp/4/2/4_HRP2015-016/_article/-char/en
6.  Sone M, Nakajima Y, Woodhams R, Shioyama Y, Tsurusaki M, Hiraki T, Yoshimatsu M, Hyodoh H, Kubo T, Takeda S, Minakami H. Interventional radiology for critical hemorrhage in obstetrics: Japanese Society of Interventional
    Radiology (JSIR) procedural guidelines. Jpn J Radiol. 2015 Apr;33(4):233-40. doi: 10.1007/s11604-015-0399-0. Epub 2015 Feb 19. PMID: 25694338.
7.  Kim TH, Lee HH, Kim JM, Ryu AL, Chung SH, Seok Lee W. Uterine artery embolization for primary postpartum hemorrhage. Iran J Reprod Med. 2013 Jun;11(6):511-8. PMID: 24639786; PMCID: PMC3941316.

KEEP A HIGH THRESHOLD FOR INVASIVE PROCEDURES

This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert
opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by the treating physician. There will be no
indemnity for direct or indirect consequences. Kindly visit the website of ICMR for more information: (icmr.gov.in) for more information. Indian Council of Medical Research, Ministry of Health & Family
Welfare, Government of India.
```