#!/usr/bin/env python
# coding: utf-8

# In[ ]:


''' Opentrons Setup

    A 12-well reservoir is placed in position 1
        - this code uses '4ti0131_12_reservoir_21000ul', this is the 12-well reservoir available in the lab
        - A1 is filled with PBS, minimum volume needed is 9.6 ml
          because we are filling all 96 wells with 100 ul
        - A2 is filled with Protein, minimum volume needed is 1.6 ml
          because we fill the first column (8 wells) with 200 ul
        - A12 is used as trash in the serial dilutions

    A 96-well plate is placed in position 2
        - this code uses 'costar3370flatbottomtransparent_96_wellplate_200ul', this is the 96-well plate available in the lab

    A 96-tip_rack is placed in position 3
        - this code uses 'opentrons_96_tiprack_300ul', adapt the code
          to specify the tip rack available in the lab

        '''


from opentrons import protocol_api

metadata = {'apiLevel': '2.11'}
#protocol = .get_protocol_api('2.8')
def run(protocol: protocol_api.ProtocolContext):
    #Labware
    reservoir = protocol.load_labware('4ti0131_12_reservoir_21000ul', 1)
    plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 2)
    trash = reservoir.columns()[-1]
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 3)

    #pipette with 8-channels
    '''Because there is only one motor in a multi-channel pipette, multi-channel pipettes will always aspirate and dispense on all channels simultaneously.'''
    p300 = protocol.load_instrument('p300_multi_gen2', 'left', tip_racks=[tiprack_1])


    # Add PBS
    p300.pick_up_tip(tiprack_1['A1'])
    for i in range(2,13): #1,2, ..., 12
        p300.transfer(100, reservoir['A1'], plate['A'+str(i)], new_tip='never')

    # Add Protein
    p300.drop_tip()
    p300.transfer(200, reservoir['A2'], plate['A1'], new_tip='once')


    # Serial Dilutions
    p300.pick_up_tip(tiprack_1['A3'])

    for i in range(1, 12):
        init_well = 'A' + str(i)
        next_well = 'A' + str(i+1)

        if init_well == 'A11':
            p300.transfer(100, plate[init_well], dest=trash, mix_before=(3,50), touch_tip=False, blow_out=True,
                      blowout_location='trash', new_tip='never')
        else:
            p300.transfer(100, plate[init_well], plate[next_well], mix_before=(3,50), touch_tip=False, blow_out=True,
                          blowout_location='destination well', new_tip='never')

    p300.drop_tip()
        
    for line in protocol.commands():
            print('\n')
            print(line)


# In[ ]:




