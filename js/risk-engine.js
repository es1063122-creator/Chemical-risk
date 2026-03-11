function calculateRiskFromChemical(item) {
  const amount = Number(document.getElementById("amountLevel")?.value || 1);
  const freq = Number(document.getElementById("frequencyLevel")?.value || 1);
  const vent = Number(document.getElementById("ventilationLevel")?.value || 1);

  const score =
    Number(item.hazard_score || 0) +
    Number(item.danger_score || 0) +
    amount + freq + vent;

  let label = "리스크 레벨 2";
  if (score >= 14) label = "리스크 레벨 5";
  else if (score >= 11) label = "리스크 레벨 4";
  else if (score >= 8) label = "리스크 레벨 3";

  const riskBox = document.getElementById("riskBox");
  const scoreBox = document.getElementById("scoreBox");
  const controlBox = document.getElementById("controlBox");

  if (riskBox) riskBox.textContent = label;
  if (scoreBox) scoreBox.textContent = `점수: ${score}`;

  const controls = [];
  if ((item.ghs || []).some(v => /인화성|flammable/i.test(v))) {
    controls.push("화기 엄금", "정전기 방지", "국소배기");
  }
  if ((item.ghs || []).some(v => /독성|toxic/i.test(v))) {
    controls.push("밀폐공정 검토", "노출 최소화", "방독마스크 검토");
  }
  if ((item.ghs || []).some(v => /부식|corrosive/i.test(v))) {
    controls.push("내화학 장갑", "보안면", "비상세안장치");
  }

  if (controlBox) {
    controlBox.innerHTML = [...new Set(controls)].map(v => `<li>${v}</li>`).join("");
  }

  return { score, label, controls: [...new Set(controls)] };
}