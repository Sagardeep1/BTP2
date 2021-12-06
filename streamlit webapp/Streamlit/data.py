import random
import datetime
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

def function(time_m: str, blk: str = 'n') -> str:
    """
    Takes any arbitrary minute of of time as an input and returns the starting minute of the block
    Example: 06 -> 00, 17 -> 15, 36 -> 30, 48 -> 45
    """

    if blk == 'p':
        block_region = int(time_m) // 15 + 1
        op = (block_region - 1) * 15
        return str(op) * 2 if 1 == len(str(op)) else str(op)
    else:
        op = str(((int(time_m) // 15 + 1) * 15) % 60)
        return op * 2 if 1 == len(op) else op


def digit_convert(number: int) -> str:
    """
    Takes digit in int form and converts it to two digits (if only one) by adding preceding zero, returns str
    Example: 4 -> '04'
    """
    if len(str(number)) == 1:
        return '0' + str(number)
    else:
        return str(number)


def block_number(n):
    """
    Takes a block number and converts it into a block between 1 and 96
    Example: converts block 97 to block 1
    """
    if n > 96:
        return n % 96
    else:
        return n


# Defines the seed input for random functions (for 15 minute values)
def function_seed(blk_no, day, mon):
    return (96 * 96) * blk_no + 96 * day + mon


# Defines the seed input for random functions (for 1 day values)
def function_seed_day(day, mon):
    return 32 * day + mon


# Take frequency as input and output the deviation rate
def deviation_rate(f):
    if 49.48 <= f <= 50.00:
        return 3.0304
    elif f == 50.01:
        return 2.5063
    elif f == 50.02:
        return 1.8798
    elif f == 50.03:
        return 1.2532
    elif f == 50.04:
        return 0.6266
    else:
        return 0


def ui_dev_charge_calculate(dev, f, rs):
    if dev <= 0 and f >= 49.85:
        return round(rs * dev * f, 2)
    else:
        return 0


def ui_charge_above_and_150_calculate(dev, f, s, a, rs):
    if f >= 49.85 and 0.12 * s <= 150:
        if 0.85 * s <= a < 0.88 * s:
            return round(-1 * 50 * (-dev - 0.12 * s), 2)
        elif 0.8 * s <= a < 0.85 * s:
            return round((-1 * (100 * (-dev - 0.15 * s) + 1.5 * s)) * rs, 2)
        else:
            return round((-1 * (250 * (-dev - 0.2 * s) + 6.5 * s)) * rs, 2)
    else:
        return 0


def ui_dev_charge_above_and_012_calculate(dev, f, s, rs):
    if f >= 49.85 and 0.12 * s > 150:
        if 150 < dev <= 200:
            return round((- 1 * (50 * (- dev - 150)) * rs), 2)
        elif 200 < -dev <= 250:
            return round((- 1 * (100 * (-dev - 200) + 2500) * rs), 2)
        elif -dev > 250:
            return round((- 1 * (250 * (- dev - 250) + 7500)) * rs, 2)
        else:
            return 0
    else:
        return 0


def ui_dev_charge_below_dc_calculate(dev, f, s, a, rs):
    if a <= s and f < 49.85:
        return round(dev * rs * 250, 2)
    else:
        return 0


def ui_dev_charge_below_dc_add_calculate(dev, f, s, a, rs):
    if a <= s and f < 49.85:
        return round(dev * rs * 250, 2)
    else:
        return 0


def oi_dev_charge_calculate(dev, s, a, rs):
    if a > s and dev > 0.12 * s and 0.12 * s < 150:
        return round(0.12 * s * rs * 250, 2)
    elif a > s and dev < s * 0.12 and dev < 150:
        return round(dev * rs * 250, 2)
    elif a > s and 0.12 * s > 150:
        return round(150 * rs * 250, 2)
    elif a > s and 0.12 * s < 150:
        return round(0.12 * s * rs * 250, 2)
    else:
        return 0


def oi_dev_charge_add_calculate(dev, f, s, a):
    if a > s > 400 and f >= 50.1:
        return round(dev * 250 * min(50.03, 0) / 100, 2)
    elif a > s and s <= 400 and f >= 50.1 and dev > 48:
        return round((dev - 48) * 250 * min(50.03, 0) / 100, 2)
    else:
        return 0


def past_deviations_calculate(cur_blk_no):
    """Calculates the deviations for the day till the current block and returns them in an array"""
    op_dev, op_sg, op_ag = [], [], []
    op_block_no = []
    cur_date = str(datetime.date.today())
    cur_day = int(cur_date[-2:])
    cur_mon = int(cur_date[-5:-3])
    i = 1

    while i <= cur_blk_no:
        # # Day change
        # if cur_blk_no == 0:
        #     cur_blk_no = 96
        #     i += 1

        # print("Function Block...")
        # print("Current Block Number: ", i)
        # print("Seed Value:", function_seed(block_number(i), cur_day, cur_mon))

        random.seed(function_seed(i, cur_day, cur_mon))
        s = round(150 + random.random() * 50, 2)
        a = round(150 + random.random() * 50, 2)
        op_dev.append(round(a - s, 2))
        op_sg.append(s)
        op_ag.append(a)
        op_block_no.append(i)
        # print("Current AG:", a, "Current SG:", s, "Current Deviation:", round(a - s, 2), "\n")

        i += 1

    return op_dev, op_sg, op_ag, op_block_no


def continuous_blocks_calculated(dev_array):
    """Takes an array containing the deviations from the 1st block to the current block, then returns the number of
    number of positive or negative continuous blocks"""

    sign = dev_array[-1]
    total = 1

    for i in range(len(dev_array) - 2, -1, -1):
        if sign > 0:
            if dev_array[i] > 0:
                total += 1
            else:
                break
        elif sign < 0:
            if dev_array[i] < 0:
                total += 1
            else:
                break
        else:
            total = 0
            break

    # Positive, Negative
    p, n = 0, 0

    if sign > 0:
        p = total
    elif sign < 0:
        n = total

    return p, n


def alarm_calculation(dev_array):
    """If there is sustained deviation (more than 20MW with reference to schedule) for 11 blocks, raise alarm"""
    # print("Function: Alarm")
    if len(dev_array) < 11:
        return 0, ""
    else:
        sign = dev_array[-1]
        total = 0

        if sign > 20:
            total += 1
            i = 10
            while i >= 1:
                if dev_array[-1 - i] > 20:
                    total += 1
                    i -= 1
                else:
                    break
            if total == 11:
                return 1, "Warning: Sustained Positive Violation for 11 Blocks"
            else:
                return 0, ""

        elif sign < -20:
            total += 1
            i = 10
            while i >= 1:
                if dev_array[-1 - i] < -20:
                    total += 1
                    i -= 1
                else:
                    break
            if total == 11:
                return 1, "Warning: Sustained Negative Violation for 11 Blocks"
            else:
                return 0, ""


def sign_violations_calculate(dev_array):
    """Calculates the sign violations i.e. if deviation continues in one direction for more than 12 blocks,
    it is required to correct it the latest by the 13th block or additional penalties corresponding to the number of
    sign violations is incurred"""

    if len(dev_array) < 13:
        return 0
    else:
        sign = dev_array[-1]
        total = 0

        if sign > 20:
            total += 1
            i = 1
            while i <= len(dev_array) - 1:
                if dev_array[-1 - i] > 20:
                    total += 1
                    i += 1
                else:
                    break
            if total > 12:
                return total - 12
            else:
                return 0

        elif sign < -20:
            total += 1
            i = 1
            while i <= len(dev_array) - 1:
                if dev_array[-1 - i] < -20:
                    total += 1
                    i += 1
                else:
                    break
            if total > 12:
                return total - 12
            else:
                return 0
    return 0

###
t = str(datetime.datetime.now().time())
t_hh, t_mm, t_ss = t[:2], t[3:5], t[6:8]
current_block_place = int(t_mm) // 15 + 1
next_block_place = 1 if current_block_place == 4 else current_block_place + 1

current_block_number = (int(t_hh) * 60 + int(t_mm)) // 15 + 1
current_block_start = t_hh + ":" + digit_convert((int(t_mm) // 15) * 15)
next_block_start = digit_convert(((int(t_hh) + 1) % 24) if current_block_place == 4 else t_hh) + ":" + function(t_mm)
current_block_end = next_block_start
next_block_end = digit_convert(
    (int(next_block_start[:2]) + 1) % 24) + ":" + "00" if next_block_place == 4 else digit_convert(
    int(next_block_start[:2])) + ":" + digit_convert(int(next_block_start[-2:]) + 15)

current_block = current_block_start + "-" + current_block_end
next_block = next_block_start + "-" + next_block_end

###
time_elapsed_mm, time_elapsed_ss = digit_convert(int(t_mm) % 15), digit_convert(int(t_ss))
time_remaining_in_seconds = digit_convert(15 * 60 - (int(time_elapsed_mm) * 60 + int(time_elapsed_ss)))
time_remaining_mm, time_remaining_ss = digit_convert(int(time_remaining_in_seconds) // 60), digit_convert(
    int(time_remaining_in_seconds) % 60)

time_elapsed = time_elapsed_mm + ":" + time_elapsed_ss
time_remaining = time_remaining_mm + ":" + time_remaining_ss

# Date calculation (used in seeding of random functions)
date = str(datetime.date.today())
date_day = int(date[-2:])
date_mon = int(date[-5:-3])

#Randomizing the values as per the specified ranges
random.seed(function_seed(block_number(current_block_number), date_day, date_mon))
# Update in intervals of 15 minutes (1 time block)
sg = round(150 + random.random() * 50, 2)
ag = round(150 + random.random() * 50, 2)
dc = round(150 + random.random() * 50, 2)
frequency = round(49.5 + random.random() * 1.5, 2)
deviation = round(ag - sg, 2)
ag_by_sg_percent = round((ag / sg) * 100, 2)

rupees = deviation_rate(frequency)

# Charges
ui_dev_charge = ui_dev_charge_calculate(deviation, frequency, rupees)
ui_dev_charge_above_and_150 = ui_charge_above_and_150_calculate(deviation, frequency, sg, ag, rupees)
ui_dev_charge_above_and_012 = ui_dev_charge_above_and_012_calculate(deviation, frequency, sg, rupees)
ui_dev_charge_below_dc = ui_dev_charge_below_dc_calculate(deviation, frequency, sg, ag, rupees)
ui_dev_charge_below_dc_add = ui_dev_charge_below_dc_add_calculate(deviation, frequency, sg, ag, rupees)
oi_dev_charge = oi_dev_charge_calculate(deviation, sg, ag, rupees)
oi_dev_charge_add = oi_dev_charge_add_calculate(deviation, frequency, sg, ag)

sum_ui = ui_dev_charge + ui_dev_charge_above_and_150 + ui_dev_charge_above_and_012 + ui_dev_charge_below_dc + ui_dev_charge_below_dc_add
total_charge = sum_ui + oi_dev_charge + oi_dev_charge_add
total_charge_add = ui_dev_charge_above_and_150 + ui_dev_charge_above_and_012 + ui_dev_charge_below_dc_add + oi_dev_charge_add

fuel = round(deviation * 250 * 151.4 / 100 * (-1), 2)
net_gain = round(fuel + total_charge, 2)

#"Previous Block Number and Time"
previous_block_number = 96 if current_block_number == 1 else current_block_number - 1

previous_block_end = current_block_start

# ----
previous_block_start_mm = digit_convert((int(previous_block_end[-2:]) - 15) % 60)
previous_block_start_hh = digit_convert(int(t_hh) - 1) if current_block_place == 1 else t_hh
# ----

previous_block_start = previous_block_start_hh + ":" + previous_block_start_mm

previous_block = previous_block_start + "-" + previous_block_end

#"""Previous Block Data"""
# Same parameters calculated; Added a 'previous_' prefix to differentiate

random.seed(function_seed(current_block_number - 1, date_day, date_mon))
previous_sg = round(150 + random.random() * 50, 2)
previous_ag = round(150 + random.random() * 50, 2)
previous_dc = round(150 + random.random() * 50, 2)
previous_frequency = round(49.5 + random.random() * 1.5, 2)
previous_deviation = round(previous_ag - previous_sg, 2)
previous_ag_by_sg_percent = round((previous_ag / previous_sg) * 100, 2)

# Deviation Rate
previous_rupees = deviation_rate(previous_frequency)

previous_ui_dev_charge = ui_dev_charge_calculate(previous_deviation, previous_frequency, previous_rupees)
previous_oi_dev_charge = oi_dev_charge_calculate(previous_deviation, previous_sg, previous_ag, previous_rupees)

previous_ui_dev_charge_above_and_150 = ui_charge_above_and_150_calculate(previous_deviation, previous_frequency,
                                                                         previous_sg, previous_ag, previous_rupees)
previous_ui_dev_charge_above_and_012 = ui_dev_charge_above_and_012_calculate(previous_deviation, previous_frequency,
                                                                             previous_sg, previous_rupees)

previous_ui_dev_charge_below_dc = ui_dev_charge_below_dc_calculate(previous_deviation, previous_frequency, previous_sg,
                                                                   previous_ag, previous_rupees)

previous_ui_dev_charge_below_dc_add = ui_dev_charge_below_dc_add_calculate(previous_deviation, previous_frequency,
                                                                           previous_sg, previous_ag, previous_rupees)
previous_oi_dev_charge_add = oi_dev_charge_add_calculate(previous_deviation, previous_frequency, previous_sg,
                                                         previous_ag)

previous_sum_ui = previous_ui_dev_charge + previous_ui_dev_charge_above_and_150 + previous_ui_dev_charge_above_and_012 + previous_ui_dev_charge_below_dc + previous_ui_dev_charge_below_dc_add

previous_total_charge = previous_sum_ui + previous_oi_dev_charge + previous_oi_dev_charge_add
previous_total_charge_add = previous_ui_dev_charge_above_and_150 + previous_ui_dev_charge_above_and_012 + previous_ui_dev_charge_below_dc_add + previous_oi_dev_charge_add

previous_fuel = round(previous_deviation * 250 * 151.4 / 100 * (-1), 2)
previous_net_gain = round(previous_fuel + previous_total_charge, 2)

#"""Deviations for Past Blocks (Used to calculate continuous +ve/-ve blocks and sign violations"""
# print("Current Block Number: ", current_block_number)
# print("Seed Value:", function_seed(block_number(current_block_number), date_day, date_mon))
# print("Current AG:", ag, "Current SG:", sg, "Current Deviation:", deviation, "\n")


past_dev_array, plot_y_sg, plot_y_ag, plot_x_blk_no = past_deviations_calculate(current_block_number)
continuous_pos, continuous_neg = continuous_blocks_calculated(past_dev_array)
# print(past_dev_array)
# print("Cont +ve:", continuous_pos, "Cont -ve:", continuous_neg)
alarm, alarm_message = alarm_calculation([past_dev_array])
# print(alarm, alarm_message)
sign_violations = sign_violations_calculate(past_dev_array)

#"""Next Block Data"""
random.seed(function_seed(block_number(current_block_number + 1), date_day, date_mon))
sg_plus_one = round(150 + random.random() * 50, 2)

random.seed(function_seed(block_number(current_block_number + 2), date_day, date_mon))
sg_plus_two = round(150 + random.random() * 50, 2)

random.seed(function_seed(block_number(current_block_number + 3), date_day, date_mon))
sg_plus_three = round(150 + random.random() * 50, 2)

random.seed(function_seed(block_number(current_block_number + 4), date_day, date_mon))
sg_plus_four = round(150 + random.random() * 50, 2)

#"""Updated every 24 hours"""
random.seed(function_seed_day(date_day, date_mon))
fuel_price = round(2 + random.random() * 8, 2)

#"""Machine Learning"""
ml_x_block_number = list(map(float, "1  5  9 13 17 21 25 29 33 37 41 45 49 53 57 61 65 69 73 77 81 85 89 93".split()))
ml_y_predicted_value = list(map(float, "177.59978236 177.30424698 177.20475222 177.27930507 177.50591037 177.8625708  "
                                       "178.32728687 178.87805692 179.49287714 180.14974156 180.82664201 181.50156821 "
                                       "182.15250768 182.75744579 183.29436574 183.74124857 184.07607316 184.27681623 "
                                       "184.32145231 184.18795381 183.85429094 183.29843176 182.49834217 "
                                       "181.4319859".split()))

ml_y_actual_value = list(map(float, "177.48200039 180.15761821 178.08133878 176.91963417 176.22494649 176.07705779 "
                                    "177.19595252 178.35765713 180.01945904 181.64818058 182.94999027 183.90737498 "
                                    "184.63708893 184.98345982 185.53025881 185.68203931 185.76182137 185.7812804  "
                                    "185.20918467 184.55341506 183.38198093 182.73788675 182.62891613 "
                                    "181.36018681".split()))

#new_title = '<span style="font-family:sans-serif; color:Green; font-size: 20px;">New image: </span>'
#st.write(new_title, t_mm,unsafe_allow_html=True)


#Display part
st.header('POWER PLANT WEB APPLICATION')

data = [['Current Blk No.', str(current_block_number)], ['BLK. Time', str(current_block)], ['Time Elapsed (mm:ss)', time_elapsed],
['Time Remaining (mm:ss)', str(time_remaining)], ['Inst. BLK. Hz', str(frequency)], ['Avg. BLK. Hz', str(frequency-0.05)],
['FUEL RATE', str(fuel_price)], ['B.E.F', str(rupees)]]
  
# Create the pandas DataFrame
df = pd.DataFrame(data, columns = ['Parameters', 'Values'])

def color_negative_red(value):
  color = 'green'
  return 'color: %s' % color  
# print dataframe.

st.dataframe(df.style.applymap(color_negative_red, subset=['Values']))

col1, col2, col3, col4 = st.columns(4)

### Previous Block Data ###
if col1.button("PREVIOUS BLOCK DATA"):
    st.subheader('PREVIOUS BLOCK DATA')
    data = [['Block No.', str(previous_block_number)], ['Block Time', str(previous_block)], ['DC (MW)', str(previous_dc)],
    ['SG (MW)', str(previous_sg)], ['AG/SG %', str(previous_ag_by_sg_percent)], ['Avg. Hz', str(previous_frequency)],
    ['Dev. MW', str(previous_deviation)], ['Dev. Rate', str(0)], ['Dev. (Rs.)', str(previous_rupees)], ['Addi. Dev.(Rs.)', str(0)], 
    ['Total Dev.', str(previous_sum_ui)], ['Fuel Cost(Rs.)', str(previous_fuel)], ['Net Gain(Rs.)', str(previous_net_gain)]]
    
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns = ['Parameters', 'Values'])
    def color_negative_red1(value):
        if value == "Fuel Cost(Rs.)":
            color ='red'
        elif value == "Block No." or value == "Block Time":
            color = 'white'
        elif value == "Avg. Hz":
            color = 'pink'
        elif value == "Dev. MW" or value == "Dev. Rate":
            color = 'orange'
        elif value == "Dev. (Rs.)":
            color = 'green'
        else:
            color = 'yellow'

        return 'color: %s' % color  
    st.dataframe(df.style.applymap(color_negative_red1, subset=['Parameters']))


### Current Block Data ###
if col2.button("CURRENT BLOCK DATA"):
    st.subheader('CURRENT BLOCK DATA')
    data = [['Block No.', str(current_block_number)], ['Block Time', str(current_block)], ['DC (MW)', str(dc)],
    ['SG (MW)', str(sg)], ['AG/SG %', str(ag_by_sg_percent)], ['Avg. Hz', str(frequency)],
    ['Dev. MW', str(deviation)], ['Dev. Rate', str(0)], ['Dev. (Rs.)', str(rupees)], ['Addi. Dev.(Rs.)', str(0)], 
    ['Total Dev.', str(sum_ui)], ['Fuel Cost(Rs.)', str(fuel)], ['Net Gain(Rs.)', str(net_gain)], ['Cont. +ve blocks', str(continuous_pos)],
    ['Cont. -ve blocks', str(continuous_neg)], ['Sign Violations', str(sign_violations)]]
    
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns = ['Parameters', 'Values'])
    def color_negative_red1(value):
        if value == "Fuel Cost(Rs.)":
            color ='red'
        elif value == "Block No." or value == "Block Time":
            color = 'white'
        elif value == "Avg. Hz":
            color = 'pink'
        elif value == "Dev. MW" or value == "Dev. Rate":
            color = 'orange'
        elif value == "Dev. (Rs.)":
            color = 'green'
        else:
            color = 'yellow'

        return 'color: %s' % color
    st.dataframe(df.style.applymap(color_negative_red1, subset=['Parameters']))


### SG values ###
if col3.button("NEXT BLOCKS SG VALUES"):
    st.subheader('NEXT SG VALUES')
    data = [['S1', str(sg_plus_one)], ['S2', str(sg_plus_two)], ['S3', str(sg_plus_three)], ['S4', str(sg_plus_four)]]
    
    # Create the pandas DataFrame
    df = pd.DataFrame(data, columns = ['Parameters', 'Values'])
    def color_negative_red1(value):
        if value == "S1":
            color ='red'
        elif value == "S2":
            color = 'orange'
        elif value == "S3":
            color = 'green'
        else:
            color = 'yellow'

        return 'color: %s' % color
    st.dataframe(df.style.applymap(color_negative_red1, subset=['Parameters']))

#Plotting Functions
if col4.button("PLOT ENERGY GENERATION DATA"):
    image = Image.open('plot_btp.jpg')
    st.image(image, caption='Actual Data along with predicted model data')