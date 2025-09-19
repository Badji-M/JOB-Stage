/* PAPE MAMADOU BADJI STA25-08-2025*/ 
clear all

cd "C:\Users\hp\OneDrive\Bureau\JOB"
import excel "Data\Data.xlsx", sheet("NationalIndex") firstrow clear


drop if _n >= 109

drop if extra == 0

destring CibleInternational lower_raw, replace

rename performancepositif1négatif2 performance

gen score = cond(performance == 1, (valeur actuelle - lower_raw)/(CibleInternational-lower_raw) , (lower_raw - valeuractuelle)/(lower_raw - CibleInternational))

replace score = 0 if score < 0
replace score = 1 if score > 1


gen test = score<0
replace test=. if missing(score)

drop if score == . | test == 1


*Moyenne par ODD
collapse (mean) score, by(ODD)


/* Moyenne par ODD sans supprimer les lignes originales
bysort ODD: egen ODD_index = mean(score) */

egen ODD_global = mean(score)

di ODD_global





