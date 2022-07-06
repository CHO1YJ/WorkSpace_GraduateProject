# Example of low-level Python wrapper for rpi_ws281x library.
# Author: Tony DiCola (tony@tonydicola.com), Jeremy Garff (jer@jers.net)
#
# This is an example of how to use the SWIG-generated _rpi_ws281x module.
# You probably don't want to use this unless you are building your own library,
# because the SWIG generated module is clunky and verbose.  Instead look at the
# high level Python port of Adafruit's NeoPixel Arduino library in strandtest.py.
#
# This code will animate a number of WS281x LEDs displaying rainbow colors.
import _rpi_ws281x as ws

# LED configuration.
LED_CHANNEL = 0
LED_COUNT = 16              # How many LEDs to light.
LED_FREQ_HZ = 800000        # Frequency of the LED signal.  Should be 800khz or 400khz.
LED_DMA_NUM = 10            # DMA channel to use, can be 0-14.
LED_GPIO = 18               # GPIO connected to the LED signal line.  Must support PWM!
LED_BRIGHTNESS = 255        # Set to 0 for darkest and 255 for brightest
LED_INVERT = 0              # Set to 1 to invert the LED signal, good if using NPN
#                             transistor as a 3.3V->5V level converter.  Keep at 0
#                             for a normal/non-inverted signal.

# Define colors which will be used by the example.  Each color is an unsigned
# 32-bit value where the lower 24 bits define the red, green, blue data (each
# being 8 bits long).
DOT_COLORS = [0x003300,   # red
              0x333300,   # yellow
              0x330000,	  # green
              0x000000,   # clear
              0x200000]	  # test-green


# Create a ws2811_t structure from the LED configuration.
# Note that this structure will be created on the heap so you need to be careful
# that you delete its memory by calling delete_ws2811_t when it's not needed.
leds = ws.new_ws2811_t()

# Initialize all channels to off
for channum in range(2):
    channel = ws.ws2811_channel_get(leds, channum)
    ws.ws2811_channel_t_count_set(channel, 0)
    ws.ws2811_channel_t_gpionum_set(channel, 0)
    ws.ws2811_channel_t_invert_set(channel, 0)
    ws.ws2811_channel_t_brightness_set(channel, 0)

channel = ws.ws2811_channel_get(leds, LED_CHANNEL)

ws.ws2811_channel_t_count_set(channel, LED_COUNT)
ws.ws2811_channel_t_gpionum_set(channel, LED_GPIO)
ws.ws2811_channel_t_invert_set(channel, LED_INVERT)
ws.ws2811_channel_t_brightness_set(channel, LED_BRIGHTNESS)

ws.ws2811_t_freq_set(leds, LED_FREQ_HZ)
ws.ws2811_t_dmanum_set(leds, LED_DMA_NUM)

# Initialize library with LED configuration.
resp = ws.ws2811_init(leds)
if resp != ws.WS2811_SUCCESS:
    message = ws.ws2811_get_return_t_str(resp)
    raise RuntimeError('ws2811_init failed with code {0} ({1})'.format(resp, message))

# Wrap following code in a try/finally to ensure cleanup functions are called
# after library is initialized.
try:
    num_led = 10 # 해당값부터 LED_COUNT까지 점등
    for i in range(LED_COUNT):
        color = DOT_COLORS[0]
        color = DOT_COLORS[4]
#        color = DOT_COLORS[2]

        # Set the LED color buffer value.
        ws.ws2811_led_set(channel, num_led + i, color)

    # Send the LED color data to the hardware.
    resp = ws.ws2811_render(leds)

finally:
    # Ensure ws2811_fini is called before the program quits.
    ws.ws2811_fini(leds)
    # Example of calling delete function to clean up structure memory.  Isn't
    # strictly necessary at the end of the program execution here, but is good practice.
    ws.delete_ws2811_t(leds)
