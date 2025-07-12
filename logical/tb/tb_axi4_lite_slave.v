`timescale 1ns/1ps

module tb_axi4_lite_slave();
    parameter ADDR_WIDTH = 32;
    parameter DATA_WIDTH = 32;

    reg                         iCLK, iRST;
    
    reg                         s_AWVALID;
    reg [2:0]                   s_AWPROT;
    reg [ADDR_WIDTH-1:0]        s_AWADDR;
    wire                        s_AWREADY;
    
    reg                         s_WVALID;
    reg [DATA_WIDTH-1:0]        s_WDATA;
    reg [(DATA_WIDTH/8)-1:0]    s_WSTRB;
    wire                        s_WREADY;
    
    reg                         s_BREADY;
    wire                        s_BVALID;
    wire [1:0]                  s_BRESP;

    wire [ADDR_WIDTH-1:0]       write_addr;
    wire [DATA_WIDTH-1:0]       write_data;
    wire                        write_done;

    axi4_lite_slave #(
        .ADDR_WIDTH(ADDR_WIDTH), .DATA_WIDTH(DATA_WIDTH)
    ) dut (
        /* clock and reset */
        .iCLK(iCLK), .iRST(iRST),

        /* write */
        .s_AWVALID(s_AWVALID), .s_AWPROT(s_AWPROT), .s_AWADDR(s_AWADDR), .s_AWREADY(s_AWREADY),
        .s_WVALID(s_WVALID), .s_WDATA(s_WDATA), .s_WSTRB(s_WSTRB), .s_WREADY(s_WREADY),
        .s_BREADY(s_BREADY), .s_BVALID(s_BVALID), .s_BRESP(s_BRESP),

        /* read */
        .s_ARVALID(1'b0), .s_ARPROT(3'b0), .s_ARADDR(32'b0), .s_ARREADY(),
        .s_RREADY(1'b0), .s_RVALID(), .s_RRESP(), .s_RDATA(),

        /* interfaces */
        .write_done(write_done), .write_addr(write_addr), .write_data(write_data),
        .read_addr(), .read_data(32'b0)
    );

    always #5 iCLK = ~iCLK;

    initial begin
        $dumpfile("logical/sim/tb_axi4_lite_slave.vcd");
        $dumpvars(0, tb_axi4_lite_slave);
        
        iCLK        = 1;
        iRST        = 0;
        s_AWVALID   = 0;
        s_AWPROT    = 3'b000;
        s_AWADDR    = 0;
        s_WVALID    = 0;
        s_WDATA     = 0;
        s_WSTRB     = 4'b1111;
        s_BREADY    = 0;

        #10; iRST = 1;

        #20;
            s_AWADDR    = 32'h0000_0010;
            s_AWVALID   = 1;
            s_WDATA     = 32'hDEADBEEF;
            s_WVALID    = 1;
            s_BREADY    = 1;

        #40;
            s_AWVALID   = 0;
            s_WVALID    = 0;
            s_BREADY    = 0;

        #50;
        $finish;
    end

endmodule
