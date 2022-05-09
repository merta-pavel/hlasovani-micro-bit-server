#Server
radio.set_group(69)
radio.set_transmit_power(7)
radio.set_transmit_serial_number(True)

my_serial_number = control.device_serial_number()
zmena_hlasovani = False
hlasovani = True
print(my_serial_number)

votes = {}

#přijatí zprávy
def on_received_value(name, value):
    global votes
    serial_number = radio.received_packet(RadioPacketProperty.SERIAL_NUMBER)

    if name == "vote" and hlasovani == True:
        if zmena_hlasovani == True:
            votes[serial_number] = value
            radio.send_value("success", int(str(serial_number) + "1"))
        else:
            if not(serial_number in votes):
                votes[serial_number] = value
                radio.send_value("success", int(str(serial_number) + "1"))
            else:
                radio.send_value("success", int(str(serial_number) + "0"))
    elif name == "vote" and hlasovani == False:
        radio.send_value("success",  int(str(serial_number) + "0"))

#zobrazení hlasů
def on_logo_event_pressed():
    print(votes)

#povolit/zakázat změnu hlasování
def on_button_pressed_b():
    global zmena_hlasovani
    if zmena_hlasovani == False:
        zmena_hlasovani = True
    else:
        zmena_hlasovani = False

#povolit/zakázat hlasování
def on_button_pressed_a():
    global hlasovani
    if hlasovani == False:
        hlasovani = True
        radio.send_value("toggle", 1)
    else:
        hlasovani = False
        radio.send_value("toggle", 0)

#vymazání hlasů
def on_pin_pressed_p2():
    votes.pop()

input.on_pin_pressed(TouchPin.P2, on_pin_pressed_p2)
input.on_button_pressed(Button.B, on_button_pressed_b)
input.on_logo_event(TouchButtonEvent.PRESSED, on_logo_event_pressed)
radio.on_received_value(on_received_value)
