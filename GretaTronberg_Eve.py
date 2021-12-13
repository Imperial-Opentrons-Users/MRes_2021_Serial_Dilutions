#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from opentrons import protocol_api

metadata = {
    'protocolName':'Protocol',
    'author':'WillCathal <example@gmail.com>',
    'description':'Cathal and Wills Opentrons adventure',
    'apiLevel': '2.8'}

def run(protocol: protocol_api.ProtocolContext):


    #labware
    plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 3)
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    tiprack_2 = protocol.load_labware('opentrons_96_tiprack_300ul', 4)
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack_1])
    p20 = protocol.load_instrument('p20_single_gen2', 'right', tip_racks=[tiprack_1])

    reservoir = protocol.load_labware('4ti0131_12_reservoir_21000ul', 2) #changed the name of the
    #A1 row of the reservoir is flourescein
    #A2 row is PBS

    #commands

    #load 100ul f-lacein in well 1
 
    p300.pick_up_tip()
    p300.aspirate(100,reservoir['A1']) #Aspirate Flourescein
    p300.dispense(100, plate['A1'])
    p300.drop_tip()


    #load 100ul PBS in rest of wells
    #PBS into all wells #range of A3 to A12
    p300.pick_up_tip()
    wells = ['A2', 'A3','A4','A5','A6','A7' ,'A8' ,'A9', 'A10', 'A11', 'A12']
    for i in wells: 
        p300.aspirate(100, reservoir['A2'])
        p300.dispense(100, plate[i])
    p300.drop_tip()

    #load 100ul f-lacein in well 2

    p300.pick_up_tip()
    p300.aspirate(100,reservoir['A1']) #Aspirate Flourescein
    p300.dispense(100, plate['A2'])
    p300.drop_tip()

    #serially dilute
    p300.transfer(100, plate.wells('A2','A3','A4','A5','A6','A7','A8','A9','A10'), plate.wells('A3','A4','A5','A6','A7','A8','A9','A10', 'A11'), mix_after=(3, 50))

    #remove 100uL from last well and trash tip 
    p300.pick_up_tip()
    p300.aspirate(100, plate['A11'])
    p300.dispense(100, reservoir['A3'])
    p300.drop_tip()

