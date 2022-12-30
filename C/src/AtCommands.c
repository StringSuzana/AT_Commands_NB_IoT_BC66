#include "AtCommand.h"
#include "AtResponse.h"
#include "ResponseStatusEnum.h"

AtResponse ERROR_RESPONSE = {
    .status = STATUS_ERROR,
    .response = {"ERROR"},
    .response_size = 1,
    .wanted = NULL,
    .wanted_size = 0};

AtCommand at_read_ati()
{
    AtResponse ati_response = {
        .status = STATUS_OK,
        .response_size = 4,
        .response = {"Quectel_Ltd", "Quectel_BC66NA", "Revision: BC66NBR01A01:<revision>", "OK"},
        .wanted_size = 1,
        .wanted = {{.name = "<revision>", .value = "", .response_row = 2}}};

    AtResponsesArray expected_responses = {
        .responses_size = 2,
        .responses = {ati_response, ERROR_RESPONSE}};

    AtCommand at_read_ati = {
        .command = "ATI",
        .description = "Display Product Identification Information.",
        .long_description = "",
        .expected_responses_size = 2,
        .expected_responses = expected_responses,
        .max_wait_for_response = 1};

    return at_read_ati;
}
