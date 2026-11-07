# Sahaaya AI

A multilingual, voice-first citizen assistance prototype for Telugu, Hindi and English.

## Features
- Gnani Prisma speech-to-text
- Gnani Timbre v2.5 text-to-speech
- Government scheme reference finder
- Application preparation guidance
- Grievance draft generator (does not submit)
- Farmer information assistant with official reference links
- SQLite interaction history

## Setup (Windows PowerShell)

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Open `.env`, add your Gnani API key, then run:

```powershell
streamlit run app.py
```

## Notes
- The code uses the official `gnani-vachana` Python SDK.
- Speech recognition sends the recorded audio to Gnani Prisma.
- Speech generation uses Timbre v2.5. Check the voice names available for your account and change the three voice settings in `.env` if needed.
- The optional Evon adapter uses Hugging Face InferenceClient only when `HF_TOKEN` and `EVON_MODEL` are configured and the selected model is available through that inference provider. Otherwise the app uses its local verified-reference response path.
- The knowledge base is a starter dataset. Verify and expand every entry from current official sources before public release.
- This is an independent prototype, not an official government service. It does not determine eligibility, submit forms or file grievances.
