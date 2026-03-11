async function extractTextFromPdf(file) {
  pdfjsLib.GlobalWorkerOptions.workerSrc =
    "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

  const buffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: new Uint8Array(buffer) }).promise;

  let fullText = "";
  const maxPages = Math.min(pdf.numPages, 15);

  for (let i = 1; i <= maxPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const pageText = content.items.map(item => item.str).join(" ");
    fullText += pageText + "\n";
  }

  return fullText.replace(/\s+/g, " ").trim();
}

function parseSdsText(text) {
  const result = {
    cas: null,
    chemical: null,
    hazardKeywords: [],
    rawText: text
  };

  const casMatch = text.match(/\b\d{2,7}-\d{2}-\d\b/);
  if (casMatch) result.cas = casMatch[0];

  const hazardMap = [
    { key: "flammable", labels: ["인화성", "flammable", "highly flammable", "引火", "dễ cháy"] },
    { key: "toxic", labels: ["독성", "toxic", "acute toxicity", "毒性", "độc tính"] },
    { key: "corrosive", labels: ["부식성", "corrosive", "腐食", "ăn mòn"] },
    { key: "eye irritation", labels: ["눈 자극", "eye irritation", "H319"] },
    { key: "drowsiness", labels: ["졸림", "drowsiness", "H336"] }
  ];

  const lower = text.toLowerCase();

  hazardMap.forEach(h => {
    if (h.labels.some(label => lower.includes(label.toLowerCase()))) {
      result.hazardKeywords.push(h.key);
    }
  });

  if (result.cas) {
    const found = findChemicalExact(result.cas);
    if (found) {
      result.chemical = found;
      return result;
    }
  }

  const foundByName = window.CHEMICAL_DB.find(item => {
    return (
      lower.includes((item.name_ko || "").toLowerCase()) ||
      lower.includes((item.name_ja || "").toLowerCase()) ||
      lower.includes((item.name_en || "").toLowerCase()) ||
      lower.includes((item.name_vi || "").toLowerCase())
    );
  });

  if (foundByName) result.chemical = foundByName;
  return result;
}

function applySdsParseResult(parsed, lang = "ko") {
  if (parsed.chemical) {
    applyChemicalToForm(parsed.chemical, lang);

    const amountLevel = document.getElementById("amountLevel");
    const ventilationLevel = document.getElementById("ventilationLevel");

    if (parsed.hazardKeywords.includes("toxic") && amountLevel) {
      amountLevel.value = "3";
    }
    if (parsed.hazardKeywords.includes("flammable") && ventilationLevel) {
      ventilationLevel.value = "3";
    }

    if (typeof calculateRiskFromChemical === "function") {
      calculateRiskFromChemical(parsed.chemical);
    }
  }
}

function bindPdfReader(lang = "ko") {
  const fileInput = document.getElementById("sdsPdfFile");
  const status = document.getElementById("pdfReadStatus");
  if (!fileInput) return;

  fileInput.addEventListener("change", async e => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      if (status) status.textContent = "PDF 분석 중...";
      const text = await extractTextFromPdf(file);
      const parsed = parseSdsText(text);
      applySdsParseResult(parsed, lang);

      if (status) {
        status.textContent = parsed.chemical
          ? `PDF 분석 완료 / 매칭: ${getDisplayName(parsed.chemical, lang)}`
          : "PDF 분석 완료 / DB 자동 매칭 없음";
      }
    } catch (err) {
      console.error(err);
      if (status) status.textContent = "PDF 분석 실패";
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  bindPdfReader("ko");
});