*Replication code of “Corporate debt booms, financial constraints, and the investment nexus”
* by PARTHA PRATIM ROY

*For Data cleaing purpose, I used Python, and I tried to convert it a stata code
**  but could have kept the code errorless after converting in stata do file
***   That's why for only data cleaning part is in py file and all my analysis is in this do file. 

* My downloaded file from WRDS is "updated_firm_data.dta" and converted 6 different cleaned files. 


clear all
set more off 

ssc install weakivtest, replace
ssc install estout, replace
ssc install outreg2, replace

*a log file
log using all_output.log, text replace


****        when debt horizon is 1

use h1_clean_data.dta, clear


*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects")

*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)	



****        when debt horizon is 4

use h4_clean_data.dta, clear

*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects") 

*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)		
	
****        when debt horizon is 8

use h8_clean_data.dta, clear

*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects")


*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)		
	


****        when debt horizon is 12

use h12_clean_data.dta, clear

*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects") 
	

*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)		
	

****        when debt horizon is 16

use h16_clean_data.dta, clear

*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects") 

	
*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)	
	

****        when debt horizon is 20

use h20_clean_data.dta, clear

*changing from string to numeric
encode tic, gen(tic_id)
encode datacqtr, gen(datacqtr_num)



****regressing vulnerable firms on various B/S items
xtset tic_id datacqtr_num

** on capex 
xtreg capxy vulnerable i.datacqtr_num, fe
estimates store model_capex

*on liquidity
xtreg liquidity vulnerable i.datacqtr_num, fe
estimates store model_liquidity

*on debt
xtreg dlttq vulnerable i.datacqtr_num, fe
estimates store model_debt

*on debt boom
xtreg debt_boom vulnerable i.datacqtr_num, fe
estimates store model_debt_boom

*on sales
xtreg revtq vulnerable i.datacqtr_num, fe
estimates store model_sales

*on tobins_Q
xtreg tobins_Q vulnerable i.datacqtr_num, fe
estimates store model_tobins_Q

*on ROA
xtreg ROA vulnerable i.datacqtr_num, fe
estimates store model_ROA

*on stock price
xtreg prccq vulnerable i.datacqtr_num, fe
estimates store model_stock_price

*on size
gen log_asset = log(atq)
xtreg log_asset vulnerable i.datacqtr_num, fe
estimates store model_size

*all the effects
esttab model_capex model_liquidity model_debt model_debt_boom ///
    model_sales model_tobins_Q model_ROA model_stock_price model_size, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Regression Results with Fixed Effects")

**** Effect of debt boom on real investment 
gen investment = log(capxy)

ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)

*Diagnostic of IV
estat firststage


***congestion effects
*on capex
xtreg capxy unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store capex_congestion

*on stock price
xtreg prccq unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store price_congestion

*on efficiency or total asset turnover
gen turnover = revtq/atq
xtreg turnover unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store turnover_congestion

*on Return on Assets
xtreg ROA unconstrained unconstrained#c.vul_sh unconstrained#c.vul_sh#c.debt_boom log_asset liquidity tobins_Q i.datacqtr_num, fe
estimates store roa_congestion

*all congestion effects
esttab capex_congestion price_congestion turnover_congestion roa_congestion, ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    label title("Congestion Effects") 

*Additional robustness: using GFC dummy
ivregress 2sls investment (debt_boom vulnerable#c.debt_boom = ind_Debt_ratio vulnerable#c.ind_Debt_ratio vulnerable#c.ind_Debt_ratio#GFC) vulnerable vulnerable#c.log_asset vulnerable#c.liquidity vulnerable#c.tobins_Q i.tic_id i.datacqtr_num, first vce(cluster tic_id)	

log close

