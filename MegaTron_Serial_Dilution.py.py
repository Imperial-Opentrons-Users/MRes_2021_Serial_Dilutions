#!/usr/bin/env python
# coding: utf-8

from opentrons import protocol_api

# metadata
metadata = {
    'protocolName': 'iGEM Fluorescence v1',
    'author': 'MegaTron – Team 1',
    'description': 'Test',
    'apiLevel': '2.11'
}

# protocol run function. the part after the colon lets your editor know
# where to look for autocomplete suggestions

def run(protocol: protocol_api.ProtocolContext):
	#Define labware
    plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul',
                                   3) #it points to a definition file of the plasticware
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 1)
    reservoir = protocol.load_labware('4ti0131_12_reservoir_21000ul', 2)

    # Pipettes
    p300 = protocol.load_instrument('p300_multi_gen2',  'left', tip_racks=[tiprack_1])

    # Pipette buffer from column 1 in reservoir to columns 2 to 12 in the plate
    p300.transfer(100, reservoir.columns()[0], plate.columns()[1:12],
                  touch_tip=False,
                  blow_out=True,
                  blowout_location='destination well',
                  new_tip='once')

    #Pipette initial of fluorescein into first column
    p300.pick_up_tip()
    p300.transfer(200, reservoir.columns()[1], plate.columns()[0],
                 mix_before=(3,150), # making sure fluoro is well mixed before starting dilution
                 touch_tip=False,
                 blow_out=True,
                 blowout_location='destination well',
                 new_tip='never')

    #Serial dilution
    p300.transfer(100, plate.columns()[0:10], plate.columns()[1:11],
                 mix_after=(3,150), #three times, 150 uL each time
                 touch_tip=False,
                 blow_out=True,
                 blowout_location='destination well',
                 new_tip='never')

    #Pick up 100 uL from Column 11, discard
    p300.transfer(100, plate.columns()[10], reservoir.columns()[11],
                  touch_tip=False,
                  blow_out=True,
                  blowout_location='destination well',
                  new_tip='never')

    p300.drop_tip()
