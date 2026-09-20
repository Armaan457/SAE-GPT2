# Disentangling GPT-2 with Sparse Autoencoders (SAEs)

Mechanistic interpretability study of **GPT-2 Small (Layer 6 residual stream)** using **SAEs**. By using this, we expand the 768-dimensional activation space into **2,048 sparse latent features** .

Using the **Logit Lens** and **Input Gate Alignment**, we map these learned latents directly to vocabulary tokens, revealing how GPT-2 processes syntax, morphology, and multi-token semantic bindings.

---

## Architectural Comparison & Benchmark

Trained 3 SAE variants on 507,227 activations extracted from GPT-2 Layer 6 using WikiText-2:

| Architecture | Reconstruction MSE | Active Features ($L_0$) | Sparsity % |
| :--- | :---: | :---: | :---: |
| **Vanilla ReLU SAE** | `0.2547` | 64.78 | 3.16% |
| **TopK SAE ($k=32$)** | `0.2413` | 32.00 | 1.56% | 
| **Gated SAE** | **`0.1831`** | 71.40 | 3.49% |

---

## Analysis and Findings

Detailed insights in [`insights.md`](insights.md):

## Quickstart

1. Setup Environment
    ```bash
    git clone https://github.com/Armaan457/SAE-GPT2.git
    cd SAE-GPT2
    ```

2. Create and activate a virtual environment:
    - **macOS/Linux:**
       ```bash
       python -m venv env
       source env/bin/activate
       ```
    - **Windows:**
       ```bash
       python -m venv env
       env\Scripts\activate
       ```

3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


4. Run the Notebooks
* Run `variations/gated.ipynb` to retrain the Gated SAE or extract layer activations.
* Run `analysis.ipynb` for the full interactive suite of logit plots, token searches, PCA maps, and input-output comparisons.

---

