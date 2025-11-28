```markdown
# Standard Treatment Workflow (STW) for the Management of **POSTPARTUM HAEMORRHAGE (PPH)**

*October/2019*

*ICD 072*

More than 500 ml of blood loss or any amount of bleeding which causes derangement of vital parameters is **PPH**

**RED FLAG SIGN:**

*   PR > 120/min
*   Systolic BP < 100 mm Hg
*   Tachypnea < 95%
*   SpO2 < 95%
*   Deterioration of sensorium

*   Call for help
*   Rapid Initial Assessment - evaluate vital signs: PR, BP, RR and Temperature
*   Establish two IV lines with wide bore cannula (16-18 gauge)
*   Draw blood for grouping and cross matching
*   Start RL/NS, infuse 1 L in 15-20 minutes
*   Give Oxygen @ 6-8 L/minute by mask,
*   Insert indwelling Catheter and connect to urobag
*   Check vitals and blood loss frequently - at least every 15 minutes
*   Monitor input and output

**SUPPORTIVE MANAGEMENT**

*   Monitoring of vitals
*   Measurement of input and output
*   Give blood transfusion as indicated

*   Give Inj. Oxytocin 10 IU IM (if not given after delivery)
*   Start Oxytocin infusion: 20 IU in 500 ml RL/NS @ 40-60 drops per minute
*   IV bolus of oxytocin should NOT be given
*   Check to see if placenta has been delivered.

```mermaid
graph TD
    A[Initial Assessment and Actions] --> B{PLACENTA NOT DELIVERED};
    A --> C{PLACENTA DELIVERED};
    
    B --> D[Continue Oxytocin drip];
    B --> E[Palpate uterus];
    B --> F[Attempt controlled cord traction if uterus is contracted];
    
    C --> G[Fundal Massage of the uterus];
    C --> H[Inspect placenta for completeness];
    C --> I[Explore uterus for any retained placental bits/membranes/clots and evacuate];
    
    I --> J{PLACENTA DELIVERED};
        J --> K[Continue oxytocin and uterine massage];
        J --> L[Check for completeness of placenta and membranes];
    
    I --> M{PLACENTA NOT DELIVERED};
        M --> N[Shift for manual removal of placenta (MRP)];
        
    L --> O{Uterus well contracted but bleeding continuing};
        O --> P[TRAUMATIC PPH];
            P --> Q[Explore for cervical/vaginal/perineal tears. Repair if present];
            P --> R[If bleeding persists despite repair of above, suspect inadequate repair, rupture uterus or scar dehiscence];
            P --> S[Shift to OT for exploration under GA and/or laparotomy];
            P --> T[Arrange for blood / blood product at the earliest];
        
    L --> U{Uterus flabby};
        U --> V[ATONIC PPH];
            V --> W[Bimanual compression and pharmacotherapy as per details below];
    
    V --> X[If bleeding continues without any apparent cause check for coagulopathy];
```

3 ml of crystalloid solution should be used to replace every ml of blood lost during the initial part of the acute bleeding phase

## MANAGEMENT OF ATONIC PPH

### PHARMACOTHERAPY

(Any of the following options can be used either alone or combination as per availability)

*   Inj Methyl Ergometrine 0.2 mg IM or IV slowly
    *   Contraindicated in hypertension, severe anemia, heart disease
    *   Can be repeated after 15 minutes to a maximum of 5 doses (1mg)
*   Tab Misoprostol (PGE1) 800 µg
    *   Per rectal or sublingual
*   Inj Carboprost (PGF2 alpha) 250 µg IM
    *   Contraindicated in asthma
    *   Can be repeated every 20 minutes to a maximum of 8 doses (2 mg)

```mermaid
graph TD
    A[Pharmacotherapy] --> B{Bleeding not controlled};
    A --> C{Bleeding controlled};
    
    B --> D[Explore uterus for retained bits];
    B --> E[Continue bimanual compression & Oxytocin infusion @10-20 units/hr];
    B --> F{Bleeding not controlled};
    
    F --> G[Check for coagulation defects];
        G --> H[If present give blood and blood components];
    
    C --> I[Repeat uterine massage every 15 minutes for first two hours];
    C --> J[Monitor vitals every 10 minutes for 30 minutes, every 15 minutes for next 30 minutes and every 30 minutes for next 3-6 hours or until stable];
    C --> K[Continue Oxytocin infusion @5-10 units/hr (total Oxytocin not to exceed 100 IU in 24 hours)];
    
    E --> L[Intra uterine balloon tamponade using condom catheter];
    L --> M{Bleeding still not controlled};
    
    M --> N[Surgical intervention];
        N --> O[Uterine compression sutures];
        N --> P[Systematic uterine devascularisation by doing Uterine → Ovarian Internal Iliac artery ligation];
        N --> Q[Hysterectomy];
```

Tranexamic Acid (1g slow IV) has recently been recommended as an adjunctive treatment for PPH to be used as early as possible irrespective of cause but definitely within three hours of delivery. It can be repeated after 30 minutes if bleeding persists. Standard treatment for PPH must continue meanwhile 1, 2
1 The WOMAN trial, The Lancet, 2017
2 WHO update on Tranexamic Acid, 2017

Timely Referral to a higher centre must be considered if facilities for blood transfusion or exploration and surgical intervention are not available. Patient must be transported with I/V fluids containing oxytocin on flow and preferably with uterine/vaginal tamponade in situ.
Aortic compression may be used as a short time measure to reduce blood loss while awaiting definitive steps.
Non-pneumatic anti-shock garment (NASG) should be used during transport if available
Uterine artery embolization may be offered in selected patients if facilities are available

**COUNSELLING IS AN IMPORTANT ADJUNCT TO MANAGEMENT**

**KEEP A HIGH THRESHOLD FOR INVASIVE PROCEDURES**

This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit our web portal (stw.icmr.org.in) for more information.
Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
```