/**
 * Defines a abstract class that allows access to the peripherlas
 * on board when implemented completely.
 */

#ifndef _PER_ACCESS_H
#define _PER_ACCESS_H
#include "error.h"
#include <stdint.h>
class PerAccess
{
public:
    virtual uint digitalOut(uint pinNo, uint val) = 0;
    virtual uint digitalIn(uint pinNo, uint * outVal) = 0;
    virtual uint analogIn(uint pinNo, uint * outVal) = 0;
    virtual uint analogOut(uint pinNo, uint val) = 0;

};
#endif
