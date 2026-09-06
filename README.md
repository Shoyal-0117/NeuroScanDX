# NeuroScanDX

*(internally referred to as BTDS — **B**rain **T**umor **D**etection & **S**egmentation — kept here for reference since it appears in early planning docs and commit history.)*

A web-based clinical-decision-support **demo** that classifies brain MRI scans for tumor presence/type and segments the tumor region, with visual overlays (segmentation mask + Grad-CAM heatmap).

> ⚠️ **This is an academic demo, not a certified diagnostic tool.** It is not intended for real clinical use, and no output should be interpreted as implying clinical certainty.

## What it does

1. User uploads a 2D MRI slice (PNG/JPG)
2. A classifier (ResNet18 / EfficientNet-B0, transfer learning) predicts: **glioma / meningioma / pituitary / no tumor**
3. If a tumor is predicted, a U-Net segmentation model localizes the tumor region
4. Grad-CAM generates a heatmap showing what the classifier focused on
5. Results (label, confidence, mask overlay, heatmap) are displayed on a results page

## Tech Stack

| Layer | Tech |
| --- | --- |
| ML | Python, PyTorch, OpenCV |
| Backend | FastAPI |
| Frontend | React (Vite) |
| Deployment | Docker, Render/Railway |

## Evaluation Metrics (locked — do not report accuracy alone)

| Task | Metric |
| --- | --- |
| Classification | F1-score, Precision, Recall (per class) |
| Segmentation | Dice coefficient, IoU |

Accuracy alone is misleading for segmentation (background pixels dominate) and insufficient for classification (masks class imbalance).

## Project Structure

```
NeuroScanX/
├── data/                  # raw / processed / split datasets (gitignored, not committed)
├── notebooks/             # data exploration + training notebooks
├── models/
│   ├── classifier/        # classification model code + weights
│   ├── segmenter/         # U-Net code + weights
│   └── gradcam/           # Grad-CAM module
├── backend/                # FastAPI app (routes, services, schemas)
├── frontend/               # React app
├── tests/                  # backend + inference tests
├── docker-compose.yml
├── Dockerfile.backend
├── Dockerfile.frontend
├── .env.example
└── README.md
```

## Getting Started (Local Dev)

### Prerequisites
- Python 3.10+
- Node.js 18+
- (Optional) Docker + Docker Compose
- Git Bash (Windows users — recommended over plain PowerShell/CMD)

### Backend setup
```bash
python -m venv venv
source venv/bin/activate          # Windows Git Bash: source venv/Scripts/activate
pip install -r backend/requirements.txt
cp .env.example .env              # then fill in values
uvicorn backend.main:app --reload
```

### Frontend setup
```bash
cd frontend
npm install
npm run dev
```

### Datasets
Datasets are **not** committed to this repo (see `.gitignore`). Download separately:
- [Kaggle: Brain Tumor MRI Dataset (Nickparvar)](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) — classification, 4-class
- [Kaggle: LGG MRI Segmentation (Mateusz Buda)](https://www.kaggle.com/datasets/mateuszbuda/lgg-mri-segmentation) — segmentation, image+mask pairs

Place downloaded data under `data/raw/`.

## Model Interface Contract (FROZEN — flag before changing)

| Model | Input shape | Output |
| --- | --- | --- |
| Classifier | `(3, 224, 224)` normalized tensor | 4-class softmax logits |
| Segmenter (U-Net) | `(1 or 3, 256, 256)` normalized tensor | Binary mask, same H×W |

Any change to these shapes ripples through preprocessing, training, and the backend inference pipeline — confirm with both teammates before altering.

## Team Setup — One-Time Per Machine

Both teammates must run this **individually** after cloning. It is not synced by `git push` — skipping it on either machine reintroduces notebook merge-conflict noise.

```bash
pip install nbstripout
cd NeuroScanDX
nbstripout --install
```

Verify it's active:
```bash
git check-attr filter -- notebooks/test.ipynb
# Expected: notebooks/test.ipynb: filter: nbstripout
```

**What this does:** strips Jupyter notebook output/execution metadata automatically on commit, so re-running cells doesn't create false diffs or merge conflicts between teammates editing the same notebook.

## Branching Workflow

- `main` is protected — no direct commits.
- Work happens on `feature/<description>` branches, merged via Pull Request.
- Suggested ownership split to minimize file conflicts:
  - **Classifier track:** `models/classifier/`, `notebooks/01_*`, `notebooks/02_*`
  - **Segmenter track:** `models/segmenter/`, `notebooks/03_*`
- Always `git pull origin main` before branching off for a new session.

## Team

| Member | Role |
| --- | --- |
| Shoyal Haldar | Classification model + backend |
| Ayaz Anwar | Segmentation model + frontend |

## Project Status

🚧 In progress — **Weekend 1: Setup & Foundations**

See SRS / Build Approach docs for full weekend-by-weekend timeline.

## Known Limitations

- Works on 2D MRI slices only (not full 3D volumes)
- Trained on public datasets — may not generalize to other scanner types/populations
- Not HIPAA-compliant, not for real patient data
- Decision-support demo only — does not imply clinical certainty
