#ifndef AT_COMMANDS_H
#define AT_COMMANDS_H
#include "AtCommand.h"
#include "AtResponse.h"
#include "ResponseStatusEnum.h"
#include "Read.h"

const char ATI[] = "ATI";

struct AtCommand at_read_ati = {
    .command = ATI,
    .description = "Display Product Identification Information.",
    .read_response_method = Read_answer,
    .expected_responses = {
        {.status = Status_OK,
         .response = {"Quectel_Ltd", "Quectel_BC66NA", "Revision: BC66NBR01A01:<revision>", "OK"},
         .wanted = {{.name = "<revision>", .value = "", .response_row = 0}},
         .wanted_count = 1},
        {.status = Status_ERROR,
         .response = {"ERROR"},
         .wanted = {},
         .wanted_count = 0}},
    .expected_responses_count = 2,
    .max_wait_for_response = 1};

#endif /* AT_COMMANDS_H */
