#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from opentrons import protocol_api

metadata = {'apiLevel': '2.7'}

def run(protocol: protocol_api.ProtocolContext):
    plate = protocol.load_labware("costar3370flatbottomtransparent_96_wellplate_200ul", "1")
    tiprack_1 = protocol.load_labware("opentrons_96_tiprack_300ul", "2")
    reservoir = protocol.load_labware("4ti0131_12_reservoir_21000ul", "3")
    p300 = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tiprack_1])

    p300.transfer(200, reservoir.wells("A1"), plate.wells("A1"), new_tip = "once")
    
    p300.pick_up_tip()
    for i in range(1,11):
        p300.distribute(100, reservoir.wells("A2"), plate.columns()[i], new_tip = "never")
    p300.drop_tip()

    p300.pick_up_tip()
    for i in range(0,11):
        j = i+1
        p300.transfer(100, plate.columns()[i], plate.columns()[j], mix_after=(3, 75, 0.5), new_tip = "never")
    p300.drop_tip()

