#include "AtCommand.h"
#include "../at_responses/AtResponse.h"

static AtResponse ERROR_RESPONSE = {
        .status = STATUS_ERROR,
        .rows = {"ERROR"},
        .row_size = 1,
        .wanted_params = NULL,
        .wanted_size = 0
};

static AtCommand at_read_ati()
{
    const AtResponse ati_response = {
            .status = STATUS_OK,
            .row_size = 4,
            .rows = {"Quectel_Ltd", "Quectel_BC66", "Revision: <revision>", "OK"},
            .wanted_size = 1,
            .wanted_params = {{.name = "<revision>", .value = "", .response_row = 2}}
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
            .row_size = 2,
            .rows = {"+CGSN:<IMEI>", "OK"},
            .wanted_size = 1,
            .wanted_params = {{.name = "<IMEI>", .value = "", .response_row = 0}}
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
            .row_size = 4,
            .rows = {"+CGSN:<IMEI>", "OK"},
            .wanted_size = 1,
            .wanted_params = {{.name = "<IMEI>", .value = "", .response_row = 0}}
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
