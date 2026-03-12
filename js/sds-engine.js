pdfjsLib.GlobalWorkerOptions.workerSrc =
  "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

function extractCasFromText(text) {
  const m = text.match(/\b\d{2,7}-\d{2}-\d\b/);
  return m ? m[0] : "";
}

function inferGhsFromSdsText(text) {
  const t = text.toLowerCase();
  const ghs = [];

  if (
    t.includes("flammable") ||
    t.includes("highly flammable") ||
    t.includes("가연성") ||
    t.includes("인화성")
  ) {
    ghs.push("인화성");
  }

  if (
    t.includes("corrosive") ||
    t.includes("corrosion") ||
    t.includes("부식성")
  ) {
    ghs.push("부식성");
  }

  if (
    t.includes("toxic") ||
    t.includes("acute toxicity") ||
    t.includes("독성")
  ) {
    ghs.push("독성");
  }

  if (
    t.includes("carcinogenic") ||
    t.includes("carcinogen") ||
    t.includes("발암성")
  ) {
    ghs.push("발암성");
  }

  if (
    t.includes("eye irritation") ||
    t.includes("serious eye damage") ||
    t.includes("눈 자극")
  ) {
    ghs.push("눈 자극");
  }

  if (
    t.includes("skin irritation") ||
    t.includes("피부 자극")
  ) {
    ghs.push("피부 자극");
  }

  return [...new Set(ghs)];
}

function inferPpeFromSdsText(text) {
  const t = text.toLowerCase();
  const ppe = [];

  if (t.includes("gloves") || t.includes("protective gloves") || t.includes("장갑")) {
    ppe.push("보호장갑");
  }

  if (
    t.includes("goggles") ||
    t.includes("eye protection") ||
    t.includes("safety glasses") ||
    t.includes("보안경") ||
    t.includes("보호안경")
  ) {
    ppe.push("보호안경");
  }

  if (
    t.includes("respirator") ||
    t.includes("gas mask") ||
    t.includes("organic vapor respirator") ||
    t.includes("방독마스크")
  ) {
    ppe.push("방독마스크");
  }

  if (
    t.includes("protective clothing") ||
    t.includes("chemical protective clothing") ||
    t.includes("보호복")
  ) {
    ppe.push("보호복");
  }

  if (
    t.includes("face shield") ||
    t.includes("안면보호")
  ) {
    ppe.push("안면보호구");
  }

  return [...new Set(ppe)];
}

function inferStorageFromSdsText(text) {
  const t = text.toLowerCase();
  const storage = [];

  if (
    t.includes("keep away from heat") ||
    t.includes("keep away from ignition sources") ||
    t.includes("화기엄금")
  ) {
    storage.push("화기엄금");
  }

  if (
    t.includes("well ventilated place") ||
    t.includes("ventilated") ||
    t.includes("환기")
  ) {
    storage.push("환기보관");
  }

  if (
    t.includes("tightly closed") ||
    t.includes("keep container tightly closed") ||
    t.includes("밀폐")
  ) {
    storage.push("밀폐용기");
  }

  if (
    t.includes("store locked up") ||
    t.includes("잠금")
  ) {
    storage.push("잠금 보관");
  }

  return [...new Set(storage)];
}

function mergeUnique(base = [], extra = []) {
  return [...new Set([...(base || []), ...(extra || [])])];
}

async function readPdfText(file) {
  const arr = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: arr }).promise;

  let text = "";

  for (let i = 1; i <= pdf.numPages; i++) {
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    const pageText = content.items.map(v => v.str).join(" ");
    text += pageText + "\n";
  }

  return text;
}

function findChemicalByCas(cas) {
  return CHEMICAL_DB.find(item => item.cas === cas) || null;
}

function findChemicalByName(text) {
  const t = text.toLowerCase();

  return CHEMICAL_DB.find(item => {
    return (
      (item.name_ko && t.includes(item.name_ko.toLowerCase())) ||
      (item.name_en && t.includes(item.name_en.toLowerCase())) ||
      (item.name_ja && t.includes(item.name_ja.toLowerCase()))
    );
  }) || null;
}

function calculateRiskFromItem(item) {
  const amount = Number(document.getElementById("amountLevel")?.value || 1);
  const freq = Number(document.getElementById("frequencyLevel")?.value || 1);
  const vent = Number(document.getElementById("ventilationLevel")?.value || 1);
  const time = Number(document.getElementById("workTimeLevel")?.value || 1);

  const hazard = Number(item.hazard_score || item.hazardWeight || 3);
  const danger = Number(item.danger_score || item.dangerWeight || 3);

  const score = hazard + danger + amount + freq + vent + time;

  let level = "리스크 레벨 2";
  let cls = "low";

  if (score >= 15) {
    level = "리스크 레벨 5";
    cls = "high";
  } else if (score >= 12) {
    level = "리스크 레벨 4";
    cls = "high";
  } else if (score >= 9) {
    level = "리스크 레벨 3";
    cls = "mid";
  }

  return { score, level, cls };
}

function renderSdsAnalysis(item, risk) {
  document.getElementById("chemName").value = item.name_ko || item.name_en || "";
  document.getElementById("casNo").value = item.cas || "";
  document.getElementById("ghsBox").textContent = (item.ghs || []).join(", ") || "-";
  document.getElementById("exposureBox").textContent = (item.exposure || []).join(", ") || "-";
  document.getElementById("ppeBox").textContent = (item.ppe || []).join(", ") || "-";
  document.getElementById("storageBox").textContent = (item.storage || []).join(", ") || "-";
  document.getElementById("riskBox").innerHTML = `<span class="pill ${risk.cls}">${risk.level}</span>`;
  document.getElementById("scoreBox").textContent = `Score : ${risk.score}`;

  const controls = [];
  if ((item.ghs || []).includes("인화성")) controls.push("점화원 차단", "화기엄금", "국소배기");
  if ((item.ghs || []).includes("부식성")) controls.push("내화학 장갑 착용", "안면보호구 착용");
  if ((item.ghs || []).includes("독성")) controls.push("방독마스크 착용", "노출 최소화");
  if ((item.ghs || []).includes("발암성")) controls.push("밀폐 공정 검토", "화학방호복 착용");

  document.getElementById("controlBox").innerHTML =
    [...new Set(controls)].map(v => `<li>${v}</li>`).join("");
}

function applyToReports(item, risk) {
  const workDesc = document.getElementById("workDesc")?.value || "";

  if (document.getElementById("r1-work")) document.getElementById("r1-work").value = workDesc;
  if (document.getElementById("m1-name")) document.getElementById("m1-name").value = item.name_ko || item.name_en || "";
  if (document.getElementById("m1-cas")) document.getElementById("m1-cas").value = item.cas || "";

  if (document.getElementById("r2-work")) document.getElementById("r2-work").value = workDesc;
  if (document.getElementById("r2m1-name")) document.getElementById("r2m1-name").value = item.name_ko || item.name_en || "";
  if (document.getElementById("r2m1-cas")) document.getElementById("r2m1-cas").value = item.cas || "";

  if (document.getElementById("r2-hm1-method")) document.getElementById("r2-hm1-method").value = "SDS 자동 분석";
  if (document.getElementById("r2-hm1-level")) document.getElementById("r2-hm1-level").value = `${risk.level} / ${(item.ghs || []).join(", ")}`;
  if (document.getElementById("r2-dm1-method")) document.getElementById("r2-dm1-method").value = "SDS 자동 분석";
  if (document.getElementById("r2-dm1-level")) document.getElementById("r2-dm1-level").value = `${risk.level} / ${(item.storage || []).join(", ")}`;
  if (document.getElementById("r2-control")) document.getElementById("r2-control").value = (item.ppe || []).join("\n");
}

async function handleSdsUpload(file) {
  const statusBox = document.getElementById("pdfStatus");
  if (statusBox) statusBox.textContent = "PDF 분석 중...";

  const text = await readPdfText(file);
  const cas = extractCasFromText(text);

  let matched = null;
  if (cas) {
    matched = findChemicalByCas(cas);
  }
  if (!matched) {
    matched = findChemicalByName(text);
  }

  if (!matched) {
    if (statusBox) statusBox.textContent = "DB 매칭 실패";
    alert("SDS에서 화학물질을 찾지 못했습니다.");
    return;
  }

  const ghsFromPdf = inferGhsFromSdsText(text);
  const ppeFromPdf = inferPpeFromSdsText(text);
  const storageFromPdf = inferStorageFromSdsText(text);

  const mergedItem = {
    ...matched,
    ghs: mergeUnique(matched.ghs, ghsFromPdf),
    ppe: mergeUnique(matched.ppe, ppeFromPdf),
    storage: mergeUnique(matched.storage, storageFromPdf)
  };

  const risk = calculateRiskFromItem(mergedItem);

  renderSdsAnalysis(mergedItem, risk);
  applyToReports(mergedItem, risk);

  if (statusBox) {
    statusBox.textContent = cas
      ? `PDF 분석 완료 / CAS ${cas} 매칭`
      : "PDF 분석 완료 / 이름 기반 매칭";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const sdsInput = document.getElementById("sdsFile");
  if (!sdsInput) return;

  sdsInput.addEventListener("change", async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await handleSdsUpload(file);
    } catch (err) {
      console.error(err);
      const statusBox = document.getElementById("pdfStatus");
      if (statusBox) statusBox.textContent = "PDF 분석 오류";
      alert("SDS PDF 분석 중 오류가 발생했습니다.");
    }
  });
});