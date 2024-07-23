import random
import numpy as np
import pandas as pd
from multiprocessing import Pool
import itertools


# Function to reset the simulation for a new cycle
def restartsim(
        staff_pool, staffpershift1, staffpershift2, staffpershift3, shift_day):
    # Staffs are assigned numbers ranging from 0 to staff_pool
    # staff_pool = total number of staffs
    # staffpershift1 = number of staffs in the 1st shift
    # staffpershift2 = number of staffs in the 2nd shift (40% of the 1st shift)
    # staffpershift3 = number of staffs in the 3rd shift (40% of the 1st shift)
    # shift_day = number of shifts per day

    # roster = a data frame to store the roster, with 21 rows, each row showing the staff for the day
    # The columns in roster dataframe shows the staffs in each shift: shift number - staff slot number
    # e.g.: Shift1-2 is the 2nd staff slot for the 1st shift
    # e.g.: Shift2-3 is the 3rd staff slot for the 2nd shift
    # Depending on number of shifts per day, may need one, two or three shifts in roster
    roster = pd.DataFrame(index=range(0,21),columns=['Shift1-'+str(i) for i in range(0,staffpershift1)])
    if shift_day >= 2:
        for i in range (0, staffpershift2):
            roster['Shift2-'+str(i)] = 0
    if shift_day == 3:
        for i in range (0, staffpershift3):
            roster['Shift3-'+str(i)] = 0

    # Create a staff list with 3 columns,
    # 'infected' column shows if the staff is infected: 0 = susceptible; 1 = infected
    # 'rest' column shows if the staff is resting after working shift (won't be select for roster): 0 = not resting, 1 = resting;
    # 'ref' column is a reference column with value set to 0.
    stafflist = pd.DataFrame(index=range(0,staff_pool),columns=['infected','rest','ref'])
    stafflist.loc[0:staff_pool, 'infected']=0
    stafflist.loc[0:staff_pool, 'rest']=0
    stafflist.loc[0:staff_pool, 'ref']=0
    return stafflist,roster


# Function to fill up the roster with staff number; ensure that the staffs rest for a minimal period after working a shift
def fillroster1(staff_pool, f, Nday, stafflist, roster):
    # staff_pool = total number of staffs
    # f = shift change frequency/interval
    # Nday = total number of staff for 1 day
    # stafflist = dataframe showing which staff are infected and resting, and with a reference column
    # roster = data frame with 21 rows, each showing the staff for the day

    # num_cycle = number of shift rotation over the 21 days of simulation;
    num_cycle = int(21/f)

    # Special handling for f = 14 as 21 is not a multiple of 14.
    if f == 14:
        temp = random.sample(stafflist[stafflist.loc[:,'rest']==0].index.values.tolist(),k=Nday)
        for j in range(0,f):
            roster.iloc[j] = temp
        stafflist.loc[temp,'rest']=1
        temp = random.sample(stafflist[stafflist.loc[:,'rest']==0].index.values.tolist(),k=Nday)
        for j in range(f,21):
            roster.iloc[j] = temp

    # For other f values, fill up the roster by randomly drawing Nday non-resting staffs from the staff list
    else:
        for i in range (0,num_cycle):
            temp = random.sample(stafflist[stafflist.loc[:,'rest']==0].index.values.tolist(),k=Nday)
            for j in range(0,f):
                roster.iloc[f*i+j] = temp
            stafflist['rest']=stafflist['rest']-1
            stafflist['rest']=stafflist[['rest','ref']].max(axis=1)
            stafflist.loc[temp,'rest']=1


# Function to model probabilistic transmission via contact within lab
def contact(p, c1, c2, c3, day, staffpershift1, staffpershift2,
            staffpershift3, stafflist, roster, shift_day):
    # p = probability of disease transmission
    # c1,c2,c3 = contact rate for shift 1,2 and 3 respectively
    # day = number of days after the simulation start
    # staffpershift1 = number of staffs in the 1st shift
    # staffpershift2 = number of staffs in the 2nd shift (40% of the 1st shift)
    # staffpershift3 = number of staffs in the 3rd shift (40% of the 1st shift)
    # stafflist = dataframe showing which staff are infected and resting, and with a reference column
    # roster = data frame with 21 rows, each showing the staff for the day
    # shift_day = number of shifts per day

    # To determine which staff is in 1st shift
    staff_in_shift = roster.loc[day,['Shift1-'+str(i) for i in range(0,staffpershift1)]]

    # Form a dataframe with it
    staff_in_shift_df = stafflist.iloc[list(staff_in_shift)]

    # For Shift 1:
    # If there is at least 1 infected staff
    if stafflist['infected'][staff_in_shift].sum()>0:
        # identify staffs who are infected
        staff_I = staff_in_shift_df[staff_in_shift_df['infected']==1]
        # identify staffs who are susceptible
        staff_S = staff_in_shift_df[staff_in_shift_df['infected']==0]

        for j in list(staff_I.index):
            # The number of successful contact per infected staff, k is determined by Poisson distribution
            contact.n_infected = min(np.random.poisson(lam=p*c1, size=1),[len(staff_in_shift)-1])

            # Randomly select k staff from those working in the same shift
            staff_infected = random.sample(list(staff_S.index)+list(staff_I[staff_I.index != j].index),k=contact.n_infected[0])
            for i in range(0,len(staff_infected)):
                stafflist['infected'][staff_infected[i]]=1

    if shift_day >= 2:
        # For Shift 2: repeating the same infectious process in Shift 1
        staff_in_shift = roster.loc[day,['Shift2-'+str(i) for i in range(0,staffpershift2)]]
        staff_in_shift_df = stafflist.iloc[list(staff_in_shift)]

        if stafflist['infected'][staff_in_shift].sum()>0:
            staff_I = staff_in_shift_df[staff_in_shift_df['infected']==1]
            staff_S = staff_in_shift_df[staff_in_shift_df['infected']==0]

            for j in list(staff_I.index):
                contact.n_infected = min(np.random.poisson(lam=p*c2, size=1),[len(staff_in_shift)-1])
                staff_infected = random.sample(list(staff_S.index)+list(staff_I[staff_I.index != j].index),k=contact.n_infected[0])
                for i in range(0,len(staff_infected)):
                    stafflist['infected'][staff_infected[i]]=1

    if shift_day == 3:
        # For Shift 3: repeating the same infectious process in Shift 1
        staff_in_shift = roster.loc[day,['Shift3-'+str(i) for i in range(0,staffpershift3)]]
        staff_in_shift_df = stafflist.iloc[list(staff_in_shift)]

        if stafflist['infected'][staff_in_shift].sum()>0:
            staff_I = staff_in_shift_df[staff_in_shift_df['infected']==1]
            staff_S = staff_in_shift_df[staff_in_shift_df['infected']==0]

            for j in list(staff_I.index):
                contact.n_infected = min(np.random.poisson(lam=p*c3, size=1),[len(staff_in_shift)-1])
                staff_infected = random.sample(list(staff_S.index)+list(staff_I[staff_I.index != j].index),k=contact.n_infected[0])
                for i in range(0,len(staff_infected)):
                    stafflist['infected'][staff_infected[i]]=1


def run_model(
        staff_strength, f, staffpershift1, shift_day, secondary_attack_rate):
    '''
    Run the COVID-19 simulation model for a single given set of parameters.

    Parameters:
    ----------
    staff_strength : list
        Staff strength
    f : list
        Frequency of staff change
    staffpershift1 : list
        Number of staff per shift
    shift_day : list
        Number of shifts per day
    secondary_attack_rate : number between 0 and 1
        Probability of COVID-19 transmission through contact between an
        infected staff and susceptible staff
    Returns:
    --------
    res : dictionary
        Contains the model parameters and results from end of day 7, 14 and 21
    '''
    # Set result to NA if the input is strength 2 and more than 1 shift per day
    if (staff_strength == 2 and shift_day > 1):
        res = {'strength': staff_strength,
               'change': f,
               'shift': staffpershift1,
               'shift_day': shift_day,
               'day7': np.nan,
               'day14': np.nan,
               'day21': np.nan}
    # Otherwise, run the model...
    else:
        result = pd.DataFrame(index=range(0, 100),
                              columns=[str(i) for i in range(0, 22)])
        staffpershift2 = int(staffpershift1*0.4)
        staffpershift3 = int(staffpershift1*0.4)
        staff_pool = staffpershift1*staff_strength

        # Adjust Nday depending on whether it is 1, 2 or 3 shifts per day
        if shift_day == 1:
            Nday = staffpershift1
        elif shift_day == 2:
            Nday = staffpershift1 + staffpershift2
        elif shift_day == 3:
            Nday = staffpershift1 + staffpershift2 + staffpershift3

        p = secondary_attack_rate
        c1 = 0.40*staffpershift1  # number of contact for shift 1
        c2 = 0.40*staffpershift2  # number of contact for shift 2
        c3 = 0.40*staffpershift3  # number of contact for shift 3

        #  n = number of cycle for the same simulation param
        for n in range(0, 100):
            # Call the function to reset simulation
            stafflist, roster = restartsim(staff_pool, staffpershift1,
                                           staffpershift2, staffpershift3,
                                           shift_day)

            # Call the function to fill the staff roster
            fillroster1(staff_pool, f, Nday, stafflist, roster)

            # Let the 1st person in the roster be infected;
            stafflist['infected'][roster.iloc[0][0]] = 1

            # Run the simulation for 21 days
            for day in range(0, 21):
                contact(p, c1, c2, c3, day, staffpershift1, staffpershift2,
                        staffpershift3, stafflist, roster, shift_day)
                result[str(day)][n] = stafflist['infected'].sum()/staff_pool

            # Store results in a dictionary
            res = {'strength': staff_strength,
                   'change': f,
                   'shift': staffpershift1,
                   'shift_day': shift_day,
                   'day7': result.median()[6],
                   'day14': result.median()[13],
                   'day21': result.median()[20]}

    # Print that this simulation is done, to help with monitoring progress
    print_param = ['shift_day', 'strength', 'change', 'shift']
    print(f'Finished simulation {[res.get(p) for p in print_param]}')
    return res


def run_scenarios(strength=[2, 4, 6],
                  staff_change=[1, 3, 7, 14, 21],
                  staff_shift=[5, 10, 20, 30],
                  shift_day=[1, 2, 3],
                  secondary_attack_rate=0.15):
    '''
    Run the COVID-19 simulation model with a range of scenarios, with
    parallel processing to improve run time.

    Parameters:
    ----------
    strength : list
        Staff strength
    staff_change : list
        Frequency of staff change
    staff_shift : list
        Number of staff per shift
    shift_day : list
        Number of shifts per day
    secondary_attack_rate : number between 0 and 1
        Probability of COVID-19 transmission through contact between an
        infected staff and susceptible staff

    Returns:
    --------
    res : dataframe
        Dataframe with results from all the varying model parameters
    '''
    # Generate list of tuples with every possible combination of parameters
    paramlist = list(itertools.product(
        strength, staff_change, staff_shift, shift_day))
    # Append the other parameter required by the model
    paramlist = [list(tup) + [secondary_attack_rate] for tup in paramlist]

    # Create a process pool that uses all the CPUs and apply the function
    # This runs the model through all the scenarios using parallel processing
    with Pool() as pool:
        resultlist = pool.starmap(run_model, paramlist)

    # Convert list into dataframe with row for each result
    res = pd.melt(pd.DataFrame(resultlist),
                  id_vars=['strength', 'change', 'shift', 'shift_day'],
                  var_name='end_of_day', value_name='prop_infected')

    # Strip 'day' from the end_of_day column (so just left with 7, 14, 21)
    res['end_of_day'] = pd.to_numeric(res['end_of_day'].str.replace('day', ''))

    return res
