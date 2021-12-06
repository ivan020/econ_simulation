# -*- coding: utf-8 -*-
"""
Spyder Editor

The simulation is based on the Lengnick's Baseline Macroeconomic Agent-Based model
"""

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt

nMonths = 1000
nDays = 21
burn = 1000
H = 1000
F = 100
B = 10
num_typeA = 7
delta = .019
phi_max = 1
phi_min = .25
theta = .75
Phi_max = 1.15
Phi_min = 1.025
alpha = 3
Psi_price = .25
Psi_quant = .25
xi = .1
pi = .1
lambd = 3
Theta = .75
gamma = 3
beta = 5
n = 7
ki = .01
r = .03

bav = 2 #firm or a household is visiting at most bav banks
ber = 1 #the banks are required to keep ber amount of liquidity at reserves
        #if less, the government prints the money to fullfill missing liquidity
pla_hh = .5 #probability of loan approval for very risky household
pla_fi = .35 #probability of loan approval for very risky firm
plb_hh = .20 #probability that a risk-free household will take the loan
plb_fi = .30 #probability that a risk-free firm will take the loan

list_HH = []
list_FI = []
list_BA = []


def HH(name, w, m, c, alpha, risk_score):
    name = name
    w=w
    m=m
    c=c
    typeA = []
    typeB = []
    typeC_R = []
    typeD_R = []
    dividend = 0
    employed = False
    alpha = alpha
    P = 1.0
    loan = 0.0
    deposit = 0.0
    rate_on_deposit = .0
    deposited_funds = 0
    loan_rate = .0
    risk_profile = 0
    loan_capacity = 0
    serviceable_loan = 0
    household = {'name':name,
                 'w':w,
                 'm':m,
                 'c':c,
                 'typeA':typeA,
                 'typeB':typeB,
                 'typeC_R':typeC_R,
                 'typeD_R':typeD_R,
                 'dividend':dividend,
                 'alpha':alpha,
                 'employed':employed,
                 'alpha':alpha,
                 'P':P,
                 'loan':loan,
                 'deposit':deposit,
                 'deposited_funds': deposited_funds,
                 'loan_rate':loan_rate,
                 'deposit_rate':rate_on_deposit,
                 'risk_profile':risk_profile,
                 'loan_capacity':loan_capacity,
                 'serviceable_loan':serviceable_loan}
    return household

def hh_consumption_update(list_HH):
    for h in range(H):
        c_temp = list_HH[h]['m'] / list_HH[h]['P']
        list_HH[h]['c'] = min(c_temp**alpha, c_temp)
    return list_HH


def FI(name, w, inv, inv_min, inv_max, p,p_min, p_max, delta, Phi_min, Phi_max, phi_min, phi_max, theta, lambd, gamma, Theta):
    name = name
    w, m = w, 0 #wage, liquidity
    inv, inv_min, inv_max = inv, inv_min, inv_max
    Phi_min, Phi_max, phi_min, phi_max, d = Phi_min, Phi_max, phi_min, phi_max, inv
    theta, Theta = theta, Theta
    mc = 0
    to_hire, to_fire = 0,0
    gamma, lambd = gamma, lambd
    months_w_open_position = 0
    typeB = []
    typeA = []
    typeC_C = []
    typeD_C = []
    loan = 0.0
    deposit = 0
    deposit_with_bank = 0.0
    loan_rate = 0
    deposit_rate = 0
    credit_score = 0
    m_buf = 0
    dailyProduction = 0
    loan_capacity = 0
    borrowed_funds = 0
    firm ={'name': name,
           'w':w,
           'm':m,
           'p':p,
           'inv':inv,
           'inv_min':inv_min,
           'inv_max': inv_max,
           'Phi_min':Phi_min,
           'Phi_max':Phi_max,
           'phi_min':phi_min,
           'phi_max':phi_max,
           'd':d,
           'theta':theta,
           'Theta':Theta,
           'mc':mc,
           'to_hire':to_hire,
           'to_fire':to_fire,
           'gamma':gamma,
           'lambd':lambd,
           'months_w_open_position':months_w_open_position,
           'typeA':typeA,
           'typeB':typeB,
           'typeC_C':typeC_C,
           'typeD_C':typeD_C,
           'loan':loan,
           'loan_rate':loan_rate,
           'deposited_equity':deposit,
           'deposit_at_bank': deposit_with_bank,
           'deposit_rate':deposit_rate,
           'credit_score':credit_score,
           'm_buf':m_buf,
           'dailyProduction':dailyProduction,
           'loan_capacity':loan_capacity,
           'borrowed_funds':borrowed_funds}
    return firm

def update_labour_price(list_FI):
    for f in range(F):
        if list_FI[f]['to_hire'] > 0:
            list_FI[f]['months_w_open_position'] = list_FI[f]['months_w_open_position'] + 1
        #else:
        if list_FI[f]['to_hire'] == 0 and list_FI[f]['months_w_open_position']> 0:
            list_FI[f]['w'] = list_FI[f]['w']*(1-np.random.uniform(0, delta))
            list_FI[f]['months_w_open_position'] = 0
        if list_FI[f]['months_w_open_position'] >= gamma:
            list_FI[f]['w'] = list_FI[f]['w'] * (1+np.random.uniform(0,delta))
        list_FI[f]['inv_max'] = phi_max*list_FI[f]['d']
        list_FI[f]['inv_min'] = phi_min*list_FI[f]['d']
        list_FI[f]['d'] = 0
        list_FI[f]['mc'] = list_FI[f]['w']/lambd/nDays
        list_FI[f]['p_max'] = Phi_max * list_FI[f]['mc']
        list_FI[f]['p_min'] = Phi_min * list_FI[f]['mc']
        if list_FI[f]['inv'] < list_FI[f]['inv_min']:
            list_FI[f]['to_hire'] = 1
            #print(f'firm {f} is hiring!')
            list_FI[f]['to_fire'] = 0
            if list_FI[f]['p'] < list_FI[f]['p_max'] and np.random.uniform(0, theta):
                list_FI[f]['p'] = list_FI[f]['p'] * (1+np.random.uniform(0,theta))
                #print(f'firm {f} is increasing the price!')
        #else:
        if list_FI[f]['inv'] > list_FI[f]['inv_max']:
            list_FI[f]['to_fire'] = 1
            #print(f'firm {f} is firing!')
            list_FI[f]['to_hire'] = 0
            list_FI[f]['months_w_open_position'] = 0
            if list_FI[f]['p'] > list_FI[f]['p_min'] and np.random.uniform(0,1) < Theta:
                list_FI[f]['p'] = list_FI[f]['p'] * (1-np.random.uniform(0, theta))
                #print(f'firm {f} is decreasing prices!')
    return list_FI


def BA(name, m, risk_tolerance):
    name = name
    risk_tolerance = risk_tolerance
    m = m
    deposits_f = 0
    interest_expense_f = 0
    deposits_h=0
    interest_expense_h = 0
    loans_f = 0
    interest_income_f = 0
    loans_h = 0
    interest_income_h = 0
    total_deposit_expense = 0
    loans_given = 0
    total_loan_income = 0
    funds_from_money_supply = 0
    typeC_R = []
    typeC_C = []
    typeD_R = []
    typeD_C = []
    bank = {'name': name,
             'm':m,
             'deposits_f':deposits_f,
             'interest_expense_f': interest_expense_f,
             'deposits_h':deposits_h,
             'interest_expense_h':interest_expense_h,
             'loans_f':loans_f,
             'interest_income_f':interest_income_f,
             'loans_h':loans_h,
             'interest_income_hh':interest_income_h,
             'total_deposit_expense':total_deposit_expense,
             'loans_given':loans_given,
             'total_loan_income':total_loan_income,
             'funds_from_money_supply':funds_from_money_supply,
             'typeC_R':typeC_R,
             'typeC_C':typeC_C,
             'typeD_R':typeD_R,
             'typeD_C':typeD_C,
             'risk_tolerance': risk_tolerance}
    return bank
#this function defines size of the loan a firm or a household can get
def update_loan_offer(list_HH, list_FI):
    liquidity_at_firms = []
    liquidity_at_households = []
    for f in range(F):
        liquidity_at_firms.append(list_FI[f]['m'])
        if list_FI[f]['loan'] == 0:
            if sum(liquidity_at_firms)>0:
                list_FI[f]['loan_capacity'] = list_FI[f]['m'] / sum(liquidity_at_firms)
            else:
                list_FI[f]['loan_capacity'] = 0
        
    for h in range(H):
        liquidity_at_households.append(list_HH[h]['m'])
        if list_HH[h]['loan'] == 0:
            list_HH[h]['loan_capacity'] = list_HH[h]['m']/sum(liquidity_at_households)
    return list_HH, list_FI


def federal_government(mo, total_employment, total_production,total_liquidity ,list_BA, list_HH, list_FI, r):
    #interest rate is a function of employment rate, liquidity with banks and production
    if mo > 3: #starts working only when there is some stats to be collected
        employment_rate =[]
        emp = []
        production = []
        total_open_positions = []
        total_emp_m2 = total_employment[-2]
        total_emp_m1 = total_employment[-1]
        production_m2 = total_production[-2]
        production_m1 = total_production[-1]
        total_production_past_months = [production_m2, production_m1]
        total_employment_past_months = [total_emp_m2, total_emp_m1]
        mean_past_employment = np.mean(total_employment_past_months)
        mean_past_production = np.mean(total_production_past_months)
        wage = []
        #collecting the data
        for f in range(F):
            production.append(list_FI[f]['dailyProduction'])
            total_open_positions.append(list_FI[f]['to_hire'])
            wage.append(list_FI[f]['w'])
        total_production = sum(production)
        total_open_positions = sum(total_open_positions)
        minimum_wage = .8*min(wage)
        for h in range(H):
            emp.append(list_HH[h]['employed'])
            total_employment = sum(emp)
        employment_rate = (total_employment/H)*100
        #in case of recession
        if total_production < mean_past_production and employment_rate<mean_past_employment:
            r = r*(1+np.random.uniform(-0.02,-0.01)) #central bank cuts the interest rate by random value with 0 upper bound
            for h in range(H):
                if list_HH[h]['employed'] == False:
                    list_HH[h]['w']=minimum_wage #unemployed household gets benefits
                    list_HH[h]['m'] = list_HH[h]['m'] + minimum_wage
        
        else:
            print('interest rate stays unchanged')
        #the federal government will print money and distribute it to banks that do not meet capital requirements at any time
        for b in range(B):
            if list_BA[b]['m'] < ber:
                money_supply = ber - list_BA[b]['m']
                if money_supply < 0:
                    money_supply = ber + list_BA[b]['m']
                list_BA[b]['m'] = list_BA[b]['m'] + money_supply
                list_BA[b]['funds_from_money_supply'] = money_supply
        return r, list_BA, list_HH, list_FI
    
#the following function defines banks risk appetite and each households' and firms' risk profile
def bank_risk_metric(list_HH, list_FI, list_BA):
    #determine banks risk tolerance
    banks_liquidity = []
    for b in range(B):
        banks_liquidity.append(list_BA[b]['m'])
    mean_banks_liquidity = np.mean(banks_liquidity)
    #bank needs to collect the data on firms and households at point in time
    #we start with households
    wages = []
    hh_liquidity = []
    for h in range(H):
        wages.append(list_HH[h]['w'])
        hh_liquidity.append(list_HH[h]['m'])
    mean_wage = np.mean(wages)
    mean_hh_liquidity = np.mean(hh_liquidity)
    
    #firms have a bit more data
    marginal_cost = []
    f_liquidity = []
    clients = []
    workers = []
    for f in range(F):
        marginal_cost.append(list_FI[f]['mc'])
        f_liquidity.append(list_FI[f]['m'])
        clients.append(len(list_FI[f]['typeA']))
        workers.append(len(list_FI[f]['typeB']))
    mean_marginal_cost = np.mean(marginal_cost)
    mean_f_liquidity = np.mean(f_liquidity)
    mean_clients = np.mean(clients)
    mean_workers = np.mean(workers)
    #each agent receives a risk profile based on a scoring system

    #banks with higher liquidity are willing to finance riskier enterprises
    #banks with positive 
    for b in range(B):
        if list_BA[b]['m'] >= mean_banks_liquidity:
            bank_risk_tolerance = .5
        if list_BA[b]['m'] < mean_banks_liquidity:
            bank_risk_tolerance = 0
        list_BA[b]['risk_tolerance'] = bank_risk_tolerance
    #firms with higher risk profile borrow at a higher rate but they deposit at lower rate
    #let risk profile consist of 4 groups: 0 (very risky),1  2(moderate) and 3 (risk-free)
    for f in range(F):
        if list_FI[f]['mc'] > mean_marginal_cost:
            risk_profile_mc = .25
        else:
            risk_profile_mc = 0
        if list_FI[f]['m'] > mean_f_liquidity:
            risk_profile_liq = .25
        else:
            risk_profile_liq = 0
        if len(list_FI[f]['typeA']) > mean_clients:
            risk_profile_clientele = .25
        else:
            risk_profile_clientele = 0
        if len(list_FI[f]['typeB'])> mean_workers:
            risk_profile_size_workers = .25
        else:
            risk_profile_size_workers = 0
        list_FI[f]['credit_score'] = risk_profile_mc+risk_profile_liq+risk_profile_clientele+risk_profile_size_workers
    #households with better financial standing can borrow at lower rate and deposit at higher rate
    for h in range(H):
        if list_HH[h]['w'] > mean_wage:
            risk_profile_hh_w = .5
        else:
            risk_profile_hh_w = 0
        if list_HH[h]['m'] > mean_hh_liquidity:
            risk_profile_hh_m = .5
        else:
            risk_profile_hh_m = 0
        list_HH[h]['risk_profile'] = risk_profile_hh_w+risk_profile_hh_m
    return list_FI, list_HH, list_BA

#definition of borrowing process
def borrowing(list_FI, list_HH, list_BA, interest_rate, CR_df, CC_df):
    #start with households: they want to borrow to consume more
    #if the wage of the household is less than the mean wage offered by all firms, it borrows to meet higher consumption
    wages = []
    for f in range(F):
        wages.append(list_FI[f]['w'])
    desired_wage = np.mean(wages)
    for h in range(H):
        if list_HH[h]['loan'] == 0: #rule out the Ponzi scheme condition
            if list_HH[h]['w'] < desired_wage: #apriori a household with .5 or 0 risk profile
                for i in range(bav):
                    index = random.choice(range(B))
                    bank = list_BA[index]
                    if list_HH[h]['loan_capacity'] < bank['m']:
                        to_borrow = list_HH[h]['loan_capacity']
                    else:
                        to_borrow = bank['m']
                #if moderate credit score and bank is very risk averse, it randomly charges the highest score
                    if bank['m'] > 0:
                        if bank['risk_tolerance'] == .5 and list_HH[h]['loan'] == 0:
                            if list_HH[h]['risk_profile'] == .5 and list_HH[h]['loan'] == 0:
                    #the loan is inelasticly given as a proportion of household wealth 
                                bank['m'] = bank['m'] - to_borrow
                                list_HH[h]['m'] = list_HH[h]['m'] + to_borrow
                                bank['loans_h'] = bank['loans_h']+to_borrow
                                list_HH[h]['serviceable_loan'] = to_borrow
                                list_HH[h]['loan'] = to_borrow
                                list_HH[h]['loan_capacity'] = 0
                                list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.05,.09) #the interest on hh with moderate risk
                                list_HH[h]['typeC_R'].append(bank['name'])
                                bank['typeC_R'].append(h)
                                CR_df.loc[h, index] = True
                    #if very low credit score and bank is very risk averse, we need probability
                            if list_HH[h]['risk_profile'] == 0 and pla_hh > np.random.uniform(0,1) and list_HH[h]['loan'] == 0:
                                bank['m'] = bank['m'] - to_borrow
                                bank['loans_h'] = bank['loans_h']+to_borrow
                                list_HH[h]['m'] = list_HH[h]['m'] + to_borrow
                                list_HH[h]['serviceable_loan'] = to_borrow
                                list_HH[h]['loan_capacity'] = 0
                                list_HH[h]['typeC_R'].append(bank['name'])
                                list_HH[h]['loan'] = to_borrow
                                list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.1,.14)
                                bank['typeC_R'].append(h)
                                CR_df.loc[h, index]
                        if bank['risk_tolerance'] == 0 and list_HH[h]['loan'] == 0: #if the risk tolerance is low, then bank will service any household
                            bank['m'] = bank['m'] - to_borrow
                            list_HH[h]['m'] = list_HH[h]['m'] + to_borrow
                            bank['loans_h'] = bank['loans_h']+to_borrow
                            list_HH[h]['serviceable_loan'] = to_borrow
                            list_HH[h]['loan'] = to_borrow
                            list_HH[h]['loan_capacity'] = 0
                            if list_HH[h]['risk_profile'] == 1:
                                list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.02, .05)
                            if list_HH[h]['risk_profile'] == .5:
                                list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.05,.09)
                            if list_HH[h]['risk_profile'] == 0:
                                list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.1,.14)
                        bank['typeC_R'].append(h)
                        list_HH[h]['typeC_R'].append(bank['name'])
                        CR_df.loc[h, index] = True
        #for the case of household having a very high credit score, it decides whether to take the loan or not     
                    if list_HH[h]['risk_profile'] == 1 and list_HH[h]['loan'] == 0:
                        if plb_hh > np.random.uniform(0,1): #if True, then hh will go to a randomly picked bank
                            b = random.choice(range(B))
                            bank = list_BA[b]
                            bank['m'] = bank['m'] - to_borrow
                            list_HH[h]['m'] = list_HH[h]['m'] + to_borrow
                            bank['loans_h'] = bank['loans_h']+to_borrow
                            list_HH[h]['serviceable_loan'] = to_borrow 
                            list_HH[h]['loan'] = to_borrow
                            list_HH[h]['loan_capacity'] = 0
                            list_HH[h]['typeC_R'].append(b)
                            list_HH[h]['loan_rate'] = interest_rate + np.random.uniform(.02, .05)
                            bank['typeC_R'].append(h)
                            CR_df.loc[h,b] = True
    #firm borrowing
    for f in range(F):
        #the firm will borrow to save the workforce and thus to keep up with inv manufacturing to sell more 
        if list_FI[f]['loan'] == 0:
            nhh = len(list_FI[f]['typeB'])
            cap_exp = list_FI[f]['w'] * nhh
            total_m = list_FI[f]['m'] + list_FI[f]['m_buf']
            if cap_exp > total_m:
                to_borrow = cap_exp - total_m
                for i in range(bav):
                    b = random.choice(range(B))
                    bank = list_BA[b]
                    if bank['m'] < to_borrow:
                        to_borrow = bank['m']
                    #in case a bank risk tolerance is high
                    if bank['m'] > 0:
                        if bank['risk_tolerance'] == .5 and list_FI[f]['loan'] == 0:
                        #in case of B investment grade, 
                            if list_FI[f]['credit_score'] == .5 and list_FI[f]['loan'] == 0:
                                bank['m'] = bank['m'] - to_borrow
                                bank['loans_f'] = bank['loans_f']+to_borrow
                                list_FI[f]['m'] = list_FI[f]['m'] + to_borrow
                                list_FI[f]['loan'] = to_borrow #replace this value with to_borrow so to have a proper accounting
                                list_FI[f]['borrowed_funds'] = to_borrow
                                list_FI[f]['loan_capacity'] = 0
                                list_FI[f]['typeC_C'].append(bank['name'])
                                bank['typeC_C'].append(f)
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.04, .06)
                                CC_df.loc[f,b] = True
                        #in case of C investment grade, the firm still gets the loan at higher rate
                            if list_FI[f]['credit_score'] == .25 and list_FI[f]['loan'] == 0:
                                bank['m'] = bank['m'] - to_borrow
                                bank['loans_f'] = bank['loans_f']+to_borrow
                                list_FI[f]['m'] = list_FI[f]['m'] + to_borrow
                                list_FI[f]['loan'] = to_borrow
                                list_FI[f]['borrowed_funds'] = to_borrow
                                list_FI[f]['loan_capacity'] = 0
                                list_FI[f]['typeC_C'].append(bank['name'])
                                bank['typeC_C'].append(f)
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.06,.08)
                                CC_df.loc[f,b] = True
                        #in case of D investment grade (junk bond), the company gets approved only with certain probability
                            if list_FI[f]['credit_score'] == 0 and pla_fi > np.random.uniform(0,1) and list_FI[f]['loan'] == 0:
                                bank['m'] = bank['m'] - to_borrow
                                list_FI[f]['m'] = list_FI[f]['m'] + to_borrow
                                bank['loans_f'] = bank['loans_f']+to_borrow
                                list_FI[f]['loan'] = to_borrow
                                list_FI[f]['borrowed_funds'] = to_borrow
                                list_FI[f]['loan_capacity'] = 0
                                list_FI[f]['typeC_C'].append(bank['name'])
                                bank['typeC_C'].append(f)
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.08,.1)
                                CC_df.loc[f,b] = True
                        if bank['risk_tolerance'] == 0 and list_FI[f]['loan'] == 0: #any firm gets a loan approval, but the rate will differ
                            bank['m'] = bank['m'] - to_borrow
                            list_FI[f]['m'] = list_FI[f]['m'] + to_borrow
                            bank['loans_f'] = bank['loans_f']+to_borrow
                            list_FI[f]['loan'] = to_borrow
                            list_FI[f]['borrowed_funds'] = to_borrow
                            list_FI[f]['loan_capacity'] = 0
                            list_FI[f]['typeC_C'].append(bank['name'])
                            bank['typeC_C'].append(f)
                        # decision regarding the rate on loan, st the firm's credit rating
                            if list_FI[f]['credit_score'] == .5 and list_FI[f]['loan'] == 0:
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.04, .06)
                            if list_FI[f]['credit_score'] == .25 and list_FI[f]['loan'] == 0:
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.06, .08)
                            if list_FI[f]['credit_score'] == 0 and list_FI[f]['loan'] == 0:
                                list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(0.08, 0.1)
                            CC_df.loc[f,b] = True
                if list_FI[f]['credit_score'] == 1 and list_FI[f]['loan'] == 0:
                #in case of A investment grade, the firm may want to borrow with certain probability
                    if plb_fi > np.random.uniform(0,1):
                        to_borrow = list_FI[f]['loan_capacity'] #it borrows a full allowable amount of money
                        index = random.choice(range(B)) 
                        bank = list_BA[index]
                        bank['m'] = bank['m'] - to_borrow
                        bank['loans_f'] = bank['loans_f']+to_borrow
                        list_FI[f]['m'] = list_FI[f]['m'] + to_borrow
                        list_FI[f]['loan'] = to_borrow
                        list_FI[f]['borrowed_funds'] = to_borrow
                        list_FI[f]['loan_capacity'] = 0
                        list_FI[f]['typeC_C'].append(bank['name'])
                        bank['typeC_C'].append(f)
                        list_FI[f]['loan_rate'] = interest_rate + np.random.uniform(.02,.04)
                        CC_df.loc[f,b] = True
                        
    return list_FI, list_HH, list_BA, CR_df, CC_df

#the next function defines the payback loan for both firms and households

def payback_loan(list_FI, list_HH, list_BA, CR_df, CC_df):
    #first firms are paying back from their total liquidity (m+m_buf)
    for f in range(F):
        #if after the transaction the borrowed_funds are >0
        if list_FI[f]['loan'] >0:
            index = list_FI[f]['typeC_C'][0] #there should be only one bank
            bank = list_BA[index]
            interest_expense = list_FI[f]['loan'] * list_FI[f]['loan_rate'] 
            transaction = interest_expense
            if transaction > list_FI[f]['m']:
                transaction = list_FI[f]['m']
            list_FI[f]['m'] = list_FI[f]['m'] - transaction
            bank['m'] = bank['m'] + transaction
            bank['loans_f'] = bank['loans_f'] - transaction
            bank['interest_income_f'] = bank['interest_income_f'] + transaction
            list_FI[f]['borrowed_funds'] = list_FI[f]['borrowed_funds'] - transaction
            #in case the loan was repaid in full
            if list_FI[f]['borrowed_funds'] <= 0:
                list_FI[f]['loan'] = 0
                list_FI[f]['borrowed_funds'] = 0
                list_FI[f]['loan_rate'] = 0
                list_FI[f]['typeC_C'].remove(bank['name'])
                bank['typeC_C'].remove(f)
                CC_df.loc[f,bank['name']] = False
    #households paybacks
    for h in range(H):
        if list_HH[h]['loan']>0:
            index = list_HH[h]['typeC_R'][0]
            bank = list_BA[index]
            loan_interest_payment = list_HH[h]['loan'] * list_HH[h]['loan_rate']
            transaction = loan_interest_payment
            if transaction > list_HH[h]['m']:
                transaction = list_HH[h]['m']
            list_HH[h]['m'] = list_HH[h]['m'] - transaction
            bank['m'] = bank['m'] + transaction
            bank['interest_income_hh'] = bank['interest_income_hh'] + transaction
            list_HH[h]['serviceable_loan'] = list_HH[h]['serviceable_loan'] - transaction
            if list_HH[h]['serviceable_loan'] <= 0:
                list_HH[h]['loan'] = 0
                list_HH[h]['serviceable_loan'] = 0
                list_HH[h]['loan_rate'] = 0
                list_HH[h]['typeC_R'].remove(bank['name'])
                bank['typeC_R'].remove(h)
                CR_df.loc[h, bank['name']] = False
    return list_FI, list_HH, list_BA, CR_df, CC_df

#the depositing of funds activity
#I'll assume that a firm or household with low credit rating will withdraw deposit earlier than the one with high
#Also assume that depositing is only available for those who do not have any loans
#thus, the household with low rating will deposit money at least rate and vice versa
#households and firms can also deposit up to 50% of its current liquidity m
#this could be argued that the size of the deposit depends on the welfare of the household,
#so that a wealthy houeshold will deposit more money, while not that wealthy will deposit less
def deposit(list_BA, list_HH, list_FI, DR_df, DC_df, r):
    #starting with households again:
    for h in range(H):
        if list_HH[h]['loan'] == 0 and list_HH[h]['m'] > 0 and list_HH[h]['deposited_funds'] == 0: #household will randomly decide on the amount of money it wants to deposit
            index = random.choice(range(B))
            bank = list_BA[index]
            if list_HH[h]['risk_profile'] == 1:
                #this hh will, again, get the best possible deal
                #they will also deposit more money
                hh_money_to_deposit = list_HH[h]['m'] * np.random.uniform(.15,.2)
                list_HH[h]['deposited_funds'] = hh_money_to_deposit #this amount is for accumulation
                list_HH[h]['deposit_with_bank'] = hh_money_to_deposit #this amount is for accounting purposes
                list_HH[h]['deposit_rate'] = r + np.random.uniform(.06, .08)
                list_HH[h]['m'] = list_HH[h]['m'] - hh_money_to_deposit
                list_HH[h]['typeD_R'].append(bank['name'])
                bank['m'] = bank['m'] + hh_money_to_deposit
                bank['deposits_h'] = bank['deposits_h'] + hh_money_to_deposit
                bank['typeD_R'].append(h)
                #recognize the relationship
                DR_df.loc[h,bank['name']]=True
            if list_HH[h]['risk_profile'] ==.5 and list_HH[h]['deposited_funds'] == 0:
                hh_money_to_deposit = list_HH[h]['m'] * np.random.uniform(.1,.15)
                list_HH[h]['deposited_funds'] = hh_money_to_deposit
                list_HH[h]['deposit_with_bank'] = hh_money_to_deposit
                list_HH[h]['deposit_rate'] = r+np.random.uniform(.04,.06)
                list_HH[h]['m']=list_HH[h]['m'] - hh_money_to_deposit
                list_HH[h]['typeD_R'].append(bank['name'])
                bank['m'] = bank['m'] + hh_money_to_deposit
                bank['deposits_h'] = bank['deposits_h'] + hh_money_to_deposit
                bank['typeD_R'].append(h)
                DR_df.loc[h, bank['name']] = True
            if list_HH[h]['risk_profile'] == 0 and list_HH[h]['deposited_funds'] == 0: #the worst credit rating would probably need money soon
                hh_money_to_deposit = list_HH[h]['m'] * np.random.uniform(.05,.1)
                list_HH[h]['deposited_funds'] = hh_money_to_deposit
                list_HH[h]['deposit_with_bank'] = hh_money_to_deposit
                list_HH[h]['deposit_rate'] = r + np.random.uniform(.02,.04)
                list_HH[h]['m'] = list_HH[h]['m'] - hh_money_to_deposit
                bank['m'] = bank['m'] + hh_money_to_deposit
                bank['deposits_h'] = bank['deposits_h'] + hh_money_to_deposit
                list_HH[h]['typeD_R'].append(bank['name'])
                bank['typeD_R'].append(h)
                DR_df.loc[h,bank['name']] = True
        #the firms side 
    for f in range(F):
        if list_FI[f]['loan'] == 0 and list_FI[f]['deposited_equity'] == 0: #works only if the firm has no debt outstanding
            #any company that has excess funds will be allowed to make a deposit, so
            nhh = len(list_FI[f]['typeB'])
            cap_exp = list_FI[f]['w'] * nhh
            total_m = list_FI[f]['m'] + list_FI[f]['m_buf']
            leftover = total_m - cap_exp
            if leftover > 0: #leftover should be a positive amount of liquidity
                #if the leftover is positive, the firm randomly picks up a bank with which it wants to deposit
                b = random.choice(range(B))
                bank = list_BA[b]
                if list_FI[f]['credit_score'] == 1 and list_FI[f]['deposited_equity'] == 0:
                    #a good business can deposit up to 20% of their leftover money
                    funds_to_deposit = leftover * np.random.uniform(0.15, 0.20)
                    #they will also get a better deal, since the size of their deposit is the largest
                    list_FI[f]['deposited_equity'] = funds_to_deposit
                    list_FI[f]['deposit_at bank'] = funds_to_deposit
                    #establish a rate
                    list_FI[f]['deposit_rate'] = r + np.random.uniform(0.03,0.04)
                    #transaction
                    list_FI[f]['m'] = list_FI[f]['m'] - funds_to_deposit
                    bank['m'] = bank['m'] + funds_to_deposit
                    bank['deposits_f'] = bank['deposits_f'] + funds_to_deposit
                    #establish the relationship
                    bank['typeD_C'].append(f)
                    list_FI[f]['typeD_C'].append(bank['name'])
                    DC_df.loc[f,bank['name']] = True
                if list_FI[f]['credit_score'] == .5 and list_FI[f]['deposited_equity'] == 0:
                    funds_to_deposit = leftover * np.random.uniform(.1,.15) #up to 15% 
                    list_FI[f]['deposited_equity'] = funds_to_deposit
                    list_FI[f]['deposit_at_bank'] = funds_to_deposit
                    list_FI[f]['deposit_rate'] = r + np.random.uniform(.02,.03)
                    list_FI[f]['m'] = list_FI[f]['m'] - funds_to_deposit
                    bank['m'] = bank['m'] + funds_to_deposit
                    bank['deposits_f'] = bank['deposits_f'] + funds_to_deposit
                    bank['typeD_C'].append(f)
                    list_FI[f]['typeD_C'].append(bank['name'])
                    DC_df.loc[f, bank['name']] = True
                if list_FI[f]['credit_rating'] == .25 and list_FI[f]['deposited_equity'] == 0:
                    funds_to_deposit = leftover * np.random.uniform(.05,.1)
                    list_FI[f]['deposited_equity'] = funds_to_deposit
                    list_FI[f]['deposit_at_bank'] = funds_to_deposit
                    list_FI[f]['deposit_rate'] = r+np.random.uniform(0.01,0.02)
                    list_FI[f]['m'] = list_FI[f]['m'] - funds_to_deposit
                    bank['m'] = bank['m'] + funds_to_deposit
                    bank['deposits_f'] = bank['deposits_f'] + funds_to_deposit
                    bank['typeD_C'].append(f)
                    list_FI[f]['typeD_C'].append(bank['name'])
                    DC_df.loc[f, bank['name']] = True
                if list_FI[f]['credit_score'] == 0 and list_FI[f]['deposited_equity'] == 0:
                    funds_to_deposit = leftover * np.random.uniform(.01,.05)
                    list_FI[f]['deposited_equity'] = funds_to_deposit
                    list_FI[f]['deposit_at_bank'] = funds_to_deposit
                    list_FI[f]['deposit_rate'] = r + np.random.uniform(.005,.01)
                    list_FI[f]['m'] = list_FI[f]['m'] - funds_to_deposit
                    bank['m'] = bank['m'] + funds_to_deposit
                    bank['deposits_f'] = bank['deposits_f'] + funds_to_deposit
                    bank['typeD_C'].append(f)
                    list_FI[f]['typeD_C'].append(bank['name'])
                    DC_df.loc[f, bank['name']] = True
    return list_FI, list_HH, list_BA, DC_df, DR_df

#at the end of the month, the bank pays back the loan with some accumulated %
def payback_deposit(list_FI, list_HH, list_BA, DC_df, DR_df):
    #we start with households again
    for h in range(H):
        if list_HH[h]['deposited_funds'] > 0:
            index = list_HH[h]['typeD_R'][0]
            bank = list_BA[index]
            transaction_amount = list_HH[h]['deposited_funds'] *(1+list_HH[h]['deposit_rate'])
            bank['m'] = bank['m'] - transaction_amount
            bank['interest_expense_h'] = bank['interest_expense_h'] + transaction_amount
            list_HH[h]['m'] = list_HH[h]['m'] + transaction_amount
            list_HH[h]['deposited_funds'] = 0
            list_HH[h]['deposit_with_bank'] = 0
            list_HH[h]['deposit_rate'] = 0
            bank['typeD_R'].remove(h)
            list_HH[h]['typeD_R'].remove(bank['name'])
            DR_df.loc[h, bank['name']] = False
    for f in range(F):
        if list_FI[f]['deposited_equity'] > 0:
            index = list_FI[f]['typeD_C'][0]
            bank = list_BA[index]
            transaction_amount = list_FI[f]['deposited_equity'] * (1 + list_FI[f]['deposit_rate'])
            bank['m'] = bank['m'] - transaction_amount
            bank['interest_expense_f'] = bank['interest_expense_f'] + transaction_amount
            list_FI[f]['m'] = list_FI[f]['m'] + transaction_amount
            list_FI[f]['deposited_equity'] = 0
            list_FI[f]['deposit_at_bank'] = 0
            list_FI[f]['deposit_rate'] = 0
            bank['typeD_C'].remove(f)
            list_FI[f]['typeD_C'].remove(bank['name'])
            DC_df.loc[f, bank['name']] = False
    return list_FI, list_HH, list_BA, DR_df, DC_df
            

def produce(list_FI):
    for f in range(F):
        list_FI[f]['dailyProduction'] = lambd*len(list_FI[f]['typeB'])
        list_FI[f]['inv'] = list_FI[f]['inv'] + lambd*len(list_FI[f]['typeB'])
    return list_FI

def update_price(list_HH,list_FI, A_df):
    for h in range(H):
        f_index = random.choice(range(num_typeA))
        f = list_HH[h]['typeA'][f_index]
        while True:
            f_new = random.choice(range(F))
            if A_df.loc[h, f_new] == False:
                break
        price_f = list_FI[f]['p']
        price_f_new = list_FI[f_new]['p']
        if np.random.uniform(0,1) < Psi_price and ((price_f - price_f_new) >= (xi*price_f)):
            A_df.loc[h,f] = False
            #print(f'firm {f} and household {h} are cancelling the contract!')
            A_df.loc[h,f_new] = True
            #print(f'firm {f_new} and household {h} are making a deal!')
            list_HH[h]['typeA'][f_index] = f_new
            
            
            list_FI[f_new]['typeA'].append(h)
            list_FI[f]['typeA'].remove(h)
    return list_FI, list_HH, A_df
            
def update_typeA_quant(list_HH, list_FI, A_df, A_df_constraints):
    for h in range(H):
        total_constraint = A_df_constraints.iloc[h].sum()
        if np.random.uniform(0, 1) < Psi_quant and total_constraint > 0:
            probability = np.random.uniform(0, 1)
            f_index = -1
            cumulative_probability = 0
            while True:
                f_index=f_index+1
                f = list_HH[h]['typeA'][f_index]
                cumulative_probability = cumulative_probability+(A_df_constraints.loc[h,f] / total_constraint)
                if probability <= cumulative_probability or f_index >= num_typeA-1:
                    break
            while True:
                f_new = random.choice(range(F))
                #print(h, f_new)
                if A_df.loc[h,f_new] == False:
                    break
            A_df.loc[h,f] = False
            #print(f'household {h} and firm {f} are breaking agreement due to low quantity')
            A_df.loc[h,f_new] = True
            #print(f'household {h} and firm {f_new} are establishing new relationship')
            #print(f,h)
            list_HH[h]['typeA'][f_index] = f_new #instead of removing, you are replacing
            list_FI[f_new]['typeA'].append(h)
            list_FI[f]['typeA'].remove(h)
            
    return list_FI, list_HH, A_df

def updateTypeB(list_HH, list_FI, B_df):
    for f in range(F):
        if list_FI[f]['to_fire'] > 0:
            employees = list_FI[f]['typeB']
            if len(employees) > 0:
                #print(employees, type(employees))
                if len(employees) > 1:
                    to_fire_hh_id = random.choice(employees)
                if len(employees) == 1:
                    to_fire_hh_id = employees[0]
                #to_fire_hh_id = random.choice(employees) if len(employees) > 1 else employee
                #print(to_fire_hh_id)
                list_HH[to_fire_hh_id]['employed'] = False
                list_FI[f]['typeB'].remove(to_fire_hh_id)
                #print(f'household {to_fire_hh_id} is getting fired from firm {f}')
                list_HH[to_fire_hh_id]['typeB'] = []
                
                B_df.loc[to_fire_hh_id,f] = False
            list_FI[f]['to_fire'] = 0
    for h in range(H):
        if list_HH[h]['employed'] == True:
            b_zero = 1
            f = list_HH[h]['typeB']
            #f = int(f)
            if list_HH[h]['w'] <= list_FI[f]['w']:
                probability = pi
                list_HH[h]['w'] = list_FI[f]['w']
            else:
                probability = 1
        if list_HH[h]['employed'] == False:
            b_zero = beta
            #f = np.nan
            #print(f)
            probability = 1
            list_HH[h]['w'] = .9*list_HH[h]['w']
            #print(f'household {h} is making reduction')
        if np.random.uniform(0,1) < probability:
            templist_f = list(range(F))
            if list_HH[h]['employed'] == True:
                f = list_HH[h]['typeB']
                templist_f.remove(f)
                
            for i in range(b_zero):
                rnd = random.choice(templist_f)
                
                if list_FI[rnd]['to_hire']>0:
                    if list_HH[h]['employed'] == True:
                        if list_FI[rnd]['w']>list_FI[f]['w']:
                            B_df.loc[h,f] = False
                            B_df.loc[h, rnd] = True
                            #print(f'household {h} is exiting firm {f} to firm {rnd}')
                            list_FI[f]['typeB'].remove(h)
                            list_HH[h]['employed'] = True
                            list_HH[h]['typeB'] = rnd
                            list_FI[rnd]['typeB'].append(h)
                            list_FI[rnd]['to_hire'] = list_FI[rnd]['to_hire'] - 1
                            break
                    if list_HH[h]['employed'] == False:
                        if list_FI[rnd]['w'] >= list_HH[h]['w']:
                            B_df.loc[h,rnd] = True
                            #print(f'unemployed household {h} found a job at {f}!')
                            list_HH[h]['employed'] = True
                            list_HH[h]['typeB'] = rnd
                            list_FI[rnd]['typeB'].append(h)
                            list_FI[rnd]['to_hire'] = list_FI[rnd]['to_hire'] - 1
                            break
                    templist_f.remove(rnd)
    return list_FI, list_HH, B_df
            


def update_average_price(list_FI, list_HH):
    prices_list = []
    for h in range(H):
        suppliers = list_HH[h]['typeA']
        for i in suppliers:
            prices_list.append(list_FI[i]['p'])
        list_HH[h]['P'] = np.mean(prices_list)
    return list_HH


def goodmarketdailyevent(list_HH, list_FI, A_df_constraint):
    HHorder = random.sample(range(H), H)
    for h in HHorder:
        templist = list_HH[h]['typeA']
        purchased_quantity = 0.0
        visitedfirms = -1.0
        household_demand = list_HH[h]['c']/nDays
        while list_HH[h]['m'] > 0 and purchased_quantity < .95 *household_demand and visitedfirms < n and len(templist)>0:
            if len(templist)>1:
                f = random.choice(templist)
            else:
                f = templist[0]
            #print(f)
            current_demand = min(household_demand - purchased_quantity, list_HH[h]['m']/list_FI[f]['p'])
            param = current_demand - list_FI[f]['inv']
            A_df_constraint.loc[h,f] = max(param, 0)
            transaction_quantity = min(current_demand, list_FI[f]['inv'])
            list_FI[f]['d'] = list_FI[f]['d'] + transaction_quantity
            list_FI[f]['inv'] = list_FI[f]['inv'] - transaction_quantity
            list_FI[f]['m'] = list_FI[f]['m'] + transaction_quantity*list_FI[f]['p']
            list_HH[h]['m'] = list_HH[h]['m'] - transaction_quantity * list_FI[f]['p']
            purchased_quantity = purchased_quantity + transaction_quantity
            templist[templist !=f ]
            visitedfirms +=1
            if templist is None:
                templist = []
    return list_FI, list_HH, A_df_constraint

def firm_wage_expense(list_HH, list_FI):
	for f in range(F):
		hh_temp = list_FI[f]['typeB']
		nhh = len(hh_temp)
		list_FI[f]['m'] = list_FI[f]['m'] +list_FI[f]['m_buf']
		amount_paid = min(list_FI[f]['w']*nhh, list_FI[f]['m'])
		list_FI[f]['m'] = list_FI[f]['m'] - amount_paid
		
		if nhh > 0:
			amount_paid_per_capita = amount_paid/nhh
			list_FI[f]['w'] = amount_paid_per_capita
			for h in hh_temp:
				list_HH[h]['m'] = list_HH[h]['m']+amount_paid_per_capita
		list_FI[f]['m_buf'] = min(ki*amount_paid, list_FI[f]['m'])
		list_FI[f]['m'] = list_FI[f]['m'] - list_FI[f]['m_buf']
	return list_FI, list_HH

#this function is not working properly
def firm_dividend_expense(list_HH, list_FI):
	aggregate_profit = 0
	aggregate_wealth = 0
	for f in range(F):
		aggregate_profit = aggregate_profit + list_FI[f]['m']
		list_FI[f]['m'] = 0
	for h in range(H):
		aggregate_wealth = aggregate_wealth + list_HH[h]['m']
	if aggregate_wealth > 0 and aggregate_profit >0:
		for h in range(H):
			list_HH[h]['dividend'] = aggregate_profit*(list_HH[h]['m'] / aggregate_wealth)
			list_HH[h]['m'] = list_HH[h]['m'] + list_HH[h]['dividend']			
	return list_FI, list_HH

def quantity_produced(list_FI):
    production = []
    #firms = []
    for i in range(len(list_FI)):
        production.append(list_FI[i]['dailyProduction'])
    return sum(production)


def get_employment(list_HH):
    total_employment = []
    for i in range(len(list_HH)):
        household = list_HH[i]
        total_employment.append(household['employed'])
    employment_rate = (sum(total_employment)/H) * 100
    return employment_rate

def get_total_liquidity(list_BA):
    total_liquidity = []
    for i in range(len(list_BA)):
        total_liquidity.append(list_BA[i]['m'])
    return sum(total_liquidity)
def get_money_supply(list_BA):
    total_supply = []
    for i in range(len(list_BA)):
        total_supply.append(list_BA[i]['funds_from_money_supply'])
    return sum(total_supply)

def get_hh_consumption(list_HH):
    consumption = []
    for i in range(H):
        consumption.append(list_HH[h]['c'])
    return sum(consumption)

def get_inflation_data(list_HH):
    price_for_goods = []
    for i in range(H):
        price_for_goods.append(list_HH[h]['P'])
    return sum(price_for_goods)

list_FI = []
list_HH = []
list_BA = []
#the simulation#
for i in range(H):
	w, m = np.random.normal(1,.2) , np.random.normal(1,.2)
	c = int(np.random.choice(np.arange(21,105),1))
	household = HH(i, w, m, c, alpha, 0)
	list_HH.append(household)

for i in range(F):
	w, p = np.random.normal(1,0.2), np.random.normal(.015, .002)
	inv = np.random.choice(range(10))
	inv_min = inv*.9
	inv_max = inv*1.1
	p_min = p*.9
	p_max = p*1.1
	firm = FI(i, w, inv,inv_min, inv_max, p,p_min,p_max, delta, Phi_min, Phi_max, phi_min, phi_max, theta, lambd, gamma, Theta)
	list_FI.append(firm)

for i in range(B):
    m = np.random.normal(1,.2)
    bank = BA(i,m,.5)
    list_BA.append(bank)
    
    
A_df = pd.DataFrame(False, index = np.arange(H), columns = np.arange(F))
A_df_constraints = pd.DataFrame(False, index = np.arange(H), columns = np.arange(F))
B_df = pd.DataFrame(False, index = np.arange(H), columns = np.arange(F))
CR_df = pd.DataFrame(False, index = np.arange(H), columns = np.arange(B))
CC_df = pd.DataFrame(False, index = np.arange(F), columns = np.arange(B))
DR_df = pd.DataFrame(False, index = np.arange(H), columns = np.arange(B))
DC_df = pd.DataFrame(False, index = np.arange(F), columns = np.arange(B))

for h in range(H):
    newF = random.choice(range(F))
    #print(newF,h)
    B_df.loc[h,newF] = True
    list_HH[h]['typeB'] = newF
    list_FI[newF]['typeB'].append(h)
    list_HH[h]['employed'] = True
    #newtypeA = list(np.repeat(1,num_typeA))
    newtypeA = []
    counter = 0
    while counter < num_typeA:
        f = random.choice(range(F))
        #print(h,f)
        #print(f)
        if A_df.loc[h,f] == False:
            A_df.loc[h,f] = True
            list_HH[h]['typeA'].append(f)
            list_FI[f]['typeA'].append(h)
            counter += 1
            #print(counter, num_typeA)

    #list_HH[h]['typeA'] = newtypeA
#total_production, employment, wage, price, dividend, to_hire, output = np.repeat(0,nMonths)

total_employment =[]
production = []
total_production = []
total_liquidity = []
total_money_supply = []
total_consumption = []
interest_rate_movements = []
inflation = []

rep_liquidity = []
rep_inventory = []
rep_wage = []
rep_price = []
rep_hh_m = []
rep_hh_div = []
rep_hh_w = []
rep_hh_e = []
rep_hh_emp = []
for mo in range(nMonths):
    if mo>3:
        temp = federal_government(mo, total_employment, total_production, total_liquidity, list_BA, list_HH, list_FI, r)
        temp = list(temp)
        r, list_BA, list_HH, list_FI = temp[0], temp[1], temp[2], temp[3]
    else:
        r=.1
    temp = []
    temp = bank_risk_metric(list_HH, list_FI, list_BA)
    temp = list(temp)
    list_FI, list_HH, list_BA = temp[0], temp[1], temp[2]
    temp = []
    if mo>3:
        temp = update_loan_offer(list_HH, list_FI)
        temp = list(temp)
        list_HH, list_FI = temp[0], temp[1]
    list_FI = update_labour_price(list_FI)
    #print('labour_price is updated!')
    temp = update_price(list_HH, list_FI, A_df)
    temp = list(temp)
    list_FI, list_HH, A_df = temp[0], temp[1], temp[2]
    #temp = []
    temp = update_typeA_quant(list_HH, list_FI, A_df, A_df_constraints)
    #print('typeA quantity is updated!')
    temp = list(temp)
    list_FI, list_HH, A_df = temp[0], temp[1], temp[2]
    #temp = []
    A_df_constraints = pd.DataFrame(0, index = np.arange(H), columns = np.arange(F))
    temp = updateTypeB(list_HH, list_FI, B_df)
    #print('typeB relations are updated!')
    temp = list(temp)
    list_FI, list_HH, B_df = temp[0], temp[1], temp[2]
    #print(list_FI)
    #print(list_HH)
    #print('typeB relations are: /n', B_df)
    #print('typeA relations are: /n',A_df)
    temp = []
    list_HH = update_average_price(list_FI, list_HH)
    #print('average prices are updated!')
    list_HH = hh_consumption_update(list_HH)
    #print('hh consumption is updated!')
    for day in range(nDays):
        #print(f'day {day} starts!')
        temp = goodmarketdailyevent(list_HH, list_FI, A_df_constraints)
        temp = list(temp)
        list_FI, list_HH, A_df_constraints = temp[0], temp[1], temp[2]
        list_FI = produce(list_FI)
        #print(f'day {day} is over!')
        temp = []
    temp = payback_deposit(list_FI, list_HH, list_BA, DC_df, DR_df)
    temp = list(temp)
    list_FI, list_HH, list_BA, DR_df, DC_df = temp[0], temp[1], temp[2], temp[3], temp[4]
    temp = []
    temp = borrowing(list_FI, list_HH, list_BA, r, CR_df, CC_df)
    temp = list(temp)
    list_FI, list_HH, list_BA, CR_df, CC_df = temp[0], temp[1], temp[2], temp[3], temp[4]
    temp = []
    temp = firm_wage_expense(list_HH, list_FI)
    #print('wages are paid!')
    temp = list(temp)
    list_FI, list_HH = temp[0], temp[1]
    temp = []
    temp = payback_loan(list_FI, list_HH, list_BA, CR_df, CC_df)
    temp = list(temp)
    list_FI, list_HH, list_BA, CR_df, CC_df=temp[0], temp[1], temp[2], temp[3], temp[4]
    temp = firm_dividend_expense(list_HH, list_FI)
    #print('firms paid dividend proceeds!')
    temp = list(temp)
    list_FI, list_HH = temp[0], temp[1]
    temp = []
    temp = deposit(list_BA, list_HH, list_FI, DR_df, DC_df, r)
    temp = list(temp)
    list_FI, list_HH, list_BA, DR_df, DC_df = temp[0], temp[1], temp[2], temp[3], temp[4]
    temp = []
    '''
    if mo %2 == 0:
        temp = payback_deposit(list_FI, list_HH, list_BA, DC_df, DR_df)
        temp = list(temp)
        list_FI, list_HH, list_BA, DR_df, DC_df = temp[0], temp[1], temp[2], temp[3], temp[4]
    '''
    #summary stats
    rep_firm = list_FI[7]
    rep_house = list_HH[3]
    rep_liquidity.append(rep_firm['m'])
    rep_inventory.append(rep_firm['inv'])
    rep_wage.append(rep_firm['w'])
    rep_price.append(rep_firm['p'])
    rep_hh_m.append(rep_house['m'])
    rep_hh_div.append(rep_house['dividend'])
    rep_hh_w.append(rep_house['w'])
    rep_hh_e.append(rep_house['employed'])
    rep_hh_emp.append(rep_house['typeB'])
    total_employment.append(get_employment(list_HH))
    total_production.append(quantity_produced(list_FI))
    total_liquidity.append(get_total_liquidity(list_BA))
    interest_rate_movements.append(r)
    total_money_supply.append(get_money_supply(list_BA))
    total_consumption.append(get_hh_consumption(list_HH))
    inflation.append(get_inflation_data(list_HH))
    
    print(mo, get_employment(list_HH), quantity_produced(list_FI), get_total_liquidity(list_BA))
    print('='*40)
    print('='*11, 'MONTH:', mo, 'IS OVER', '='*11)
    print('='*40)
    print(f"====ECONOMY'S_TOTAL_EMPLOYMENT_IS:_{round(total_employment[-1],2)}=")
    print(f'====THE_TOTAL_OUTPUT_IS:___________{total_production[-1]}=')
    print(f'====THE PRICE PER GOOD IS:_________{round(inflation[-1],2)}=')
    print(f'====MONEY SUPPLY IS:_______________{round(total_money_supply[-1],2)}=')
    print(f'====CONSUMPTION IS:________________{round(total_consumption[-1],2)}=')
    print(f'====INTEREST RATE IS:______________{round(interest_rate_movements[-1]*10,2)}=')
    
    print('='*40)
    print('='*11, 'MONTH: ', mo+1, 'BEGINS', '='*11)
    print('='*40)


df = pd.DataFrame({'total_production': total_production,
                   'total_employment': total_employment,
                   'total_money_supply': total_money_supply,
                   'total_consumption': total_consumption,
                   'inflation_data':inflation,
                   'interest_rate':interest_rate_movements,
                   'rep_liquidity': rep_liquidity,
                   'rep_price': rep_price,
                   'rep_inventory':rep_inventory,
                   'rep_hh_liq': rep_hh_m,
                   'rep_hh_div': rep_hh_div,
                   'rep_hh_w': rep_hh_w,
                   'rep_hh_e': rep_hh_e})

df.to_csv('test_output_1_w_banking.csv')
