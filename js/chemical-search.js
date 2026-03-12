function normalize(v){
return (v || "").toLowerCase().trim()
}

function searchChemical(keyword){

const k = normalize(keyword)

return CHEMICAL_DB.filter(item=>{

return(

item.cas.includes(k) ||

normalize(item.name_ko).includes(k) ||

normalize(item.name_en).includes(k) ||

normalize(item.name_ja).includes(k)

)

})

}

function findExactChemical(keyword){

const k = normalize(keyword)

return CHEMICAL_DB.find(item=>{

return(

item.cas===k ||

normalize(item.name_ko)===k ||

normalize(item.name_en)===k

)

})

}