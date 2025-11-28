```markdown
# Standard Treatment Workflow (STW)
FEEDS & FLUIDS IN NEONATES
ICD-10-R63.3

PART A
Nutritional plan for infants not on enteral feeds at admission

IF ANY OF THE FOLLOWING ARE PRESENT

```mermaid
graph LR
    A[Nutritional plan for infants not on enteral feeds at admission] --> B{IF ANY OF THE FOLLOWING ARE PRESENT};
    B -- NO --> C[Gestation <35 wks & REDF in antenatal USG];
    B -- OR --> D[Gestation <35 wks and birth weight <3rd centile or AEDF in antenatal USG, need for extensive resuscitation, OR HIE, 5 minute Apgar <7, has RED signs (Part B)];
    B -- OR --> E[Suspected Gl malformation or suspected NEC];
    C --> F[NPO for 24 h→ Re-assess → Abdomen soft, no distension → Start feeds @ 10-20 ml/kg/d→ If tolerates, increase @ half of weight/gestation specific increments];
    D --> G[Keep NPO for 6 h→ Re-assess → Abdomen soft, no distension & recovery from red signs → Start feeds as per gestation/weight specific protocol];
    E --> H[Keep NPO → Take pediatric surgery consultation*];
    F --> I[GA <26 weeks* BW < 750 g];
    F --> J[GA 26-27 weeks* BW 750-999 g];
    F --> K[GA 28-30 weeks BW 1000-1250 g];
    F --> L[GA >30 weeks BW >1250 g];
    I --> M[NPO for 24 h Trophic feeds @ 10 ml/kg/d for 48 h Increase @ 10-15 ml/kg/d];
    J --> N[NPO for 24 h Start feeds @ 20 ml/kg/d Increase @ 15-20 ml/kg/d];
    K --> O[Start feeds @ 30 ml/kg/d Increase @ 30 ml/kg/d];
    L --> P[All fluid as feeds from D1];
```

*   For total daily fluid requirement see table 1. Remaining fluid requirement after accounting for feed volume, should be given as IV fluids and if feasible as **PN** in neonates born at less than 28 weeks or 1000 g*
*   IV fluids can be stopped once infant is tolerating feeds @ 120 mL/kg/d, if blood glucose is maintained.
*   Preferred mode of feeding: < 32 weeks: Oro-Gastric tube; 32-34 weeks: Spoon/Paladai; and ≥ 35weeks: Breast feeds
*   Choice of milk in order of preference: **Expressed breast milk (EBM)** >> pasteurized donor human milk >> formula milk
*   Frequency of feeds: q 2 h if **PMA** < 32 weeks/weight <1500g and q 3 h if > 32weeks/weight ≥1500g
*   Add supplements as per Table 2

*Indicates conditions which need admission/referral to tertiary care health facility*

PART B
Nutritional plan for infants on partial or full enteral feeds at admission

```mermaid
graph LR
    A[Nutritional plan for infants on partial or full enteral feeds at admission] --> B{ARE ANY OF THESE RED SIGNS PRESENT?};
    B -- YES --> C[Keep NPO and start IV fluids Consider PN if gestation < 28 weeks or weight <1000 g* Take Pediaric surgery consultation if suspecting Gl obstruction or peritonitis*];
    B -- NO --> D[Continue feeds and advance as given in flow chart in part A];
    B --> E[Significant respiratory distress (Silverman/ Downe score>6)];
    B --> F[Ongoing hypoxia or moderate to severe apneas];
    B --> G[Ongoing seizures];
    B --> H[Severe hypothermia];
    B --> I[Shock needing inotropes];
    B --> J[Feed intolerance (abdominal distension with vomiting, bilious or bloody gastric aspirates)];
    C --> K[Every 12-24 h re-assess for readiness of feed by presence of soft abdomen, no distension and absence of red signs];
    K --> L[Restart at 50% of the volume of feed being tolerated before making NPO and make increment as per chart in part A];
```

TABLE 1
Maintenance volume (Enteral + IV, mL/kg/d) and type of IV fluids

| BIRTH WEIGHT             | DAY 1 | DAY 2 | DAY 3 | DAY 4                                                                | DAY 5   | DAY 6     | DAY 7     |
| :----------------------- | :---- | :---- | :---- | :------------------------------------------------------------------- | :------ | :-------- | :-------- |
| <1000 g or  Gestation <28 | 80-100 |       |       | Advance strictly as per clinical and lab hydration status              |         |           |           |
| 1000-1250g  28 to 30 weeks | 80    | 100   | 120   | 140                                                                  | 150     | 150-160   | 150-160   |
| >1250 g  >30 weeks       | 60    | 80    | 100   | 120                                                                  | 140     | 150       | 150-160   |
| Type of IV  fluids       |       |       |       | Start with D10 Titrate dextrose concentration as per blood glucose | N/5 in D10 with KCI |           |           |

*   Table 1 is a general guide and daily increments may be based on daily weight change, urine output, serum sodium and co-morbidities such as PDA or sepsis
*   Daily increments of feed should be based on tolerance and weight gain.
*   Monitor growth by regular measurement of weight and head circumference. Once full feeds have been achieved, preterm neonates are expected to gain weight @ 10-20 g/kg/day. Plot the growth parameters on intergrowth 21st postnatal charts for preterm neonates
*   If not gaining weight adequately on exclusive enteral feeds, after 2 weeks of life, feed volume may be increased gradually upto 200-250 mL/kg/d as per tolerance

TABLE 2
Supplements
*   Start when infant is on 100ml/kg/day of enteral feeds
*   Start **Iron** at 2 weeks of age
**Weight <1800 gram or Gestation <35 weeks**
*   If on **EBM** Or Donor Milk: **HMF + Iron + Vitamin D3**
*   If on Breastfeeds: **Iron + Calcium + Phosphorus + Multivitamins + Vitamin D3**
*   If on Preterm Formula: Iron and Vitamin D3
**Weight >=1800 gram and Gestation >=35 weeks**
Vitamin D3 and Iron (only for gestation <37 weeks)

| Dose                          | Duration                                                                                      |
| :---------------------------- | :-------------------------------------------------------------------------------------------- |
| Iron: 2mg/kg/day              | Iron and Vit-D3: till 1 year                                                                    |
| Vit -D3: 400 IU to 800 IU/day | Calcium and Phosphorus: till term PMA                                                            |
| Calcium: 120mg/kg/day         | Multivitamins: till 6 months                                                                  |
| Phosphorus: 60mg/kg/day       |                                                                                               |

AEDF: Absent end diastolic flow
HIE: Hypoxic ischemic encephalopathy
HMF: Human milk fortifiers
ABBREVIATIONS
NEC: Necrotizing enterocolitis
PDA: Patent ductus arteriosus
PMA: Post menstrual age
PN: Parenteral nutrition
REDF: Reversed end diastolic flow

EARLY AND AGGRESSIVE ENTERAL FEEDING BY BREASTMILK DECREASES MORTALITY AND MORBIDITY

*This STW has been prepared by national experts of India with feasibility considerations for various levels of healthcare system in the country. These broad guidelines are advisory, and are based on expert opinions and available scientific evidence. There may be variations in the management of an individual patient based on his/her specific condition, as decided by the treating physician. There will be no indemnity for direct or indirect consequences. Kindly visit the website of DHR for more information: (stw.icmr.org.in) for more information. Department of Health Research, Ministry of Health & Family Welfare, Government of India.*
