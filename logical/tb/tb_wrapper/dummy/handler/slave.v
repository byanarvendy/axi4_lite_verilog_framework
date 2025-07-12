module slave #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32
) (
    input                           iCLK, iRST,
    input                           w_REQ, r_REQ,
    input                           iDONE,
    input       [DATA_WIDTH-1:0]    w_DATA,
    input       [ADDR_WIDTH-1:0]    w_ADDR, r_ADDR,

    output reg  [DATA_WIDTH-1:0]    r_DATA
);

    /* generate random addresses and data */
    parameter               NUM_ENTRIES  = 256;

    reg [DATA_WIDTH-1:0]    data [0:NUM_ENTRIES-1];

    integer                 i;

    initial begin
        for (i = 0; i < NUM_ENTRIES; i = i + 1) begin
            data[i]         = $urandom;
        end
    end


    /* logic */
    initial begin
        r_DATA = 32'h00000000;
    end
    always @(posedge iCLK or negedge iRST) begin
        if (!iRST) begin
            r_DATA <= 32'h00000000;
        end else begin
            if (w_REQ) begin
                data[w_ADDR] <= w_DATA;
            end else if (r_REQ) begin
                r_DATA <= data[r_ADDR];
            end
        end
    end

endmodule