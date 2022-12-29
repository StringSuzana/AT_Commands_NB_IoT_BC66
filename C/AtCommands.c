#ifndef AT_COMMANDS_H
#define AT_COMMANDS_H

#include "AtCommand.h"
#include "AtResponse.h"
#include "ResponseStatusEnum.h"

const AtCommand at_read_ati = {
    .command = "ATI",
    .description = "Display Product Identification Information.",
    .long_description = "",
    .expected_responses_count = 2,
    .expected_responses = NULL,
    .max_wait_for_response = 1};

#endif /* AT_COMMANDS_H */
