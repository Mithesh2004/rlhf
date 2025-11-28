```markdown
# Standard Treatment Workflow (STW)
POST-ASPHYXIAL MANAGEMENT OF NEONATES
ICD-10-P21.0

## IMMEDIATE MANAGEMENT OF AN ASPHYXIATED NEONATE

```mermaid
graph LR
    A[Need for Positive pressure ventilation (PPV) at birth OR Referred with history of delayed cry at birth] --> B{PPV for <60 seconds OR Delayed cry and resuscitation details not available};
    B -- Yes --> C[Assess 15 minutes after birth OR at admission];
    C -- Yes --> D{1. Lethargy/coma or irritability? 2. Absent spontaneous movements? 3. Absent Suck and Moro's reflex? 4. Abnormal movements (limb jerks, cycling, swimming, chewing, sucking movements which are persistent and monotonous) ? 5. Respiratory distress? 6. Features of shock ?};
    D -- Yes --> E[At risk of hypoxic-ischemic encephalopathy (HIE)];
    E -- Yes --> F[Check vitals and blood glucose Temperature, heart rate, respiratory rate, oxygen saturation (SpO₂), capillary refill time Check blood glucose];
    F --> G[Stabilization and Supportive Treatment Secure airway If SpO2 <91%, start O₂ by prongs/hood If respiratory distress persists, follow STW for respiratory distress; consider CPAP if chest retractions or persistent hypoxia Start IV 10% dextrose at 60 mL/kg/day Maintain normal temperature; avoid hyperthermia Target blood glucose of 50-125 mg/dL If infant has seizures, follow STW for seizure];
    
    B -- No --> L[Shift to mother's side Initiate breastfeeding Skin-to-skin contact Observe every 15 minutes for 1 hour];
    D -- No --> L;
    E -- No --> H{Initiate feeds once vitals are stable Switch to breastfeeding as early as possible. Continue monitoring for 24hrs};
    H -- Yes --> I{No HIE or Mild HIE};
    I -- Yes --> M[Assess for moderate to severe HIE Lethargic or comatose with ANY ONE of the following: 1. Seizures 2. Decreased muscle tone 3. Absent/weak Suck or Moro's reflex};
    M -- Yes --> N[Needs further assessment; may need therapeutic hypothermia];
    N --> O{Moderate or severe HIE};
    M -- No --> G;
```

## NEONATE WITH MODERATE OR SEVERE HYPOXIC-ISCHEMIC ENCEPHALOPATHY

```mermaid
graph LR
    A{FULFILLS ALL OF THE FOLLOWING CRITERIA? ≥ 36 weeks gestational age ≥ 1800g birth weight < 6 hrs old Admission temperature 36-37.4 °C} --> B{All of the following are fulfilled: pH <7 or base excess ≥16 on cord or arterial blood gas done within 1 h of life AND Apgar score< 5 at 10 minutes or at least 10 min of PPV AND History of acute perinatal event (such as but not limited to placental abruption, uterine rupture, cord prolapse)};
    A -- No --> C[PROVIDE SUPPORTIVE TREATMENT Secure airway If SpO2 <91%, start O₂ by prongs/hood Start IV 10% dextrose at 60 mL/kg/day Maintain normal temperature; avoid hyperthermia Target blood glucose of 50-125 mg/dL If infant has seizures, follow STW for seizures];
    B -- No --> C;
    B -- Yes --> D{Moderate to Severe HIE}
    D -- Yes --> E{Written protocol and facility for therapeutic hypothermia and level-3 intensive care available?}
    E -- No --> F[REFER TO HIGHER CENTRE];
    E -- Yes --> G[Initiate whole body cooling using a servo-controlled mattress/phase-change material (PCM) based device / ice or gel packs. If using gel or ice packs/PCM - ensure presence of nurse in 1:1 ratio for the neonate being cooled Whatever the device used, the cooling targets and monitoring are similar: Continuous rectal temperature monitoring is required from initiation until 8 hrs after rewarming Target rectal temperature is 33-34 °C Induction: aim to attain target temperature in the first 30 minutes Maintenance: continue to maintain target temperature for 72 hrs after initiation Rewarming: increase rectal temperature to 36.5 °C over 6-12 hrs, at a rate ≤ 0.5 °C per hour];
```

### ABBREVIATIONS
*   BE: Base excess
*   CBC: Complete blood count
*   CRP: C reactive protein
*   CSF: Cerebrospinal fluid
*   **HIE**: Hypoxic-ischemic encephalopathy
*   NICU: Neonatal intensive care unit
*   PPV: Positive pressure ventilation
*   SNCU: Special newborn care unit

### REFERENCES

1.  NNF Working Group. Position Statement and Guidelines for Use of Therapeutic Hypothermia to treat Neonatal Hypoxic Ischemic Encephalopathy in India. New Delhi: National
    Neonatology Forum, India; 2021 Oct.
2.  Sarnat HB, Sarnat MS. Neonatal Encephalopathy Following Fetal Distress: A Clinical and Electroencephalographic Study. Arch Neurol-chicago. 1976; 33(10):696-705.
3.  Abate BB, Bimerew M, Gebremichael B, Kassie AM, Kassaw M, Gebremeskel T, et al. Effects of therapeutic hypothermia on death among asphyxiated neonates with
    hypoxic-ischemic encephalopathy: A systematic review and meta-analysis of randomized control trials. Plos One. 2021; 16(2):e0247229.

### FREQUENT MULTI-SYSTEM MONITORING IS A MUST

This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and
are based on expert opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by
the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit the website of DHR for more information: (stw.icmr.org.in) for more information.

Department of Health Research, Ministry of Health & Family Welfare, Government of India.
```