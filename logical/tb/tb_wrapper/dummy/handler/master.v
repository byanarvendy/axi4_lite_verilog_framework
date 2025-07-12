module master #(
    parameter ADDR_WIDTH = 32,
    parameter DATA_WIDTH = 32,
    parameter MAX_OFFSET = 2
) (
    input                           iCLK, iRST,
    input                           iDONE,
    input       [DATA_WIDTH-1:0]    r_DATA,

    output                          w_REQ, r_REQ,
    output reg  [DATA_WIDTH-1:0]    w_DATA,
    output reg  [ADDR_WIDTH-1:0]    w_ADDR, r_ADDR
);

    /* generate random addresses and data */
    parameter               NUM_ENTRIES  = 100;

    reg [ADDR_WIDTH-1:0]    addr [0:NUM_ENTRIES-1];
    reg [DATA_WIDTH-1:0]    data [0:NUM_ENTRIES-1];

    integer                 i;
    integer                 offset_base;
    integer                 byte_offset;

    initial begin
        for (i = 0; i < NUM_ENTRIES; i = i + 1) begin
            offset_base     = $urandom_range(0, MAX_OFFSET - 1);
            byte_offset     = $urandom_range(0, 255);
            addr[i]         = (offset_base << 8) | byte_offset;
            data[i]         = $urandom;
        end
    end


    /* logic */ 
    integer                 j;
    reg                     init;
    
    always @(posedge iCLK or negedge iRST) begin
        if (!iRST) begin
            j               <= 1;
            init            <= 1'b1;
            w_ADDR          <= 32'h00000000;
            r_ADDR          <= 32'h00000000;
            w_DATA          <= 32'h00000000;
        end
        else begin
            if (iDONE) begin                
                if (j < 32) begin
                    j       <= j + 1;
                    w_ADDR  <= (w_REQ) ? addr[j] : 32'h00000000;
                    w_DATA  <= (w_REQ) ? data[j] : 32'h00000000;
                    r_ADDR  <= (r_REQ) ? addr[j] : 32'h00000000;
                end
                else begin
                    j       <= 0;
                end
            end

            init            <= (!r_DATA[31]);
        end
    end

    assign w_REQ = !init;
    assign r_REQ =  init;
    
endmodule