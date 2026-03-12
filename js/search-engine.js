function normalize(text){
  return (text || "").toLowerCase().trim()
}

function searchChemical(keyword){

  const k = normalize(keyword)

  return CHEMICAL_DB.filter(item => {

    return (
      (item.cas && item.cas.includes(k)) ||
      normalize(item.name_en).includes(k) ||
      normalize(item.name_ko).includes(k)
    )

  })

}