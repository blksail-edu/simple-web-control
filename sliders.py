import gradio as gr
from motor_test import test_motor
from threading import Thread, Event
import queue
import time
from pymavlink import mavutil


global motor_values
motor_values = [0, 0, 0, 0, 0, 0]
run_thread = Event()
run_thread.set()


def arm_rov(mav_connection):
    mav_connection.arducopter_arm()
    print("Waiting for the vehicle to arm")
    mav_connection.motors_armed_wait()
    print("Armed!")


def disarm_rov(mav_connection):
    mav_connection.arducopter_disarm()
    print("Waiting for the vehicle to disarm")
    mav_connection.motors_disarmed_wait()
    print("Disarmed!")


def stop_all():
    global motor_values
    motor_values = [0, 0, 0, 0, 0, 0]


def update_m1(x, state):
    global motor_values
    motor_values[0] = x


def update_m2(x, state):
    global motor_values
    motor_values[1] = x


# write m3 until m6
def update_m3(x, state):
    global motor_values
    motor_values[2] = x


def update_m4(x, state):
    global motor_values
    motor_values[3] = x


def update_m5(x, state):
    global motor_values
    motor_values[4] = x


def update_m6(x, state):
    global motor_values
    motor_values[5] = x


# run threaded while loop, with an async queue to send commands to the drone
# the queue will be filled by the gradio sliders
# the while loop will run until the queue is empty
def call_motors(mav_connection):
    while run_thread.is_set():
        for i in range(len(motor_values)):
            test_motor(mav_connection=mav_connection, motor_id=i, power=motor_values[i])
            pass
        time.sleep(0.2)
        # print confirmation in purple
        # print("\033[95m" + "Motor values sent to drone: " + str(motor_values) + "\033[0m")


with gr.Blocks() as demo:
    slider_m1 = gr.Slider(-100, 100, step=1, value=0, label="Motor 1")
    slider_m2 = gr.Slider(-100, 100, step=1, value=0, label="Motor 2")
    slider_m3 = gr.Slider(-100, 100, step=1, value=0, label="Motor 3")
    slider_m4 = gr.Slider(-100, 100, step=1, value=0, label="Motor 4")
    slider_m5 = gr.Slider(-100, 100, step=1, value=0, label="Motor 5")
    slider_m6 = gr.Slider(-100, 100, step=1, value=0, label="Motor 6")

    state = gr.State(value=0)

    sliders = [slider_m1, slider_m2, slider_m3, slider_m4, slider_m5, slider_m6]
    slider_m1.release(
        update_m1, inputs=[slider_m1, state], outputs=[], api_name="m1_slider"
    )
    slider_m2.release(
        update_m2, inputs=[slider_m2, state], outputs=[], api_name="m2_slider"
    )
    slider_m3.release(
        update_m3, inputs=[slider_m3, state], outputs=[], api_name="m3_slider"
    )
    slider_m4.release(
        update_m4, inputs=[slider_m4, state], outputs=[], api_name="m4_slider"
    )
    slider_m5.release(
        update_m5, inputs=[slider_m5, state], outputs=[], api_name="m5_slider"
    )
    slider_m6.release(
        update_m6, inputs=[slider_m6, state], outputs=[], api_name="m6_slider"
    )

    # add button in new row that calls function "stop all"
    with gr.Row():
        button = gr.Button(value="STOP ALL", label="Stop all")

    button.click(stop_all, inputs=[], outputs=[], api_name="stop_all")


if __name__ == "__main__":
    print("here")
    # run call_motors as thread
    mav_con = mavutil.mavlink_connection("udpin:0.0.0.0:14550")
    mav_con.wait_heartbeat()
    arm_rov(mav_con)
    t = Thread(target=call_motors, args=(mav_con,))
    t.start()
    demo.launch(server_name="0.0.0.0")
    run_thread.clear()
    disarm_rov(mav_con)
    t.join()
