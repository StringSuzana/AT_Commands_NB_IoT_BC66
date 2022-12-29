#ifndef AT_RESPONSE_FUNCTION_POINTER_H
#define AT_RESPONSE_FUNCTION_POINTER_H

#include "AtResponse.h"
#include "ResponseStatusEnum.h"

// Define the function pointer type
typedef AtResponse (*AtResponseFunctionPointer)(Status result_status, const char **result_array, size_t result_array_len, AtResponse *at_expected_response);

#endif /* AT_RESPONSE_FUNCTION_POINTER_H */
