

#ifndef _ARD_PER_ACCESS_H
#define _ARD_PER_ACCESS_H

#include "PerAccess.h"
#include "error.h"


class ArdPerAccess : public PerAccess
{
public:
    uint digitalOut(uint pinNo, uint val);
    uint digitalIn(uint pinNo, uint * val);
    uint analogOut(uint pinNo, uint val);
    uint analogIn(uint pinNo, uint * outVal);
private:
#ifdef ARDUINO
    static const uint _maxDigiPins = 14;                       /**< Maximun number of digital pins */
    static const uint _maxAnInPins = 6;                        /**< Maximum number of ADC channels */
    static const uint _maxAnOutVal = 255;                      /**< Maximum value that can be output by the PWM uint */
#elif defined(ARDUINO_MEGA)
    static const uint _maxDigiPins = 54;                       /**< Maximun number of digital pins */
    static const uint _maxAnInPins = 16;                       /**< Maximum number of ADC channels */
    static const uint _maxAnOutVal = 255;                      /**< Maximum value that can be output by the PWM uint */
#endif

};

#endif

