function normalizeText(v) {
  return (v || "").toString().trim().toLowerCase();
}

function getDisplayName(item, lang = "ko") {
  return item[`name_${lang}`] || item.name_ko || item.name_en || "";
}

function searchChemicals(keyword, limit = 20) {
  const q = normalizeText(keyword);
  if (!q) return [];

  return window.CHEMICAL_DB.filter(item => {
    return (
      normalizeText(item.cas).includes(q) ||
      normalizeText(item.name_ko).includes(q) ||
      normalizeText(item.name_ja).includes(q) ||
      normalizeText(item.name_en).includes(q) ||
      normalizeText(item.name_vi).includes(q) ||
      (item.synonyms || []).some(s => normalizeText(s).includes(q))
    );
  }).slice(0, limit);
}

function renderAutocomplete(keyword, lang = "ko") {
  const list = document.getElementById("chemicalSuggestions");
  if (!list) return;

  const results = searchChemicals(keyword, 20);
  list.innerHTML = results.map(item => {
    const label = `${item.cas} | ${getDisplayName(item, lang)}`;
    return `<option value="${item.cas}">${label}</option>`;
  }).join("");
}

function findChemicalExact(keyword) {
  const q = normalizeText(keyword);
  if (!q) return null;

  return window.CHEMICAL_DB.find(item => {
    return (
      normalizeText(item.cas) === q ||
      normalizeText(item.name_ko) === q ||
      normalizeText(item.name_ja) === q ||
      normalizeText(item.name_en) === q ||
      normalizeText(item.name_vi) === q ||
      (item.synonyms || []).some(s => normalizeText(s) === q)
    );
  }) || null;
}

function bindAutocomplete(currentLang = "ko") {
  const input = document.getElementById("searchKeyword");
  if (!input) return;

  input.addEventListener("input", e => {
    renderAutocomplete(e.target.value, currentLang);
  });

  input.addEventListener("change", e => {
    const found = findChemicalExact(e.target.value) || searchChemicals(e.target.value, 1)[0];
    if (found) {
      applyChemicalToForm(found, currentLang);
    }
  });
}

function applyChemicalToForm(item, lang = "ko") {
  const chemName = document.getElementById("chemName");
  const casNo = document.getElementById("casNo");
  const ghsBox = document.getElementById("ghsBox");
  const exposureBox = document.getElementById("exposureBox");
  const ppeBox = document.getElementById("ppeBox");
  const storageBox = document.getElementById("storageBox");

  if (chemName) chemName.value = getDisplayName(item, lang);
  if (casNo) casNo.value = item.cas;
  if (ghsBox) ghsBox.textContent = (item.ghs || []).join(", ");
  if (exposureBox) exposureBox.textContent = (item.exposure_routes || []).join(", ");
  if (ppeBox) ppeBox.textContent = (item.ppe || []).join(", ");
  if (storageBox) storageBox.textContent = (item.storage || []).join(", ");

  if (typeof calculateRiskFromChemical === "function") {
    calculateRiskFromChemical(item);
  }
}