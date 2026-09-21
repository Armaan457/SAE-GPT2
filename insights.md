## 1. Top Features by Vocabulary Impact

Sorting the learned features by vocabulary influence shows that Layer 6 focuses heavily on grammar rules, word endings, and structural syntax:

| Rank | Feature ID | Promoted Tokens | Linguistic Role |
| :---: | :---: | :--- | :--- |
| 1 | **#536** | `s • sburg • sb` | **Geographic suffixes**: Completes city names (*Strasbourg, Augsburg, Duisburg*). |
| 2 | **#861** | `respectively • alike • depending` | **Parallel coordination**: Matches pairwise lists (*"A and B are X and Y, respectively"*). |
| 3 | **#32** | `ing • ed • ation` | **Morphological endings**: Attaches tense and noun endings to verb roots. |
| 4 | **#1818** | `rd • RD • peat` | **Ordinal and repetitive endings**: Suffix completions (*3rd, 23rd, repeat*). |
| 5 | **#829** | `anymore • nor • whatsoever` | **Negative Polarity Items**: Words used only in negative contexts (*"not ... anymore"*). |
| 6 | **#945** | `than • than • Than` | **Comparative conjunctions**: Completes comparisons (*"greater than"*, *"rather than"*). |
| 7 | **#1797** | `worldly • wise • kinds` | **Adjective compounds**: Completes common phrases (*"street-wise"*, *"other-worldly"*). |
| 8 | **#1535** | `) • ?) • ?).` | **Bracket balance**: Emits closing brackets after an opening parenthesis. |
| 9 | **#1128** | `sake • purposes • reasons` | **Justification clauses**: Causal framing words (*"for the sake of"*). |
| 10 | **#843** | `own • Own • favorite` | **Possessive reinforcement**: Emphatic possessive phrases (*"their own"*). |

---

## 2. Concept Probing: Reverse Token Lookups

Looking up specific words across all features shows how the model separates concepts and handles phrases:

| Target Word | Feature ID | Promoted Tokens | What the Circuit Does |
| :--- | :---: | :--- | :--- |
| `' York'` | **#329** | `York • Zealand • Orleans • Hampshire` | **The "New [Place]" Circuit**: Groups locations that typically follow the word *"New"*. |
| `' Court'` | **#393** | `cases • Court • judge • Justice • yers` | **Legal Domain**: Activates on court proceedings and judicial roles. |
| `' because'` | **#375** | `albeit • namely • although` | **Reasoning Connectors**: Subordinating and explanatory transitions. |
| `' 19'` | **#374** | `8 • 9 • 2` | **Numerical Continuations**: Predicts subsequent number tokens in numerical sequences (*8, 9, 2*). |
| `' said'` | **#912** | `recommends • conclud • speculate`| **Attribution Split**: Separates speech actions (verbs) from the people speaking (sources). |
| `' activist'`| **#1378** | `activists • activist • activism` | **Single-Topic Feature**: Isolated political advocacy without unrelated meanings. |

---

## 3. Input vs. Output Alignment (Feature Symmetry)

Comparing what triggers each feature on input against what tokens it predicts on output reveals clean symmetry:

* **Feature #329 ("New [Place]"):**
  * **Input Trigger:** Fires on place roots like *York, Zealand, Hampshire, Orleans*.
  * **Output Prediction:** Promotes *York, Zealand, Orleans, Hampshire, Yorkers*, while suppressing unrelated words.
  * **Role:** When the model reads *"New"*, this feature primes all relevant geographical continuations.

* **Feature #393 (Legal Domain):**
  * **Input Trigger:** Fires on terms like *Court, court, judge, filed, lawyers*.
  * **Output Prediction:** Promotes judicial terms like *cases, Court, judge, Justice*.
  * **Role:** Keeps track of legal context across sentences to prime courtroom vocabulary.

---

## 4. Feature Geometry (PCA Landscape)

Projecting decoder weights into 2D reveals clear organization across the feature space:
* **Syntax at the Edges:** Punctuation and bracket balancers (#1535) sit on outer edges due to strong vocabulary-wide impact.
* **Semantic Clusters:** Entity and topic features (places #329, law #393, activism #1378) group into distinct topical neighborhoods.
* **Numbers:** Digit trackers (#374) occupy their own separate direction away from regular text.

---

## 5. Concept Suppression & Feature Ablation

Using Layer 6 activation hooks, we tested what happens when you surgically remove or suppress these learned directions during live generation:

| Target Concept | Target Token | Clean Prob | Ablated Prob | Suppressed Prob | Live Text Shift |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **#329 ("New [Place]")** | `' York'` | 55.9% | 13.9% | 3.0% | Switched from `"New York"` to `"New Belgium"`. |
| **#1378 (Activism)** | `' supporters'` | 40.5% | 26.9% | 0.3% | Shifted from political rally to `"well-dressed guests"`. |
| **#393 (Legal / Court)** | `' court'` | 35.2% | 18.9% | 0.05% | Shifted from courtroom to `"federal government's security forces"`. |

* Orthogonal projection sets the feature to zero, cutting the top token's probability drastically, but strong pre-trained priors from other layers can still keep it at rank 1. Negative steering actively penalizes the direction, knocking it below competitors to force creative substitutions.
* Suppressing a concept did not cause grammatical collapse or gibberish. GPT-2 maintained fluent syntax while dynamically steering into alternative, contextually valid domains.
