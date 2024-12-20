import pandas as pd

df = pd.read_stata("updated_firm_data.dta")


IT_SERVICE = ['ACN', 'AI', 'ALYA','ARBB','ASGN','ATGL',
                'AUR','BBAI','BR','BTCM','CACI','CD','CDW',
                'CLPS','CLVT','CNDT','CNXC','CRGE','CSPI','CTG',
                'CTLP','CTM','CTSH','DLB','DMRC','DTST','DXC',
                'EPAM','EXLS','FI','FIS','FLYW','FORTY','G',
                'GDS','GDYN','GIB','GLOB','GMM','HCKT', 'IBEX','IBM',
                'III','INFY','INOD','IT','JFU','JKHY','KD','LDOS',
                'MGIC','NABL','NOTE','NYAX','PAY','PRFT','PSFE',
                'SAIC','SASI','SRT','TASK','TLS','TTEC','TWKS',
                'UIS','USIO','VNET','VYX','WAVD','WIT','WNS','WYY','XRX']

TELECOM = ['AMX', 'ANTE', 'ASTS','ATEX','ATNI','ATUS','BCE','CABO',
           'CCOI','CHT','CHTR','CMCSA','CNSL', 'COMS','CXDO','DISH',
           'FNGR','FYBR','GOGO','GSAT','IDCC','IDT','IHS','IRDM','KORE','KT',
           'LBRDA','LBRDK','LBTYA','LBTYB','LBTYK','LILA','LILAK','LUMN','MIMO',
           'OOMA','ORAN','PHI','RBBN','RCI','RDCM','SHEN','SIFY','SKM','T','TDS',
           'TEF','TEO','TIGO','TIMB','TKC','TLK','TMUS','TU','TV','UCL','USM','VEON','VIV',
           'VOD','VZ','WOW']

ELECTRONICS = ['ALNT','APH','BELFA','BELFB','BHE','CLS','CPSH','CTS','DAIO',
               'DAKT','DSWL','ELTK','FLEX','FN','GLW','HOLO','IMTE','JBL','KOPN','KULR',
               'LFUS','LGL','LPTH','LYTS','MEI','MMAT','MPTI','MTEK','NEON','NSYS',
               'OSIS','OST','OUST','PLXS','REFR','RELL','ROG','SANM','SGMA','TEL','TTMI',
               'VIAO','VICR','WBX']


#vulneable firm 
df['liquidity'] = df['actq']/df['atq']
df['Debt_ratio'] = df["dlttq"]/df['atq']
df['TotalDebt_ratio'] = df.groupby('datacqtr')['Debt_ratio'].transform('sum')
df['DebtPercentage'] = (df['Debt_ratio'] / df['TotalDebt_ratio']) * 100
df['DebtPercentage'] = (df['Debt_ratio'] / df['TotalDebt_ratio']) * 100

df['Total_liquidity'] = df.groupby('datacqtr')['liquidity'].transform('sum')
df['liquidity_Percentage'] = (df['liquidity'] / df['Total_liquidity']) * 100

df['vulnerable'] = ((df['DebtPercentage'] > 0.66) & (df['liquidity_Percentage'] <0.33)).astype(int)
df['unconstrained'] = ((df['DebtPercentage'] < 0.33) & (df['liquidity_Percentage'] >0.66)).astype(int)
#dropping nan
df = df.drop(columns=['ulcoq', 'tieq', 'teqq'])


#industry specification

industry_map = {ticker: 'IT_SERVICE' for ticker in IT_SERVICE}
industry_map.update({ticker: 'TELECOM' for ticker in TELECOM})
industry_map.update({ticker: 'ELECTRONICS' for ticker in ELECTRONICS})

df['industry'] = df['tic'].map(industry_map)

###finding industry Debt ratio
grouped = df.groupby(['datacqtr', 'industry']).agg({'dlttq': 'sum', 'atq': 'sum'}).reset_index()
grouped['ind_Debt_ratio'] = grouped['dlttq'] / grouped['atq']
df = df.merge(grouped[['datacqtr', 'industry', 'ind_Debt_ratio']], on=['datacqtr', 'industry'], how='left')


#TQ and 
df['tobins_Q'] = df['mkvaltq']/df['atq']
df['ROA'] = df['niq']/df['atq']

#finding the vulnerable firms share in an industry for each quarter
vul_assets = df[df['vulnerable'] == 1].groupby(['datacqtr', 'industry'])['atq'].sum().rename("vul_assets")
total_assets = df.groupby(['datacqtr', 'industry'])['atq'].sum().rename("total_assets")
vul_sh_df = pd.concat([vul_assets, total_assets], axis=1).reset_index()
vul_sh_df['vul_assets'] = vul_sh_df['vul_assets'].fillna(0)
vul_sh_df['vul_sh'] = vul_sh_df['vul_assets'] / vul_sh_df['total_assets']
df = df.merge(vul_sh_df[['datacqtr', 'industry', 'vul_sh']], on=['datacqtr', 'industry'], how='left')

#adding Global Financial Crisis dummy variable
df['GFC'] = (df['fyearq'] >= 2008).astype(int)

#coverting various dataset according to the horizon

df = df.dropna()

df = df.sort_values(by=["datacqtr", "tic"])

#dataset 1-horizon =1
df.to_stata("h1_clean_data.dta", write_index=False)


#dataset 2-horizon =4
filtered_df_h4 = df.iloc[::4].reset_index(drop=True)
filtered_df_h4.to_stata("h4_clean_data.dta", write_index=False)

#dataset 3-horizon =8
filtered_df_h8 = df.iloc[::8].reset_index(drop=True)
filtered_df_h8.to_stata("h8_clean_data.dta", write_index=False)

#dataset 4-horizon =12
filtered_df_h12 = df.iloc[::12].reset_index(drop=True)
filtered_df_h12.to_stata("h12_clean_data.dta", write_index=False)

#dataset 5-horizon =16
filtered_df_h16 = df.iloc[::16].reset_index(drop=True)
filtered_df_h16.to_stata("h16_clean_data.dta", write_index=False)

#dataset 6-horizon =20
filtered_df_h20 = df.iloc[::20].reset_index(drop=True)
filtered_df_h20.to_stata("h20_clean_data.dta", write_index=False)



