#include "AtCommand.h"
#include "AtResponse.h"

static AtResponse ERROR_RESPONSE = {
        .status = STATUS_ERROR,
        .response = {"ERROR"},
        .response_size = 1,
        .wanted = NULL,
        .wanted_size = 0
};

static AtCommand at_read_ati()
{
    const AtResponse ati_response = {
            .status = STATUS_OK,
            .response_size = 4,
            .response = {"Quectel_Ltd", "Quectel_BC66NA", "Revision: BC66NBR01A01:<revision>", "OK"},
            .wanted_size = 1,
            .wanted = {{.name = "<revision>", .value = "", .response_row = 2}}
    };

    AtResponseArray expected_responses = {
            .responses_size = 2,
            .responses = {ati_response, ERROR_RESPONSE}
    };
    const AtCommand ati = {
            .command = "ATI",
            .description = "Display Product Identification Information.",
            .expected_responses_size = 2,
            .expected_responses = expected_responses,
            .max_wait_for_response = 1
    };
    return ati;
}

static AtCommand at_read_imei()
{
    const AtResponse imei_response = {
            .status = STATUS_OK,
            .response_size = 4,
            .response = {"+CGSN:<IMEI>", "OK"},
            .wanted_size = 1,
            .wanted = {{.name = "<IMEI>", .value = "", .response_row = 0}}
    };
    AtResponseArray expected_responses = {
            .responses_size = 2,
            .responses = {imei_response, ERROR_RESPONSE}
    };
    const AtCommand imei = {
            .command = "AT+CGSN=1",
            .description = "Display Product IMEI.",
            .expected_responses_size = 2,
            .expected_responses = expected_responses,
            .max_wait_for_response = 1
    };

    return imei;
}
static AtCommand at_read_imei_replace_test()
{
    const AtResponse imei_response = {
            .status = STATUS_OK,
            .response_size = 4,
            .response = {"+CGSN:<IMEI>", "OK"},
            .wanted_size = 1,
            .wanted = {{.name = "<IMEI>", .value = "", .response_row = 0}}
    };
    AtResponseArray expected_responses = {
            .responses_size = 2,
            .responses = {imei_response, ERROR_RESPONSE}
    };
    const AtCommand imei = {
            .command = "AT+CGSN=<IMEI_PICK>",
            .description = "Display Product IMEI.",
            .expected_responses_size = 2,
            .expected_responses = expected_responses,
            .max_wait_for_response = 1
    };

    return imei;
}
