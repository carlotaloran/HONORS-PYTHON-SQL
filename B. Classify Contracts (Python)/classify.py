# --------------------------------------------------------------------------------------------
# This script defines a function to re-classify credit contracts into cost and investment
# categories (see Theoretical Framework), edited but heavily written by ChatGPT. It inputs 
# the contract file 'operacao_gleba_master', cleaned in STATA, and outputs a re-classified
# file, 'operacao_gleba_master_reclass'. Run this script on the local terminal.
# --------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------------
# SETUP
# --------------------------------------------------------------------------------------------

# Dependencies
import pandas as pd
import unicodedata

# Path definitions
CSV_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/CREDIT_DEFOREST_DATA/CREDIT_DEFOREST_DATA_CLEAN/CREDIT_DATA/OPERACAO_GLEBA/operacao_gleba_master.csv"
OUTPUT_PATH = "/Users/carlotaloranlopez/Desktop/CREDIT_DEFOREST/CREDIT_DEFOREST_DATA/CREDIT_DEFOREST_DATA_CLEAN/CREDIT_DATA/OPERACAO_GLEBA/operacao_gleba_master_reclass.csv"

# Columns used for purpose / rules
CATEGORICAL_COLS = [
    "cd_programa",       # government program abbreviation
    "cd_modalidade",     # specific use of credit
    "cd_produto",        # product (e.g., soy, cows)
    "cd_categ_emitente"  # borrower size
]
NUMERIC_COLS = [
    "vl_juros",          # interest rate
    "vl_prev_prod",      # predicted production revenue
    "vl_parc_credito",   # loan size
    "vl_rec_proprio",    # personal contribution
    "vl_area_informada"  # reported farm area
]

# Thresholds for numeric indicators of investment (set by ChatGPT)
LOAN_SIZE_THRESHOLD = 50000           # Loans above this → likely investment
PRED_PROD_THRESHOLD = 100000          # High predicted production → likely investment
FARM_AREA_THRESHOLD = 50              # Large farm area → more likely investment

# Program restrictions
program_mapping = {
    "abc+": "investimento",
    "ftra": "custeio",
    "funcafé": None,       # 'either' → fallback to normal rules
    "inovagro": "investimento",
    "moderagro": "investimento",
    "moderfrota": "investimento",
    "no program": None,    # 'either'
    "procab-agro": "custeio",
    "prodecoop": "investimento",
    "proirriga": "investimento",
    "pronaf": None,        # 'either'
    "pronamp": None,       # 'either'
    "14": None             # 'either', not identified in the data
}

# String normalization function
def normalize_text(s):
    if isinstance(s, str):
        s = s.lower().strip()
        s = unicodedata.normalize("NFKD", s)
        s = "".join(c for c in s if not unicodedata.combining(c))
    return s


# --------------------------------------------------------------------------------------------
# Define reclassification function
# --------------------------------------------------------------------------------------------

def classify(row):
    """ Rules: 
        - Default: custeio (cost) 
        - Investimento (investment) if: 
            - Keywords indicate capital/tech improvement, OR 
            - Numeric thresholds exceeded set values
     """
    # Check cd_programa mapping
    prog = str(row.get("cd_programa", "")).lower()
    mapped = program_mapping.get(prog, None)
    if mapped is not None:
        return mapped  # fixed outcome

    # Combine categorical fields into a string
    parts = [str(row[col]) for col in CATEGORICAL_COLS]
    text = " ".join(parts)
    text = normalize_text(text)

    # Define investment keywords (ChatGPT)
    investment_keywords = [
        "maquina", "trator", "implemento", "tecnologia",
        "reforma", "infraestrutura", "melhoria", "equipamento",
        "benfeitoria", "instalacao", "capital"
    ]

    # Check keywords
    for kw in investment_keywords:
        if kw in text:
            return "investimento"

    # Numeric thresholds
    if (row.get("vl_parc_credito", 0) > LOAN_SIZE_THRESHOLD or
        row.get("vl_prev_prod", 0) > PRED_PROD_THRESHOLD or
        row.get("vl_area_informada", 0) > FARM_AREA_THRESHOLD):
        return "investimento"

    # Else, return default custeio
    return "custeio"


# --------------------------------------------------------------------------------------------
# Reclassify contracts
# --------------------------------------------------------------------------------------------

# Load operacao_gleba_master
df = pd.read_csv(CSV_PATH)

# Fill NaN in classification columns only
for col in CATEGORICAL_COLS:
    if col in df.columns:
        df[col] = df[col].fillna("missing").astype(str)

for col in NUMERIC_COLS:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Classify
df['cd_finalidade_corrected'] = df.apply(classify, axis=1)

# Flag contracts where original target changed
if 'cd_finalidade' in df.columns:
    df['changed'] = df['cd_finalidade'] != df['cd_finalidade_corrected']
else:
    df['changed'] = False

# Save output to repo
df.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print(f"CSV saved to: {OUTPUT_PATH}")

# Print summary
counts = df['cd_finalidade_corrected'].value_counts()
print("\n=== Corrected contract counts ===")
print(counts)
changed_count = df['changed'].sum()
print(f"\nNumber of contracts corrected: {changed_count}")