#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from opentrons import protocol_api
metadata = {'apiLevel': '2.8'}

def run(protocol:protocol_api.ProtocolContext):
    #Labware
    tiprack = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    reservoir = protocol.load_labware('usascientific_12_reservoir_22ml', 2) # A1 fluorescein, A2 PBS
    plate = protocol.load_labware('corning_96_wellplate_360ul_flat', 3)
    #pipettes
    p300 = protocol.load_instrument('p300_multi_gen2', 'right', tip_racks=[tiprack])
    protocol.max_speeds['Z'] = 10

    # 6. Add 200 μlL of fluorescein 1X stock solution into A1, B1, C1, D1
    p300.transfer(200, reservoir['A1'], plate['A1'], blow_out=True, blowout_location='destination well') 

    # 5. Add 100 μL of 1X PBS into wells A2, B2, C2, D2....A12, B12, C12, D12
    p300.pick_up_tip()
    for i in range(11):
        p300.transfer(100, reservoir['A2'], plate[f"A{i+2}"], new_tip='never') 
    p300.drop_tip()

    # 7. Transfer 100 μL of fluorescein stock solution from A1 into A2
    # 8. Mix A2 by pipetting up and down 3x and transfer 100 μL into A3
    # ......
    # 16. Mix A10 by pipetting up and down 3x and transfer 100 μL into A11
    p300.pick_up_tip()
    for i in range(10):
        p300.transfer(100, plate[f'A{i+1}'], plate[f'A{i+2}'], mix_after=(3,50), new_tip='never')

    # 17. Mix A11 by pipetting up and down 3x and transfer 100 μLl into liquid waste
    p300.aspirate(100,plate['A1'])
    p300.drop_tip()

