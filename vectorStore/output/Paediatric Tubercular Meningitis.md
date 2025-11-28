```markdown
# Standard Treatment Workflow (STW) for the Management of
PAEDIATRIC TUBERCULAR MENINGITIS
ICD-10-A17.0

## WHEN TO SUSPECT?
*   Fever with one or more of the following
    *   Headache
    *   Vomiting
    *   Seizures
    *   Irritability/Lethargy/ Drowsiness
    *   Loss of function e.g. recent onset deviation of eyes/mouth and/or weakness of arm/leg and/or altered mentation
    *   Malaise, Anorexia, Weight loss

*   Symptoms are usually of 5 to 7 days duration with insidious onset, particularly with history of exposure to infectious TB in past 2 years

## EXAMINATION
*   Assessment of sensorium*
*   Full/bulging anterior fontanelle
*   Meningeal irritation- Neck stiffness, Kernig's sign & Brudzinski's sign
*   Examine eye, if feasible for papillodema/ choroid tubercles/optic atrophy
*   Cranial nerves
*   Motor system including power, reflexes plantar responses
*   Peripheral lymph nodes
*   Chest examination for signs of pulmonary involvement

*Use any standardized scale including Glasgow Coma scale/AVPU scale

## INVESTIGATIONS
**Essential**
*   CBC
*   CSF examination
    *   Cell count and differential
    *   Sugar (with simultaneous blood sugar)
    *   Protein
    *   NAAT*
    *   MGIT culture
    *   Bacterial culture
*   HIV
*   Contrast enhanced CT scan of head
*   CXR
*   Gastric lavage/ Induced sputum in patients where CXR is abnormal and CSF NAAT is negative

*ICMR/NTEP approved NAAT test, use 3-5 ml CSF if possible

**Desirable**
*   MRI brain with contrast when CECT head is not contributory

**Optional**
*   CSF cryptococcal antigen
*   Contrast CT chest/abdomen to look for extracranial sites of infection

## NEUROIMAGING IN TB
CECT showing
*   Hydrocephalus (ventricular dilatation)
*   Thick basal exudates
*   Tuberculoma

## DIAGNOSTIC ALGORITHM
*   Immediate investigations
    *   CBC, HIV
    *   CECT head
    *   CSF: Cell count including differential, CSF sugar (with blood sugar), protein, NAAT, bacterial culture
    *   CXR
AFB seen/CSF NAAT +ve (Microbiologically confirmed TBM)

```mermaid
graph LR
    A[SUSPECTED TBM?] --> B{Criterion 1 \n ≥3 of the following \n ≥5 days of symptoms as above \n TLC < 15,000/cumm \n CSF WBC 10-500/cumm \n CSF sugar < 50% of blood sugar \n CSF lymphocytes >50% \n Neuroimaging finding of (one or more): \n > Basal exudates \n > Hydrocephalus \n > Infarct \n > Tuberculoma};
    C{Criterion 2- Criteria positive if at least 2 \n of the following 3 risk factors are present \n HIV infection \n Severe acute malnutrition \n Recent contact with infectious TB} --> B;
    D[Criterion 3 \n Evidence of TB elsewhere] --> B;
    B --> E{2 or more criteria met};
    E -- Yes --> F[Start treatment];
    E -- No --> G[Continue investigations & management for partially \n treated bacterial meningitis \n IF NOT BETTER];
    G --> H[Repeat LP after 48-72 hours \n Expand search for TB elsewhere \n Consider MRI contrast if not done earlier];
    H --> I{Re-review criterion 1, 2 & 3 and see if ≥ 2 criterion fulfilled};
    I -- Yes --> F;
    I -- No --> J{Does patient have falling CSF glucose/dropping sensorium? \n Have new focal deficit?};
    J -- Yes --> F;
    J -- No --> K[Continue \n evaluation];
```

## TREATMENT
*   Treatment should be started & follow-up to be done as per NTEP guidelines
*   Anti TB drug regimen
    *   2 HRZE and 10 HRE (in appropriate doses)
    *   Pyridoxine 10 mg/day
*   Corticosteroids
    *   Prednisolone 2 mg/kg/day for 4 weeks & then taper over 4 weeks
    *   Slower taper needed in some patients

*Equivalent dose of another steroid formulation may be used either injectable/oral
*   Other supportive therapy
    *   Care of unconscious child
    *   Nasogastric feeding, if indicated
    *   Anti edema measures (mannitol/ hypertonic saline/glycerol/ acetazolamide)
    *   Anticonvulsants, if seizures
*   Surgical therapy, if indicated
    *   External ventricular drain
    *   VP shunt
*   Cases should be managed at least at a district hospital
*   Early referral to Medical College/ higher centre to be considered if
    *   Unresponsive child/rapid deterioration indicating need for intensive care
    *   No diagnosis after initial evaluation
    *   Surgical treatment needed
    *   MDR TB meningitis
    *   No improvement/deterioration after 2-4 weeks of treatment
*   Need for ICU care

## ABBREVIATIONS
HRZE: Isoniazid; Rifampicin; Pyrazinamide; Ethambutol
AFB: Acid-fast Bacillus
CXR: Chest X-ray
CBC: Complete Blood Count
HIV: Human Immunodeficiency Virus
CECT: Contrast Enhanced Computed Tomography
CSF: Cerebro-spinal Fluid
ICU: Intensive Care Unit
CT: Computed Tomography
LP: Lumbar Puncture
MDR: Multi-drug Resistant
MGIT: Mycobacteria Growth Indicator Tube
MRI: Magnetic Resonance Imaging
NAAT: Nucleic Acid Amplification Test
NTEP: National TB Elimination Programme
TB: Tuberculosis
TBM: Tubercular Meningitis
TLC: Total Leucocyte Count
VP: Ventriculo-peritoneal
WBC: White Blood Cells

## REFERENCES
1.  National TB Elimination Programme, Central TB Division. Training Modules for Programme Managers & Medical Officers. Ministry of Health & Family Welfare, Government of India
    https://tbcindia.gov.in/index1.php?lang=1&level=1&sublinkid=5465&lid=3540 Last access on 05 March, 2022.
2.  Guidelines for Programmatic Management of Drug Resistant Tuberculosis in India March 2021. National TB Elimination Programme, Central TB Division, Ministry of Health & Family Welfare, Government of India https://tbcindia.gov.in/showfile.php?lid=3590 Last access on 05 March, 2022.

This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit our web portal (stw.icmr.org.in) for more information.
Indian Council of Medical Research and Department of Health Research, Ministry of Health & Family Welfare, Government of India.
```