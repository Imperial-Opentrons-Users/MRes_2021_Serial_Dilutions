#!/usr/bin/env python
# coding: utf-8

# In[2]:


from opentrons import protocol_api


metadata = {'apiLevel': '2.8'}
# protocol = simulate.get_protocol_api('2.8')

def run(protocol: protocol_api.ProtocolContext):
    # Loading labware
    tiprack1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat',3)
    left = protocol.load_instrument(
            'p300_multi_gen2', 'left', tip_racks=[tiprack1])
    Reservoir = protocol.load_labware('nest_12_reservoir_15ml',6)# Load a pre-prepared reservoir which contains the manually loaded stock solution and PBS in A1 and A2 well respectively 

    ## 1. Transfer of PBS 

    # Creating a list of destination wells for distribution of the PBS solution 
    positions = [] 
    for i in range (2,13): 
        positions.append("A"+str(i))

    # Pick up tips on the right side of the tip rack for time and distance optimisation     
    left.pick_up_tip(tiprack1['A12']) 
    left.distribute(100,Reservoir['A2'], [plate.wells_by_name()[well_name] for well_name in positions],touch_tip=True,new_tip='never')

            # Blowing out at current location to ensure every drop of solution has been dispensed (for accuracy)
            # Touch tip at current wells to ensure no droplets are attached to the pipette tip
            # (To avoid contamination as the pipette moves across the deck to refill on PBS)

    # Drop the tips as we go on to transfer the stock solution 
    left.drop_tip() 

    ## 2. Transfer of stock solution 

    # Pick up tips available on the right side of the tip rack for time optimisation
    left.pick_up_tip(tiprack1['A11']) 

    # Aspirate 200 ul of the stock solution (in column 1) from the reservoir
    left.aspirate(200, Reservoir['A1']) 

    # Dispense this PBS into column 1 of the plate
    left.dispense(200, plate['A1'])
    left.blow_out()
    left.touch_tip()

    # Transfer 100 ul of solution from the wells in current column (column i) to the adjacent one (column i + 1)
    # There are 10 dilutions to be performed, totalling at 11 concentrations, with the last well as negative control( PBS only)
    for i in range (1, 11):  
        start = "A" + str(i)
        end = "A" + str(i + 1)
        left.transfer(100, plate[start], plate[end], mix_after=(3, 100), touch_tip=True, blow_out=True, blowout_location='destination well', new_tip='never')

    # Ensuring the last well in the serial dilution protocol has the same volume as the other wells, avoiding biased fluorescent output
    #Dropping the tip and disposing of the last 100 uL of serial diluted solution
    left.aspirate(100, plate['A11'])
    left.drop_tip()






