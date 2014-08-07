/**
 * Implements the peripheral access functionalities
 */

#include "ArdPerAccess.h"
#include "error.h"
#include <WProgram.h>

/**
 * Outputs the given logic level at the given pin
 */

uint ArdPerAccess::digitalOut(uint pinNo, uint val)
{
    if (pinNo > _maxDigiPins) {
        return ERR_INVALID_PIN;
    }
    pinMode(pinNo, OUTPUT);
    if (val == 0) {
        digitalWrite(pinNo, LOW);
    } else {
        digitalWrite(pinNo, HIGH);
    }
    return ERR_SUCCESS;
}

/**
 * Reads the voltage level at given pin and returns
 * it's logical value.
 */

uint ArdPerAccess::digitalIn(uint pinNo, uint * val)
{
    if (pinNo > _maxDigiPins) {
        return ERR_INVALID_PIN;
    }

    pinMode(pinNo, INPUT);

    *val = digitalRead(pinNo);
    return ERR_SUCCESS;
}

/**
 * Outputs the analog value.
 */

uint ArdPerAccess::analogOut(uint pinNo, uint val)
{
#ifdef ARDUINO
    int anOutPins[] = { 5, 6, 9, 10, 11};       /* PWM output pins */
#elif defined (ARDUINO_MEGA)
    int anOutPins[] = { 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13};       /* PWM output pins */
#endif

    if (val > _maxAnOutVal) {
        return ERR_INVALID_ARG;
    }
    if (pinNo > sizeof(anOutPins)/sizeof(anOutPins[0])) {
        return ERR_INVALID_PIN;
    }

    pinMode(anOutPins[pinNo], OUTPUT);
    analogWrite(anOutPins[pinNo], val);
    return ERR_SUCCESS;
}

/**
 * Reads the volatge at the given analog input pin
 * and returns the digital representation of the same
 */

uint ArdPerAccess::analogIn(uint pinNo, uint * outVal)
{
    if (pinNo > _maxAnInPins) {
        return ERR_INVALID_PIN;
    }

    *outVal = analogRead(pinNo);
    return ERR_SUCCESS;
}






