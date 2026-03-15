import fitz
from openai import OpenAI

client = OpenAI(api_key="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")

def extract_text(pdf):
    doc = fitz.open(pdf)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

inspection_text = extract_text("inspection.pdf")
thermal_text = extract_text("thermal.pdf")

prompt = f"""
You are a building inspection expert.

Using the following reports, generate a Detailed Diagnostic Report (DDR).

Inspection Report:
{inspection_text}

Thermal Report:
{thermal_text}

Create the report with these sections:

1. Property Issue Summary
2. Area-wise Observations
3. Probable Root Cause
4. Severity Assessment
5. Recommended Actions
6. Additional Notes
7. Missing or Unclear Information

Rules:
- Do NOT invent information
- If information is missing write "Not Available"
- Use simple language
"""

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

report = response.choices[0].message.content

with open("DDR_Report.txt", "w", encoding="utf-8") as f:
    f.write(report)

print("DDR report generated successfully!")