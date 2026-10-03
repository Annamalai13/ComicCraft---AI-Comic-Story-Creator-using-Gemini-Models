# ComicCraft Demonstration Guide

**Project:** ComicCraft – AI Comic Story Creator  
**Team ID:** SWTID-2026-2688  
**Team size:** 5  
**Team leader:** Annamalai H  
**Team members:** Harikrishnan M, Deepanraj S, Arunagiri A, Dineshkumar V

## Prerequisites
- Python version compatible with the project dependencies.
- Access credentials for the configured Google Gemini service.
- Suitable compute and dependencies if Stable Diffusion is run locally; confirm model access and hardware requirements.

## Setup
1. Clone the project repository and enter its directory.
2. Create and activate a virtual environment.
3. Install dependencies (adapt versions to the project lockfile):

```bash
pip install fastapi uvicorn jinja2 google-generativeai diffusers fpdf python-dotenv
```

4. Create a `.env` file locally and configure required credentials, for example `GOOGLE_API_KEY=...`. Never commit `.env` or share secret values.
5. Start the development server from the directory containing `main.py`:

```bash
uvicorn main:app --reload
```

6. Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Demonstration flow
1. Enter a concise story premise and any supported options.
2. Submit the form and show validation and generation status.
3. Review the generated outline, panel script, and illustrations.
4. Generate and download the PDF.
5. Demonstrate an invalid input or provider failure and explain the error handling.

## Notes
The exact model names, dependency versions, environment variable names, and local compute requirements must match the repository implementation. Generation time depends on provider and hardware; do not promise a response-time target without measured evidence.
