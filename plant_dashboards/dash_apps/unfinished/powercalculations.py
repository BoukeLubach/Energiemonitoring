import pandas as pd
from sqltags import get_sql_data, store_dataframe


caloric_value_gas = 31.65   #MJ/Nm3store_dataframe(df, tablename)

hot_oil = {
    'cp'                    : {'value': 2.7, 'uom': 'kj/kgK'},
    'density'               : {'value': 696, 'uom': 'kg/m3'},           #density @270°C, all oil flow is measured in supply(high) temperatures
    'furnace_temperature'   : {'value': 277, 'uom': 'degC'}
    }


def calculate_oil_energy(Tin, Tout, Flow):
    """Calculates hot oil energy from mCpdeltaT measurements T in degC, Flow in kg/h"""
    
    #check if tempreature going in is higher than the temperature leaving the column, if this is the case an oil temperature of 275 is assumed
    Tin.loc[Tin<Tout]=275
    
    df = hot_oil['cp']['value']*(Tin-Tout)*Flow/3600
    return df


def JT_correction(supplyT, supplyP, finalP):
    """Takes data or dataframe with inlet temperature and pressure, and outlet pressure,
    returns  final temperature""" 
    
    ##temperature correction based on Joule Thompson effect = 0.4°C cooling for every 1bar pressure loss
    finalT = supplyT-0.4*(supplyP-finalP)
    
    return finalT


def m3_to_Nm3(TdegC, PbarG, m3Flow):
    
    Tref = 273          #degK
    Pref = 1.0325       #barA
    Nm3Flow = m3Flow * ((PbarG+Pref)/Pref) * (Tref/(Tref+TdegC))
    
    return Nm3Flow 
    



def calculate_ng_energy(NGflow):
    "Takes dataframe with natural gas flow (Nm3/h) and returns a dataframe with power in kW"
    
    ngPower = caloric_value_gas*NGflow/3.6
    

    return ngPower




tags = ['82F01', '82F13', '82F73', '82T01', '82T13', '82T73', '82T74', '45T12', 
        '45F02', '45F03', 'B45F02', 'B45F12', '45T11', '45T13', 'B45T13', 'B45T15',
        '82T23', '16F102', '16F02', '16F23', '16F62', 'B14FI04', '16T107', '16T07', 
        '16T27', '16T60', 'B14T10', '28F14','28F74','C28F14','28F02','B28F02']

##Furnace 
#82F01 m3/h
#82F13 m3/h
#82F73 m3/h
#82T01 degC
#82T13 degC
#82T73 degC
#82T74 degC

##Recovery oil flows
#45F02      m3/h     
#45F03      m3/h
#B45F02     m3/h
#B45F12     m3/h

##PPD oil flows
#16F102     kg/h
#16F02      kg/h
#16F23      m3/h
#16F62      kg/h
#B14FI04    ton/h

##TDC oil flows
#28F02      kg/h 
#28F74      kg/h
#C28F14     kg/h    
#28F02      kg/h
#B28F02     kg/h


data = get_sql_data(tags, 'alltags')


TDC_return_T = 210 
TDC_oil_T = 275

powerdata = pd.DataFrame()

##calculate oil consumption energy
powerdata['power_4500_1'] = calculate_oil_energy(data['45T12'], data['45T11'], data['45F02']*hot_oil['density']['value'])
powerdata['power_4500_2'] = calculate_oil_energy(data['45T12'], data['45T13'], data['45F03']*hot_oil['density']['value'])
powerdata['power_B4500_1'] = calculate_oil_energy(data['45T12'], data['B45T13'], data['B45F02']*hot_oil['density']['value'])
powerdata['power_B4500_2'] = calculate_oil_energy(data['45T12'], data['B45T15'], data['B45F12']*hot_oil['density']['value'])
powerdata['Recovery_total'] = powerdata['power_4500_1'] + powerdata['power_4500_2'] + powerdata['power_B4500_1'] + powerdata['power_B4500_2']

powerdata['power_AC1401'] = calculate_oil_energy(data['82T23'], data['B14T10'], data['B14FI04']*1000)
powerdata['power_AC1601'] = calculate_oil_energy(data['82T23'], data['16T07'], data['16F02'])
powerdata['power_AC1602'] = calculate_oil_energy(data['82T23'], data['16T27'], data['16F23']*hot_oil['density']['value'])
powerdata['power_AC1621'] = calculate_oil_energy(data['82T23'], data['16T107'], data['16F102'])
powerdata['power_AC1604'] = calculate_oil_energy(data['82T23'], data['16T60'], data['16F62'])
powerdata['PPD_total'] = powerdata['power_AC1401'] + powerdata['power_AC1601'] + powerdata['power_AC1602'] + powerdata['power_AC1621'] + powerdata['power_AC1604']


powerdata['power_2851'] = hot_oil['cp']['value']*(TDC_oil_T-TDC_return_T)*data['28F02']/3600
powerdata['power_B2851'] = hot_oil['cp']['value']*(TDC_oil_T-TDC_return_T)*data['B28F02']/3600
powerdata['power_2840'] = hot_oil['cp']['value']*(TDC_oil_T-TDC_return_T)*data['28F14']/3600
powerdata['power_2850'] = hot_oil['cp']['value']*(TDC_oil_T-TDC_return_T)*data['28F74']/3600
powerdata['power_C2840'] = hot_oil['cp']['value']*(TDC_oil_T-TDC_return_T)*data['C28F14']/3600
powerdata['TDC_total'] = powerdata['power_2851'] + powerdata['power_B2851'] + powerdata['power_2840'] + powerdata['power_2850'] + powerdata['power_C2840']



store_dataframe(powerdata, 'hopower')









ng_tags = ['91T01', '91F01', '87F22', '82F04', '82F211', '82F74']
ng_data = get_sql_data(ng_tags, 'alltags')

ng_P_purch = 7.8                #local measurement
ng_temp_Afurnace = 0.11         #local measurement
ng_temp_Bfurnace = 0.10         #local measurement
ng_temp_Cfurnace = 0.23         #local measurement
ng_temp_Incinerator = 0.4

ng_data['NG_temp_A_furnace'] =  JT_correction(ng_data['91T01'], ng_P_purch, ng_temp_Afurnace)
ng_data['NG_temp_B_furnace'] = JT_correction(ng_data['91T01'], ng_P_purch, ng_temp_Bfurnace) 
ng_data['NG_temp_C_furnace'] = JT_correction(ng_data['91T01'], ng_P_purch , ng_temp_Cfurnace) 
ng_data['NG_temp_Incinerator'] = JT_correction(ng_data['91T01'], ng_P_purch , ng_temp_Incinerator) 

ng_data['NG_flow_A_furnace'] = m3_to_Nm3(ng_data['NG_temp_A_furnace'], ng_temp_Afurnace, ng_data['82F04'])
ng_data['NG_flow_B_furnace'] = m3_to_Nm3(ng_data['NG_temp_B_furnace'], ng_temp_Bfurnace, ng_data['82F211'])
ng_data['NG_flow_C_furnace'] = m3_to_Nm3(ng_data['NG_temp_C_furnace'], ng_temp_Cfurnace, ng_data['82F74'])
ng_data['NG_flow_Incinerator'] = m3_to_Nm3(ng_data['NG_temp_Incinerator'], ng_temp_Incinerator, ng_data['87F22'])



ngPower = pd.DataFrame()

ngPower['A_furnace'] = calculate_ng_energy(ng_data['NG_flow_A_furnace'])
ngPower['B_furnace'] = calculate_ng_energy(ng_data['NG_flow_B_furnace'])
ngPower['C_furnace'] = calculate_ng_energy(ng_data['NG_flow_C_furnace'])
ngPower['Incinerator'] = calculate_ng_energy(ng_data['NG_flow_Incinerator'])

ngPower['Furnaces_total'] = ngPower['A_furnace'] + ngPower['B_furnace'] + ngPower['C_furnace'] 
ngPower['Users_total'] = ngPower['Furnaces_total'] + ngPower['Incinerator']
ngPower['Purchase'] = calculate_ng_energy(ng_data['91F01'])


store_dataframe(ngPower, 'ngpower')




