import adafruit_character_lcd.character_lcd_rgb_i2c as character_lcd
import board
import busio
import json
from pytz import timezone
from datetime import datetime, time

from calendar_grabber import CalGrab

TIMEZONE = timezone('US/Eastern')
WORK_START = time(9, 00)
WORK_STOP = time(17, 00)
WORK_DAYS = [0, 1, 2, 3, 4]
with open("config.json") as f:
    CALENDARS = json.load(f)
    print(CALENDARS)

COLOR_RED = [100, 0, 0]
COLOR_GREEN = [0, 100, 0]
COLOR_BLUE = [0, 0, 100]
COLOR_PURPLE = [100, 0, 50]

lcd_columns = 16
lcd_rows = 2
i2c = busio.I2C(board.SCL, board.SDA)
lcd = character_lcd.Character_LCD_RGB_I2C(i2c, lcd_columns, lcd_rows)


def is_event_active(events, now):
    for event in events:
        if event.start_time < now and event.end_time > now:
            return True


def is_work_time(now):
    return now < WORK_STOP and now > WORK_START


def format_text(text):
    formatted = text[:16]
    formatted += f"\n" + text[16:]
    return formatted


def update_display(color, text, cursor=False, blink=False):
    text = format_text(text)
    lcd.clear()
    lcd.color = color
    lcd.message = text
    lcd.cursor = cursor
    lcd.blink = blink


def process_events(events):
    now = datetime.now(tz=TIMEZONE)
    is_working_time = is_work_time(now.time())
    is_weekend = now.weekday() not in WORK_DAYS
    print(is_weekend, now.weekday())

    if is_event_active(events, now):
        if is_weekend:
            update_display(color=COLOR_PURPLE, text="Welp its the weekend and still working -_-")
        elif is_working_time:
            update_display(color=COLOR_RED, text="Meeting in Progress")
        else:
            update_display(color=COLOR_RED, text="Get me out of here -_-")
    else:
        if is_weekend or not is_working_time:
            update_display(color=COLOR_GREEN, text="Non-working time.  No event. ")
        else:
            update_display(color=COLOR_BLUE, text="Work time - No event")


def main():
    cg = CalGrab("./.auth.json", CALENDARS, [process_events])
    cg.update_at_interval(10)


if __name__ == '__main__':
    main()
