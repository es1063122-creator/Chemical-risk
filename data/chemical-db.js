window.CHEMICAL_DB = [
  {
    id: "chem-0001",
    cas: "67-64-1",
    name_ko: "아세톤",
    name_ja: "アセトン",
    name_en: "Acetone",
    name_vi: "Acetone",
    synonyms: ["2-propanone", "dimethyl ketone"],
    category: "유기용제",
    source: "PubChem / OSHA / SDS",
    ghs: [
      "인화성 액체",
      "눈 자극",
      "졸림 및 어지러움"
    ],
    exposure_routes: ["흡입", "피부 접촉", "눈"],
    ppe: ["보호안경", "내화학 장갑", "국소배기"],
    storage: ["화기 엄금", "정전기 방지", "밀폐 보관"],
    first_aid: {
      inhale: "신선한 공기가 있는 곳으로 이동",
      skin: "오염 의복 제거 후 충분히 세척",
      eyes: "수분간 물로 세척",
      ingest: "즉시 의학적 조치 검토"
    },
    hazard_score: 3,
    danger_score: 3,
    fire_score: 3,
    toxicity_score: 2,
    sds_keywords: ["flammable", "eye irritation", "drowsiness", "acetone"]
  },
  {
    id: "chem-0002",
    cas: "108-88-3",
    name_ko: "톨루엔",
    name_ja: "トルエン",
    name_en: "Toluene",
    name_vi: "Toluen",
    synonyms: ["methylbenzene", "toluol"],
    category: "유기용제",
    source: "SDS",
    ghs: [
      "인화성 액체",
      "흡입 유해",
      "중추신경계 영향"
    ],
    exposure_routes: ["흡입", "피부"],
    ppe: ["유기용제용 방독마스크", "보호장갑", "보호안경"],
    storage: ["환기 유지", "점화원 격리", "밀폐 보관"],
    first_aid: {
      inhale: "신선한 공기 공급",
      skin: "비누와 물로 세척",
      eyes: "충분한 물로 세척",
      ingest: "의료진 상담"
    },
    hazard_score: 4,
    danger_score: 4,
    fire_score: 3,
    toxicity_score: 3,
    sds_keywords: ["toluene", "flammable", "vapour", "narcotic"]
  },
  {
    id: "chem-0003",
    cas: "67-56-1",
    name_ko: "메탄올",
    name_ja: "メタノール",
    name_en: "Methanol",
    name_vi: "Methanol",
    synonyms: ["methyl alcohol", "wood alcohol"],
    category: "알코올",
    source: "SDS",
    ghs: [
      "고인화성 액체",
      "급성 독성",
      "장기 손상"
    ],
    exposure_routes: ["흡입", "피부", "섭취"],
    ppe: ["방독마스크", "보호안경", "내화학 장갑"],
    storage: ["화기 엄금", "밀폐 보관"],
    first_aid: {
      inhale: "즉시 환기된 곳으로 이동",
      skin: "즉시 세척",
      eyes: "즉시 세안",
      ingest: "즉시 응급조치"
    },
    hazard_score: 5,
    danger_score: 4,
    fire_score: 3,
    toxicity_score: 5,
    sds_keywords: ["methanol", "toxic", "flammable", "organ damage"]
  }
];