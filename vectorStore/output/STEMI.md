```markdown
# Standard Treatment Workflow (STW) for the Management of ST ELEVATION MYOCARDIAL INFARCTION (STEMI)

October/2019
ICD-10-121.3

CONSIDER ANGINA IF

*   Diffuse retrosternal pain, heaviness or constriction
*   Radiation to arms or neck or back
*   Associated with sweating
*   Easily reproduced with post-meal exertion
*   Consider atypical presentation: Exertional fatigue or breathlessness or profuse sweating or epigastric discomfort/ syncope
*   More likelihood if known patient of CAD/ multiple risk factors

ACUTE CORONARY SYNDROME:

1.  Angina at rest or lasting more than 20 minutes
2.  Recent worsening of stable angina (crescendo) to CCS class III
3.  New onset effort angina of less than 1 month in CCS class II/III
4.  Post infarction angina

ANGINA UNLIKELY IF:

*   Variable location or characteristic
*   Long lasting (hours to days) or short lasting (less than a minute)
*   Restricted to areas above jaw or below epigatrium
*   Localized to a point
*   Pricking or piercing or stabbing type of pain
*   Precipitated by movement of neck or arms or respiration

ECG: If **ST Elevation**: Follow **ST Elevation MI (STEMI)** protocol
If no **ST Elavation**: UA/NSTEMI

## PATIENT WITH STEMI WITHIN 12 HOURS

ECG REVEALS ST ELEVATION MI*

*   Refer to primary angioplasty/ thrombolysis capable hospital
*   *Includes new onset LBBB

### GENERAL MEASURES

1.  Admit in ICU equipped with continuous ECG monitoring & defibrillation
2.  Routine bio-chemistry and serial cardiac enzymes (troponin)
3.  Pain relief by opioid
4.  O2 if saturation less than 90%
5.  Aspirin 325 mg, Clopidogrel 300 mg and Atorvastatin 80 mg
6.  Echocardiography, particularly for mechanical complication

### PCI CAPABLE HOSPITAL

1.  Proceed for PCI
2.  Radial route preferred
3.  Preferably within 90 minutes

### DURING PROCEDURE

1.  Use unfractionated heparin
2.  No routine thrombosuction
3.  Tackle culprit artery only unless shock
4.  DES to be preferred

### POST PROCEDURE

1.  Continue dual antiplatelets for at least 1 year

### PCI INCAPABLE CENTRE

A. Tranfer to PCI capable hospital if PCI can be performed within 120 min

B. If Transfer to PCI capable hospital not feasible

### THROMBOLYSE

1.  Within 12 hours of symptom onset, if no contra-indication
2.  Preferably with fibrin specific agent Tenecteplase/ TPA/ Reteplase or Streptokinase, if fibrin-specific are unavailable
3.  Therapy to be started within 10 min preferably

### POST THROMBOLYSIS

1.  ECG to be done at 60-90 min after starting thrombolysis to assess whether thrombolysis is successful (>50% ST settlement with pain relief) or not
2.  If successful, transfer patient for PCI within 3-24 hours
3.  If thrombolysis failed, transfer patient immediately for PCI capable hospital
4.  Enoxaparin (preferred over unfractionated heparin) to be continued till PCI OR discharge

## LOOK FOR OTHER CAUSES OF CHEST PAIN (ONGOING OR WITHIN 12 HRS)

*   Unequal or absent peripheral pulses - Dissection of Aorta
*   Respiratory evaluation - Pleuritis/ Pneumonitis/ embolism/ pneumothorax
*   Pericardial rub
*   Neuralgia or herpes

## PATIENT WITH STEMI IN 12-24 HOURS

Transfer to PCI capable hospital immediately
If ongoing pain, thrombolysis and transfer immediately

## PATIENT WITH STEMI AFTER 24 HOURS

Angiography with a view to PCI only if any of following/ Contra indications of angiography:

*   Recurrent anginal pain not controlled by medical therapy
*   Cardiogenic shock
*   Acute LVF
*   Mecahnical complication
*   Dynamic ST-T changes
*   Life threatening ventricular arrhythmias

## ABSOLUTE CONTRA-INDICATIONS TO THROMBOLYIC THERAPY:

*   Previous intra-cerebral hemorrhage or stroke of unknown etiology
*   Ischemic stroke in last 6 months
*   CNS neoplasm or AV malformation
*   Recent (within 1 month) major trauma/surgey/ head injury
*   Recent (within 1 month) major GI bleed
*   Known bleeding tendency (except menstrual bleed)
*   Severe uncontrolled hypertension
*   Aortic dissection

## DRUGS & DOSAGE

### Anti-platelets

1.  Aspirin: Loading dose 325 mg followed by 75 mg OD
2.  Clopidogrel: Loading dose 300 mg followed 75 mg OD
3.  Prasugrel: Loading dose 60 mg followed by 10 mg OD
4.  Ticagralor: Loading dose 180 mg followed by 90 mg BD

### Anti-ischemic:

*   Metoprolol:
    *   Short acting: 25-100 mg BD
    *   Long acting: 25-100 mg OD
*   Nitrates:
    *   Isosorbide mono-nitare 20 to 60 mg in 2 divided dose
    *   Nitroglycerine sustained release 2.6 to 6.5 mg BD
    *   Nitroglycerine IV 5-25 mcg/min infusion
*   Statins: High dose Atorvastatin 80 mg OD
*   Ace-inhibitor:
    *   Ramipril 2.5-10 mg OD
    *   Enalapril 2.5-10mg BD
*   Oxygen: If oxygen saturation below 90%
*   Morphine: Titrated in a dose of 2-4 mg IV every 15 minutes
*   Beta-blocker: Oral beta-blocker if LVEF is less than 40%

### Anti thrombotics:

1.  Unfractionated heparin: Bolus of 60 U/Kg (maximum 5000 U) followed by 12 U/Kg hourly infusion to maintain APTT at 50-70 sec
2.  Enoxaparin: 1 mg/Kg SC 12 hrly

### Thrombolyic Therapy:
Tenecteplase

*   35 mg IV bolus if 60-70 Kg
*   40 mg IV bolus if 70-80 Kg
*   45 mg IV bolus if more than 80 Kg
Reteplase

*   10 mg IV bolus, repeat after 30 min
Alteplase

*   15 mg IV bolus followed by 0.75 mg/Kg over 30 min upto 50 Kg weight, then 0.5 mg/Kg over 60 min up to 35 mg
Streptokinase
*   1.5 million units IV over 60 min

```mermaid
graph TD
    A[EMS or non primary-PCI capable centre] --> B{PCI possible <120 mins?};
    B -- Yes --> C[Immediate transfer to PCI centre];
    B -- No --> D{Successful fibrinolysis};
    D -- Yes --> E[Immediate transfer to Coronary angiography Preferably 3-24 hours];
    D -- No --> F[Rescue PCI Immediately Preferably <90mins (<60 mins) in early presenters];
    H[Immediate fibrinolysis];
    G[Primary-PCI capable centre] --> H;
    C --> Primary PCI;
    F --> Pan centre;
    H --> I[The time point the diagnosis is confirmed with patient history & ECG ideally within 10mins from the First Medical Contract (FMC). All delays are related to FMC.];
```

## STEMI DIAGNOSIS*

### KEEP A HIGH THRESHOLD FOR INVASIVE PROCEDURES

This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit our web portal (stw.icmr.org.in) for more information.
Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
```